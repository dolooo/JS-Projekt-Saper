from Interface import *

if __name__ == '__main__':
    game = Saper()
    window = MainWindow(game)
    game.setView(window)
    window.windowLoop()
