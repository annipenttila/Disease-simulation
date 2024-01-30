
class Square:
    """
    The class Square represents a single square in a simulation world.
    A square can contain either a wall or a character or it can be empty.
    """

    def __init__(self, is_wall=False):
        """
        Creates a new square. Initially there is no character in the square.
        """
        self.character = None     # most-recent holder (None if no character in square)
        self.is_wall = is_wall

    def get_character(self):
        """
        Returns the character in the square or None if there is no character in the square: Character
        """
        return self.character

    def is_empty(self):
        """
        Returns a boolean value stating whether the square is empty or not: boolean
        """
        return self.character is None

    def is_square_wall(self):
        """
        Returns a boolean value stating whether there is a wall in the square or not: boolean
        """
        return self.is_wall

    def set_character(self, character):
        """
        Marks the square as containing a character, if possible.
        If the square was not empty, the method fails to do anything.

        Parameter character is the char to be placed in this square: Character
        Returns a boolean value indicating if the operation succeeded: boolean
        """
        if self.is_empty():
            self.character = character
            return True
        else:
            return False

    def remove_character(self):
        """
        Removes the character in this square.
        Returns the char removed from the square or None, if there was no char: Character
        """
        removed_character = self.get_character()
        self.character = None
        return removed_character
