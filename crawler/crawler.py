from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib
from urlparse import urlparse
from collections import deque
import re
import argparse
import os
import sys
from util import UrlBlacklist
from linkscrub import scrub
from google import google


def google_for_urls(term, limit=100):
    search_results = google.search(term, pages=5, lang='en')
    li = [x.link for x in search_results]
    links = []
    for x in range(0, limit):
        if len(search_results) > x:
            links.append(search_results[x].link)
    return links


def crawl(urls):
    blacklist = UrlBlacklist(list(urls))
    urls = deque(blacklist.remove_blacklisted())

    processed_urls = set()
    emails = set()

    while len(urls):
        url1 = urls.pop()
        # add to processed immediately, to support failure
        processed_urls.add(url1)

        parts = urlparse(url1)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url1[:url1.rfind('/') + 1] if '/' in parts.path else url1

        # get url's content
        print("Processing %s" % url1)
        try:
            response = requests.get(url1)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore pages with errors
            continue

        # extract all email addresses and add them into the resulting set
        new_emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        # emails.update(new_emails)
        f = open('emails.txt', 'a')
        for email in new_emails:
            f.write("%s\n" % email)
        f.close()

        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text, "html.parser")

        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link

            # add the new url to the queue if it was not enqueued nor processed yet
            if not link in urls and not link in processed_urls:
                if not blacklist.is_blacklisted(link):
                    urls.append(link)

        # scrub linkset to ensure crawler doesn't waste time on one site
        # urls = scrub_linkset(urls)
        urls_list = list(urls)
        scrubbed = scrub(urls_list, 4)
        print("*****SCRUBBED RESULT********\n\n\n")
        print(scrubbed)
        print("*****SCRUBBED RESULT END********\n\n\n")
        urls = deque(scrubbed)

    return emails


if __name__ == "__main__":

    urls = google_for_urls(sys.argv[1])
    crawl_urls = deque()
    for url in urls:
        crawl_urls.append(url)
    emails = crawl(crawl_urls)
    print(emails)

    '''links = ['http://this.com', 'http://this.com/that', 'http://this.com/this', 'http:guy.com']
    linkq = deque()
    for url in links:
        linkq.append(url)
    print linkq
    stuff = scrub_linkset(linkq, 2)
    print(stuff)'''
