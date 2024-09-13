from django import forms
from adminpanel.models import Profile, User
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
import re


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label='First Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, label='Last Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(max_length=50, required=True, label='Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    username = forms.CharField(max_length=50, required=True, label='Username',
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password1 = forms.CharField(max_length=50, required=True, label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(max_length=50, required=True, label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            self.add_error('password1', 'Password should have at least 8 characters')

        if not re.search(r'[a-z]', password):
            self.add_error('password1', 'Password should have at least 1 lowercase letter')

        if not re.search(r'[0-9]', password):
            self.add_error('password1', 'Password should have at least 1 number')

        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Phone"
    )
    profile_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe yourself'
        }),
        label="About"
    )
    profile_image = forms.ImageField(
        label="Profile Picture",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )
    id_proof = forms.ImageField(
        label="ID Proof",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Profile
        exclude = ['user']


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Username"
    )
    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    
class ForgotPasswordForm(forms.Form):
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Email'}),
        label="Enter your registered email"
    )
   

class OtpForm(forms.Form):
    otp = forms.IntegerField(        
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'******'}),
        label="Enter OTP"
        
    )

class SetNewPassword(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=50,
        required=True,
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New Password',
            'class': 'form-control'
        })
    )
    
    new_password2 = forms.CharField(
        max_length=50,
        required=True,
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields=['new_password1','newpassword2']