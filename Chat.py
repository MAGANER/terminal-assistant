from Perplexity import create_perplexity
from colors import color
import os
import time

class Chat:
    def __init__(self):
        self.__models = ["llama-2-13b-sft","llama-2-70b-chat","llama-2-13b-chat","llama-2-7b-chat"]
        
        self.__curr_m = 0
        self.perp = None

    def print_main_menu(self):
        print("choose model to use:")
        for m in enumerate(self.__models):
            id, line = m
            print("{}){}".format(id,line))
        choice = input(">>")
        if choice in ("0","1","2","3"):
            return int(choice)
        else:
            os.system("clear||cls")
            self.print_main_menu()
    def run_chat(self):
        print(color.blue+"[you]:"+color.end,end="")
        s = "".join(list(iter(input, '')))
    def run(self):
        self.__curr_m = self.print_main_menu()

        os.system("clear||cls")
        while True:
            self.run_chat()
