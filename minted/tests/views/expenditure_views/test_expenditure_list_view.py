from django.test import TestCase
from django.urls import reverse
from minted.models import Expenditure, User, Category
from minted.tests.helpers import reverse_with_next

class ExpenditureListTest(TestCase):

    fixtures = ['minted/tests/fixtures/default_user.json']

    def setUp(self):
        self.category = Category.objects.get(pk=1)
        self.url = reverse('expenditures', self.category.name)
        self.user = User.objects.get(pk=1)

    def test_expenditure_list_url(self):
        self.assertEqual(self.url, '/category_list/Entertainment/')

    def test_get_expenditure_list(self):
        self.client.login(email=self.user.email, password='Password123')
        self._create_test_expenditures()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenditures_list.html')
        self.assertEqual(len(response.context['expenditures']), 9)
        for num in range(1, 10):
            self.assertContains(response, f'expenditure{num}')
            self.assertContains(response, f'2023-0{num}-2{num}')
            self.assertContains(response, f'2{num}.00')
            expenditure = Expenditure.objects.get(id=num)
            expenditure_url = reverse('edit_expenditure', category_name=self.category.name, expenditure_id=expenditure.id)
            self.assertContains(response, expenditure_url)


    def _create_test_expenditures(self, num_expenditures=10):
        for num in range(1, num_expenditures):
            Expenditure.objects.create(
                user = self.user,
                category = self.category,
                title = f'expenditure{num}',
                price = f'2{num}.00',
                date = f'2023-0{num}-2{num}',
                description = f'This is expenditure number {num}',
                receipt_image = None
            )


