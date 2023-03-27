from django.core.exceptions import ValidationError
from django.test import TestCase
from minted.models import Expenditure

class ExpenditureModelTestCase(TestCase):
    """Unit tests for the Expenditure model"""

    fixtures = [
        "minted/tests/fixtures/default_user.json",
        "minted/tests/fixtures/default_other_user.json",
        "minted/tests/fixtures/default_third_user.json",
        "minted/tests/fixtures/default_expenditures.json",
        "minted/tests/fixtures/default_spending_limit.json",
        "minted/tests/fixtures/default_categories.json",
    ]

    def setUp(self):
        self.expenditure = Expenditure.objects.get(pk = 1)
        self.second_expenditure = Expenditure.objects.get(pk = 2)

    def test_expenditure_is_valid(self):
        self._assert_expenditure_is_valid()

    def test_expenditure_must_have_category(self):
        self.expenditure.category = None
        self._assert_expenditure_is_invalid()

    def test_title_cannot_be_blank(self):
        self.expenditure.title = ''
        self._assert_expenditure_is_invalid()
    
    def test_title_can_contain_50_chars(self):
        self.expenditure.title = 'a' * 50
        self._assert_expenditure_is_valid()

    def test_title_cannot_contain_more_than_50_chars(self):
        self.expenditure.title = 'a' * 51
        self._assert_expenditure_is_invalid()

    def test_titles_do_not_need_to_be_unqiue(self):
        self.second_expenditure.title = self.expenditure.title
        self._assert_expenditure_is_valid()

    def test_amount_can_be_8_digits(self):
        self.expenditure.amount = 123456.78
        self._assert_expenditure_is_valid()

    def test_amount_cannot_be_more_than_8_digits(self):
        self.expenditure.amount = 1234567.89
        self._assert_expenditure_is_invalid()
    
    def test_amount_not_more_than_2_decimal_places(self):
        self.expenditure.amount = 12.123
        self._assert_expenditure_is_invalid()
    
    def test_date_cannot_be_blank(self):
        self.expenditure.date = None
        self._assert_expenditure_is_invalid()

    def test_description_can_contain_200_chars(self):
        self.expenditure.description = 'a' * 200
        self._assert_expenditure_is_valid()
    
    def test_description_cannot_contain_more_than_200_chars(self):
        self.expenditure.description = 'a' * 201
        self._assert_expenditure_is_invalid()

    def test_description_can_be_blank(self):
        self.expenditure.description = ''
        self._assert_expenditure_is_valid()

    def test_image_file_can_be_blank(self):
        self.expenditure.receipt = None
        self._assert_expenditure_is_valid()


    def _assert_expenditure_is_valid(self):
        try:
            self.expenditure.full_clean()
        except ValidationError:
            self.fail("Test expenditure should be valid")
    
    def _assert_expenditure_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.expenditure.full_clean()