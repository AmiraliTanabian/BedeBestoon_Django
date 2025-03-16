from django.shortcuts import render
from .forms import contactUsForm, ContactUsModelForm
from .models import Messages
from datetime import datetime

# Create your views here.
def contact_us_page(request):
    if request.method != "POST":
        context = {'form_obj': ContactUsModelForm()}
        return render(request, "contact_us/contact_us.html", context)
    else:
        form_obj = ContactUsModelForm(data=request.POST)

        if not form_obj.is_valid():
            context = {'form_obj': form_obj}
            return render(request, "contact_us/contact_us.html", context)

        else:
            form_obj.save()

            context = {'form_obj': form_obj, 'status':True}
            return render(request, "contact_us/contact_us.html", context)
