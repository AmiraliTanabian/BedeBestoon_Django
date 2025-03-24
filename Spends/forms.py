from django import forms

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
