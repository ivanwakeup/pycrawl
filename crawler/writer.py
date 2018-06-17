from os.path import expanduser
from blacklist import Blacklist


class EmailWriter(object):

    __emails = set()

    __homedir = expanduser("~")

    __tier_1_emails = ('{}/tier_1_emails.txt'.format(__homedir), set())
    __tier_2_emails = ('{}/tier_2_emails.txt'.format(__homedir), set())

    __should_write = False

    def __init__(self, blacklist=None):
        self.blacklist = blacklist

    def add_email(self, email):
        self.__check_should_write()
        if not self.blacklist.is_blacklisted(email):
            self.__emails.add(email)

    def add_emails(self, emails):
        self.__check_should_write()
        if emails:
            for email in emails:
                if self.blacklist:
                    if not self.blacklist.is_blacklisted(email):
                        self.__emails.add(email)
                else:
                    self.__emails.add(email)

    def __check_should_write(self):
        if self.__should_write:
            self.write()
        elif len(self.__emails) > 10:
            self.__should_write = True

    def __sort_emails_into_tiers(self):
        for email in self.__emails:
            if EmailWriter.is_tier_1(email):
                self.__tier_1_emails[1].add(email)
            else:
                self.__tier_2_emails[1].add(email)

    @staticmethod
    def is_tier_1(email):
        tier1 = ["gmail", "yahoo", "hotmail", "aol"]
        for tier in tier1:
            if tier in email:
                return True

    def __write_tier_1(self):
        filename, emails = self.__tier_1_emails
        f = open(filename, 'a')
        for email in emails:
            f.write("%s\n" % email)
        f.close()

    def __write_tier_2(self):
        filename, emails = self.__tier_2_emails
        f = open(filename, 'a')
        for email in emails:
            f.write("%s\n" % email)
        f.close()

    def __empty_email_sets(self):
        self.__tier_1_emails = ('{}/tier_1_emails.txt'.format(self.__homedir), set())
        self.__tier_2_emails = ('{}/tier_2_emails.txt'.format(self.__homedir), set())
        self.__emails = set()

    def write(self):
        self.__sort_emails_into_tiers()
        self.__write_tier_1()
        self.__write_tier_2()
        self.__empty_email_sets()
        self.__should_write = False
