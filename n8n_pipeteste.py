from typing import List, Union, Generator, Iterator, Optional
from pprint import pprint
import requests, json, warnings

class Pipeline:
    def __init__(self):
        self.name = "AIM - N8N Agent Pipeline2"
        self.api_url = "https://n8n.autointmind.com/webhook-test/62f78f96-6cae-4cfd-985d-27d2da8fd8b5"     # Set correct hostname
        self.verify_ssl = True
        self.debug = False
        # Please note that N8N do not support stream reponses

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup: {__name__}")
        pass
    
    async def on_shutdown(self): 
        # This function is called when the server is shutdown.
        print(f"on_shutdown: {__name__}")
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        # This function is called before the OpenAI API request is made. You can modify the form data before it is sent to the OpenAI API.
        print(f"inlet: {__name__}")
        if self.debug:
            print(f"inlet: {__name__} - body:")
            pprint(body)
            print(f"inlet: {__name__} - user:")
            pprint(user)
        return body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        # This function is called after the OpenAI API response is completed. You can modify the messages after they are received from the OpenAI API.
        print(f"outlet: {__name__}")
        if self.debug:
            print(f"outlet: {__name__} - body:")
            pprint(body)
            print(f"outlet: {__name__} - user:")
            pprint(user)
        return body

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe: {__name__}")
        
        if self.debug:
            print(f"pipe: {__name__} - received message from user: {user_message}")
        
        # This function triggers the workflow using the specified API.
        response = requests.get(self.api_url)
        if response.status_code == 200:
            # Process and yield each chunk from the response
            try:
                return response.json()
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON from line. Error: {str(e)}")
                return "Error in JSON parsing."
        else:
            return f"Workflow request failed with status code: {response.status_code}"
