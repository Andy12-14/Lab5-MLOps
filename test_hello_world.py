import unittest
from hello_world import app, generate_html, greet


class TestHelloWorldApp(unittest.TestCase):
	def setUp(self):
		# Use the Flask test_client to make requests to the app without running a server
		self.client = app.test_client()

	def test_greet_returns_expected_string(self):
		expected = 'Welcome to CI/CD 101 using GitHub Actions!'
		self.assertEqual(greet(), expected)

	def test_generate_html_contains_message_and_image(self):
		msg = 'Hello Test'
		html = generate_html(msg)
		self.assertIsInstance(html, str)
		# message should be present
		self.assertIn(msg, html)
		# basic structure
		self.assertIn('<html>', html)
		self.assertIn('<body>', html)
		# image tag with expected domain should be present
		self.assertIn('build5nines.com', html)

	def test_generate_html_preserves_special_chars(self):
		msg = '<script>alert("x")</script>'
		html = generate_html(msg)
		# The function does not escape HTML, so the exact string should appear
		self.assertIn(msg, html)

	def test_hello_world_route_returns_html(self):
		response = self.client.get('/greeting')
		# Flask should return 200 OK for the greeting route
		self.assertEqual(response.status_code, 200)
		data = response.get_data(as_text=True)
		# Response should contain the greeting
		self.assertIn(greet(), data)
		# And the image should be in the payload
		self.assertIn('build5nines.com', data)
		# Content-Type should be HTML
		self.assertIn('text/html', response.content_type)


if __name__ == '__main__':
	unittest.main()

