import curses
import os
from main_menu import *
from chat_menu import *

class Window:
    def __init__(self, models):
        self.screen = curses.initscr()
        self.screen.leaveok(True)
        curses.noecho()
        curses.curs_set(0)
        curses.cbreak()
        self.screen.keypad(True)

        curses.start_color()
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)

        self.main_menu = MainMenu(models,self.screen,self.__get_screen_center())
        self.chat_menu = ChatMenu(self.screen,self.__get_screen_center())

    def __del__(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def __get_screen_center(self):
        return int(curses.COLS/2), int(curses.LINES/2)
        
    
    def __show_border(self):
        #draw top border
        for x in range(curses.COLS):
            self.screen.addstr(0,x,"-\n",curses.color_pair(1))

        #draw bottom border
        for x in range(curses.COLS):
            self.screen.addstr(curses.LINES-2,x,"-",curses.color_pair(1))

        #draw left border
        for y in range(1,curses.LINES-2):
            self.screen.addstr(y,0,"|",curses.color_pair(1))

        #draw right border
        for y in range(1,curses.LINES-2):
            self.screen.addstr(y,curses.COLS-1,"|",curses.color_pair(1))


    def run(self, menu_to_run=True):
        self.screen.erase()

        x,y = self.__get_screen_center()
        while True:
            self.__show_border()

            if menu_to_run:
                if self.main_menu.run():
                    return self.run(False)
            else:
                 self.chat_menu.run()
                 
            self.screen.refresh()
