from square import Square
from spreader import Spreader
from recovered import Recovered
import random
#  from user_input import user_input


class SimulationWorld:

    def __init__(self, width, height):
        """
                Creates a new simulation world with the specified dimensions.
                Initially all the squares of the new world are empty.

                Parameter width is the width of the world in squares: int

                Parameter height is the height of the world in squares: int
        """

        self.squares = [None] * width
        for x in range(self.get_width()):  # stepper
            self.squares[x] = [None] * height
            for y in range(self.get_height()):  # stepper
                self.squares[x][y] = Square()  # fixed value

        self.characters = []  # container
        self.turn = 0         # kinda like stepper (but not quite) index to characters list
        self.end = False
        self.name = None
        self.mortality_rate = 0

    def is_end(self):
        return self.end

    def set_mortality_rate(self, mortality_rate_in_percents):
        rate = mortality_rate_in_percents / 100
        self.mortality_rate = rate

    def get_mortality_rate(self):
        return self.mortality_rate

    def get_name(self):
        return self.name

    def get_width(self):
        """
        Returns width of the world in squares: int
        """
        return len(self.squares)

    def get_height(self):
        """
        Returns the height of the world in squares: int
        """
        return len(self.squares[0])

    def add_character(self, character, location, facing):
        """
        Adds a new character in the simulation world. (Note! This method also
        takes care that the character is aware if its new position.
        This is done by calling character's set_world method.)

        Parameter character is the character to be added: Character

        Parameter location is the coordinates of the character: Coordinates

        Parameter facing is the direction the character is facing initially : tuple

        Returns False if the square at the given location is not empty or the given character is already located in some
        world (this or some other world), True otherwise: boolean

        See Character.set_world(SimulationWorld, Coordinates, Direction)
        """
        if character.set_world(self, location, facing):
            self.characters.append(character)
            self.get_square(location).set_character(character)
            return True
        else:
            return False

    def get_square(self, coordinates):
        """
        Parameter coordinates is a location in the world: Coordinates
        Returns the square that is located at the given location. If the given coordinates point outside the world,
        this method returns a square that contains a wall and is not located in any simulation world: Square
        """
        if self.contains(coordinates):
            return self.squares[coordinates.get_x()][coordinates.get_y()]
        else:
            return Square(True)

    def get_number_of_characters(self):
        """
        Returns the number of characters added to this world: int
        """
        return len(self.characters)

    def get_character(self, turn_number):
        """
        Returns the character which has the given "turn number".
        The turn numbers of the characters in a world are determined by
        the order in which they were added. I.e., the first character has
        a turn number of 0, the second one's number is 1, etc.

        Parameter turn_number is the turn number of a character. Must be on the interval [0, (number of characters minus 1)].: int

        Returns the character with the given turn number: Character
        """
        if 0 <= turn_number < self.get_number_of_characters():
            return self.characters[turn_number]
        else:
            return None

    def get_next_character(self):
        """
        Returns the character to act next in this world's round-robin turn system, or None if there aren't any
        characters in the world: Character

        See next_character_turn()
        """
        if self.get_number_of_characters() < 1:
            return None
        else:
            return self.characters[self.turn]

    def next_character_turn(self):
        """
        Lets the next character take its turn. That is, calls the
        take_turn method of the character whose turn it is,
        and passes the turn to the next character. The turn is passed
        to the character with the next highest turn number (i.e. the one
        that was added to the world after the current character), or wraps
        back to the first character (turn number 0) if the last turn number
        was reached. That is to say: the character which was added first,
        moves first, followed by the one that was added second, etc.,
        until all characters have moved and the cycle starts over.
        If there are no characters in the world, the method does nothing.

        See get_next_character()
        """
        current = self.get_next_character()
        if current is not None:
            self.turn = (self.turn + 1) % self.get_number_of_characters()
            current.take_turn()

        if current.infected:
            for char in self.get_characters():
                if 0 < current.calculate_distance(char) <= 1.5:
                    if char.susceptible and char.get_age() == 1:
                        if random.random() <= 0.25:    # the infection rate for young people:
                            char.infect()
                            new_brain = Spreader(char)
                            char.set_brain(new_brain)
                            char.brain.disease_length = current.brain.get_disease_length()

                    elif char.susceptible and char.get_age() == 2:
                        if random.random() <= 0.5:    # the infection rate for adults:
                            char.infect()
                            new_brain = Spreader(char)
                            char.set_brain(new_brain)
                            char.brain.disease_length = current.brain.get_disease_length()

                    elif char.susceptible and char.get_age() == 3:
                        if random.random() <= 0.75:    # the infection rate for elderly people:
                            char.infect()
                            new_brain = Spreader(char)
                            char.set_brain(new_brain)
                            char.brain.disease_length = current.brain.get_disease_length()

            duration = current.brain.get_duration()
            average_length = current.brain.get_disease_length()

            # the approximation for the coefficient that scales the probability of staying infected
            coefficient = (1 - 0.5 ** (1/(average_length+1))) / 0.5
            if random.random() < (1-self.mortality_rate)*coefficient*(duration/average_length):  # the given infection rate:
                current.cure()
                new_brain = Recovered(current, 1)
                current.set_brain(new_brain)

            elif random.random() < self.mortality_rate*coefficient*(duration/average_length):
                current.eliminate()

    def next_full_turn(self):
        """
        Lets each character take its next turn. That is, calls the next_character_turn
        a number of times equal to the number of characters in the world.
        """
        counter = 0
        for char in self.get_characters():
            if char.infected:
                counter = 1
        if counter == 0:
            self.end = True
            return False

        for count in range(self.get_number_of_characters()):      # stepper
            self.next_character_turn()

        return True

    def contains(self, coordinates):
        """
        Determines if this world contains the given coordinates.
        Parameter coordinates is a coordinate pair: Coordinates
        Returns a boolean value indicating if this world contains the given coordinates: boolean
        """
        x_coordinate = coordinates.get_x()
        y_coordinate = coordinates.get_y()
        return 0 <= x_coordinate < self.get_width() and 0 <= y_coordinate < self.get_height()

    def get_characters(self):
        """
        Returns an array containing all the characters currently located in this world: list
        """
        return self.characters[:]

    def get_len_age_groups(self):
        """
        returns the sizes of each age group
        """
        young = 0
        adults = 0
        elderly = 0

        for character in self.get_characters():
            if character.age == 1:
                young += 1
            elif character.age == 2:
                adults += 1
            else:
                elderly += 1

        return young, adults, elderly

    def get_len_spreaders(self):
        """
        returns the current number of spreaders in the population
        """
        count = 0
        young = 0
        adults = 0
        elderly = 0

        for character in self.get_characters():
            if character.infected:
                count += 1
                if character.get_age() == 1:
                    young += 1
                elif character.get_age() == 2:
                    adults += 1
                else:
                    elderly += 1

        return count, young, adults, elderly

    def get_len_susceptible(self):
        """
        returns the current number of susceptible people in the population
        """
        count = 0
        young = 0
        adults = 0
        elderly = 0

        for character in self.get_characters():
            if character.susceptible:
                count += 1
                if character.get_age() == 1:
                    young += 1
                elif character.get_age() == 2:
                    adults += 1
                else:
                    elderly += 1

        return count, young, adults, elderly

    def get_len_recovered(self):
        """
        returns the current number of recovered in the population
        """
        count = 0
        young = 0
        adults = 0
        elderly = 0

        for character in self.get_characters():
            if character.recovered:
                count += 1
                if character.get_age() == 1:
                    young += 1
                elif character.get_age() == 2:
                    adults += 1
                else:
                    elderly += 1

        return count, young, adults, elderly

    def get_len_deceased(self):
        """
        returns the current number of deceased in the population
        """
        count = 0
        young = 0
        adults = 0
        elderly = 0

        for character in self.get_characters():
            if character.eliminated:
                count += 1
                if character.get_age() == 1:
                    young += 1
                elif character.get_age() == 2:
                    adults += 1
                else:
                    elderly += 1

        return count, young, adults, elderly


