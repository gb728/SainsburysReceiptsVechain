from veryfi import Client
from abc import ABC
import json
import os

class VeryfiParser():
    def __init__(self,filename: str) -> None:

        #for authentication
        self.client_id = 'vrfeo1g7YYMTyc8NP8Fs3JMpZVBS0CWcdkJKMCi'
        self.client_secret = 'HdhxdfERzRXZAG3Uc9iMXespB8gXHsCK5O4DAhdDadHBWcMzzZUcwPfoYYTnVw77bbNkVMyPywMYxo7oI1RE9FuG6C958kDx8IExoO1eS2Dz2P3MIKHFBADmgwWm6hRo'
        self.username = 'ecoscannerv'
        self.api_key = '3d70f8f9ce36e30d160ca64c57584c04'

        #to be sent to the veryfiAPI
        self.categories = ['Grocery', 'Utilities', 'Travel']
        self.file_path = filename


        self.items = None
        self.response = None

    def get_response(self) -> None:
        if os.path.isfile("response.json"):
            response = json.loads("response.json")
        else:
            veryfi_client = Client(self.client_id, 
                                    self.client_secret, 
                                    self.username, 
                                    self.api_key)
            
            response = veryfi_client.process_document(self.file_path, 
                                                        categories=self.categories)
            self.response = response
            json.dumps(self.response)

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
