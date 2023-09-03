import curses
from base_menu import BaseMenu

class MainMenu(BaseMenu):
    def __init__(self,models,screen,screen_center):
        BaseMenu.__init__(self,screen,screen_center)
        
        self.__models = models
        self.__curr_model = 0

    def __print_title(self):
        '''x, y - screen center'''
        x,y = self.screen_x_center, self.screen_y_center
        
        title = "Welcome to Terminal Assistant!"

        x-= int(len(title)/2)
        y-=5
        
        self.screen.addstr(y,x,title)

        x+=5
        y+=2
        self.screen.addstr(y,x,"choose model to use:")

        x+=3
        curr = False
        for m in self.__models:
            y+=1
            curr = True if m == self.__models[self.__curr_model] else False

            if curr:
                self.screen.addstr(y,x,m,curses.color_pair(2))
            else:
               self.screen.addstr(y,x," "*(len(m)+5))
               self.screen.addstr(y,x,m,curses.color_pair(1))

    def process_input(self):
        val = self.screen.getch()
        
        if val == ord("q"):
            exit(0)
        elif val == ord("s"):
            self.__curr_model+=1
            if self.__curr_model > 3:
                self.__curr_model = 0
        elif val == ord("w"):
            self.__curr_model-=1
            if self.__curr_model < 0:
                self.__curr_model = 3
        elif val == 10:#enter
            return True

        return None

    def run(self,):
        self.__print_title()
        return self.process_input()
        
