from django import forms
from .models import Messages

class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = Messages
        exclude = ["datetime"]
        labels = {
            "name":"",
            "email":"",
            "subject":"",
            "text":""
        }

        error_messages = {
            "name" : {"required":"لطفا نام خود را وارد کنید"},
            "subjetc" : {"required":"لطفا عنوان پیام را وارد کنید"},
            "email":{"required":"لطفا ایمیل خود را وارد کنید"},
            "text":{"required":"لطفا متن پیام خود را وارد کنید "}
        }
        widgets = {
            "name" : forms.TextInput(attrs={"placeholder":'نام و نام خانوادگی'}),
            "subject": forms.TextInput(attrs={"placeholder":"عنوان پیام"}),
            "email": forms.EmailInput(attrs={"placeholder":"ایمیل"}), 
            "text": forms.Textarea(attrs = {"placeholder":"متن پیام"})
        }
    