from tkinter import *
from Functionality import *
import time


# glowne okno gry
class MainWindow:
    def __init__(self, controller):
        # ustawienia parametrów głównego okna gry
        self._window = Tk()
        self._controller = controller
        self._window.title("Saper")
        self._window.iconbitmap("images/icon.ico")
        # wykrywanie wciskanych przycisków
        self._window.bind("<Key>", lambda fun: controller.pressedKey(fun.char))
        # menu główne
        self.mainMenu = MainMenu(self._window, controller)
        # mapa gry
        self.gameMap = GameMap(self._window, controller)
        # licznik czasu
        self.gameMap.timer()

    def windowLoop(self):
        self._window.mainloop()

    def setController(self, controller):
        self._controller = controller


# menu glowne zawierajace 3 pola tekstowe do wprowadzenia parametrow rozgrywki oraz przycisk rozpoczynajacy nowa gre
class MainMenu:
    def __init__(self, window, controller):
        self._window = window
        # tekst oraz pole tekstowe do wprowadzenia szerokosci mapy
        self._labelWidth = Label(self._window, text="Szerokość")
        self._labelWidth.grid(row=1, column=0, sticky="e")
        self._entryWidth = Entry(self._window)
        self._entryWidth.grid(row=1, column=1)
        # -||- do wprowadzenia wysokości mapy
        self._labelHeight = Label(self._window, text="Wysokość")
        self._labelHeight.grid(row=2, column=0, sticky="e")
        self._entryHeight = Entry(self._window)
        self._entryHeight.grid(row=2, column=1)
        # -||- do wprowadzenia liczby min na mapie
        self._labelMines = Label(self._window, text="Liczba min")
        self._labelMines.grid(row=3, column=0, sticky="e")
        self._entryMines = Entry(self._window)
        self._entryMines.grid(row=3, column=1)
        # przycisk rozpoczęcia nowej gry
        self._buttonStart = Button(self._window, text="Nowa Gra")
        self._buttonStart.grid(columnspan=2)
        self._buttonStart.bind("<Button-1>", lambda fun: controller.newGame())

        self._labelError = Label(self._window, text="", fg="red")

    def getEntrySettings(self):
        return self._entryWidth.get(), self._entryHeight.get(), self._entryMines.get()

    def showError(self, comment):
        self._labelError.config(text=comment)
        self._labelError.grid(row=6, columnspan=2)

    def clearEntryData(self):
        self._labelError.grid_forget()


# mapa gry ktora po prawej stronie wyswietla liczbe min oraz oflagowanych pól, a takze licznik czasu
class GameMap:
    def __init__(self, window, controller, positionx=3, positiony=1):
        self._controller = controller
        self._posX = positionx
        self._posY = positiony
        self._window = window
        self._mapOfButtons = []
        self._markedMines = 0

        self._timerStarted = False
        self._timerRunning = False
        self._time = time.time()
        self._flagImage = PhotoImage(file='images/flag.png')
        self._mineImage = PhotoImage(file='images/mine.png')

        self._textNumberOfMines = StringVar()
        self._textMarkedMines = StringVar()
        self._textTimer = StringVar()
        self._textTimer.set("0")

        self._labelWinLost = Label(self._window, text="white")
        self._labelEmpty = Label(self._window, image='', width="2")
        self._labelMarkedMines = Label(self._window, textvariable=self._textMarkedMines)
        self._labelMarkedIcon = Label(self._window, image=self._flagImage)
        self._labelMines = Label(self._window, textvariable=self._textNumberOfMines)
        self._labelMinesIcon = Label(self._window, image=self._mineImage)
        self._labelTimer = Label(self._window, textvariable=self._textTimer)

    def newMap(self, height, width, mines):
        self._markedMines = 0
        self._textNumberOfMines.set(str(mines))

        self._textMarkedMines.set(": 0")

        self._labelWinLost.config(text="", bg="white")
        self._labelWinLost.grid(column=self._posX, row=self._posY, columnspan=width, sticky="news")
        self._labelTimer.grid(column=self._posX + width + 1, row=self._posY, columnspan=2)

        self._labelEmpty.grid(column=width + self._posX + 1, row=self._posY + 1, rowspan=2)

        self._labelMinesIcon.grid(column=width + self._posX + 2, row=self._posY + 1)
        self._labelMines.grid(column=width + self._posX + 3, row=self._posY + 1)

        self._labelMarkedIcon.grid(column=width + self._posX + 2, row=self._posY + 2)
        self._labelMarkedMines.grid(column=width + self._posX + 3, row=self._posY + 2)

        self.drawButtons(width, height)

        self._timerStarted = True
        self._timerRunning = False

    def win(self):
        self._labelWinLost.config(text="WYGRALES!", bg="green")
        [[x.disable() for x in y] for y in self._mapOfButtons]
        self._timerRunning = False

    def defeat(self, x, y):
        self._labelWinLost.config(text="PRZEGRALES!", bg="red")
        [[xx.disable() for xx in yy] for yy in self._mapOfButtons]
        self._mapOfButtons[y][x].mark(marked="minered")
        self._timerRunning = False

    def setButtonMark(self, pos_x, pos_y, what):
        if what == "flag":
            self._markedMines += 1
            self._mapOfButtons[pos_y][pos_x].disable()
            self._mapOfButtons[pos_y][pos_x].mark("flag")
        elif what == "empty":
            self._mapOfButtons[pos_y][pos_x].mark("empty")
        elif what == "questionmark":
            self._markedMines -= 1
            self._mapOfButtons[pos_y][pos_x].active()
            self._mapOfButtons[pos_y][pos_x].mark("questionmark")
        self._textMarkedMines.set(": " + str(self._markedMines))

    def showMinePlace(self, x, y, what=""):
        self._mapOfButtons[y][x].mark(marked="highlight")
        if what != "onlyColor":
            self._mapOfButtons[y][x].mark(marked="mine")

    def uncoverPlace(self, x, y, number):
        self._mapOfButtons[y][x].uncover(number)

    def drawButtons(self, width, height):
        [[y.destroy() for y in x] for x in self._mapOfButtons]
        self._mapOfButtons = [[GameButton(self._window, i, j, self._controller.LMB, self._controller.RMB,
                                          i + self._posX, j + self._posY + 1)
                               for i in range(width)] for j in range(height)]

    def timer(self):
        if self._timerRunning:
            self._textTimer.set( str("%3.1f"%(time.time() - self._time)) )
        elif self._timerStarted:
            self._time = time.time()
            self._textTimer.set(str(0))
            self._timerRunning = True
            self._timerStarted = False
        self._window.after(100, self.timer)


