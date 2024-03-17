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

"""
def get_latest_image(folder_path):
    try:
        # Get a list of all files in the folder
        all_files = os.listdir(folder_path)

        # Filter out non-image files (e.g., .jpg, .jpeg, .png)
        image_files = [file for file in all_files if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if not image_files:
            raise ValueError("No image files found in the specified folder.")

        # Get the latest image file based on creation time
        latest_image = max(image_files, key=os.path.getctime)

        return latest_image
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
folder_path = 'C:\\Uni\\Yr 1\\Lent\\Hackathon\\SainsburysReceiptsVechain\\Images'  # Specify the correct path
latest_image_name = get_latest_image(folder_path)

if latest_image_name:
    print(f"The most recent image file is: {latest_image_name}")
else:
    print("No valid image files found in the folder.")"""

#only need to input the name of the image into here!!!!!! it goes Images/xxxxxxx.jpg or whatever
filename = 'Images/IMG_0835.jpeg'
parser = VerifyParser(filename)
items = parser.get_line_items()

#print(items)

items = [(product, price) for product, price in items if isinstance(price, (int, float)) and price >= 0]

itemsholder=[]
for i in range(len(items)):
    itemsholder.append(search_product(items[i]))  

   
combined_list = [(item[0][0][0], item[0][0][1],item[0][1]) for item in itemsholder]

print(combined_list) 
print('end')

#dictionary
#[('MONSTER PIPELINE', 1.85, 'https://www.sainsburys.co.uk/gol-ui/product/monster-energy-pipeline-punch-500ml'), ('BRIE, BACON & CHILLI', 3.0, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-brie-bacon-chilli-chutney-sandwich'), ('PIZZA SWIRL', 1.1, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-cheese---onion-pizza')]
#[('IRN BRU 1L', 1.1, 'https://www.sainsburys.co.uk/shop/gb/groceries/irn-bru-1l'), ('LINDT INTENSE ORANG', 1.6, 'https://www.sainsburys.co.uk/gol-ui/product/lindt-excellence-intense-orange-100g'), ('LINDT INTENSE ORANG', 1.6, 'https://www.sainsburys.co.uk/gol-ui/product/lindt-excellence-intense-orange-100g'), ('CARROTS LOOSE', 0.07, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-carrots-loose')]
#(There is an error with one of the items as it its cant like find a result for it or smth)
#[('HERBAL ESSENCES', 2.0, 'https://www.sainsburys.co.uk/shop/gb/groceries/health-beauty/herbal-essences'), ('JS 8 BRIOCHE ROLLS', 1.5, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-milk-chocolate-chip-brioche-roll-x8'), ('SSTC HW ANTIBC SILK', 0.6, 'https://www.sainsburys.co.uk/gol-ui/product/ecover-laundry-liquid--delicate-750ml')]
#[('EMMI MR.BIG 370ML', 2.65, 'https://www.sainsburys.co.uk/gol-ui/product/emmi-mr-big-skinny-caff%C3%A8-latte-370ml'), ('NAKD BB MUFF B/BAR', 1.35, 'https://www.sainsburys.co.uk/gol-ui/product/n-kd-big-bar-blueberry-muffin-45g'), ('ALL DAY BREAKFAST SW', 2.75, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-all-day-breakfast-sandwich')]
#(outputs the link to the search result on sainsbury not a specific product but that isnt really much of an issue)
#[('STARBUCKS G CAFFE LA', 2.8, 'https://www.sainsburys.co.uk/gol-ui/product/starbucks-seattle-latte-220ml'), ('ALL DAY BREAKFAST SW', 2.75, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-all-day-breakfast-sandwich'), ('JS 2X MIN CURED PIES', 1.3, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-mini-pork-pies-x2-100g')]
#[('ALL DAY BREAKFAST SW', 2.75, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-all-day-breakfast-sandwich'), ('JS SCOTCH EGG', 1.3, 'https://www.sainsburys.co.uk/gol-ui/groceries/dairy-eggs-and-chilled/savoury-snacks/scotch-eggs/c:1019159'), ('COSTA REG VNL LATTE', 3.5, 'https://www.sainsburys.co.uk/gol-ui/product/costa-coffee-latte-250ml')]
#(Again didnt search specifically)
#[('JS STONEBAKED BBQ CH', 3.5, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-stonebaked-bbq-chicken-hand-stretched-pizza-300g'), ('JS SB MEAT FEAST', 3.5, 'https://www.sainsburys.co.uk/gol-ui/product/sainsburys-stonebaked-meat-feast-306g')]











    #print(get_product_details(link))
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
