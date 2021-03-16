#Prabhnoor Singh SWE-INT submissions
import requests
import json
import pandas as pd

#ANSWER 1
#################################################################
#Using this url we wil initiate a download job for all products.
#Since List all item is not being used anymore , I will use
#get batch product download. I will be making 2 calls to get the url
#for the CSV file of all the products.First call to get the job_id
#Second call using that job_id to get all products,
def getUserProductData():
    url = "https://merchant.wish.com/api/v2/product/create-download-job"
    params = {
        "format": "json",
        "access_token": "an_example_access_token"
    }
    
    r = requests.post(url, params=params)
    jsonResponse = r.json()
    
    #Status code is 401 because we dont have the access_token here. 
    #So it is not able to authenticate. But I will assume that access_token
    #is valid and I get a valid response 
    job_id = jsonResponse['data']
    
    #Get data from job_id
    
    url = "https://merchant.wish.com/api/v2/product/get-download-job-status"
    params = {
        "format": "json",
        "access_token": "an_example_access_token",
        "job_id":job_id
    }
    
    #This 3 call is to download the CSV file
    r = requests.post(url, params=params)
    newJsonResponse = r.json()
    donwloadUrl = ''
    #If the status code is FINISHED, it means our data file is ready.
    if (newJsonResponse['data']['status'] == 'FINISHED'):
        donwloadUrl = newJsonResponse['data']['download_link']
    
    #Now using this donloadUrl we can download the CSV file of all products.
    data = pd.read_csv(donwloadUrl)
    return data
    #Here data is a csv file which has all the data of products.
    #I have made an assumption that CSV file will be a list of all the
    # products i.e. list of wish data model.
##################################################################

#ANSWER 2
def getDeliverrData(wishData):
    #Since we need only physical item , please see answer 3
    
    title = ""
    
    #I am assigning the title value only
    #once because all product variants come under the same product.So they
    #can have same description.
    title = wishData['data']['Product']['description']
    
    #Since a customer buys a product variant and not the actual product
    #I will look for product variants.
    #variantList is a list of all variants
    variantList = wishData['data']['Product']['variants']
    #track is a list which stores each product variant as a deliverr item
    track = []
    for object in variantList:
        productId = ""
        sku = ""
        productId = object['Variant']['product_id']
        sku = object['Variant']['sku']
        #Here I am making each deliverr item for each product variant
        item = {"productId":productId,"sku":sku,"title":title}
        track.append(item)
    #Here deliverrItem is a Json Object which has a list of all the
    #product variants
    deliverrItem = json.dumps(track)
    return deliverrItem
    
##########################################################################

#Answer 3

#This is something I would actually discuss with my co worker.
#Actually I went and searched about the wish api. And it turns out that
#wish only allows deliverable items to be sold on their platform.Digital
#item is prohibited to be sold there.So all the products list that I got
#in my Answer 1 will have physical items. So I dont need to worry about the
#case if the product is physical or not.

###########################################################################
