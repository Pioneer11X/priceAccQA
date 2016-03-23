# This is the script where we select some random products from our website and get their prices ( for a specific store of course )

import keys
import pymysql
import pymysql.cursors
import urllib2
import re

# first we need to formualte the url

# We need to get the popular subcategories from our DB and for that we need to connect to our db

class StoreQA:

	store = ""
	subcategories = []

	def __init__(self, store):
		self.store = store

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
				result = cursor.fetchall()
		except:
			print "Exception Occured"
			result = "None as an Exception Occured. Please check"
		finally:
			connection.close()
			print("Store: " + self.store)
			for row in result:
				self.subcategories.append(row)


		return self.subcategories

	def getRandomProducts(self):

		for subCat in self.subcategories:
			print(subCat)
			url = "http://www.mysmartprice.com/" + subCat['category'] + "/" + subCat['subcategory'] + "?subcategory=" + subCat['subcategory'] + "&property=store:" + self.store
			print(url)
			dump = urllib2.urlopen(url)
			dumpString = dump.read()
			itemIdSearchString = "prdct-item prdct-item--nc\" data-mspid=\"([\d]*)\""
			priceSearchString = "<div class=\"prdct-item__prc (prdct-item__prc-mdl)*\">\n<span class=\"prdct-item__rpe\">&#8377;</span>\n<span class=\"prdct-item__prc-val\">([\d]*)</span>\n</div>"
			itemIdMatches = re.findall(itemIdSearchString,dumpString)
			priceMatches = re.findall(priceSearchString,dumpString)
			print(itemIdMatches)
			print(priceMatches)
			exit()






test = StoreQA("jabong")
test.getPopSubCat()
test.getRandomProducts()

new = StoreQA("flipkart")
new.getPopSubCat()
