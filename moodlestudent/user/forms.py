from django.contrib.auth.models import User
from django import forms

class UserAppForm(forms.ModelForm):
    password1 =forms.CharField(label ="Password", max_length=200, widget = forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation Password",max_length=200, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name']

    def check_password(self):
        if(self.password_confirmation!=self.password):
            raise forms.ValidationError()


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=200)
    password = forms.CharField(label="Password", max_length=200, widget = forms.PasswordInput)




class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']
