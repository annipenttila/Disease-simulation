from PyQt6 import QtWidgets, QtGui, QtCore
from character import Character
from coordinates import Coordinates
from direction import Direction


class CharacterGraphicsItem(QtWidgets.QGraphicsPolygonItem):

    # consider the shape of the item
    """
        The class CharacterGraphicsItem extends QGraphicsPolygonItem to link it together to the visual
        representation of a Character. The QGraphicsPolygonItem handles the drawing, while the
        Character knows its own location and status.
    """

    def __init__(self, character, square_size):
        # Call init of the parent object
        super(CharacterGraphicsItem, self).__init__()

        self.character = character
        self.square_size = square_size
        brush = QtGui.QBrush(1)  # 1 for even fill
        self.setBrush(brush)
        self.constructTriangleVertices()
        self.updateAll()

    def constructTriangleVertices(self):
        """
        This method sets the shape of this item into a triangle.

        The QGraphicsPolygonItem can be in the shape of any polygon.
        We use triangles to represent characters, as it makes it easy to
        show the current facing of the character.
        """
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        # Add the corners of a triangle to the polygon object
        triangle.append(QtCore.QPointF(self.square_size/2, 0))  # Tip
        triangle.append(QtCore.QPointF(0, self.square_size))    # Bottom-left
        triangle.append(QtCore.QPointF(self.square_size, self.square_size))  # Bottom-right
        triangle.append(QtCore.QPointF(self.square_size/2, 0))  # Tip

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

        # Set the origin of transformations to the center of the triangle.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.square_size/2, self.square_size/2)

    def updateAll(self):
        """
        Updates the visual representation to correctly resemble the current
        location, direction and status of the parent character.
        """
        # if Character.is_deceased(self.character):
        # THEN WHAT? remove character? remove triangle

        self.updatePosition()
        self.updateRotation()
        self.updateColor()

    def updatePosition(self):

        """
        Update the coordinates of this item to match the attached character.
        Remember to take into account the size of the squares.

        A character in the first (0, 0) square should be drawn at (0, 0).

        See: For setting the position of this GraphicsItem, see
        QGraphicsPolygonItem at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGraphicsPolygonItem.html
        and its parent class QGraphicsItem at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGraphicsItem.html

        For getting the location of the parent character, look at the Character-class
        in character.py.
        """
        new_location = Character.get_location(self.character)
        x_coord = Coordinates.get_x(new_location)
        y_coord = Coordinates.get_y(new_location)

        QtWidgets.QGraphicsPolygonItem.setPos(self, x_coord * self.square_size, y_coord * self.square_size)

    def updateRotation(self):
        """
        Rotates this item to match the rotation of parent character.
        A method for rotating can be found from QGraphicsItem at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGraphicsItem.html
        """
        # my code:
        character_facing = Character.get_facing(self.character)
        if character_facing == Direction.NORTH:
            self.setRotation(0)
        if character_facing == Direction.EAST:
            self.setRotation(90)
        if character_facing == Direction.SOUTH:
            self.setRotation(180)
        if character_facing == Direction.WEST:
            self.setRotation(270)

    def updateColor(self):
        """
        Draw spreaders in red, susceptible in yellow and recovered individuals in green.
        - red: (255, 0, 0)
        - yellow: (255, 255, 0)
        - green: (0, 255, 0)
        See: setBrush() at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QAbstractGraphicsShapeItem.html
        and QBrush at https://doc.qt.io/qtforpython/PySide6/QtGui/QBrush.html
        and QColor at https://doc.qt.io/qtforpython/PySide6/QtGui/QColor.html
        Look at character.py for checking the status of the individual.
        """
        # if Character.is_deceased():
        #    self.scene().removeItem(self)

        if Character.is_deceased(self.character):   # black, DECEASED
            self.setBrush(QtGui.QColor(0, 0, 0))

        if Character.is_infected(self.character):
            self.setBrush(QtGui.QColor(255, 0, 0))  # red, INFECTED

        elif Character.is_susceptible(self.character):
            if Character.get_age(self.character) == 1:
                self.setBrush(QtGui.QColor(255, 255, 200))  # light yellow, YOUNG
            elif Character.get_age(self.character) == 2:
                self.setBrush(QtGui.QColor(255, 255, 0))    # yellow, ADULT
            elif Character.get_age(self.character) == 3:
                self.setBrush(QtGui.QColor(255, 165, 0))    # orange, ELDERLY

        elif Character.is_recovered(self.character):
            self.setBrush(QtGui.QColor(0, 255, 0))          # green, RECOVERED
