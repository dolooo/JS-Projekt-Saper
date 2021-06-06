from tkinter import *
import random


class Saper:
    def __init__(self):
        # ustawienia wstepne rozgrywki
        self._writtenCode = ""
        self._clearedButtons = 0
        self._gameEnded = False
        self._firstGame = False
        self._mines = 0
        self._markedMines = 0
        self._correctlyMarkedMines = 0
        self._mapWidth = 0
        self._mapHeight = 0
        self._mapOfMines = []

    def setView(self, view):
        self._view = view

    def pressedKey(self, char):
        self._writtenCode = char + self._writtenCode[0:5]
        self.gameExtras()

    def getAndSetEntrySettings(self):
        self._mapWidth, self._mapHeight, self._mines = self._view.mainMenu.getEntrySettings()
        self._mapWidth = int(self._mapWidth)
        self._mapHeight = int(self._mapHeight)
        self._mines = int(self._mines)
        if not 2 <= self._mapWidth <= 15 or not 2 <= self._mapHeight <= 15 or \
                not 0 <= self._mines <= self._mapWidth * self._mapHeight:
            raise WrongDataException("")
        self._view.gameMap.newMap(self._mapHeight, self._mapWidth, self._mines)
        self.newRandomMap()
        self._view.mainMenu.clearEntryData()
        self._firstGame = True

    def resetSettings(self):
        self._gameEnded = False
        self._markedMines = 0
        self._correctlyMarkedMines = 0
        self._clearedButtons = 0

    def newGame(self):
        self.resetSettings()
        try:
            self.getAndSetEntrySettings()
        except WrongDataException:
            self._view.mainMenu.showError("Złe wymiary lub zła ilość min")

    def newRandomMap(self):
        rd = random.sample(range(0, self._mapWidth * self._mapHeight), self._mines)
        self._mapOfMines = [["Mn" if j * self._mapWidth + i in rd else "0n" for i in range(self._mapWidth)]
                            for j in range(self._mapHeight)]
        self._mapOfMines = [["Mn" if self._mapOfMines[j][i][0] == "M" else str(self.countNeighbourMines(i, j)) + "n" for i in
                             range(self._mapWidth)] for j in range(self._mapHeight)]

    def countNeighbourMines(self, x, y):
        counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i + y < 0 or j + x < 0:
                    continue
                try:
                    if self._mapOfMines[i + y][j + x][0] == "M":
                        counter += 1
                except IndexError:
                    continue
        return counter

    def LMB(self, pos_x, pos_y):
        if self._mapOfMines[pos_y][pos_x][0] == "M":
            self._gameEnded = True
            self.showMines()
            self._view.gameMap.defeat(pos_x, pos_y)
        else:
            if self._mapOfMines[pos_y][pos_x][0] == "0":
                self._clearedButtons += self.uncoverEmptyFields(pos_x, pos_y)
            else:
                self._clearedButtons += 1
                self._view.gameMap.uncoverPlace(pos_x, pos_y, int(self._mapOfMines[pos_y][pos_x][0]))
            self._mapOfMines[pos_y][pos_x] = self._mapOfMines[pos_y][pos_x][0] + "o"
            self.winCheck()

    def RMB(self, pos_x, pos_y):
        if not self._gameEnded and self._mapOfMines[pos_y][pos_x][1] != "o":
            if self._mapOfMines[pos_y][pos_x][1] == "f":
                self._markedMines -= 1
                self._mapOfMines[pos_y][pos_x] = self._mapOfMines[pos_y][pos_x][0] + "q"
                if self._mapOfMines[pos_y][pos_x][0] == "M":
                    self._correctlyMarkedMines -= 1
                self._view.gameMap.setButtonMark(pos_x, pos_y, "questionmark")
            elif self._mapOfMines[pos_y][pos_x][1] == "q":
                self._mapOfMines[pos_y][pos_x] = self._mapOfMines[pos_y][pos_x][0] + "n"
                self._view.gameMap.setButtonMark(pos_x, pos_y, "empty")
            else:
                self._mapOfMines[pos_y][pos_x] = self._mapOfMines[pos_y][pos_x][0] + "f"
                self._markedMines += 1
                if self._mapOfMines[pos_y][pos_x][0] == "M":
                    self._correctlyMarkedMines += 1
                self._view.gameMap.setButtonMark(pos_x, pos_y, "flag")
            self.winCheck()

    def showMines(self, what=""):
        for j in range(self._mapHeight):
            for i in range(self._mapWidth):
                if self._mapOfMines[j][i][0] == "M":
                    self._view.gameMap.showMinePlace(i, j, what)

    def gameExtras(self):
        if "xyzzy" in self._writtenCode[::-1]:
            self._writtenCode = ""
            self.showMines(what="onlyColor")

    def uncoverEmptyFields(self, x, y):
        uncovered = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if y + i < 0 or x + j < 0 or self._mapOfMines[y + i][x + j][1] == "f":
                        continue
                    elif self._mapOfMines[y + i][x + j][1] in "nq":
                        uncovered += 1
                        self._mapOfMines[y + i][x + j] = self._mapOfMines[y + i][x + j][0] + "o"
                        self._view.gameMap.uncoverPlace(x + j, y + i, int(self._mapOfMines[y + i][x + j][0]))
                        if self._mapOfMines[y + i][x + j][0] == "0":
                            uncovered += self.uncoverEmptyFields(x + j, y + i)
                except IndexError:
                    continue
        return uncovered

    def winCheck(self):
        if self._mines == self._correctlyMarkedMines == self._markedMines or \
                self._clearedButtons == self._mapWidth * self._mapHeight - self._mines:
            self._gameEnded = True
            self._view.gameMap.win()


# wlasna klasa wyjątku (wprowadzania niewlasciwych danych)
class WrongDataException(Exception):
    def __init__(self, comment):
        self.comment = comment

    def __str__(self):
        return self.comment


