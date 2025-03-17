from .forms import ContactUsModelForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages



class ContactUsView(FormView):
    is_valid = False
    form_class = ContactUsModelForm
    template_name = "contact_us/contact_us.html"
    success_url = reverse_lazy("contact_us_page")

    def form_valid(self, form):
        self.is_valid = True
        form.save()
        messages.success(self.request, "پیام شما با موفقیت ثبت شد. نتیجه آن با ایمیل به شما ارسال خواهد شد.")
        return super().form_valid(form)
