from django import forms 
from .models import Account
from dataclasses import field
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
	password = 	forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Please enter password'}))
	confirm_password = 	forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}))
	class Meta:
		model  = Account
		fields = ['first_name','last_name','username','email','phone_number','password',]

	def __init__(self,*args,**kwargs):
		super(RegistrationForm,self).__init__(*args,**kwargs)
		self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
		self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
		self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")

		if password != confirm_password:
			raise forms.ValidationError(
                "Password does not match."
            )


class LoginForm(forms.ModelForm):
    password = 	forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Please enter password'}))
    class Meta:
        model = User
        fields = ['email','password']


    def __init__(self,*args,**kwargs):
					super(LoginForm,self).__init__(*args,**kwargs)
					for field in self.fields:
        						self.fields[field].widget.attrs['class'] = 'form-control'





