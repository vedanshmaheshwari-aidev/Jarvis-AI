from ollama import Client
from jarvis.config import config


class OllamaClient:
    def __init__(self):
        self.client = Client(host=config.OLLAMA_HOST)

    def chat(self,model:str,  message: str) -> str:
        response = self.client.chat(model=model,
                                    messages=[{
                                               "role": "user",
                                               "content": message}],
                                               )
        return response['message']['content']
    

ollama_client = OllamaClient()