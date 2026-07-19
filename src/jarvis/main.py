import os
import time


from jarvis.banner import show_banner
from jarvis.brain import brain
from jarvis.memory import memory
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
            memory.clear()
            clear_screen()
            show_banner()
            continue


        start = time.perf_counter()

        model = brain.choose_model(question)

        model_name =  "⚡ Fast Model" if model == "qwen2.5:3b" else "🧠 Reasoning Model"

        print(f"\n {model_name} ({model})")

        # answer = ollama_client.chat(model,question)


        print("\n⚡ Generating...\n")
        print("Jarvis > ", end="", flush=True)

        memory.add_user(question)

        answer = ollama_client.chat(model)

        memory.add_assistant(answer)

        end = time.perf_counter()

        print(f"\n ⏱️ Response time: {end - start:.2f} seconds\n")


if __name__ == "__main__":
    main()

