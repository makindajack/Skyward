from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse


from django.test import SimpleTestCase
from django.urls import reverse


class HomepageTests(SimpleTestCase):
    """ Home page test"""
    def setUp(self):
        """Set up the test by making a GET request to the homepage URL."""
        url = reverse("home")
        self.response = self.client.get(url)
        print(f"This is the repsonse: {self.response.content}")

    def test_url_exists_at_correct_location(self):
        """Test that the homepage URL exists and returns a 200 status code."""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        """Test that the homepage uses the correct template."""
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self):
        """Test that the homepage contains the expected HTML content."""
        self.assertContains(self.response, "home pag")

    def test_homepage_does_not_contain_incorrect_html(self):
        """Test that the homepage does not contain unexpected HTML content."""
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")