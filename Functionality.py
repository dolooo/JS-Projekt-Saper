import random


class Saper:
    def __init__(self):
        """ustawienia wstępne rozgrywki"""
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
        """ustawienie pola będącego okienkiem naszej gry"""
        self._view = view

    def pressedKey(self, char):
        """funkcja przechwytująca ciąg znaków wpisywanych przez uzytkownika
            wywołuje ona funkcję sprawdzającą czy przypadkiem użytkownik nie podał kodu specjalnego """
        self._writtenCode = char + self._writtenCode[0:5]
        self.gameExtras()

    def getAndSetEntrySettings(self):
        """-odbieranie i ustawianie ustawień wejściowych
        -sprawdzenie czy są one zgodne z definicją gry (jeśli nie to rzucenie wyjątku)
        -jeśli dane są prawidłowe to tworzy nową mapę oraz losowo wypełnia ją minami"""
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
        """zresetowanie ustawień gry"""
        self._gameEnded = False
        self._markedMines = 0
        self._correctlyMarkedMines = 0
        self._clearedButtons = 0

    def newGame(self):
        """uruchomienie nowej gry """
        self.resetSettings()
        try:
            self.getAndSetEntrySettings()
        except WrongDataException:
            self._view.mainMenu.showError("Złe wymiary lub zła ilość min")

    def newRandomMap(self):
        """wypełnienie mapy ustawiając w losowy sposób miny przy użyciu funkcjonalności random, oraz
        oznaczanie pustych pól liczbami oznaczającymi liczbę sąsiadujących min tego pola
        M - mina
        0 - puste pole
        1-8 - pole z odpowiednią liczbą sąsiadujących min
        n - znacznik "nothing" (określany za pomocą PPM)
         przykładowo kombinacja Mn oznacza, że na danym polu jest mina i nie ma żadnego znacznika """
        rd = random.sample(range(0, self._mapWidth * self._mapHeight), self._mines)
        self._mapOfMines = [["Mn" if j * self._mapWidth + i in rd else "0n" for i in range(self._mapWidth)]
                            for j in range(self._mapHeight)]
        self._mapOfMines = [["Mn" if self._mapOfMines[j][i][0] == "M" else str(self.countNeighbourMines(i, j))
                            + "n" for i in range(self._mapWidth)] for j in range(self._mapHeight)]

    def countNeighbourMines(self, x, y):
        """liczenie min sąsiadujących z wybranym przyciskiem"""
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
        """funkcjonalność lewego przycisku myszy
            jesli klikniemy na minę - gra się konczy, miny odkrywają się, uruchamia sie procedura od przegranej
            jesli klikniemy w puste pole, odkrywamy puste pola w poblizu (jesli nie sąsiaduje z żadną miną),
            licznik wcisnietych pól wzrasta"""
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
            self._mapOfMines[pos_y][pos_x] = self._mapOfMines[pos_y][pos_x][0] + "x"
            self.winCheck()

    def RMB(self, pos_x, pos_y):
        """funkcjonalność prawego przycisku myszy
            znaczniki : x - "nieaktywny", f - "flag", q - "questionmark", n - "nothing"
        jeśli gra jeszcze się nie zakończyła oraz dana mina nie ma znacznika x:
            jesli pole ma znacznik f, to oznaczenie pola zmienia się na q
            jesli pole ma znacznik q, to oznaczenie pola zmienia się na n
            jesli pole ma znacznik n, to oznaczenie pola zmienia sie na f"""
        if not self._gameEnded and self._mapOfMines[pos_y][pos_x][1] != "x":
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
        """procedura wyświetlająca pola z minami"""
        for j in range(self._mapHeight):
            for i in range(self._mapWidth):
                if self._mapOfMines[j][i][0] == "M":
                    self._view.gameMap.showMinePlace(i, j, what)

    def gameExtras(self):
        """kod, po którego wpisaniu uruchamia się procedura wyswietlenia pol z minami"""
        if "xyzzy" in self._writtenCode[::-1]:
            self._writtenCode = ""
            self.showMines(what="onlyColor")

    def uncoverEmptyFields(self, x, y):
        """procedura odkrywania pustych obszarow"""
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
        """sprawdzenie czy oznaczono prawidlowo wszystkie miny lub czy wcisnieto wszystkie przyciski poza minami
            wtedy gra się konczy i uruchamiana jest procedura odpowiedzialna za wygraną"""
        if self._mines == self._correctlyMarkedMines == self._markedMines or \
                self._clearedButtons == self._mapWidth * self._mapHeight - self._mines:
            self._gameEnded = True
            self._view.gameMap.win()


class WrongDataException(Exception):
    """wlasna klasa wyjątku (wprowadzania niewlasciwych danych)"""
    def __init__(self, comment):
        self.comment = comment

    def __str__(self):
        return self.comment
