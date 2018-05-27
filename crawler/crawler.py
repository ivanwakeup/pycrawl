from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urlparse import urlparse
from collections import deque
import re
import sys
from blacklist import Blacklist
from linkscrub import scrub
from google import google


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


def find_emails_from_url(url):
    print("Processing %s" % url)
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        response = None

    if response is not None:
        emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))
    else:
        emails = set()
    return emails


def process_url():
    return


def crawl(links):
    blacklist = Blacklist.factory("url", list(links))
    links_to_process = deque(blacklist.remove_blacklisted())

    processed_urls = set()
    emails = set()

    while len(links_to_process):
        url1 = links_to_process.pop()
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
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))

        email_blacklist = Blacklist.factory("email", new_emails)
        new_emails = set(email_blacklist.remove_blacklisted())
        gmails = get_gmail_address_set(new_emails)

        f = open('emails.txt', 'a')
        f2 = open('gmail_emails.txt', 'a')

        for email in new_emails:
            f.write("%s\n" % email)

        for email in gmails:
            f2.write("%s\n" % email)

        f.close()
        f2.close()

        # create a beautiful soup for the html document
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
            if link not in links_to_process and link not in processed_urls:
                if not blacklist.is_blacklisted(link):
                    links_to_process.appendleft(link)

        # scrub linkset to ensure crawler doesn't waste time on one site
        # urls = scrub_linkset(urls)
        urls_list = list(links_to_process)
        scrubbed = scrub(urls_list, 4)
        print("*****SCRUBBED RESULT********\n\n\n")
        print(scrubbed)
        print("*****SCRUBBED RESULT END********\n\n\n")
        links_to_process = deque(scrubbed)

    return emails


if __name__ == "__main__":

    urls = google_for_urls(sys.argv[1])
    crawl_urls = deque()
    for url in urls:
        crawl_urls.append(url)
    emails_out = crawl(crawl_urls)
    print(emails_out)

    '''links = ['http://this.com', 'http://this.com/that', 'http://this.com/this', 'http:guy.com']
    linkq = deque()
    for url in links:
        linkq.append(url)
    print linkq
    stuff = scrub_linkset(linkq, 2)
    print(stuff)'''
