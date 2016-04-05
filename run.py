import getMspWebsitePrice
import time
import cache

# Lets see how this turns out.
# First we need to create a StoreQA class to get the subcategories for a specific store.as

# store = "jabong"

stores = ['shopclues', 'amazon', 'jabong', 'flipkart', 'yepme']

for store in stores:

    percentage = 0.00

    logFile = open(store + ".log","w")
    messedUpFile = open("messedUpCache/" + store + ".cache", 'w')

    print(store)

    TotalTime = {
        "StoreQAInit":0,
        "CacheInit":0,
        "StoreRegexInit":0,
        "GetProducts":0,
        "ItemInit":0,
        "ItemUrlGrab":0,
        "ItemGetStorePrice":0,

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
        if i%100 == 0:
            print("%d/%d Done." % (i, noOfProducts))

        # try:
        startTime = time.time()

        item = getMspWebsitePrice.Item(products[i][0],products[i][1])

        tempTime = time.time()
        timeTaken = tempTime - startTime
        startTime = tempTime
        # print("Item Initialiser : %s Seconds"%timeTaken)
        TotalTime['ItemInit'] += timeTaken

        tempUrl = cacheVariable.getUrl(item.item_id)
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
            correct+=1
            counted+=1
        elif storePrice!=0:
            wrong+=1
            counted+=1
        '''except:
            print(Exception.__class__)
            print("Number of Producst checked: " + str(i))
            print("Correct: " + str(correct))
            percentage = (float(correct)/float(i+1)) * 100
            break
        '''

    if counted != 0:
        percentage = (float(correct)/float(counted)) * 100
    else:
        percentage = None
    # TODO SO, we need to change how the percentae is calculated. In case of an exception, we currently calculate the wrong percentage( The denominator must be Number of Products Checked rather than noOfTotalProducts. Fix that.
    print (str(percentage) + " is the accuracy for store: " + store)
    print("Total: %d\nChecked: %d\nCorrect: %d\nWrong: %d"%(noOfProducts, counted, correct, wrong))
    print(TotalTime)
    logFile.close()
