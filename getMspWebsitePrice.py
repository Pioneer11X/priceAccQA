# This is the script where we select some random products from our website and get their prices ( for a specific store of course )

import keys
import pymysql
import pymysql.cursors

# first we need to formualte the url

# We need to get the popular subcategories from our DB and for that we need to connect to our db

class StoreQA:

    store = "jabong"

    def getPopSubCat(self):

        connection = pymysql.connect(
                host=keys.mysqlHost,
                user=keys.mysqlUser,
                password=keys.mysqlPass,
                db=keys.mysqlCrawlDb,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

		try:
			with connection.cursor() as cursor:
				# sql = "select item_id from fashion_lines where store = '" + self.store + "' limit 1"
				sql = "select distinct fel.category, fel.subcategory from fashion_entry_url fel, subcategory_crawl_config scc where fel.category = scc.category and fel.store ='" + self.store + "' and scc.crawl_day_of_week = -1"
				cursor.execute(sql)
				result = cursor.fetchone()
				print(result)
		except:
			print "Exception Occured"
			result = "kappa"
		finally:
			connection.close()
			print ( result )

		return



store = "jabong"
test = StoreQA()
test.getPopSubCat()
