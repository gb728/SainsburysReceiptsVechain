from veryfi import Client
from abc import ABC
import json
import os
from product_search.search_product import search_product
from product_search.models.Product import Product
import requests
from bs4 import BeautifulSoup
from zenrows import ZenRowsClient



class VerifyParser():
    def __init__(self, filename: str) -> None:
        self.client_id = 'vrfeo1g7YYMTyc8NP8Fs3JMpZVBS0CWcdkJKMCi'
        self.client_secret = 'HdhxdfERzRXZAG3Uc9iMXespB8gXHsCK5O4DAhdDadHBWcMzzZUcwPfoYYTnVw77bbNkVMyPywMYxo7oI1RE9FuG6C958kDx8IExoO1eS2Dz2P3MIKHFBADmgwWm6hRo'
        self.username = 'ecoscannerv'
        self.api_key = '3d70f8f9ce36e30d160ca64c57584c04'
        self.categories = ['Grocery', 'Utilities', 'Travel']
        self.file_path = filename
        self.items = None
        self.response = None

    def get_response(self) -> None:
        #if os.path.isfile("response.json"):
        #    response = json.loads("response.json")
        #else:
        veryfi_client = Client(self.client_id,
                                   self.client_secret,
                                   self.username,
                                   self.api_key)

        response = veryfi_client.process_document(self.file_path,
                                                      categories=self.categories)
        self.response = response
        with open("response.json", "w") as f:
            json.dump(self.response, f)

    def get_date(self) -> str:
        if self.items == None:
            self.get_response()

        return self.response["created_date"]

    def get_line_items(self):
        if self.items == None:
            self.get_response()

        self.items = list()
        for item in self.response["line_items"]:
            self.items.append(tuple([item['description'], item['total']]))

        return self.items


"""class SainsburyProductScraper:
    def __init__(self, sainsbury_url):
        self.sainsbury_url = sainsbury_url

    def fetch_product_page(self):
        try:
            # Set a custom User-Agent header to mimic a web browser
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            # Send a GET request to the Sainsbury's product page
            with requests.Session() as session:
                response = session.get(self.sainsbury_url, headers=headers)
                response.raise_for_status()  # Raise an exception if the request fails

            return response.content
        except Exception as e:
            print(f"Error fetching product page: {str(e)}")
            return None

    def extract_product_details(self, product_page_content):
        try:
            soup = BeautifulSoup(product_page_content, 'html.parser')

            # Extract product name
            product_name = soup.find("h1", class_="product-summary__title").text.strip()

            # Check if "Vegan" tag is present
            vegan_tag = "Vegan" in soup.text

            # Check if "Locally Sourced" tag is present
            locally_sourced_tag = "Locally Sourced" in soup.text

            # Extract origin information (if available)
            origin_info = soup.find("div", class_="product-summary__country-of-origin")
            origin = origin_info.text.strip() if origin_info else "Not specified"

            return {
                "product_name": product_name,
                "vegan_tag": vegan_tag,
                "locally_sourced_tag": locally_sourced_tag,
                "origin": origin
            }
        except Exception as e:
            print(f"Error extracting product details: {str(e)}")
            return None

# Example usage
sainsbury_link = "https://www.sainsburys.co.uk/gol-ui/product/monster-energy-pipeline-punch-500ml"
scraper = SainsburyProductScraper(sainsbury_link)
product_page_content = scraper.fetch_product_page()
print('error????????????????')

if product_page_content:
    product_details = scraper.extract_product_details(product_page_content)
    if product_details:
        print("Product Details:")
        print(f"Name: {product_details['product_name']}")
        print(f"Vegan: {product_details['vegan_tag']}")
        print(f"Locally Sourced: {product_details['locally_sourced_tag']}")
        print(f"Origin: {product_details['origin']}")
    else:
        print("Error extracting product details.")
else:
    print("Error fetching product page.")
"""
def get_product_details(sainsbury_url):
    try:
        
        url = sainsbury_url
        apikey = '3b43e9a3046235f3ec0c8965c2365a6e8a995f1a'
        params = {
            'url': url,
            'apikey': apikey,
            'js_render': 'true',
            'premium_proxy': 'true',
            'proxy_country': 'gb',
        }
        response = requests.get('https://api.zenrows.com/v1/', params=params)
        #print(response.text)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product name
        product_name = soup.find("h1", class_="product-summary__title").text.strip()

        # Check if "Vegan" tag is present
        vegan_tag = "Vegan" in soup.text

        # Check if "Locally Sourced" tag is present
        locally_sourced_tag = "Locally Sourced" in soup.text

        # Extract origin information (if available)
        origin_info = soup.find("div", class_="product-summary__country-of-origin")
        origin = origin_info.text.strip() if origin_info else "Not specified"

        return {
            "product_name": product_name,
            "vegan_tag": vegan_tag,
            "locally_sourced_tag": locally_sourced_tag,
            #"origin": origin
        }
    except Exception as e:
        return {"error": str(e)}

filename = 'DSC_0058.jpg'
parser = VerifyParser(filename)
items = parser.get_line_items()

#print(items)

items = [(product, price) for product, price in items if price >= 0]

for i in range(len(items)):
    outputitem,link=(search_product(items[i]))  
    #print(link)
    print(get_product_details(link))
    #product_details = get_product_details(link)





    """url = link
    apikey = '3b43e9a3046235f3ec0c8965c2365a6e8a995f1a'
    params = {
        'url': url,
        'apikey': apikey,
        'js_render': 'true',
        'premium_proxy': 'true',
        'proxy_country': 'gb',
    }
    response = requests.get('https://api.zenrows.com/v1/', params=params)
    print(response.text)"""
        


"""if "error" in product_details:
    print(f"Error: {product_details['error']}")
else:
    print("Product Details:")
    print(f"Name: {product_details['product_name']}")
    print(f"Vegan: {product_details['vegan_tag']}")
    print(f"Locally Sourced: {product_details['locally_sourced_tag']}")
    print(f"Origin: {product_details['origin']}")"""





# print(parser.response)