#klasa odpowiedzialna za przyciski na mapie gry
class GameButton:
    def __init__(self, window, i, j, funLMB, funRMB, positionx, positiony):
        self.window = window
        self.posX = positionx
        self.posY = positiony
        self.questionMark_image = PhotoImage(file='images/question.png')
        self.mine_image = PhotoImage(file='images/mine.png')
        self.mineRed_image = PhotoImage(file='images/red_mine.png')
        self.flag_image = PhotoImage(file='images/flag.png')
        self.number_images = {0: PhotoImage(file='images/clear.png'),
                              1: PhotoImage(file='images/n1.png'),
                              2: PhotoImage(file='images/n2.png'),
                              3: PhotoImage(file='images/n3.png'),
                              4: PhotoImage(file='images/n4.png'),
                              5: PhotoImage(file='images/n5.png'),
                              6: PhotoImage(file='images/n6.png'),
                              7: PhotoImage(file='images/n7.png'),
                              8: PhotoImage(file='images/n8.png')}
        self.empty_image = PhotoImage(file='images/empty.png')

        self.thisButton = Button(self.window, bg='grey85', disabledforeground="black", relief=RAISED, overrelief=GROOVE,
                                     width=20, image=self.empty_image, command=(lambda a=i, b=j: funLMB(a, b)))
        self.thisButton.bind("<Button-3>", lambda fun, a=i, b=j: funRMB(a, b))
        self.thisButton.grid(row=positiony, column=positionx, sticky="news", padx=0, pady=0)

    def uncover(self, number=0):
        self.thisButton.destroy()
        self.thisButton = Label(image=self.number_images[number], bg="grey85", width=20, height=20)
        self.thisButton.grid(row=self.posY, column=self.posX, sticky="news")

    def mark(self, marked="empty"):
        if marked == "minered":
            self.thisButton.destroy()
            self.thisButton = Label(image=self.mineRed_image, width=20, height=20)
        elif marked == "mine":
            self.thisButton.destroy()
            self.thisButton = Label(image=self.mine_image, width=20, height=20)
        elif marked == "highlight":
            self.thisButton.config(bg="grey65")
        elif marked == "flag":
            self.thisButton.config(image=self.flag_image)
        elif marked == "questionmark":
            self.thisButton.config(image=self.questionMark_image)
        elif marked == "empty":
            self.thisButton.config(image=self.empty_image)
        self.thisButton.grid(row=self.posY, column=self.posX, sticky="news")

    def disable(self):
        self.thisButton.config(stat=DISABLED)

    def active(self):
        self.thisButton.config(stat=ACTIVE)

    def destroy(self):
        self.thisButton.destroy()
