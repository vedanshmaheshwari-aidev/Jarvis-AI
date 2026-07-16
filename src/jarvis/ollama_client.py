from ollama import Client
from jarvis.config import config


class OllamaClient:
    def __init__(self):
        self.client = Client(host=config.OLLAMA_HOST)

    def chat(self, message: str) -> str:
        response = self.client.chat(model=config.MODEL,
                                    messages=[{
                                               "role": "user",
                                               "content": message}],
                                               )
        return response['message']['content']
    

ollama_client = OllamaClient()