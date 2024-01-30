from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import Qt

from character_graphics_item import CharacterGraphicsItem
from coordinates import Coordinates


class GUI(QtWidgets.QMainWindow):
    """
    The class GUI handles the drawing of a SimulationWorld and allows user to
    interact with it.
    """
    def __init__(self, world, square_size):
        super().__init__()

        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindow must have a centralWidget to be able to add layouts
        self.horizontal = QtWidgets.QHBoxLayout()   # Horizontal main layout
        self.centralWidget().setLayout(self.horizontal)
        self.world = world
        self.square_size = square_size
        self.added_characters = []

        self.init_window()
        self.init_buttons()

        # self.gui_exercise = GuiExercise(self.world, self.scene, self.square_size)

        self.add_character_world_grid_items()
        self.add_character_graphics_items()
        self.update_characters()
        self.update_data()

        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_characters)
        self.timer.start(10)    # Milliseconds

        bounding_rect = self.scene1.itemsBoundingRect()
        self.view1.setSceneRect(bounding_rect)

    def add_character_world_grid_items(self):
        """
        Adds an QGraphicsItem for each square in the simulation world.
        Qt uses QGraphicsItems to draw objects in the QGraphicsScene.
        QGraphicsRectItem is a subclass of QGraphicsItem, and is useful for
        easily drawing rectangular items.
        This method should only be called once, otherwise it creates duplicates!
        """

        width = self.world.get_width()
        height = self.world.get_height()

        for x in range(width):
            for y in range(height):
                square_width = self.square_size
                square_height = self.square_size
                x_coord = x * square_width
                y_coord = y * square_height

                square = self.world.get_square(Coordinates(x, y))   # toimiiko pelkkä (x,y)
                color = QtGui.QColor(211, 211, 211)

                item = QtWidgets.QGraphicsRectItem(x_coord, y_coord, square_width, square_height)
                item.setBrush(color)
                self.scene1.addItem(item)

    def get_character_graphics_items(self):

        """
        Returns all the CharacterGraphicsItem in the scene.

        NOTE: This is a silly implementation, it would be much more efficient to store
        all CharacterGraphicsItems in a list and simply return that list.
        """
        items = []
        for item in self.scene1.items():
            if type(item) is CharacterGraphicsItem:
                items.append(item)
        return items

    def update_data(self):

        young, adults, elderly = self.world.get_len_age_groups()
        number_of_spreaders, spr_young, spr_adults,  spr_elderly = self.world.get_len_spreaders()
        number_of_susceptible, sus_young, sus_adults, sus_elderly = self.world.get_len_susceptible()
        number_of_recovered, rec_young, rec_adults, rec_elderly = self.world.get_len_recovered()
        number_of_deceased, dec_young, dec_adults, dec_elderly = self.world.get_len_deceased()
        total = number_of_deceased + number_of_susceptible + number_of_recovered + number_of_spreaders
        number_of_infected = number_of_deceased + number_of_recovered

        if self.world.is_end():
            self.scene2.clear()

            text_strings = [
                f"Age group distribution:",
                f"{young} young people, {adults} adults, {elderly} elderly people\n",
                f"The simulation is over. There are no more infected people in the population.",
                f"Out of {total} people, {number_of_deceased + number_of_recovered} got infected.\n",
                f"{round((number_of_recovered/number_of_infected)*100)}% of the infected got recovered,",
                f"{rec_young} of them young, {rec_adults} adults and {rec_elderly} elderly people.\n",
                f"{round((number_of_deceased/number_of_infected)*100)}% of the infected got deceased,",
                f"{dec_young} of them young, {dec_adults} adults and {dec_elderly} elderly people.\n"
                ]

            scene_rect = self.scene2.sceneRect()
            scene_width = scene_rect.width()
            scene_height = scene_rect.height()

            # Set the position of the text item to the middle of the scene
            text_x = 0
            text_y = 0

            for text_string in text_strings:
                text_item = QGraphicsTextItem(text_string)
                text_item.setTextWidth(scene_width)         # Set the width to match the scene width
                text_item.setPos(text_x, text_y)

                self.scene2.addItem(text_item)

                text_y += text_item.boundingRect().height()

        else:
            text_strings = [
                f"Age group distribution:",
                f"{young} young people, {adults} adults, {elderly} elderly people\n",
                f"Character colours:",
                f"Red: infected",
                f"Light-yellow: susceptible 0-17y",
                f"Yellow: susceptible 18-64y",
                f"Orange: susceptible +65y",
                f"Green: recovered",
                f"Black: deceased",
                f" ",
                f"Number of each character type currently in the simulation:",
                f"Spreaders: {number_of_spreaders}",
                f"Susceptible: {number_of_susceptible}",
                f"Recovered: {number_of_recovered}",
                f"Deceased: {number_of_deceased}",
            ]

            self.scene2.clear()

            scene_rect = self.scene2.sceneRect()
            scene_width = scene_rect.width()
            scene_height = scene_rect.height()

            # Set the position of the text item to the middle of the scene
            text_x = 0
            text_y = 0

            for text_string in text_strings:
                text_item = QGraphicsTextItem(text_string)
                text_item.setTextWidth(scene_width)
                text_item.setPos(text_x, text_y)
                self.scene2.addItem(text_item)

                text_y += text_item.boundingRect().height()

    def add_character_graphics_items(self):
        """

        Finds all characters in the SimulationWorld, which do not yet have a
        CharacterGraphicsItem and adds a CharacterGraphicsItem for them.
        If every character already has a CharacterGraphicsItem, this method does nothing.
        """
        for character in self.world.get_characters():
            if character not in self.added_characters:
                character_item = CharacterGraphicsItem(character, self.square_size)
                self.scene1.addItem(character_item)
                self.added_characters.append(character)

    def init_buttons(self):
        """
        Adds buttons to the window and connects them to their respective functions
        See: QPushButton at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QPushButton.html
        """
        self.next_turn_btn = QtWidgets.QPushButton("Next full turn")
        self.next_turn_btn.clicked.connect(self.world.next_full_turn)
        self.next_turn_btn.clicked.connect(self.update_data)

        self.horizontal.addWidget(self.next_turn_btn)

    def update_characters(self):
        """
        Iterates over all character items and updates their position to match
        their physical representations in the simulation world.
        """
        for character_item in self.get_character_graphics_items():
            character_item.updateAll()

        # self.update_data()

    def init_window(self):
        """
        Sets up the window.
        """
        self.setGeometry(100, 100, 1200, 1000)
        name = self.world.get_name()
        self.setWindowTitle(f"{name} simulation")
        self.show()

        # Add a scene for drawing 2d objects
        self.scene1 = QtWidgets.QGraphicsScene()
        self.scene1.setSceneRect(0, 0, 1200, 1000)

        self.scene2 = QtWidgets.QGraphicsScene()
        self.scene2.setSceneRect(0, 0, 300, 300)

        # Add a view for showing the scene
        self.view1 = QtWidgets.QGraphicsView(self.scene1, self)
        self.view1.adjustSize()
        self.view1.show()
        self.horizontal.addWidget(self.view1)

        self.view2 = QtWidgets.QGraphicsView(self.scene2, self)
        self.view2.adjustSize()
        self.view2.show()
        self.horizontal.addWidget(self.view2)


