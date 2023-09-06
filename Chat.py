from Perplexity import create_perplexity
from colors import color
import os
import time
import signal

def catch_interruption_c(signal, frame):
    print("\n work is done. Hope it was helpful!")
    exit(0)

class Chat:
    def __init__(self):
        self.__models = ["llama-2-13b-sft","llama-2-70b-chat","llama-2-13b-chat","llama-2-7b-chat"]
        
        self.__curr_m = 0
        self.perp = None

    def __print_main_menu(self):
        print("choose model to use:")
        for m in enumerate(self.__models):
            id, line = m
            print("{}){}".format(id,line))
        choice = input(">>")
        if choice in ("0","1","2","3"):
            return int(choice)
        else:
            os.system("clear||cls")
            self.__print_main_menu()
    def __run_chat(self):
        print(color.blue+"[you]:"+color.end,end="")

        s = "".join(list(iter(input, '')))  
        s = self.perp.search(s)
        
        print(color.yellow+"[robot]:"+color.end+"\n"+s)
    def run(self):
        signal.signal(signal.SIGINT, catch_interruption_c)
        
        self.__curr_m = self.__print_main_menu()
        self.perp = create_perplexity(self.__models[self.__curr_m])
        
        os.system("clear||cls")
        while True:
            self.__run_chat()
            
        signal.pause()
