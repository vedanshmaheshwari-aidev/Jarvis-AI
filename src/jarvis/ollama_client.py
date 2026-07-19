from ollama import Client
from jarvis.config import config
from jarvis.prompts import FAST_SYSTEM_PROMPT, REASONING_SYSTEM_PROMPT


class OllamaClient:
    def __init__(self):
        self.client = Client(host=config.OLLAMA_HOST)

    def chat(self,model:str,  message: str) -> str:
        system_prompt = (
            FAST_SYSTEM_PROMPT
            if model ==config.FAST_MODEL
            else REASONING_SYSTEM_PROMPT
        )
        
        stream = self.client.chat(model = model,
                                  messages=[
                                      {
                                          "role": "system",
                                          "content": system_prompt,
                                      },
 
                                      {
                                        "role":"user",
                                       "content":message,
                                       },
                                  ],
                                  stream=True,
                                  )
        full_response = ""

        

        for chunk in stream:
            text = chunk["message"]["content"]
            print(text, end="",flush=True)
            full_response += text

        print() #print a newline after each response

        return full_response    
    

ollama_client = OllamaClient()    