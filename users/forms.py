from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.forms import ModelForm, TextInput, Textarea, EmailInput, PasswordInput, CheckboxInput
from django.template.loader import render_to_string

from .models import User, UserProfileModel


class SignUpForm(UserCreationForm):
    fullname = forms.CharField(label='Full Name',
                               min_length=2, max_length=150,
                               widget=forms.TextInput(
                                   attrs={'autofocus': True, 'id': 'inputname',
                                          'class': 'form-control', 'placeholder': 'Alex Ornald'}))
    email = forms.EmailField(label='Email address', widget=EmailInput(
        attrs={'id': 'inputEmail', 'class': 'form-control', 'placeholder': 'ornald@example.com'}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'id': 'inputPassword', 'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={'id': 'inputPassword1', 'class': 'form-control', 'placeholder': 'Password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('fullname', 'email')


class LoginForm(AuthenticationForm):
    username = UsernameField(label="Email address", widget=forms.TextInput(
        attrs={'autofocus': True,
               'id': 'inputEmail',
               'class': 'form-control',
               'placeholder': 'ornald@example.com'
               }
    ))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'id': 'inputPassword', 'class': 'form-control', 'placeholder': 'Password'}
        ),
    )

#
# class UserRegistrationForm(forms.Form):
#     username = forms.CharField(label='Username', min_length=4, max_length=150,
#                         widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
#     email = forms.EmailField(label='Email',widget=EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
#     password = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
#     password_2 = forms.CharField (label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
#     # policy_agreement = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-control','name':'remember'}))
#
#     def clean_username(self):
#         username = self.cleaned_data['username'].lower()
#         user_with_username = User.objects.filter(username=username)
#
#         if user_with_username:
#             raise ValidationError('User with given username already exists!')
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data['email'].lower()
#         user_with_email = User.objects.filter(email=email)
#         if user_with_email:
#             raise ValidationError('User with given email already exists!')
#         return email
#
#     # TODO: Check for password strength
#     def clean_password_2(self):
#         password = self.cleaned_data.get('password')
#         password_2 = self.cleaned_data.get('password_2')
#
#         if password and password_2 and password != password_2:
#             raise ValidationError('Password do not match!')
#
#         return password_2
#
#     def save(self, commit=True):
#         user = User.objects.create_user(
#             self.cleaned_data['username'],
#             self.cleaned_data['email'],
#             self.cleaned_data['password']
#         )
#         user.save()
#         return user
#
#
# class UserForm(forms.ModelForm):
#     # def clean_email(self):
#     #     email = self.cleaned_data['email'].lower()
#     #     user_with_email = User.objects.filter(email=email)
#     #     if user_with_email:
#     #         raise ValidationError('User with given email already exists!')
#     #     return email
#     #
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'username')
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
#
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        exclude = ['user', 'img', ]
        widgets = {
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'company_organization': forms.TextInput(attrs={'class': 'form-control'}),
            'soc_media_twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'soc_media_fb': forms.URLInput(attrs={'class': 'form-control'}),
            'soc_media_linkedin': forms.URLInput(attrs={'class': 'form-control'}),
        }


class CustomPasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        mail_subject = 'Revealin - Reset your password.'
        message = render_to_string(email_template_name, context)
        send_mail(
            mail_subject,
            'Revealin',
            'no-reply@revealin.com',
            [to_email],
            html_message=message,
        )
