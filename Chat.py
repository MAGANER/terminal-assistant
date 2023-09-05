from Perplexity import create_perplexity
from colors import color
import os
import time
import keyboard

class Chat:
    def __init__(self):
        self.__models = ["llama-2-13b-sft","llama-2-70b-chat","llama-2-13b-chat","llama-2-7b-chat"]
        
        self.__curr_m = 0
        self.perp = None

    def print_main_menu(self):
        print("choose model to use:")
        for m in enumerate(self.__models):
            id, line = m
            if id == self.__curr_m:
                print(color.yellow+line+color.end)
            else:
                print(line)
        os.system("clear|cls")
    def process_keys(self):
        if keyboard.is_pressed("up arrow"):
            self.__curr_m = 3 if self.__curr_m == 0 else self.__curr_m - 1
        if keyboard.is_pressed("down arrow"):
            self.__curr_m = 0 if self.__curr_m == 3 else self.__curr_m + 1
        if keyboard.is_pressed("enter"):
            return True
    def run_chat(self):
        print(color.blue+"[you]:"+color.end,end="")
        s = input()
    def run(self):
        while True:
            self.print_main_menu()
            if self.process_keys():
                break

        while True:
            self.run_chat()
