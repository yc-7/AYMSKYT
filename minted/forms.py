"""Forms in the Minted app"""

from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator
from minted.models import User, SpendingLimit, Expenditure, Category, NotificationSubscription, Subscription, Streak
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.forms import UserChangeForm

PASSWORD_REGEX_VALIDATOR = RegexValidator(
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
    message = 'Password must contain an uppercase character, a lowercase character and a number'
)

class DateInput(forms.DateInput):
    input_type = 'date'

class LogInForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    """Form to allow unregistered users to sign up"""

    class Meta:
        """Form options"""

        model = User
        fields = ['first_name', 'last_name', 'email']

    new_password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(),
        validators = [PASSWORD_REGEX_VALIDATOR]
    )

    password_confirmation = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput())

    def clean(self):
        """Clean data and generate error messages"""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Password does not match')

    def save(self, budget):
        """Creates a new user"""

        super().save(commit = False)
        return User.objects.create_user(
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            password = self.cleaned_data.get('new_password'),
            points = 10,
            is_staff = False,
            is_superuser = False,
            budget = budget,
            streak_data = Streak.objects.create(),
        )

class SpendingLimitForm(forms.ModelForm):
    class Meta:
        model = SpendingLimit
        fields = ['budget', 'timeframe']

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PasswordForm(forms.Form):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[PASSWORD_REGEX_VALIDATOR]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

class NewPasswordForm(forms.Form):
    """Form for password resets"""
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['new_password'] = forms.CharField(
            label='Password',
            widget=forms.PasswordInput(),
            validators=[PASSWORD_REGEX_VALIDATOR]
        )
        self.fields['password_confirmation'] = forms.CharField(
            label='Password confirmation',
            widget=forms.PasswordInput()
        )

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        new_password = self.cleaned_data.get('new_password')
        self.user.set_password(new_password)
        self.user.save()

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['title', 'amount', 'date', 'description', 'receipt']
        widgets = {
            'description': forms.Textarea(attrs = {'rows': 3})
        }
    date = forms.DateField(widget=DateInput())

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['user', 'budget']

    
class FriendReqForm(forms.Form):
    from_user = forms.HiddenInput()
    email = forms.EmailField()
    is_active = forms.HiddenInput()


class TimeFrameForm(forms.Form):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    time_choices = [
        ('yearly', 'Yearly'),
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    ]
    time_interval = forms.ChoiceField(choices = time_choices, widget=forms.Select)


    def clean(self):
        super().clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        time_interval = self.cleaned_data.get('time_interval')
        if start_date > end_date:
            self.add_error('start_date', 'Start date must be earlier than end date.')

class NotificationSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NotificationSubscription
        fields = ['frequency', 'subscriptions']

    subscriptions = forms.ModelMultipleChoiceField(
        queryset = Subscription.objects.all(),
        label = "Subscriptions",
        widget = forms.CheckboxSelectMultiple,
        required = False
    )
