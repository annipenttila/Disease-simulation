class Direction:

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    @staticmethod
    def get_x_step(facing):
        """
        Returns the change of the x coordinate if moving one "step"
        in the direction represented by the given compass direction.
        E.g. for C{WEST} the "x step" is
        -1 since moving one step west means a decrease of one in
        the x coordinate.

        Returns: -1, 0 or 1

        See the documentation of class Coordinates
        """
        return facing[0]

    @staticmethod
    def get_y_step(facing):
        """
        Returns the change of the y coordinate if moving one
        "step" in the direction represented by by the given compass
        direction. E.g. for C{NORTH} the "y step" is
        -1 since moving one step north means a decrease of one in
        the y coordinate.

        Returns: -1, 0 or 1

        See the documentation of class Coordinates
        """
        return facing[1]

    @staticmethod
    def get_values():
        """
        Creates a list of directions in a clockwise direction starting
        from north.

        Returns: list of direction tuples
        """
        return [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

    @staticmethod
    def get_next_clockwise(direction):
        """
        Returns the direction 90 degrees clockwise from this direction.
        Returns: another direction tuple clockwise from this one: tuple
        """
        direction_list = Direction.get_values()
        index = direction_list.index(direction)
        return direction_list[(index + 1) % 4]

    @staticmethod
    def get_next_counter_clockwise(direction):
        """
        Returns the direction 90 degrees counterclockwise from this direction.
        Returns: another direction counterclockwise from this one: tuple
        """
        direction_list = Direction.get_values()
        index = direction_list.index(direction)
        return direction_list[(index + 3) % 4]

    @staticmethod
    def get_degrees(direction):
        """
        Returns: the direction as degrees from 0 to 360.
        """
        if (direction == Direction.NORTH):
            return 0
        elif (direction == Direction.EAST):
            return 90
        elif (direction == Direction.SOUTH):
            return 180
        elif (direction == Direction.WEST):
            return 270
        else:
            print("Invalid direction given to get_degrees")
