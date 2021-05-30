from tkinter import *


class MainMenu:
    def __init__(self, window, controller):
        self._window = window

        self._labelWidth = Label(window, text="Szerokość")
        self._labelWidth.grid(row=1, column=0, sticky="e")
        self._entryWidth = Entry(window)
        self._entryWidth.grid(row=1, column=1)

        self._labelHeight = Label(window, text="Wysokość")
        self._labelHeight.grid(row=2, column=0, sticky="e")
        self._entryHeight = Entry(window)
        self._entryHeight.grid(row=2, column=1)

        self._labelMines = Label(window, text="Liczba min")
        self._labelMines.grid(row=3, column=0, sticky="e")
        self._entryMines = Entry(window)
        self._entryMines.grid(row=3, column=1)

        self._buttonStart = Button(window, text="Nowa Gra")
        self._buttonStart.grid(columnspan=2)
        self._buttonStart.bind("<Button-1>", lambda fun: controller.StartNewGame())

        self._labelError = Label(self._window, text="", fg="red")

    def getEntrySettings(self):
        return int(self._entryWidth.get()), int(self._entryHeight.get()), int(self._entryMines.get())

    def showError(self, txt):
        self._labelError.config(text=txt)
        self._labelError.grid(row=6, columnspan=2)

    def StartNewGame(self):
        self._labelError.grid_forget()
