from django.test import TestCase
from minted.models import Reward
from minted.forms import RewardForm

#class RewardFormTestCase(TestCase):

    # def test_form_has_necessary_fields(self):
    #     form = PasswordForm()
    #     self.assertIn('password', form.fields)
    #     self.assertIn('new_password', form.fields)
    #     self.assertIn('password_confirmation', form.fields)

    # def test_valid_reward_form(self):
    #     self.form_input = {'brand_name': 'Tesco', 'points_required': 20, 'expiry_date': date.today(), 'description': 'Food voucher', 'code_type': 'qr' }
    #     form = RewardForm(data=input)
    #     self.assertTrue(form.is_valid())

    # def test_invalid_spending_limit_form(self):
    #     self.form_input['code_type'] = 'Qr'
    #     form = SpendingLimitForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    # def test_form_has_necessary_fields(self):
    #     form = SpendingLimitForm()
    #     self.assertIn('budget', form.fields)
    #     self.assertIn('timeframe', form.fields)

    # def test_form_must_save_correctly(self):
    #     form = SignUpForm(data=self.form_input)
    #     before_count = User.objects.count()
    #     form.save()
    #     after_count = User.objects.count()
    #     self.assertEqual(after_count, before_count+1)
    #     user = User.objects.get(username='@janedoe')
    #     self.assertEqual(user.first_name, 'Jane')
    #     self.assertEqual(user.last_name, 'Doe')
    #     self.assertEqual(user.email, 'janedoe@example.org')
    #     self.assertEqual(user.bio, 'My bio')
    #     is_password_correct = check_password('Password123', user.password)
    #     self.assertTrue(is_password_correct)