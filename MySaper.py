import random
from random import *


class MySaper:
    def __init__(self):
        self._mapWidth = 0
        self._mapHeight = 0
        self._mines = 0
        self._markedMines = 0
        self._correctlyMarkedMines = 0
        self._mapOfMines = []
        self._clearedFields = 0
        self._firstGame = False
        self._GameEnded = False

    def setView(self, view):
        self._view = view

    def resetSettings(self):
        self._GameEnded = False
        self._markedMines = 0
        self._correctlyMarkedMines = 0
        self._clearedFields = 0
        self._mapOfMines = []

    def newGame(self):
        self.resetSettings()
        try:
            self.getSetEnteredData()
        except ValueError:
            self._view.menu.showError("Incorrect value[s]!")

    def getSetEnteredData(self):
        self._mapWidth, self._mapHeight, self._mines = self._view.menu.getEntrySettings()
        if not 2 <= self._mapWidth <= 15 or not 2 <= self._mapHeight <= 15:
            raise Exception("")
        if not 0 <= self._mines <= self._mapWidth * self._mapHeight:
            raise Exception("")
        self._view.map.new(self._mapHeight, self._mapWidth, self._mines)
        self._view.menu.StartNewGame()
        self._firstGame = True

    #To be continued...
