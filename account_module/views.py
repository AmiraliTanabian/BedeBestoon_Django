from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.utils.crypto import get_random_string
from .models import Token, TempUser, ForgetPasswordUsers
from .forms import registerForm, loginForm, ForgetPasswordForm, ResetPasswordForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils import timezone
from secrets import choice
from string import digits, punctuation, ascii_letters

def random_str(length):
    all_letters = digits + punctuation + ascii_letters
    all_letters = all_letters.replace(r'/', '')
    all_letters = all_letters.replace('\\', '')
    result = ''.join(choice(all_letters) for _ in range(length))
    return result


class ResetPasswordView(View):
    def get(self, request, random_string):
        form = ResetPasswordForm()
        forget_pass_user = get_object_or_404(ForgetPasswordUsers, random_str=random_string)
        return render(request, "Spends/reset_password_page.html",
                      {"form":form})

    def post(self, request, random_string):
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            forget_pass_user = get_object_or_404(ForgetPasswordUsers, random_str=random_string)
            email = forget_pass_user.email

            # TODO; remove items from forget password table on detect time
            # delete from forget password table
            forget_pass_user.delete()

            new_password = form.cleaned_data["password"]
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            messages.success(request, "رمز عبور شما با موفقیت تغییر پیدا کرد!")
            return HttpResponseRedirect(reverse_lazy("login_page"))

        else:
            return render(request, "Spends/reset_password_page.html",
                          {"form":form})

class ForgetPasswordView(View):
    def get(self, request):
        form = ForgetPasswordForm()
        return render(request, "Spends/forget_password.html", {
            "form":form
        })


    def post(self, request):
        form = ForgetPasswordForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            email_user = User.objects.filter(email=email)

            if not email_user.exists():
                form.add_error("email", "ایمیل شما نامعتبر است!")
                return render(request, "Spends/forget_password.html", {
                    "form": form
                })


            # email found
            else:
                random_string = get_random_string(50)
                ForgetPasswordUsers.objects.create(email=email, random_str=random_string)
                url = settings.SITE_URL +  reverse_lazy("reset_password", args=[random_string])
                email_body = render_to_string("Spends/reset_password_email.html", {
                    "verification_url":url,
                })

                msg = EmailMessage(
                    "ریست پسورد بده بستون",
                    email_body,
                    "atanabain@gmail.com",
                    [email]
                )
                msg.content_subtype = "html"
                msg.send()


                messages.success(request, "ایمیل تغییر رمز برای شما ارسال شد \n اگر ایمیل را نمیبنید پوشه spam را چک کنید!")
                return render(request, "Spends/forget_password.html", {
                    "form": form
                })




        else:
            return render(request, "Spends/forget_password.html", {
                "form": form
            })

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            context = {"username": username}
            return render(request, "Spends/logout.html", context)

        else:
            return render(request, "Spends/logout_without_login.html")

class LoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form_obj = loginForm()
            return render(request, 'Spends/login.html', {'form_obj': form_obj})

        else:
            return render(request, "Spends/login_register_limit.html")

    def post(self, request):
        form_obj = loginForm(data=request.POST)

        if form_obj.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user :
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد اکانت خود شدید!\nمیتوانید از امکانات سرویس استفاده کنید')
                return  HttpResponseRedirect(reverse('home_page'))

            else:
                return render(request, 'Spends/login.html', {'status':'username or password incorrect',
                                                             'form_obj':form_obj})

        else:
            return render(request, 'Spends/login.html', {'form_obj': form_obj})

class VerifyAccountView(View):
    def get(self, request, random_string):
        temp_object = TempUser.objects.filter(random_str=random_string)

        if not temp_object.exists():
            print("Salam")
            return render(request, 'Spends/verify_account.html', {'status': 'NotFound'})


        elif timezone.now().timestamp() - temp_object[0].date.timestamp() > 12 * 3600:
            return render(request, 'Spends/verify_account.html', {'status': 'Expired'})


        else:
            temp_object = temp_object.first()
            username = temp_object.username
            user_object = User(username=temp_object.username, password=temp_object.password, email=temp_object.email)
            user_object.save()
            this_token = Token(user=user_object, token=random_str(50))
            this_token.save()
            temp_object.delete()
            return render(request, 'Spends/verify_account.html', {'status': 'Ok', 'username': username,
                                                                  'token': this_token.token})

class AccountRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "Spends/login_register_limit.html")

        else:
            form_object = registerForm()
            return render(request, 'Spends/register.html',
                          {'status':False , 'form_object':form_object})


    def post(self, request):
        form_object = registerForm(data=request.POST)

        if form_object.is_valid():
            form_object = registerForm(data=request.POST)
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']


            #TODO; check the user dont on temp users
            #TODO; check ip
            #TODO; remove TempUser
            random_string = random_str(50)

            # Add temp info on table
            TempUser.objects.create(username=username, password=make_password(password),
                                    date=timezone.now() , email=email, random_str=random_string)
            # Send verify email
            verification_url = settings.SITE_URL +  reverse_lazy('verify_account', args=[random_string])
            email_subject = 'تایید حساب کاربری'
            email_html_content = render_to_string('Spends/email_sender.html',
                                                    {'verification_url':verification_url})
            email_from = 'atanabain@gmail.com'

            mail = EmailMessage(email_subject, email_html_content, email_from, [email])
            mail.content_subtype = 'html'
            mail.send()


            return render(request, 'Spends/register.html',
                        {'status':'OK', 'form_object':form_object})

        else:
            return render(request, 'Spends/register.html',
                {'status':False , 'form_object':form_object})
