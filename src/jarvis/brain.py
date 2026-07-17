from jarvis.config import config
from jarvis.router import is_complex


class Brain:
    def choose_model(self, question: str) -> str:
        if is_complex(question):
            return config.REASONING_MODEL
        
        return config.FAST_MODEL
    

brain = Brain()
    