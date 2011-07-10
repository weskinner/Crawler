import urllib2, sgmllib, sys

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
		self.paras = []
		self.inside_p = 0

	def start_a(self, attributes):
		"Process a hyperlink and its 'attributes'."
		for name, value in attributes:
			if name == "href":
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

	def p_is_relevant(self,p):
		return len(p) > 100



response = urllib2.urlopen(sys.argv[1])
html = response.read()

myparser = MyParser()
myparser.parse(html)

links = myparser.get_hyperlinks()
paras = myparser.get_paras()

for link in links:
	print link

for para in paras:
	print para