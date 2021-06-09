import unittest
from Interface import *
from Functionality import *


class MyTestCase(unittest.TestCase):
    def test_shouldReturnNumberOfNeighbourMines(self):
        # cala testowa mapa sklada sie z min (wlacznie z wybranym polem)
        # wiec licznik sasiadujacych min powinien pokazac wartosc 9
        # given
        game = Saper()
        window = MainWindow(game)
        game.setView(window)
        game._mapWidth = 3
        game._mapHeight = 3
        game._mines = 9
        # when
        game.newRandomMap()
        neighbourMines = game.countNeighbourMines(1, 1)
        # then
        self.assertEqual(neighbourMines, 9)

    def test_shouldEndGameIfMineClicked(self):
        # given
        gameEnded = True
        game = Saper()
        window = MainWindow(game)
        game.setView(window)
        game._mapWidth = 8
        game._mapHeight = 8
        game._mines = 12
        # when
        game.newRandomMap()
        for i in range(8):
            for j in range(8):
                if game._mapOfMines[i][j][0] == "M":
                    game._gameEnded = True
        # then
        self.assertEqual(game._gameEnded, gameEnded)

    def test_shouldCorrectlyUpdateNumberOfMarkedMines(self):
        # given
        game = Saper()
        window = MainWindow(game)
        game.setView(window)
        game._mapWidth = 8
        game._mapHeight = 8
        game._mines = 12
        # when
        game.newRandomMap()
        game._view.gameMap.setButtonMark(3, 3, "flag")
        firstTry = game._view.gameMap._markedMines
        game._view.gameMap.setButtonMark(3, 3, "empty")
        secondTry = game._view.gameMap._markedMines
        game._view.gameMap.setButtonMark(1, 1, "flag")
        thirdTry = game._view.gameMap._markedMines
        # then
        self.assertEqual(firstTry, 1)
        self.assertEqual(secondTry, 0)
        self.assertEqual(thirdTry, 1)

    def test_shouldEndGameIfAllMinesCorrectlyFlagged(self):
        # given
        gameEnded = True
        game = Saper()
        window = MainWindow(game)
        game.setView(window)
        game._mapWidth = 8
        game._mapHeight = 8
        game._mines = 12
        # when
        game.newRandomMap()
        game._markedMines = game._mines
        game._correctlyMarkedMines = game._mines
        game.winCheck()
        # then
        self.assertEqual(game._gameEnded, gameEnded)

    def test_shouldEndGameIfAllEmptyFieldsClicked(self):
        # given
        gameEnded = True
        game = Saper()
        window = MainWindow(game)
        game.setView(window)
        game._mapWidth = 8
        game._mapHeight = 8
        game._mines = 12
        # when
        game.newRandomMap()
        game._clearedButtons = game._mapWidth * game._mapHeight - game._mines
        game.winCheck()
        # then
        self.assertEqual(game._gameEnded, gameEnded)


if __name__ == '__main__':
    unittest.main()
