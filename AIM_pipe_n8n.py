from typing import List, Union, Generator, Iterator, Optional
from pprint import pprint
import requests, json, warnings
# Uncomment to disable SSL verification warnings if needed.
# warnings.filterwarnings('ignore', message='Unverified HTTPS request')
class Pipeline:
    def __init__(self):
        self.name = "AIM - N8N work test"
        self.api_url = "https://n8n.autointmind.com/webhook-test/62f78f96-6cae-4cfd-985d-27d2da8fd8b5"     # Set correct hostname
        #self.api_key = ""                                    # Insert your actual API key here
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
        headers = {
           # 'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        params = {
            "inputs": {"prompt": user_message},
            "user": body["user"]["email"]
        }
      #  response = requests.get(self.api_url, headers=headers, params=params, verify=self.verify_ssl)
        response = requests.get(self.api_url, headers=headers,  verify=self.verify_ssl)
        if response.status_code == 200:
            # Process and yield each chunk from the response
            try:
                json_data = response.json()
                # Check if 'output' exists in json_data and yield it
                if 'output' in json_data:
                    yield json_data['output']
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON from response. Error: {str(e)}")
                yield "Error in JSON parsing."
        else:
            yield f"Workflow request failed with status code: {response.status_code}"
