class Blacklist(object):
    def __init__(self, scrub_list, scrub_words):
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

    def factory(type, scrub_list):
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
        super(UrlBlacklist, self).__init__(scrub_list, self.blacklist)


class EmailBlacklist(Blacklist):
    blacklist = ['example', 'email', 'support']

    def __init__(self, scrub_list):
        super(EmailBlacklist, self).__init__(scrub_list, self.blacklist)


class ExtensionBlacklist(Blacklist):
    blacklist = ['.jpg', '.png', '.jpeg', '.mp3']

    def __init__(self, scrub_list):
        super(ExtensionBlacklist, self).__init__(scrub_list, self.blacklist)