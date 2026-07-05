from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Post


class SocialSmokeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='strongpass123')
        Post.objects.create(author=self.user, content='Hello MiniSocial!')

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello MiniSocial!')

    def test_profile_page_loads(self):
        response = self.client.get(reverse('profile', args=['alice']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '@alice')
