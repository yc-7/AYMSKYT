"""Forms in the Minted app"""

from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator
from minted.models import User, SpendingLimit, Expenditure, Category
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.forms import UserChangeForm

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
        validators = [RegexValidator(
            regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message = 'Password must contain an uppercase character, a lowercase character and a number'
            )]
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
            is_staff = False,
            is_superuser = False,
            budget = budget
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
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['title', 'price', 'date', 'description', 'receipt_image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.category = Category.objects.filter(user=self.user).get(name=kwargs.pop('category'))
        super(ExpenditureForm, self).__init__(*args, **kwargs)

    title = forms.CharField(label="Title")
    price = forms.DecimalField(label = "Amount Spent", decimal_places = 2, max_digits = 6)
    date = forms.DateField(label = "Date of Purchase", widget = forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date', 'placeholder': '--', 'class': 'form-control'}))
    description = forms.CharField(label = "Description", widget = forms.Textarea(), required = False)
    receipt_image = forms.FileField(label = "Receipt", required = False)

    def clean(self):
        super().clean()
        description = self.cleaned_data.get('description') or None
        receipt_image = self.cleaned_data.get('receipt_image') or None

    def save(self):
        """Create a new expenditure"""

        super().save(commit=False)
        return Expenditure.objects.create(
                user = self.user,
                category = self.category,
                title = self.cleaned_data.get('title'),
                price = self.cleaned_data.get('price'),
                date = self.cleaned_data.get('date'),
                description = self.cleaned_data.get('description'),
                receipt_image = self.cleaned_data.get('receipt_image')
            )

    def update(self, expenditure_id):
        """Update an existing expenditure"""

        expenditure = Expenditure.objects.get(id=expenditure_id)
        expenditure.title = self.cleaned_data.get('title')
        expenditure.price = self.cleaned_data.get('price')
        expenditure.date = self.cleaned_data.get('date')
        expenditure.description = self.cleaned_data.get('description')
        expenditure.receipt_image = self.cleaned_data.get('receipt_image')
        expenditure.save()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['user', 'budget']

        
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
        