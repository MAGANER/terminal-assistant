import curses

class Window:
    def __init__(self, models):
        self.__models = models
        self.__curr_model = 0
        
        self.screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        curses.cbreak()
        self.screen.keypad(True)

        curses.start_color()
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)

    def __del__(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def __get_screen_center(self):
        return int(curses.COLS/2), int(curses.LINES/2)
    def __print_title(self):
        title = "Welcome to Terminal Assistant!"

        x,y = self.__get_screen_center()
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
            model = "* "+m if m == self.__models[self.__curr_model] else m
            curr = True if "*" in model else False

            if curr:
                self.screen.addstr(y,x,model,curses.color_pair(2))
            else:
                self.screen.addstr(y,x," "*(len(model)+5))
                self.screen.addstr(y,x,model,curses.color_pair(1))

        
    
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

    def __run_start_menu(self):
        while True:
            self.__show_border()
            self.__print_title()

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
                break
                    
            self.screen.refresh()

    def run(self):
        self.__run_start_menu()

        model_to_use = self.__models[self.__curr_model]
