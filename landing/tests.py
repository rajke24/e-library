from django.test import TestCase, Client
from django.urls import reverse

class TestHomeView(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_GET(self):
        response = self.client.get(self.home_url, follow=True)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/home.html')