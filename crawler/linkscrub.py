from urlparse import urlparse
from collections import deque

# data = ['http://this.com', 'http://this.com/that', 'http://this.com/this', 'http://guy.com']

data = [u'https://en.wiktionary.org/wiki/thatt', u'http://www.yourdictionary.com/thatt',
        u'https://www.urbandictionary.com/tags.php?tag=thatt',
        u'https://www.tripadvisor.in/LocationPhotoDirectLink-g777115-d8738352-i218252612-Palakkayam_Thattu-Kannur_Kannur_District_Kerala.html',
        u'https://www.instagram.com/explore/tags/thatt/?hl=en',
        u'https://www.tripadvisor.com/LocationPhotoDirectLink-g777115-d8738352-i218252461-Palakkayam_Thattu-Kannur_Kannur_District_Kerala.html',
        u'https://www.ancestry.com/name-origin?surname=thatt',
        u'https://www.thefreedictionary.com/words-that-start-with-thatt',
        u'https://www.researchgate.net/profile/Timothy_Tan4',
        u'https://commons.wikimedia.org/wiki/File:Palakkayam_thatt_04.jpg', u'https://society6.com/thatthello',
        u'https://www.thattelectrical.com/past-projects?lightbox=dataItem-ifi6027g3',
        u'https://hotpads.com/2-thatt-way-hopkinton-ri-02833-1j5pp3h/pad',
        u'https://soundcloud.com/lenka-smyth2/listen-to-thatt', u'https://www.spellchecker.net/misspellings/thatt',
        u'https://search.ancestry.co.uk/cgi-bin/sse.dll?db=pubmembertrees&rank=1&sbo=t&gsbco=Sweden&gsln=Thatt',
        u'https://www.bloomberg.com/research/stocks/private/person.asp?personId=257441166&privcapId=257167415',
        u'https://www.lazada.com.my/shop/whatt-thatt?path=product.htm&hideHeadFoot=true',
        u'http://www.expert-exchange.org/blog/project-17-veha-and-thatt-get-sponsored',
        u'https://www.alt.dk/mode/lou-thatt-patriksson-hjem-og-stil',
        u'https://www.mixcloud.com/thatts-chinnouse/favorites/',
        u'https://www.tripadvisor.fr/LocationPhotoDirectLink-g777115-d8738352-i218252481-Palakkayam_Thattu-Kannur_Kannur_District_Kerala.html',
        u'https://www.zillow.com/browse/homes/ri/washington-county/02833/thatt-way_4991676/',
        u'https://www.fancythattt.com/',
        u'https://www.tripadvisor.fr/LocationPhotoDirectLink-g777115-d8738352-i218252612-Palakkayam_Thattu-Kannur_Kannur_District_Kerala.html',
        u'http://adage.com/article/focus-design/database-cosmetics-thatt-s-ibm/54424/',
        u'https://www.canpages.ca/page/NB/fredericton/thatt-electrical-company/100633768',
        u'https://www.tripadvisor.es/LocationPhotoDirectLink-g777115-d8738352-i218252612-Palakkayam_Thattu-Kannur_Kannur_District_Kerala.html',
        u'https://www.bbb.org/atlantic-provinces/business-reviews/electrician/thatt-electrical-company-inc-in-waasis-nb-41216/reviews-and-complaints',
        u'http://www.researcherid.com/rid/G-6223-2010']


def scrub(links, base_occurences=10):
    print("LINKS: {}\n\n").format(links)

    urlp = []
    for link in links:
        try:
            lp = urlparse(link)
            urlp.append(lp)
        except:
            print("BLEW UP ON: {}".format(link))
            continue

    # urlp = [urlparse(x) for x in links]

    urls_base = [x.scheme + "://" + x.netloc for x in urlp]
    base_count = [urls_base.count(x) for x in urls_base]
    urls_full = [x.scheme + "://" + x.netloc + x.path for x in urlp]

    base_and_count = zip(urls_base, base_count)

    print("BASECOUNT: {}\n\n").format(base_and_count)

    full_base_count = zip(urls_full, base_and_count)

    print("FULLBASE: {}\n\n").format(full_base_count)

    new_linklist = []
    for item in full_base_count:
        if item[1][1] < base_occurences:
            new_linklist.append(item[0])

    return new_linklist


print scrub(data)
