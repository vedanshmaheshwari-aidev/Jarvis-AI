from jarvis.config import config

def show_banner():
    print()
    print("=" * 50)
    print("🤖 Jarvis AI OS🤖")
    print(f"Version: {config.VERSION}")
    print("=" * 50)
    print()
    print("Type 'exit' to quit")
    print("Type 'clear' to clear the screen")
    print()