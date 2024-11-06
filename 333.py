from typing import List, Union, Generator, Iterator, Optional
from pprint import pprint
import requests, json, warnings


warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class Pipeline:
    def __init__(self):
        self.name = "AIM - N8N teste1"
        self.api_url = "https://n8n.autointmind.com/webhook/62f78f96-6cae-4cfd-985d-27d2da8fd8b5"     # Set correct hostname
#        self.api_key = ""                                    # Insert your actual API key here
        self.verify_ssl = True
        self.debug = False
        # Please note that N8N do not support stream reponses

    async def on_startup(self):
        print(f"on_startup: {__name__}")
        pass
    
    async def on_shutdown(self): 
        print(f"on_shutdown: {__name__}")
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        return body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        return body

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        print(f"pipe: {__name__}")
       
        headers = {
      #      'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.api_url, headers=headers, verify=self.verify_ssl)
        if response.status_code == 200:
            response.text
            try:
                return response.content
        else:
            return f"Workflow request failed with status code: {response.status_code}"
