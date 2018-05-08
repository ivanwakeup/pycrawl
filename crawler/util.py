class UrlBlacklist(object):
    blacklist = ['twitter',
                 'facebook',
                 'wikipedia',
                 'wikidata',
                 'plus.google.com',
                 'pinterest.com',
                 'yelp.com',
                 'google.com',
                 'youtube.com',
                 'amazon.com',
                 'tripadvisor.com',
                 'olark.com',
                 'instagram',
                 'aboutads.info']

    def __init__(self, url_list):
        self.url_list = url_list

    def get_blacklist(self):
        return set(self.blacklist)

    def is_blacklisted(self, url):
        blacklisted = False
        for x in self.blacklist:
            if x in url:
                blacklisted = True

        return blacklisted

    def remove_blacklisted(self):
        return [x for x in self.url_list if not self.is_blacklisted(x)]


class ExtensionBlacklist(object):
    blacklist = ['.jpg', '.png', '.jpeg', '.mp3']

    def __init__(self, url_list):
        self.url_list = url_list

    def get_blacklist(self):
        return set(self.blacklist)

    def is_blacklisted(self, url):
        blacklisted = False
        for x in self.blacklist:
            if x in url:
                blacklisted = True

        return blacklisted

    def remove_blacklisted(self):
        return [x for x in self.url_list if not self.is_blacklisted(x)]
