import curses
from base_menu import BaseMenu

class ChatMenu(BaseMenu):
    def __init__(self,screen,screen_center):
        BaseMenu.__init__(self,screen,screen_center)
        
        self.prompt_buffer = []
        self.prompt = ""
        
    def __show_off_line(self):
        '''x,y - center of the screen'''
        x,y = self.screen_x_center, self.screen_y_center
        y+=10
        
        for _x in range(0,curses.COLS):
            self.screen.addstr(y,_x,"-")

    def process_input(self):
        val = self.screen.getch()

        if val == 10:
            self.prompt_buffer.append(self.prompt)
            self.prompt = ""
        else:
            self.prompt+=chr(val)

    def run(self):
        self.__show_off_line()
        self.process_input()

