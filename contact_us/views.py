from django.shortcuts import render
from .forms import ContactUsModelForm
from django.views import View

class ContactUsView(View):
    def get(self, request):
        context = {'form_obj': ContactUsModelForm()}
        return render(request, "contact_us/contact_us.html", context)
    
    def post(self, request):
        form_obj = ContactUsModelForm(data=request.POST)

        if not form_obj.is_valid():
            context = {'form_obj': form_obj}
            return render(request, "contact_us/contact_us.html", context)

        else:
            form_obj.save()

            context = {'form_obj': form_obj, 'status':True}
            return render(request, "contact_us/contact_us.html", context)