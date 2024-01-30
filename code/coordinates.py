from direction import Direction


class Coordinates():

    """
    The class C{Coordinates} represents pairs of
    integers that specify locations on a two-dimensional grid.
    A coordinate object is immutable
    after creation.
    """
    def __init__(self, x, y):
        """
        Creates a new coordinate pair.

        Parameter x: int

        Parameter y: int
        """
        self.x = x    # fixed value
        self.y = y    # fixed value

    def get_x(self):
        """
        Returns the x coordinate (int)
        """
        return self.x

    def get_y(self):
        """
        Returns the y coordinate (int)
        """
        return self.y

    def get_neighbor(self, direction):
        """
        Returns the coordinates that are next to the coordinates, in the given direction.
        Parameter direction: tuple
        Returns the neighboring coordinates (Coordinates)
        """
        return self.get_relative(direction, 1)

    def get_relative(self, new_direction, distance):
        """
        Returns the coordinates that are a given distance from these coordinates, in the given direction. E.g. if these
        coordinates are (2, 2), and the parameters are direction .EAST and 3, the result is (5, 2).

        Parameter direction: tuple
        Parameter distance: (non-negative) int
        Returns a coordinate pair relative to this one (Coordinates)
        """
        return Coordinates(self.get_x() + Direction.get_x_step(new_direction) * distance,
                           self.get_y() + Direction.get_y_step(new_direction) * distance)

    def __str__(self):
        """
        Returns a string of the form (X, Y) representing of the coordinate pair
        """
        return '({:.0f}, {:.0f})'.format(self.get_x(), self.get_y())
