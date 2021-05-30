from tkinter import *
from MainMenu import MainMenu
from SaperMap import SaperMap


class MainWindow:
    def __init__(self, controller):
        self._window = Tk()
        self._controller = controller
        self._window.title("Saper")
        self._window.iconbitmap("graphic/icon.ico")
        self.mainMenu = MainMenu(self._window, controller)
        self.saperMap = SaperMap(self._window, controller)

    def windowLoop(self):
        self._window.mainloop()

    def setController(self, controller):
        self._controller = controller
