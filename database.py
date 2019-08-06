import psycopg2 as pg

class DatabaseOperations:
	def __init__(self):
		pass
		
	def mk_table(self, make_table):
		db = pg.connect(dbname="web_crawler")
		c = db.cursor()
		query = "create table if not exists " + make_table + "(child int4 , hrefs varchar, parent int4, scraped_status bool)"
		try:
			c.execute(query)
		except:
			pass
		db.commit()
		db.close()
		
	def insert_into(self, **kwargs):
		query = 'insert into ' + kwargs['table_name'] + ' values' + str(kwargs['to_insert'][0])
		for i in range(1, len(kwargs['to_insert'])):
			query += ','+str(kwargs['to_insert'][i])
		query += ';'
		import pdb; pdb.set_trace()
		db = pg.connect(dbname="web_crawler")
		c = db.cursor()
		c.execute(query)
		#except:
			#pass
		if 'update' in kwargs:
			self.update(update=kwargs['update'],table_name=kwargs['table_name'], set_clause=kwargs['set_clause'], where=kwargs['where'])
		self.commit(db)
		
	def select_from(self, table_name):
		conn = pg.connect(dbname='web_crawler')
		cur = conn.cursor()
		cur.execute("""SELECT * from """ + table_name + """ where scraped_status = false;""")
		rows = cur.fetchall()
		cur.close()
		return rows
		
	def select_count(self, **kwargs):
		if len(kwargs) > 1:
			query = """select count(*) from """ + kwargs['table_name'] + kwargs['where']
		elif 'table_name' in kwargs:
			query = """select count(*) from """ + kwargs['table_name']
		conn = pg.connect(dbname='web_crawler')
		cur = conn.cursor()
		cur.execute(query)
		rows = cur.fetchall()
		cur.close()
		return rows[0][0]
		
	def commit(self, connection_object):
		connection_object.commit()
		connection_object.close()
		
	def update(self, **kwargs):
		query="""update """+kwargs['table_name']+ kwargs['set_clause']+kwargs['where']
		conn = pg.connect(dbname='web_crawler')
		cur = conn.cursor()
		if 'update' in kwargs:
			cur.execute(query)
		else:	
			cur.execute(query)
		self.commit(conn)
			
		
		
		
		
		
		
		
		
		
