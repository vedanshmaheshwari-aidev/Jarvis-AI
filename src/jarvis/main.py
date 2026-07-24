import os
import time

from jarvis.banner import show_banner
from jarvis.brain import brain
from jarvis.memory import memory


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
            print("\n👋 Goodbye")
            break

        if question.lower() == "clear":
            memory.clear()
            clear_screen()
            show_banner()
            continue

        start = time.perf_counter()

        print("\n⚡ Planning...\n")

        results = brain.think(question)

        # print("Jarvis > ", end="", flush=True)

        for result in results:

            if result.success:
                print(f"Jarvis > {result.data}")
            else:
                print(f"Jarvis [{result.agent_name}] > {result.error}")

        end = time.perf_counter()

        print(f"\n⏱️ Response time: {end - start:.2f} seconds\n")


if __name__ == "__main__":
    main()