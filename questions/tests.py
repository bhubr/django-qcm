from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from movies.views import home_page
from movies.models import Movie

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>MovieLib</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertIn('<h2>Not logged-in</h2>', html)

        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'movie-title': 'X-Men'})

        self.assertEqual(Movie.objects.count(), 1)
        new_movie = Movie.objects.first()
        self.assertEqual(new_movie.title, 'X-Men')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'movie-title': 'X-Men'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/libraries/benoit-hubert/')

    def test_uses_list_template(self):
        response = self.client.get('/libraries/benoit-hubert/')
        self.assertTemplateUsed(response, 'library.html')

    def test_displays_all_list_items(self):
        Movie.objects.create(title='itemey 1')
        Movie.objects.create(title='itemey 2')

        response = self.client.get('/libraries/benoit-hubert/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

class MovieModelTest(TestCase):

    def test_saving_and_retrieving_movies(self):
        first_movie = Movie()
        first_movie.title = 'The first (ever) movie'
        first_movie.save()

        second_movie = Movie()
        second_movie.title = 'The second movie'
        second_movie.save()

        saved_movies = Movie.objects.all()
        self.assertEqual(saved_movies.count(), 2)

        first_saved_movie = saved_movies[0]
        second_saved_movie = saved_movies[1]
        self.assertEqual(first_saved_movie.title, 'The first (ever) movie')
        self.assertEqual(second_saved_movie.title, 'The second movie')