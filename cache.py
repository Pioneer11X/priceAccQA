import pymysql
import pymysql.cursors
import keys


class Cache:

    store = ""
    dataDict = {}

    def __init__(self, store):
        self.store = store
        fp = open(keys.docRoot + "urlCaches/" + store + ".cache", 'r')
        for line in fp:
            # print(line)
            temp = line.split(":::")
            # print(temp)
            self.dataDict[temp[0]] = temp[1]
        fp.close()

    def getUrl(self,item_id):
        try:
            return self.dataDict[item_id]
        except:
            # So, the item_id is not here. Now we probe the DB.
            try:
                connection = pymysql.connect(
                    host=keys.mysqlHost,
                    user=keys.mysqlUser,
                    password=keys.mysqlPass,
                    db=keys.mysqlDbName,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                with connection.cursor() as cursor:
                    sql = "select url,store from fashion_lines where item_id = '" + item_id + "'"
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    # print(result)
                    url = result['url']
                    self.dataDict[item_id] = url

                    # print(self.dataDict)

                    fp = open(keys.docRoot + "urlCaches/" + self.store + ".cache", 'a')
                    temp = item_id + ":::" + self.dataDict[item_id] + "\n"
                    temp = temp.encode('utf-8')
                    # print(temp)
                    fp.write(temp)
                    fp.close()
                connection.close()
                return self.dataDict[item_id]
            except pymysql.err.OperationalError as e:
                print("Exceptoin when trying to get the store Url for the product. Message: " + str(e))
                result = "None"
                return None