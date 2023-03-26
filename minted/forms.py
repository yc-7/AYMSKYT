"""Forms in the Minted app"""

from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator
from minted.models import User, SpendingLimit, Expenditure, Category, NotificationSubscription, Subscription, Streak, Reward, FriendRequest
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm
from .mixins import NewPasswordMixin

PASSWORD_REGEX_VALIDATOR = RegexValidator(
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
    message = 'Password must contain an uppercase character, a lowercase character and a number'
)

class DateInput(forms.DateInput):
    input_type = 'date'

class LogInForm(forms.Form):
    email = forms.CharField(label = "Email")
    password = forms.CharField(label = "Password", widget = forms.PasswordInput())
    
class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form to allow unregistered users to sign up"""

    class Meta:
        """Form options"""

        model = User
        fields = ['first_name', 'last_name', 'email']

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

class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password"""

    password = forms.CharField(label = 'Current password', widget = forms.PasswordInput())

    def __init__(self, user = None, **kwargs):
        """Construct a new form instance with a user instance"""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors"""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(email = self.user.email, password = password)
        else:
            user = None
        if user is None:
            self.add_error('password', 'Password is invalid')

    def save(self):
        """Save the user's new password"""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user

class NewPasswordForm(NewPasswordMixin):
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
        exclude = ['user', 'budget', 'colour']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if Category.objects.filter(user=self.user, name=self.cleaned_data.get('name')).exists():
            self.add_error('name', 'You already have a category with this name.')
    
class FriendReqForm(forms.Form):
    """Form to send friend requests to another user"""

    email = forms.EmailField()

    def __init__(self, user = None, **kwargs):
        """Construct a new form instance with a user instance"""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors"""

        super().clean()
        email = self.cleaned_data.get('email')

        if (User.objects.filter(email = email).count() == 0):
            self.add_error('email', 'This user does not exist')
        elif self.user is not None:
            self.to_user = User.objects.get(email = email)

            if (self.user == self.to_user):
                self.add_error('email', 'You cannot send a friend request to yourself :/')

            if (FriendRequest.objects.filter(from_user = self.to_user, to_user = self.user).count() != 0):
                self.add_error('email', 'This person has already sent you a friend request!')

            if (FriendRequest.objects.filter(from_user = self.user, to_user = self.to_user).count() != 0):
                self.add_error('email', 'You have already sent a friend request to this person')

    def save(self):
        """Create a friend request"""

        if self.user is not None:
            friend_request = FriendRequest.objects.create(
                from_user = self.user,
                to_user = self.to_user,
            )
        return friend_request

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

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        exclude = ['reward_id']
        widgets = {
            'description': forms.Textarea(attrs = {'rows': 3})
        }
    expiry_date = forms.DateField(widget=DateInput())