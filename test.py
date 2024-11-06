from typing import List, Union, Generator, Iterator, Optional

from pprint import pprint
import requests
import json
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class Pipeline:
    def __init__(self):
        self.name = "AIM - N8N teste1"
        self.api_url = "https://n8n.autointmind.com/webhook/62f78f96-6cae-4cfd-985d-27d2da8fd8b5"     # Set correct hostname
        # self.api_key = ""                                    # Insert your actual API key here
        self.verify_ssl = True
        self.debug = False
        # Please note that N8N do not support stream reponses

    async def on_startup(self):
        """
        This is an asynchronous method called when the pipeline starts.
        It prints a message indicating that the on_startup method has been called.
        :return: None
        """
        print(f"on_startup: {__name__}")
        pass
    
    async def on_shutdown(self): 
        """
        This is an asynchronous method called when the pipeline shuts down.
        It prints a message indicating that the on_shutdown method has been called.
        :return: None
        """
        print(f"on_shutdown: {__name__}")
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """
        This is an asynchronous method that handles incoming data.
        It returns the incoming data.
        :param body: The data coming into the pipeline.
        :param user: Optional user data.
        :return: The incoming data.
        """
        return body
    
    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """
        This is an asynchronous method that handles outgoing data.
        It returns the outgoing data.
        :param body: The data going out of the pipeline.
        :param user: Optional user data.
        :return: The outgoing data.
        """
        return body

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        """
        This method is a pipeline controller.
        It makes an HTTP GET request to the N8N API and returns the response.
        :param user_message: User message.
        :param model_id: Model ID.
        :param messages: Messages.
        :param body: The data coming into the pipeline.
        :return: The response from the N8N API or an error message.
        """
        print(f"pipe: {__name__}")
       
        headers = {
            # 'Authorization': f'Bearer {self.api_key}',  # inserted your actual API key here
            'Content-Type': 'application/json'
        }
        response = requests.get(self.api_url, headers=headers, verify=self.verify_ssl)
        if response.status_code == 200:
            return response.content
        else:
            return f"Workflow request failed with status code: {response.status_code}"
