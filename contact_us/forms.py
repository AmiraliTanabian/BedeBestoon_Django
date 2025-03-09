from django import forms

class contactUsForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'نام'}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder':'ایمیل'}))
    subject = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'موضوع'}))
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder':'متن پیام'}))
