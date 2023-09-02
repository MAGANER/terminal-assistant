from abc import ABC, abstractmethod

class BaseMenu(ABC):
    def __init__(self,screen,screen_center):
        self.screen = screen
        self.screen_x_center,self.screen_y_center = screen_center

    @abstractmethod
    def process_input(self):
        pass

    @abstractmethod
    def run(self):
        pass
