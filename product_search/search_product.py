import json
from product_search.models.Product import Product
from serpapi import GoogleSearch

def search_product(input_product : Product):
    link,imlink = get_product_link(input_product)

    #print('here')
    #print(link)
    #print(imlink)
    #input_product.populate_product_using_link(link)
    return [(input_product,link)]



def get_product_link(input_product : Product):
    name_on_receipt = input_product[0]

    price_in_pounds = input_product[1]
    # returns [pounds, pence] in int

    search_query : str = f"{name_on_receipt} £{price_in_pounds} Sainsbury's"
    # e.g. "cocoa powder £3.15 site:https://www.sainsburys.co.uk/"

    private_api_key = "49e5a4ce4fe4d94be42dbd3ed06605cc55e20c85002bcadebe422993536c8fd9"



    params = {
    "q": search_query,
    "hl": "en",
    "gl": "uk",
    "google_domain": "google.com",
    "api_key": private_api_key
    }

    search = GoogleSearch(params)

    results = search.get_dict()
    link = __get_link_from_results(results)
    try:
        image_link = results["inline_images"][0]["original"]
    except:
        image_link = ""
    #print(link)
    return link, image_link

def __populate_product_using_link(input_product : Product, link : str):
    pass

def __get_link_from_results(results):
    return results["organic_results"][0]["link"]

def __pounds_to_pence(price_in_pence: int):
    pounds = price_in_pence // 100
    pence = price_in_pence % 100
    return [pounds, pence]
