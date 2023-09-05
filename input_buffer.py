import curses

class InputBuffer:
    def __init__(self,screen, buffer_size):
        self.__buffer = ""
        self.size = buffer_size
        self.screen = screen

        self.quit_counter = 0
        self.x = 0
        self.y = 0

    def __decr_q_counter(self):
        if self.quit_counter != 0:
            self.quit_counter-=1
    def __is_enter(self,code):
        return code == curses.KEY_ENTER or code == 10 or code == 13

    def r(self):
        s = self.screen.getstr(self.y,self.x)
        
    def read(self):
        code = -1
        self.__buffer = ""

        curses.echo()
        self.screen.move(self.y+1,self.x)
        curses.curs_set(1)
        while self.size != len(self.__buffer):
            code = self.screen.getch()
            self.x+=1
            
            if code != 8 and not self.__is_enter(code):
                self.__buffer+=chr(code)
                self.__decr_q_counter()
            elif code == 8 and not self.__is_enter(code):
                y,x = self.screen.getyx()
                self.__buffer = self.__buffer[:-1]
                    
                self.screen.addstr(y,x," ")
                self.screen.move(y,x)
                self.__decr_q_counter()
                
            elif self.__is_enter(code):
                self.y+=1
                self.quit_counter+=1

            if self.quit_counter > 2:
                self.x = 0
                break
                
        return self.__buffer
