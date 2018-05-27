from os.path import expanduser


class EmailWriter(object):

    __emails = set()

    __homedir = expanduser("~")

    __tier_1_emails = ('{}/tier_1_emails.txt'.format(__homedir), set())
    __tier_2_emails = ('{}/tier_2_emails.txt'.format(__homedir), set())

    __should_write = False

    def __init__(self):
        pass

    def add_email(self, email):
        self.__check_should_write()
        self.__emails.add(email)

    def __check_should_write(self):
        if self.should_write:
            self.write()
        elif len(self.__emails) > 10:
            self.should_write = True

    def __sort_emails_into_tiers(self):
        for email in self.__emails:
            if EmailWriter.is_tier_1(email):
                self.__tier_1_emails[1].add(email)
            else:
                self.__tier_2_emails[1].add(email)

    @staticmethod
    def is_tier_1(email):
        if "gmail" or "yahoo" in email:
            return True

    def __write_tier_1(self):
        for filename, emails in self.__tier_1_emails:
            f = open(filename, 'a')
            for email in emails:
                f.write("%s\n" % email)
            f.close()

    def __write_tier_2(self):
        for filename, emails in self.__tier_2_emails:
            f = open(filename, 'a')
            for email in emails:
                f.write("%s\n" % email)
            f.close()

    def write(self):
        self.__sort_emails_into_tiers()
        self.__write_tier_1()
        self.__write_tier_2()
