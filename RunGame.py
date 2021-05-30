from MySaper import MySaper
from MainWindow import MainWindow


if __name__ == '__main__':
    gameSettings = MySaper()
    gameWindow = MainWindow(gameSettings)
    gameWindow.windowLoop()
