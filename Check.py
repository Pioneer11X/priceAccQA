import getMspWebsitePrice
import time
import cache
import sys
import keys

# amazon jabong flipkart shopclues babyoye bewakoof yepme zansaar koovs zivame fashionara fabfurnish snapdeal trendin pepperfry

stores = ['shopclues', 'amazon', 'jabong', 'flipkart', 'yepme', 'babyoye', 'bewakoof', 'zansaar', 'koovs', 'zivame',
          'fashionara', 'fabfurnish', 'trendin', 'snapdeal', 'pepperfry']


class Check:
    def __init__(self, store):
        self.store = store

    def accCheck(self, debugFile=None):
        store = self.store
        logFile = open(keys.docRoot + "runLogs/" + store + ".log", "w")
        messedUpFile = open(keys.docRoot + "messedUpCache/" + store + ".cache", 'w')

        # print(store)

        TotalTime = {
            "StoreQAInit": 0,
            "CacheInit": 0,
            "StoreRegexInit": 0,
            "GetProducts": 0,
            "ItemInit": 0,
            "ItemUrlGrab": 0,
            "ItemGetStorePrice": 0,

        }

        startTime = time.time()

        storeRegex = getMspWebsitePrice.StoreRegex()

        tempTime = time.time()
        timeTaken = tempTime - startTime
        startTime = tempTime
        # print("StoreRegex Initialiser : %s Seconds"%timeTaken)
        TotalTime['StoreRegexInit'] += timeTaken

        storeQA = getMspWebsitePrice.StoreQA(store)

        tempTime = time.time()
        timeTaken = tempTime - startTime
        startTime = tempTime
        # print("StoreQA Initialiser : %s Seconds"%timeTaken)
        TotalTime['StoreQAInit'] += timeTaken

        cacheVariable = cache.Cache(store)

        tempTime = time.time()
        timeTaken = tempTime - startTime
        startTime = tempTime
        # print("Cache Initialiser : %s Seconds"%timeTaken)
        TotalTime['CacheInit'] += timeTaken

        # Now, we get the products for the first popular subcategory.

        products = storeQA.getProducts(logFile)

        tempTime = time.time()
        timeTaken = tempTime - startTime
        startTime = tempTime
        # print("getProducts Function : %s Seconds"%timeTaken)
        TotalTime['GetProducts'] += timeTaken

        noOfProducts = products.__len__()

        # print str(noOfProducts) + " Items Present"
        logFile.write(str(noOfProducts) + " Items Present\n")
        logFile.write("\n")

        # TODO So, apparently the time taken to run this script is rather high ( well, it took slmost half day just for once store. So, if we want to do it for all the stores, it might not be sufficient. So, I would assume we need a better solution. Now if the time taken delay is caused because of the sql connections ( when we get the url, we need to fix that by having a cache for the url.

        correct = 0
        wrong = 0
        counted = 0
        for i in range(0, noOfProducts):
            # try:
            startTime = time.time()

            item = getMspWebsitePrice.Item(products[i][0], products[i][1])

            tempTime = time.time()
            timeTaken = tempTime - startTime
            startTime = tempTime
            # print("Item Initialiser : %s Seconds"%timeTaken)
            TotalTime['ItemInit'] += timeTaken

            tempUrl = (cacheVariable.getUrl(item.item_id)).encode('utf-8')
            item.setUrl(tempUrl)
            logFile.write(tempUrl + "\n")

            tempTime = time.time()
            timeTaken = tempTime - startTime
            startTime = tempTime
            # print("Item Url grabbing: %s Seconds"%timeTaken)
            TotalTime['ItemUrlGrab'] += timeTaken

            mspPrice = item.mspPrice
            storePrice = item.getStorePrice(storeRegex.getStoreRegex(store), messedUpFile)

            tempTime = time.time()
            timeTaken = tempTime - startTime
            startTime = tempTime
            # print("Item getStorePrice Method : %s Seconds"%timeTaken)
            TotalTime['ItemGetStorePrice'] += timeTaken

            # print "StorePrice : " + storePrice + " MSPPrice: " + mspPrice
            if storePrice == mspPrice:
                correct += 1
                counted += 1
            elif storePrice != 0:
                # Debug Block

                if debugFile != None:
                    debugFp = open(debugFile, mode='a')
                    if debugFp:
                        debugString = tempUrl.rstrip('\n') + "::" + "Store Price: " + str(storePrice) + " mspPrice: " + str(mspPrice)
                        debugFp.write(debugString)
                        debugFp.close()

                wrong += 1
                counted += 1
                # exit()
            '''elif storePrice == 0:
                print(tempUrl + "---" + storeRegex.getStoreRegex(store))
                exit()'''
            '''except:
                print(Exception.__class__)
                print("Number of Producst checked: " + str(i))
                print("Correct: " + str(correct))
                percentage = (float(correct)/float(i+1)) * 100
                break
            '''

        if counted != 0:
            percentage = (float(correct) / float(counted)) * 100
        else:
            percentage = None
        # TODO SO, we need to change how the percentae is calculated. In case of an exception, we currently calculate the wrong percentage( The denominator must be Number of Products Checked rather than noOfTotalProducts. Fix that.
        print(str(percentage) + " is the accuracy for " + store)
        print("Total: %d\nChecked: %d\nCorrect: %d\nWrong: %d" % (noOfProducts, counted, correct, wrong))
        # print(TotalTime)
        logFile.close()


def run():
    if len(sys.argv) < 2:
        exit("Usage : python %s <StoreName>" % sys.argv[0])
    elif len(sys.argv) == 3:
        debugFile = sys.argv[2]
        store = sys.argv[1]
        print(debugFile)
        print(store)
        if store not in stores:
            # print("Please enter a valid store")
            exit("Please enter a valid store.. Entered store: " + store)
        test = Check(store)
        test.accCheck(debugFile)

    elif len(sys.argv) == 2:
        store = sys.argv[1]
        print(store)
        if store not in stores:
            # print("Please enter a valid store")
            exit("Please enter a valid store.. Entered store: " + store)
        test = Check(store)
        test.accCheck()
    else:
        exit("Usage : python %s <StoreName>" % sys.argv[0])


run()
