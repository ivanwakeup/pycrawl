import logging
import re
from collections import deque
from urlparse import urlparse

import requests
import requests.exceptions
from bs4 import BeautifulSoup
from google import google

from blacklist import Blacklist
from linkscrub import scrub
from writer import EmailWriter


def google_for_urls(term, limit=100):
    search_results = google.search(term, pages=5, lang='en')
    links = []
    for x in range(0, limit):
        if len(search_results) > x:
            links.append(search_results[x].link)
    out = list(reversed(links))
    return out


def get_gmail_address_set(emails):
    out = set()
    for email in emails:
        if "gmail" in email:
            out.add(email)
    return out


def get_valid_urls_from_page(anchors):
    partial_links = []
    for anchor in anchors:
        link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        partial_links.append(link)
    return partial_links


def get_url_extras(url):
    parts = urlparse(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    return url, base_url, path


def get_url_response(url):
    print("Processing %s" % url)
    try:
        response = requests.get(url, timeout=3)
    except requests.exceptions.RequestException:
        response = requests.Response()
    return response


def get_email_set_from_response(url_response):
    emails = set(re.findall(
        r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", url_response.text, re.I))
    return emails


def process_url():
    return


def crawl(links):
    blacklist = Blacklist.factory("url", list(links))
    links_to_process = deque(blacklist.remove_blacklisted())
    email_blacklist = Blacklist(
        scrub_words=['example', 'email', 'support', 'domain', 'orders', 'info', 'github', 'registration', 'mozilla',
                     'donate', 'feedback', 'newsletter'])
    email_writer = EmailWriter(email_blacklist)
    processed_urls = set()
    emails = set()

    logger = logging.getLogger()

    while len(links_to_process):
        url1 = links_to_process.pop()
        # add to processed immediately, to support failure
        processed_urls.add(url1)

        url_extras = get_url_extras(url1)

        response = get_url_response(url1)
        if not response.ok:
            continue

        new_emails = get_email_set_from_response(response)

        email_writer.add_emails(new_emails)

        # create a beautiful soup for the html document
        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception:
            continue

        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = url_extras[1] + link
            elif not link.startswith('http'):
                link = url_extras[2] + link

            # add the new url to the queue if it was not enqueued nor processed yet
            if link not in links_to_process and link not in processed_urls:
                if not blacklist.is_blacklisted(link):
                    links_to_process.appendleft(link)

        # scrub linkset to ensure crawler doesn't waste time on one site
        # urls = scrub_linkset(urls)
        urls_list = list(links_to_process)
        scrubbed = scrub(urls_list, 4)
        logger.debug(scrubbed)
        links_to_process = deque(scrubbed)

    return emails


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Crawl the web for emails')
    parser.add_argument('--url', help='The seed url to begin crawling from.')
    parser.add_argument('--term', help='A google search term to start with.')

    args = parser.parse_args()
    urls = None
    if args.url:
        urls = [args.url]
    elif args.term:
        urls = google_for_urls(args.term)

    crawl_urls = deque()
    for url in urls:
        crawl_urls.append(url)
    emails_out = crawl(crawl_urls)
