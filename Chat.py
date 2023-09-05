import curses
from Perplexity import create_perplexity
from input_buffer import InputBuffer
class Chat:
    def __init__(self):
        self.__models = ["llama-2-13b-sft","llama-2-70b-chat","llama-2-13b-chat","llama-2-7b-chat"]
        self.__curr_m = 0
        
        self.screen = curses.initscr()
        self.screen.keypad(True)
        
        curses.cbreak()
        curses.curs_set(0)

        curses.start_color()
        curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_MAGENTA,curses.COLOR_BLACK)

        self.perp = None

        self.buffer = InputBuffer(self.screen,500)
        
        
    def __del__(self):
        curses.endwin()
        curses.nocbreak()
        curses.curs_set(1)
        self.screen.keypad(False)

    ##these function are related to process os choosing of model. first phase of application using
    def __print_models(self):
        self.screen.addstr(0,0,"choose available model:")
        for m in enumerate(self.__models):
            id, line = m
            if id == self.__curr_m:
                self.screen.addstr(1+id,0,line,curses.color_pair(1))
            else:
                self.screen.addstr(1+id,0,line,curses.color_pair(2))
    def __process_keys_to_choose_model(self):
        val = self.screen.getch()
        if val == curses.KEY_DOWN and self.__curr_m < 3:
            self.__curr_m+=1
        elif val == curses.KEY_DOWN and self.__curr_m == 3:
            self.__curr_m = 0

        if val == curses.KEY_UP and self.__curr_m > 0:
            self.__curr_m-=1
        elif val == curses.KEY_UP and self.__curr_m == 0:
            self.__curr_m=3

        if val == curses.KEY_ENTER or val == 10 or val == 13:
            return True
            
    def __choose_model(self):
        while True:
            self.__print_models()
            if self.__process_keys_to_choose_model():
                break
            
            self.screen.refresh()
    ##################################

    #these functions are related to communication with AI
    def __run_prompt_input(self):
        self.screen.addstr(self.buffer.y,self.buffer.x,"[you]:",curses.color_pair(3))
        s = self.buffer.read()
    def __talk_to_ai(self):
        while True:
            self.__run_prompt_input()
            self.screen.refresh()
            
    
    def run(self):
        self.__choose_model()
        self.perp = create_perplexity(self.__models[self.__curr_m])

        self.screen.clear()
        self.__talk_to_ai()
