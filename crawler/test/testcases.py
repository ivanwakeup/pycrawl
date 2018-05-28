import unittest

from crawler.crawler import get_email_set_from_response
from requests import Response

class TestCrawler(unittest.TestCase):

    def test_google_for_urls(self):
        pass

    def test_find_emails_from_url(self):
        response = Response("<html><body>hookit.co@gmail.com</body></html>")
        emails = get_email_set_from_response(response)
        print(emails)
        self.assertEquals(emails, set([u'hookit.co@gmail.com']))

    def test_get_url_response(self):
        url = 'http://slcm.us/18athleteguide'
        response


