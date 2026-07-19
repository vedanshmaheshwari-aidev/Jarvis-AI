import os
import time


from jarvis.banner import show_banner
from jarvis.brain import brain
from jarvis.ollama_client import ollama_client

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
def main():
    clear_screen()
    show_banner()

    while True:
        question = input("You > ").strip()

        if not question:
            continue

        if question.lower() in ["exit", "quit"]:
            print("\n 👋 Goodbye")
            break

        if question.lower() == "clear":
            clear_screen()
            show_banner()
            continue


        start = time.perf_counter()

        model = brain.choose_model(question)

        print(f"\n  🤖 Using model: {model}")

        answer = ollama_client.chat(model,question)

        end = time.perf_counter()

        print("\n Jarvis >")
        print(answer)
        print(f"\n ⏱️ Response time: {end - start:.2f} seconds\n")


if __name__ == "__main__":
    main()

#     print("=" * 40)
#     print("Jarvis AI OS")
#     print("=" * 40)

#     question = input("You: ")

#     answer = ollama_client.chat(question)

#     print("\nJarvis:")
#     print(answer)


# if __name__ == "__main__":
#     main()