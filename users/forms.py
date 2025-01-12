from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from users.models import User

class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegistrationForm(UserCreationForm, StyleFormMixin):

    class Meta:
        model = User
        fields = ['first_name','last_name','email','avatar','phone_number', 'password1','password2']

class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']

class CustomLoginForm(StyleFormMixin  ,AuthenticationForm):
    pass

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Введите ваш email")