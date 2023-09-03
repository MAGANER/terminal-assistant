import curses
from base_menu import BaseMenu
from input_buffer import InputBuffer
import copy

class ChatMenu(BaseMenu):
    def __init__(self,screen,screen_center):
        BaseMenu.__init__(self,screen,screen_center)

        self.prompt_buffer = []

        self.prompt_y_start = self.screen_y_center+11 #under the off line
        self.reading_pos = self.prompt_y_start
        self.buffer = InputBuffer(screen,curses.COLS-2)

        self.l_counter = 0
        
    def __show_off_line(self):
        '''x,y - center of the screen'''
        x,y = self.screen_x_center, self.screen_y_center
        y+=10
        
        for _x in range(0,curses.COLS):
            self.screen.addstr(y,_x,"☰")

    def process_input(self):
        if self.l_counter != 4:
            self.prompt_buffer.append(self.buffer.read(1,self.reading_pos))
            self.reading_pos+=1
            self.l_counter+=1

    
    def draw_prompt(self):
        for s in enumerate(self.prompt_buffer):
            diff, line = s
            self.screen.addstr(self.prompt_y_start+diff,1,line)
    
    def run(self):
        self.__show_off_line()
        self.process_input()
        self.draw_prompt()

