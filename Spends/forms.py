from django import forms
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV2Checkbox

class registerForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'نام کاربری'}),
                               error_messages={'required':'لطفا نام کاربری را وارد نمایید.'})
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder':'ایمیل'}),
                            error_messages={'required':'لظفا ایمیل خود را وارد نمایید'})
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور'}),
                               error_messages={'required':'لطفا رمز عبور خود را وارد نمایید'})
    again_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز'}), 
                                     error_messages={'required':'لطفا تکرار رمز خود را وارد نمایید'})
    recaptcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox(attrs={'style':'margin:auto;'}),
                               error_messages= {'invalid':'اعتبار سنجی ریکپجا ناموفق بود! لطفا مجدد تلاش بفرمایید' ,
                                                'required':'اعتبار سنجی ریکپجا ناموفق بود! لطفا مجدد تلاش بفرمایید'})

class loginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'نام کاربری'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور'}))

class addSpend(forms.Form):
    title = forms.CharField(label="عنوان خرج", widget=forms.TextInput(attrs = {'placeholder':'عنوان خرج'}))
    price = forms.IntegerField(label="مبلغ خرج", widget=forms.NumberInput(attrs=
                                                                          {"placeholder":"مبلغ"}))
    datetime = forms.DateTimeField(label="تاریخ و زمان خرج" ,widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    is_now = forms.BooleanField(required=False, label="زمان الان را برای خرج ثبت کن", widget=forms.CheckboxInput())
    note = forms.CharField(label="یاداشت", widget=forms.Textarea(attrs={"placeholder":"یاداشت"}),
                           required=False)

class addIncome(forms.Form):
    title = forms.CharField(label="عنوان درآمد", widget=forms.TextInput(attrs={'placeholder': 'عنوان درآمد'}))
    price = forms.IntegerField(label="مبلغ درآمد", widget=forms.NumberInput(attrs={'placeholder': 'مقدار  درآمد'}))
    datetime = forms.DateTimeField(label="تاریخ و زمان درآمد",
                                   widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    is_now = forms.BooleanField(required=False, label="زمان الان را برای درآمد ثبت کن", widget=forms.CheckboxInput())
    note = forms.CharField(label="یاداشت", widget=forms.Textarea(attrs={"placeholder":"یاداشت"}),
                           required=False)

class editIncome(forms.Form):
    title = forms.CharField(label="عنوان درآمد", widget=forms.TextInput(attrs={'placeholder': 'عنوان درآمد'}))
    price = forms.IntegerField(label="مبلغ درآمد", widget=forms.TextInput(attrs={'placeholder': 'مقدار  درآمد'}))
    datetime = forms.DateTimeField(label="تاریخ و زمان درآمد",
                                   widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    is_now = forms.BooleanField(required=False, label="زمان الان را برای درآمد ثبت کن", widget=forms.CheckboxInput())
    note = forms.CharField(label="یاداشت", widget=forms.Textarea(attrs={"placeholder":"یاداشت"}),
                           required=False)