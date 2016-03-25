import getMspWebsitePrice

# Lets see how this turns out.
# First we need to create a StoreQA class to get the subcategories for a specific store.as

store = "jabong"

storeQA = getMspWebsitePrice.StoreQA(store)
storeRegex = getMspWebsitePrice.StoreRegex()

# Now, we get the products for the first popular subcategory.

products = storeQA.getProducts()

noOfProducts = products.__len__()

print str(noOfProducts) + " Items Present"

correct = 0
wrong = 0
for i in range(0,noOfProducts):
    if i%10 == 0:
        print("%d/%d Done."%(i,noOfProducts))

    try:
        item = getMspWebsitePrice.Item(products[i][0],products[i][1])
        mspPrice = item.mspPrice
        storePrice = item.getStorePrice(storeRegex.getStoreRegex(store))
        # print "StorePrice : " + storePrice + " MSPPrice: " + mspPrice
        if storePrice == mspPrice:
            correct+=1
        else:
            wrong+=1
    except:
        print("Number of Producst checked: " + str(i))
        print("Correct: " + str(correct))
        break

percentage = (float(correct)/float(noOfProducts)) * 100
print (str(percentage) + " is the accuracy for store: " + store)
