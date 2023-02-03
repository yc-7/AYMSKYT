"""Forms in the PST app"""

from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator
from .models import *


class LogInForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
            'character and a number'
            )]
    )

    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
            is_staff=False,
            is_superuser=False,
        )

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['title', 'price', 'date', 'description', 'receipt_image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ExpenditureForm, self).__init__(*args, **kwargs)

    title = forms.CharField(label="Title")
    price = forms.DecimalField(label = "Amount Spent", decimal_places = 2, max_digits = 6)
    date = forms.DateField(label = "Date of Purchase", widget = forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date', 'placeholder': '--', 'class': 'form-control'}))
    description = forms.CharField(label = "Description", widget = forms.Textarea())
    receipt_image = forms.FileField(label = "Receipt")

