from django.test import TestCase
from minted.forms import ExpenditureForm
from minted.models import Expenditure, Category
from django import forms

class ExpenditureFormTestCase(TestCase):

    fixtures = ['minted/tests/fixtures/default_user.json']

    