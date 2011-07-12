import urllib2, sgmllib, sys, urlparse
from urlparse import urlparse

class MyParser(sgmllib.SGMLParser):
	"A simple parser class."

	def parse(self,s):
		"Parse the given string 's'."
		self.feed(s)
		self.close()

	def __init__(self, verbose=0):
		"Init an object, passing 'verbose' to the superclass."
		sgmllib.SGMLParser.__init__(self, verbose)
		self.hyperlinks = []
		self.paths = []
		self.paras = []
		self.inside_p = 0

	def start_a(self, attributes):
		"Process a hyperlink and its 'attributes'."
		for name, value in attributes:
			if name == "href":
				url = urlparse(value)
				if(url.path):
					self.paths.append(url.path)
				if(url.scheme and url.scheme == "http"):
					self.hyperlinks.append(value)

	def start_p(self, attributes):
		self.inside_p = 1

	def end_p(self):
		self.inside_p = 0

	def handle_data(self, data):
		if self.inside_p:
			if(self.p_is_relevant(data)):
				self.paras.append("\n\n" + data)
	
	def get_hyperlinks(self):
		return self.hyperlinks

	def get_paras(self):
		return self.paras

	def get_paths(self):
		return self.paths

	def p_is_relevant(self,p):
		return len(p) > 100



def crawl(link):
	try:
		parser = MyParser()

		h = urllib2.urlopen(link).read()	
		parser.parse(h)

		parser.get_hyperlinks().reverse()
		for l in parser.get_hyperlinks():
			print l
			crawl(l)
	except:
		print "=== ERROR GETTING " + link + " ==="

crawl(sys.argv[1])