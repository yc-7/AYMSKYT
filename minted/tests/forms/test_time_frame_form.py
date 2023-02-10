from django.test import TestCase
from minted.forms import TimeFrameForm
from django import forms
import datetime

class TimeFrameFormTest(TestCase):
    """Tests for the TimeFrame form"""

    def setUp(self):
        self.form_input = {
            'start_date': datetime.date(2023, 1, 1),
            'end_date': datetime.date(2024, 1, 1)
        }
    
    def test_form_has_necessary_fields(self):
        form = TimeFrameForm()

        self.assertIn('start_date', form.fields)
        start_date_field = form.fields['start_date']
        self.assertTrue(isinstance(start_date_field, forms.DateField))

        self.assertIn('end_date', form.fields)
        end_date_field = form.fields['end_date']
        self.assertTrue(isinstance(end_date_field, forms.DateField))

    def test_valid_time_frame_form(self):
        form = TimeFrameForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_start_date_must_be_before_end_date(self):
        self.form_input['start_date'] = datetime.date(2025, 1, 1)
        self.form_input['end_date'] = datetime.date(2021, 1, 1)
        form = TimeFrameForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_start_date_and_end_date_can_be_same(self):
        self.form_input['start_date'] = datetime.date(2025, 1, 1)
        self.form_input['end_date'] = datetime.date(2025, 1, 1)
        form = TimeFrameForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    