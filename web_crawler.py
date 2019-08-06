import re, requests
from bs4 import BeautifulSoup
from database import DatabaseOperations
from file_handling import FileOperations
from utility import Utility

class WebCrawler:
	def __init__(self, url):
		self.url = url
		self.diff_urls()
		
	def diff_urls(self):
		'''--INITIALIZING URLs--'''
		self.url_parts = re.split('[/]+', self.url)
		self.dns = re.split('[.]', self.url_parts[1])
		self.base_url1 = 'http://' + self.url_parts[1] + '/'
		self.base_url2 = 'http://' + self.url_parts[1] + '/'
		if len(self.dns) == 3:
			self.base_url1 = 'http://' + self.url_parts[1] + '/'
			self.base_url2 = 'http://' + self.dns[1] + self.dns[2] + '/'				'''--This is just for checking purpouse.--'''
			
			'''--INITIALIZING FOLDER AND TABEL--'''
		if len(self.dns) > 2:
			self.dns = self.dns[1]
		elif len(self.dns) == 2:
			
			'''--INITIALIZING FOLDER AND TABEL--'''
			self.dns = self.dns[0]
		self.choice()
		
		
			
	def choice(self):
		'''--PREPARING URL FOR CHOICE--'''
		if self.url_parts[-1] == '':
			self.url_parts.remove('')
			
		if len(self.url_parts) == 2:
			self.initial_setup(self.dns, 'base')
		elif len(self.url_parts) > 2:
			#import pdb; pdb.set_trace()
			print('press 1 to scrap from base website\t' + self.base_url1)
			print('press 2 to scrap from relative website\t' + self.url)
			self.choice = int(input())
			if  self.choice == 1:
				self.initial_setup(self.dns, 'base')
			elif self.choice == 2:
				self.dns = self.dns  + '_' + self.url_parts[-1]
				self.initial_setup(self.dns, 'relative')
				

	def initial_setup(self, dns='', path='base'):
		self.make = path + '_' + dns
		
		'''CREATE DIRECTORY FOR IMAGES.'''
		FileOperations().mk_dir(self.make)
		
		'''CREATE TABLE TO STORE LINKS.'''
		DatabaseOperations().mk_table(self.make)
		
		'''Insert ROOT link.'''
		if path == 'base':
			href = self.base_url1
			child = Utility().hash(self.base_url1)
		elif path == 'relative':
			href = self.url
			child = Utility().hash(self.url)
			
		parent, scraped_status = 1, False
		DatabaseOperations().insert_into(table_name=self.make, to_insert=[(child, href, parent, scraped_status)])
		
		
	def spider(self):
		'''--GET HREFs FROM TABLE WHICH HAS SCRAPED_STATUS AS ZERO, AND SCRAPED THEM!!!--'''
		unscraped_links = DatabaseOperations().select_from(self.make)
		do = DatabaseOperations()
		for href in unscraped_links:
			links_list = []
			raw_data = requests.get(href[1])
			souped_data = BeautifulSoup(raw_data.text, features="html.parser")
			anchors = souped_data.findAll('a')
			for i in range(len(anchors)):
				try:
					links_list.append(anchors[i]['href'])
				except:
					pass
			links_list = Utility(url=self.url, url_parts=self.url_parts, base_url1=self.base_url1, base_url2=self.base_url2).reformat_urls(list_=links_list, parent=href[0])
			import pdb; pdb.set_trace()
			do.insert_into(table_name=' '+self.make+' ', to_insert=links_list, update=True, set_clause=' set scraped_status=true ', where=' where child= ' +str(Utility().hash(href[1]))+' ')
		if (do.select_count(table_name=self.make, where=' where scraped_status=false ')) and (do.select_count(table_name=self.make) < 7800):
			self.spider()
			
			
