from urlparse import urlparse

class UrlInfo(object):
		
	def __init__(self, parseResult):
		self.parse_result = parseResult

	def get_full_url(self):
		return self.parse_result.scheme + "://" + self.parse_result.netloc + self.parse_result.path

	def get_base_url(self):
		return self.parse_result.scheme + "://" + self.parse_result.netloc


class UrlInfoUtil(object):
	

if __name__ == "__main__":
	urlp = urlparse('http://this.com/that')
	data = UrlInfo(urlp)
	print(data.get_full_url())
	print(data.get_base_url())
	
