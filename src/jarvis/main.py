from jarvis.config import config

def main():
    print("=" * 40)
    print(config.APP_NAME)
    print(f"Version: {config.VERSION}")
    print(f"Model: {config.MODEL}")
    print("=" * 40)

if __name__ == "__main__":
    main()    