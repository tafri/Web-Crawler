import re

class Utility:
	def __init__(self, **kwargs):
		if len(kwargs) != 0:
			self.url = kwargs['url']
			self.url_parts = kwargs['url_parts']
			self.base_url1 = kwargs['base_url1']
			self.base_url2 = kwargs['base_url2']
		
	def reformat_urls(self, **kwargs):
		self.links_list = kwargs['list_']
		i = 0
		while i < len(self.links_list):
			uri_parts = re.split('[/]', self.links_list[i])
			if (uri_parts[0] == '.'):
				self.links_list[i] = 'https://' + self.url_parts[1] + self.links_list[i][1:]
				i += 1
			elif (uri_parts[0] == ''):
				self.links_list[i] = 'https://' + self.url_parts[1] + self.links_list[i]
				i += 1
			elif (64 < ord(uri_parts[0][0]) < 91) or (96 < ord(uri_parts[0][0]) < 123):
				self.links_list[i] = self.base_url1 + self.links_list[i]
				i += 1
			elif len(uri_parts) > 1 and ((uri_parts[1] == self.base_url1) or (uri_parts[1] == self.base_url2)):
				i += 1
			else:
				del self.links_list[i]
		return self.links_to_tuple(kwargs['parent'])
				
				
	def links_to_tuple(self, parent):
		scraped_status, i = 0, 0
		while i < len(self.links_list):
			child = self.hash(self.links_list[i])
			self.links_list[i] = str((child, self.links_list[i], parent, False))
			i += 1
		return self.links_list

		
	def hash(self, string):
		h1, h2, i = 1, 1, 0
		while i < len(string):
			if i%2 == 0:
				h1 *= ord(string[i])
				i += 1
			else:
				h2 *= ord(string[i])
				i += 1
		i = (h1+h2)%7919
		return i
