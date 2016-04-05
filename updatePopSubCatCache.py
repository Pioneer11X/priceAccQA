import keys
import pymysql
import pymysql.cursors

stores = ['jabong','flipkart','yepme','shopclues','amazon','babyoye','trendin','fabfurnish','zivame','fashionara','zansaar','pepperfry','koovs','snapdeal','bewakoof']


for store in stores:

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
            sql = "select distinct fel.category, fel.subcategory from fashion_entry_url fel, subcategory_crawl_config scc where fel.category = scc.category and fel.store ='" + store + "' and scc.crawl_day_of_week = -1"
            # TODO So, apparently this process takes a bit too much time. We need a cache to handle this as well. We can update the cache once every week or so. We need another script for that.
            cursor.execute(sql)
            result = cursor.fetchall()
    except:
        print "Exception Occured"
        result = "None as an Exception Occured. Please check"
    finally:
        connection.close()
        cacheFile = open("popSubCatCache/" + store + '.cache','w')
        for row in result:
            str = row['category'] + ':::' + row['subcategory']
            cacheFile.write(str + "\n")
        cacheFile.close()
