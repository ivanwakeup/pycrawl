import unittest

from crawler.crawler import google_for_urls

class TestCrawler(unittest.TestCase):

    def test_google_for_urls(self):
        #should return urls related to a search term, up to a configurable number of urls

