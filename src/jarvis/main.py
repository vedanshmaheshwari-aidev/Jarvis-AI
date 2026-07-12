# from jarvis.config import config

# def main():
#     print("=" * 40)
#     print(config.APP_NAME)
#     print(f"Version: {config.VERSION}")
#     print(f"Model: {config.MODEL}")
#     print("=" * 40)

# if __name__ == "__main__":
#     main()    
from jarvis.ollama_client import ollama_client


def main():
    print("=" * 40)
    print("Jarvis AI OS")
    print("=" * 40)

    question = input("You: ")

    answer = ollama_client.chat(question)

    print("\nJarvis:")
    print(answer)


if __name__ == "__main__":
    main()