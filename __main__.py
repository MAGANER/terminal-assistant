from Chat import Chat
import os
if __name__ == "__main__":
    os.system("clear||cls")
    print('\033[?25l', end="")#hide cursor
    
    chat = Chat()
    chat.run()
    print("\033[?25h",end="")
