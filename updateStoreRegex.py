import keys
import pymysql
import pymysql.cursors

# TODO -- Need to completet the script which updates the Txt File.

class storeRegex:

    store = ""

    def __init__(self,store):
        self.store = store

    def getPriceRegex(self):
        connection = new pymysql
