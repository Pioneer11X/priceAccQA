# This is the script where we select some random products from our website and get their prices ( for a specific store of course )

import keys
import pymysql
import pymysql.cursors
import urllib2
import re
import json

# first we need to formualte the url

# We need to get the popular subcategories from our DB and for that we need to connect to our db

class Item:

	item_id = ""
	mspPrice = 0
	store = ""
	url = ""


	def __init__(self, item_id, mspPrice):
		self.item_id = item_id
		self.mspPrice = mspPrice
		(self.url,self.store) = self.getUrl()

	def getUrl(self):

		connection = pymysql.connect(
			host=keys.mysqlHost,
			user=keys.mysqlUser,
			password=keys.mysqlPass,
			db=keys.mysqlDbName,
			charset='utf8mb4',
			cursorclass=pymysql.cursors.DictCursor
		)
		try:
			#TODO SO, apparently handling data is not as easy as it is in PHP. I need to define my own class and shit now. which can decode the data dump. We use an object of that class to get the url here and we update the cache with an inbuilt method for the class.
			fp = open("urlCache.json","r")
			jsonVar = json.load(fp)
			fp.close()
			return jsonVar[self.item_id]

		except:
			try:
				with connection.cursor() as cursor:
					sql = "select url,store from fashion_lines where item_id = '" + self.item_id + "'"
					cursor.execute(sql)

					fp = open("urlCache.json","w")
					result = cursor.fetchone()
					jsonVar[self.item_id] = result
					json.dump(fp)
					fp.close()

			except:
				print("Exceptoin when trying to get the store Url for the product.")
				result = "None"
			finally:
				connection.close()

		return (result['url'],result['store'])

	def getStorePrice(self,regex):
		data = urllib2.urlopen(self.url)
		dataString = data.read()
		priceSearchString = regex
		priceMatches = re.findall(priceSearchString,dataString)
		try:
			return priceMatches[0]
		except:
			print (self.url + " is messed up")
			return 0


class StoreQA:

	store = ""
	subcategories = []

	def __init__(self, store):
		self.store = store
		self.getPopSubCat()

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

	def getProducts(self):
		itemsList = []
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
			noOfItems = itemIdMatches.__len__()
			noOfPrices = priceMatches.__len__()

			if noOfItems == noOfPrices:
				for i in range(0,noOfItems):
					temp = (itemIdMatches[i],priceMatches[i][1])
					itemsList.append(temp)
			else:
				continue
			# exit()
			return itemsList
		# return itemsList


class StoreRegex:

	priceRegex = {}

	def __init__(self):
		fp = open("storeRegex.txt",'r')
		data = fp.readlines()
		# print(data)
		noOfLines = data.__len__()
		for i in range(0,noOfLines):
			line = data[i]
			array = line.split(":::")
			self.priceRegex[array[0]] = array[1]

	def getStoreRegex(self,store):
		return self.priceRegex[store]

'''
kap = StoreRegex()
print(kap.getStoreRegex("jabong"))


trial = Item("52835269",1495)
print(trial.getStorePrice(kap.getStoreRegex("jabong")))


test = StoreQA("jabong")
test.getPopSubCat()
test.getProducts()

new = StoreQA("flipkart")
new.getPopSubCat()
'''

