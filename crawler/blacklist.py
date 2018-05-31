class Blacklist(object):
    def __init__(self, scrub_words=None, scrub_list=None):
        if scrub_list is not None:
            self.scrub_list = scrub_list
        self.scrub_words = scrub_words

    def is_blacklisted(self, url):
        blacklisted = False
        for x in self.scrub_words:
            if x in url:
                blacklisted = True

        return blacklisted

    def remove_blacklisted(self):
        return [x for x in self.scrub_list if not self.is_blacklisted(x)]

    def factory(type, scrub_list=None):
        if type == "url":
            return UrlBlacklist(scrub_list)
        if type == "ext":
            return ExtensionBlacklist(scrub_list)
        if type == "email":
            return EmailBlacklist(scrub_list)

    factory = staticmethod(factory)


class UrlBlacklist(Blacklist):
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

    def __init__(self, scrub_list):
        super(UrlBlacklist, self).__init__(self.blacklist, scrub_list)


class EmailBlacklist(Blacklist):
    blacklist = ['example', 'email', 'support', 'domain', 'orders', 'info', 'github', 'registration', 'mozilla', 'donate', 'feedback', 'newsletter']

    def __init__(self, scrub_list=None):
        super(EmailBlacklist, self).__init__(self.blacklist, scrub_list)


class ExtensionBlacklist(Blacklist):
    blacklist = ['.jpg', '.png', '.jpeg', '.mp3', '.tgz']

    def __init__(self, scrub_list):
        super(ExtensionBlacklist, self).__init__(self.blacklist, scrub_list)
