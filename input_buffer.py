import curses

class InputBuffer:
    def __init__(self,screen, buffer_size):
        self.__buffer = ""
        self.size = buffer_size
        self.screen = screen

    def read(self,x,y):
        code = -1
        self.__buffer = ""

        curses.echo()
        self.screen.move(y,x)
        curses.curs_set(1)
        while code != 10 and self.size != len(self.__buffer):
            code = self.screen.getch()
            
            if code != 8:
                self.__buffer+=chr(code)
            elif code == 8:
                self.__buffer = self.__buffer[:-1]
                self.screen.addstr(y,x+len(self.__buffer)," ")

                #new_x = 1 if len(self.__buffer) == 0 else x+len(self.__buffer)-1
                #self.screen.move(y,new_x)

        self.screen.addstr(y,x," "*len(self.__buffer))
        curses.noecho()
        curses.curs_set(0)
        return self.__buffer
