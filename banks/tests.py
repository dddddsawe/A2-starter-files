from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from banks.models import Bank, Branch

class BanksTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )

        cls.bank = Bank.objects.create(
            name='Test Bank',
            description='A test bank',
            inst_num='1234',
            swift_code='TESTCA'
        )

        cls.branch = Branch.objects.create(
            bank=cls.bank,
            name='Test Branch',
            transit_num='56789',
            address='Test Address',
            email='test@test.com',
            capacity=10
        )

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def test_bank_list_view(self):
        response = self.client.get(reverse('bank_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banks/bank_list.html')
        self.assertContains(response, self.bank.name)

    def test_bank_detail_view(self):
        response = self.client.get(reverse('bank_detail', args=[self.bank.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banks/bank_detail.html')
        self.assertContains(response, self.bank.name)
        self.assertContains(response, self.bank.description)
        self.assertContains(response, self.bank.inst_num)
        self.assertContains(response, self.bank.swift_code)

    def test_bank_create_view(self):
        response = self.client.get(reverse('bank_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banks/add_bank.html')
        self.assertContains(response, 'csrfmiddlewaretoken')
        data = {
            'name': 'New Test Bank',
            'description': 'A new test bank',
            'inst_num': '5678',
            'swift_code': 'TESTUS'
        }
        response = self.client.post(reverse('bank_create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('bank_detail', args=[2]))
        self.assertEqual(Bank.objects.count(), 2)
        new_bank = Bank.objects.get(pk=2)
        self.assertEqual(new_bank.name, data['name'])
        self.assertEqual(new_bank.description, data['description'])
        self.assertEqual(new_bank.inst_num, data['inst_num'])
        self.assertEqual(new_bank.swift_code, data['swift_code'])

    def test_branch_create_view(self):
        response = self.client.get(reverse('branch_create', args=[self.bank.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banks/add_branch.html')
        self.assertContains(response, 'csrfmiddlewaretoken')
        data = {
            'name': 'New Test Branch',
            'transit_num': '11111',
            'address': 'New Test Address',
            'email': 'newtest@test.com',
            'capacity': 5
        }
        response = self.client.post(reverse('branch_create', args=[self.bank.pk]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('branch_detail', args=[2]))
        self.assertEqual(Branch.objects.count(), 2)
        new_branch = Branch.objects.get(pk=2)
        self.assertEqual(new_branch.name, data['name'])
        self.assertEqual(new_branch.transit_num,