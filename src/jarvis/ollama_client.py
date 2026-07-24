from ollama import Client

from jarvis.config import config
from jarvis.memory import memory
from jarvis.prompts import FAST_SYSTEM_PROMPT, REASONING_SYSTEM_PROMPT


class OllamaClient:
    """
    Wrapper around the Ollama Client.
    """
    def __init__(self):
        self.client = Client(host=config.OLLAMA_HOST)

    def chat(self,model:str, prompt: str) -> str:
        """
        Send a prompt to the selected model
        """
        # ---------------------------------------------
        # Store user message
        # ---------------------------------------------
        memory.add_user(prompt)

        # ---------------------------------------------
        # Select system prompt
        # ---------------------------------------------

        system_prompt = (
            FAST_SYSTEM_PROMPT
            if model ==config.FAST_MODEL
            else REASONING_SYSTEM_PROMPT
        )


        # ---------------------------------------------
        # Build conversation
        # ---------------------------------------------
        messages = [
            {
                "role" : "system",
                "content": system_prompt,
            }
        ]    
        # Add history
        messages.extend(memory.get_messages())

        
         # ---------------------------------------------
        # Stream response
        # ---------------------------------------------

        stream = self.client.chat(model = model,
                                  messages= messages,
                                  stream=True,
                                  )
        full_response = ""

        
        # Stream the response
        # Stream the response
        for chunk in stream:
            full_response += chunk["message"]["content"]

        # Store assistant response
        memory.add_assistant(full_response)

        return full_response   
    

# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

ollama_client = OllamaClient()    