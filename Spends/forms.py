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
