from django.test import TestCase
from django.core.exceptions import ValidationError
from minted.models import User,Category

class CategoryModelTestCase(TestCase):
    """Unit tests for the Category model"""

    fixtures = [
        "minted/tests/fixtures/default_user.json",
        "minted/tests/fixtures/default_other_user.json",
        "minted/tests/fixtures/default_categories.json",
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.user = User.objects.get(email = 'johndoe@example.org')
        self.second_user = User.objects.get(email = 'janedoe@example.org')
        self.category = Category.objects.get(pk=1)
        self.second_category = Category.objects.get(pk=2)
    
    def test_category_is_valid(self):
        self._assert_category_is_valid()

    def test_category_name_need_not_be_unique(self):
        self.category.name = 'Transportation'
        self._assert_category_is_valid()

    def test_category_name_must_not_be_blank(self):
        self.category.name = ''
        self._assert_category_is_invalid()
    
    def test_category_name_may_contain_50_characters(self):
        self.category.name = 'x' * 50
        self._assert_category_is_valid()
    
    def test_category_name_must_not_contain_more_than_50_characters(self):
        self.category.name = 'x' * 51
        self._assert_category_is_invalid()
    
    def test_category_budget_cannot_be_blank(self):
        self.category.budget = None
        self._assert_category_is_invalid()

    def test_category_must_have_user(self):
        self.category.user = None
        self._assert_category_is_invalid()


    def _assert_category_is_valid(self):
        try:
            self.category.full_clean()
        except (ValidationError):
            self.fail('Test category should be valid')

    def _assert_category_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.category.full_clean()