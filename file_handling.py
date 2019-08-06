import os
#sys.path.append('./../../db')
from database import DatabaseOperations
class FileOperations:
	def __init__(self):
		pass

	def mk_dir(self, make_dir):
		mkdir_path = os.path.abspath('.') + '/' + make_dir
		print(mkdir_path)
		if not os.path.exists(mkdir_path):
			os.mkdir(mkdir_path)
			DatabaseOperations().mk_table(make_dir)
		else:
			print('path already scraped!!!')
