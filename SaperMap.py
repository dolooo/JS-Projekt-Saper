from tkinter import *


class SaperMap:
    def __init__(self, window, controller):
        self._controller = controller
        self._window = window
        self._map = []

    def newMap(self, height, width, mines):
        print("MAPA")