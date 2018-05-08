import requests, bs4, re
from urlparse import urlparse


def make_soup(url):
    r = requests.get(url)
    soup = bs4.BeatifulSoup(r.text, "html.parser")
    return soup


if __name__ == "__main__:":
    print make_soup(
