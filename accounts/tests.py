from django.urls import resolve
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.views import register

def id():
    id.counter += 1
    return str(id.counter)
id.counter = 0

# Create your tests here.
class RegisterPageTest(TestCase):

    def test_register_url_resolves_to_register_page_view(self):
        found = resolve('/register')
        self.assertEqual(found.func, register)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/register')
        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>MovieLib</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertIn('<h2>Register</h2>', html)

        self.assertTemplateUsed(response, 'registration/register.html')

    def test_can_save_a_POST_request(self):
        username = 'johndifool' + id()
        response = self.client.post('/register', data={
            'username': username,
            'email': username + '@example.com',
            'password': 'abc123'
        })

        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, 'johndifool1')
        self.assertEqual(new_user.email, 'johndifool1@example.com')

    def test_redirects_after_POST(self):
        username = 'johndifool' + id()
        response = self.client.post('/register', data={
           'username': username,
            'email': username + '@example.com',
            'password': 'abc123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/libraries/johndifool2/')