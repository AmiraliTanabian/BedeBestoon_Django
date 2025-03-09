from django.shortcuts import render
from .forms import contactUsForm
from .models import Messages
from datetime import datetime

# Create your views here.
def contact_us_page(request):
    if request.method != "POST":
        context = {'form_obj': contactUsForm()}
        return render(request, "contact_us/contact_us.html", context)
    else:
        form_obj = contactUsForm(data=request.POST)

        if not form_obj.is_valid():
            context = {'form_obj': form_obj}
            return render(request, "contact_us/contact_us.html", context)

        else:
            name = form_obj.cleaned_data['name']
            email = form_obj.cleaned_data['email']
            subject = form_obj.cleaned_data['subject']
            text = form_obj.cleaned_data['text']
            Messages.objects.create(name=name, subject=subject, email=email, text=text,
                                    datetime=datetime.now())

            context = {'form_obj': form_obj, 'status':True}
            return render(request, "contact_us/contact_us.html", context)
