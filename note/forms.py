from django import forms

from .models import User

class RegisterForm(forms.ModelForm):
    password_confirmation = forms.CharField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password_confirmation(self):
        confirmed_password = self.cleaned_data['password_confirmation']
        if confirmed_password != self.cleaned_data['password']:
            raise forms.ValidationError("Passwords should match")
        
        return confirmed_password