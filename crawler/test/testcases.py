import unittest

from crawler.crawler import find_emails_from_url

class TestCrawler(unittest.TestCase):

    def test_google_for_urls(self):
        pass

    def test_find_emails_from_url(self):
        url = "http://hoo-kit.co/contact"
        emails = find_emails_from_url(url)
        print(emails)
        self.assertEquals(emails, set([u'hookit.co@gmail.com']))


