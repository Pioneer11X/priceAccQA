# This is the script where we select some random products from our website and get their prices ( for a specific store of course )

import keys
import pymysql
import pymysql.cursors


# first we need to formualte the url

# We need to get the popular subcategories from our DB and for that we need to connect to our db

'''

connection = pymysql.connect(
		host=keys.mysqlHost,
		user=keys.mysqlUser,
		password=keys.mysqlPass,
		db=keys.mysqlDbName,
		charset='utf8mb4',
		cursorclass=pymysql.cursors.DictCursor)

try:
	with connection.cursor() as cursor:
		sql = "select * from fashion_lines where store = 'jabong' limit 1"
		cursor.execute(sql)
		result = cursor.fetchone()
		print(result)

finally:
	connection.close()

'''


class StoreQA:

	store = "jabong"
	
	'''
	def __init__(self, store):
		self.store = store
		self.result = self.getPopSubCat(store)
	'''
	

	def getPopSubCat(self):
		connection = pymysql.connect(
				host=keys.mysqlHost,
				user=keys.mysqlUser,
				password=keys.mysqlPass,
				db=keys.mysqlDbName,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
		print "here"

		try:
			with connection.cursor() as cursor:
				sql = "select distinct fel.category, felsubcategory from fashion_entry_url fel, subcategory_crawl_config scc where fel.category = scc.category and fel.store ='" + self.store + "' and scc.crawl_day_if_week = -1"
				cursor.execute(sql)
				result = cursor.fetchone()
				print(result)
		except:
			print "Exception Occured"
			result = "kappa"
		finally:
			connection.close()
			print ( result )


if __name__ == " ___main__":
	store = "jabong"
	# test = StoreQA(store)
	test = StoreQA()
	print ( test )
	test.getPopSubCat()


