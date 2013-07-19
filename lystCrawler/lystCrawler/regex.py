import re


SHOES =re.compile (r'\b[s|S]{1}hoe[s]*\b|\b[w|W]{1}edge[s]*\b|\b[b|B]{1}oot[s]*\b|\b[b|B]{1}ootie[s]*\b|\b[p|P]{1}ump[s]*\b|\b[h|H]{1}eel[s]*\b|\b[s|S]{1}neaker[s]*\b')
JEWELRY = re.compile(r'\b[b|B]{1}racelet[s]*\b|\b[n|N]{1}ecklace[s]*\b|\b[r|R]{1}ing[s]*\b|\b[e|E]{1}arring[s]*\b')
BAGS = re.compile(r'\b[b|B]{1}ag[s]*\b')
ACCESSORIES = re.compile(r'\b[s|S]{1}unglasses{1}|\b[h|H]{1}at[s]*\b')	

class itemAttributes(object):
	""" This class uses regular expressions to extract some attributes of a crawled product (type and color)"""
	

	def findType(self, description):
		"""	tries to assign a type to the item given the description
		the regular expression represent key words for a specific category
		most common type is apparel - so, if no other type found than item is most likely apparel"""

		s = re.findall(SHOES, description)
		b = re.findall(BAGS, description)
		j = re.findall(JEWELRY, description)
		r = re.findall(ACCESSORIES, description)
		print r
		if (len(s) > 0):
			return 'S'
		elif (len(b) > 0):
			return 'B'
		elif (len(j) > 0):
			return 'J'
		elif (len(r) > 0):
			return 'R'
		else:
			return 'A'

	

	def findColor(self, description):
		"""	searches the description and attempts to match a color (limited range)
	 	sets a default color if no color was found """

		color = ''
		if(len(re.findall(re.compile(r'\bblack\b'),description))):
			color+= 'black '
		if(len(re.findall(re.compile(r'\white\b'),description))):
			color+= 'white '
		if(len(re.findall(re.compile(r'\bbeige\b'),description))):
			color+= 'beige '
		if(len(re.findall(re.compile(r'\bsilver\b'),description))):
			color+= 'silver '
		if(len(re.findall(re.compile(r'\bgray\b'),description))):
			color+= 'gray '
		if(len(re.findall(re.compile(r'\bnavy\b'),description))):
			color+= 'navy '
		if(len(re.findall(re.compile(r'\bblue\b'),description))):
			color+= 'blue '
		if(len(re.findall(re.compile(r'\bgreen\b'),description))):
			color+= 'green '
		if(len(re.findall(re.compile(r'\bolive\b'),description))):
			color+= 'olive '
		if(len(re.findall(re.compile(r'\bgolden\b'),description))):
			color+= 'golden '
		if(len(re.findall(re.compile(r'\bcoral\b'),description))):
			color+= 'coral '
		if(len(re.findall(re.compile(r'\bpink\b'),description))):
			color+= 'pink '
		if(len(re.findall(re.compile(r'\bred\b'),description))):
			color+= 'red '
		if(len(re.findall(re.compile(r'\byellow\b'),description))):
			color+= 'yellow '
		if(len(re.findall(re.compile(r'\bviolet\b'),description))):
			color+= 'violet '
		if(len(re.findall(re.compile(r'\bbrown\b'),description))):
			color+= 'brown '
		if(len(re.findall(re.compile(r'\bmaroon\b'),description))):
			color+= 'maroon '
		if(len(re.findall(re.compile(r'\bcreme\b'),description))):
			color+= 'creme '
		if(color == ""):
			color+= 'def_color'
		return color
