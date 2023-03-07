from django.forms import EmailInput, TextInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Please enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=EmailInput(attrs={'type': 'email'}), required=True)
    first_name = forms.CharField(widget=TextInput(attrs={'type': 'text'}), max_length=30, required=True)
    last_name = forms.CharField(widget=TextInput(attrs={'type': 'text'}), max_length=30, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
