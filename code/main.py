import sys
from PyQt6.QtWidgets import QApplication

from gui import GUI
from user_input import user_input
from direction import Direction
from simulation_world import *
from coordinates import *
from character import *
from spreader import *
from susceptible import *
from recovered import *


def main():

    test_world, size = user_input()

    # Every Qt application must have one instance of QApplication.
    global app  # Use global to prevent crashing on exit
    app = QApplication(sys.argv)

    if 50 - size >= 10:
        gui = GUI(test_world, 50-size)
    elif size >= 60:
        gui = GUI(test_world, 8)
    else:
        gui = GUI(test_world, 12)

    # Start the Qt event loop. (i.e. make it possible to interact with the gui)
    sys.exit(app.exec())

    # Any coDe below this point will only be executed after the gui is closed.

if __name__ == "__main__":
    main()


