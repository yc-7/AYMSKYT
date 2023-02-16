"""Forms in the Minted app"""

from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator
from minted.models import User, SpendingLimit, Expenditure
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


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

class TestExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['user','title','category','price','date','description','receipt_image']

class SpendingLimitForm(forms.ModelForm):
    class Meta:
        model = SpendingLimit
        fields = ['budget', 'timeframe']
    
    # def save(self):
    #     super().save(commit=False)
    #     today = date.today()
    #     budget = self.cleaned_data.get('budget')
    #     start_date = self.cleaned_data.get('start_date')
    #     timeframe = self.cleaned_data.get('timeframe')
    #     end_date = self.cleaned_data.get('end_date')
    #     if timeframe == '/week':
    #         end_date = today - timedelta(days=today.isocalendar().weekday) + relativedelta(days =+ 7)
    #         start_date = end_date - relativedelta(days =+ 6)
    #     if timeframe == '/month':
    #         start_date = date(today.year, today.month, 1)
    #         end_date = date(today.year, (today.month+1)%12, 1) - timedelta(days=1)
    #     if timeframe == '/quarter':
    #         quarter = (today.month-1)//3 + 1
    #         start_date = date(today.year, 3 * quarter - 2, 1)
    #         end_date = date(today.year, (3* quarter)%12 + 1, 1) + timedelta(days=-1)
    #     if timeframe == '/year':
    #         start_date = date(today.year,1,1)
    #         end_date = date(today.year+1, 1, 1) - timedelta(days=1)
    #     return SpendingLimit.objects.create(budget = budget, remaining_budget = budget,
    #                                         start_date = start_date, end_date = end_date, timeframe = timeframe)
