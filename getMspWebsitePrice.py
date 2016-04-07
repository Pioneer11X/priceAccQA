# This is the script where we select some random products from our website and get their prices ( for a specific store of course )

import keys
import pymysql
import pymysql.cursors
import urllib2
import re
import random

# first we need to formualte the url

# We need to get the popular subcategories from our DB and for that we need to connect to our db

class Item:

	item_id = ""
	mspPrice = 0
	store = ""


	def __init__(self, item_id, mspPrice):
		self.item_id = item_id
		self.mspPrice = mspPrice

	def setUrl(self, url):
		self.url = url

	def getStorePrice(self,regex, logFile):
		try:
			data = urllib2.urlopen(self.url)
			dataString = data.read()
			priceSearchString = regex
			priceMatches = re.findall(priceSearchString,dataString)
		except ( urllib2.HTTPError, urllib2.URLError, urllib2.httplib.IncompleteRead ) as e:
			print(e)
		try:
			return priceMatches[0]
		except:
			# print (self.url + " is messed up")
			logFile.write(self.url + " is messed up\n")
			# print(priceMatches)
			return 0



class StoreQA:

	store = ""
	subcategories = []

	def __init__(self, store):
		self.store = store
		self.getPopSubCat()

	def getPopSubCat(self):
		store = self.store
		cacheFile = open(keys.docRoot + "popSubCatCache/" + store + '.cache','r')
		cache = cacheFile.readlines()
		for line in cache:
			lineArray = line.split(":::")
			temp = {}
			temp['category'] = lineArray[0]
			temp['subcategory'] = lineArray[1].rstrip("\n")
			self.subcategories.append(temp)
		return self.subcategories

	def getProducts(self, logFile):
		itemsList = []
		for subCat in self.subcategories:
			# print(subCat)
			url = "http://www.mysmartprice.com/" + subCat['category'] + "/" + subCat['subcategory'] + "?subcategory=" + subCat['subcategory'] + "&property=store:" + self.store
			# print(url)
			logFile.write(url + "\n")
			try:
				dump = urllib2.urlopen(url)
			except ( urllib2.HTTPError, urllib2.URLError, urllib2.httplib.IncompleteRead ) as e:
				print(e)
			dumpString = dump.read()
			itemIdSearchString = "prdct-item prdct-item--nc\" data-mspid=\"([\d]*)\""
			priceSearchString = "<div class=\"prdct-item__prc (prdct-item__prc-mdl)*\">\n<span class=\"prdct-item__rpe\">&#8377;</span>\n<span class=\"prdct-item__prc-val\">([\d]*)</span>\n</div>"
			itemIdMatches = re.findall(itemIdSearchString,dumpString)
			priceMatches = re.findall(priceSearchString,dumpString)
			noOfItems = itemIdMatches.__len__()
			noOfPrices = priceMatches.__len__()

			if noOfItems == noOfPrices:
				for i in range(0,noOfItems//10):
					j = random.randint(0,noOfItems-1)
					temp = (itemIdMatches[j],priceMatches[j][1])
					itemsList.append(temp)
				'''for i in range(0,noOfItems):
					temp = (itemIdMatches[i],priceMatches[i][1])
					itemsList.append(temp)
					'''
			else:
				continue
			# exit()
			# return itemsList
		return itemsList


class StoreRegex:

	priceRegex = {}

	def __init__(self):
		fp = open(keys.docRoot + "storeRegex.txt",'r')
		data = fp.readlines()
		# print(data)
		noOfLines = data.__len__()
		for i in range(0,noOfLines):
			line = data[i]
			line = line.rstrip('\n')
			# print(line)
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

