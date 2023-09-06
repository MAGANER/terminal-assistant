from Chat import Chat
import os
if __name__ == "__main__":
    os.system("clear||cls")
   
    chat = Chat()

    try:
        chat.run()
    except Exception as e:
        print(str(e))
        print("due to exception program was shut down.")
        exit(0)
