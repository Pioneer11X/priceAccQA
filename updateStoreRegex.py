import keys
import pymysql
import pymysql.cursors

# TODO -- Need to completet the script which updates the Txt File.

connection = pymysql.connect(
    host=keys.mysqlHost,
    user=keys.mysqlUser,
    password=keys.mysqlPass,
    db=keys.mysqlCrawlDb,
    harset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # sql = "select item_id from fashion_lines where store = '" + self.store + "' limit 1"
        sql = ""
        cursor.execute(sql)
        result = cursor.fetchall()
except:
    print "Exception Occured"
    result = "None as an Exception Occured. Please check"
finally:
    connection.close()

class storeRegex:

    store = ""

    def __init__(self,store):
        self.store = store


