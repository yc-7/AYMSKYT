from django import forms
from PST.models import SpendingLimit

class SpendingLimitForm(forms.ModelForm):
    class Meta:
        model = SpendingLimit
        fields = ['limit', 'timeframe']