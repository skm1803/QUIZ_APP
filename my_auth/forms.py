#Imports from django core
from django import forms
from .models import User
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm #now not using this,using custom
# from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Why its not ModelForm?
#Ask this question if we really need to save this data everytime users fills in this form and submit?
# #No.. So no ModelForm

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ["email","password1", "password2"]
        widgets = {
        'email':    forms.EmailInput(attrs={'class':'form-control'}),
        }

    def clean_email(self):
        restricted = ['admin','superuser','staff']
        email = self.cleaned_data.get('email')
        for i in restricted:
            if email.startswith(i):
                raise forms.ValidationError("This email is not allowed")
        return email

    def save(self,commit=True):
        user = super(RegisterForm,self).save(commit = False)
        user.active = True
        # user.staff = True
        if commit:
            user.save()
        return user


