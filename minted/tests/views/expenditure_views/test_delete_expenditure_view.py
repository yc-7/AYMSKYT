from django.test import TestCase
from django.urls import reverse
from minted.models import Category, Expenditure, User

class ExpenditureDeletionViewTestCase(TestCase):
    """Test suite for the expenditure deletion view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_categories.json',
        'minted/tests/fixtures/default_expenditures.json', 
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.expenditure_id = 1
        self.url = reverse('delete_expenditure', kwargs={'expenditure_id':self.expenditure_id})
        self.user = User.objects.get(pk = 1)

    def test_delete_expenditure_url(self):
        self.assertEqual(self.url,f"/category_list/{self.expenditure_id}/delete")

    def test_get_delete_expenditure_redirects(self):
        self.client.login(email = self.user.email, password = 'Password123')
        redirect_url = reverse('category_list')

        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_delete_expenditure(self):
        self.client.login(email = self.user.email, password = 'Password123')
        start_count = Expenditure.objects.all().count()
        self.client.post(self.url)
        end_count = Expenditure.objects.all().count()
        self.assertEqual(start_count, end_count+1)

    def test_user_cannot_delete_other_users_expenditures(self):
        self.client.login(email = self.user.email, password = 'Password123')
        
        self.expenditure_id_of_other_user = 3
        self.url = reverse('delete_expenditure', kwargs={'expenditure_id':self.expenditure_id_of_other_user})

        start_count = Expenditure.objects.all().count()
        self.client.post(self.url)
        end_count = Expenditure.objects.all().count()
        self.assertEqual(start_count, end_count)