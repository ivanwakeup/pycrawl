import unittest
from crawler.blacklist import Blacklist


class TestCrawler(unittest.TestCase):

    def test_google_for_urls(self):
        pass

    def test_blacklist(self):
        blacklist = Blacklist(scrub_words=['info'])
        self.assertTrue(blacklist.is_blacklisted("info@dudeman.com"))
        blacklist = Blacklist(scrub_words=['guy'])
        self.assertTrue(blacklist.is_blacklisted("guy@dudeman.com"))
        blacklist = Blacklist(scrub_words=['something'])
        self.assertFalse(blacklist.is_blacklisted("notsome@dudeman.com"))

    def test_email_blacklist(self):
        blacklist = Blacklist.factory("email")
        self.assertTrue(blacklist.is_blacklisted("info@dudeman.com"))
        self.assertFalse(blacklist.is_blacklisted("guy@dudeman.com"))


