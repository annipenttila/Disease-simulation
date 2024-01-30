import math
import random

from recovered import Recovered
from direction import Direction
from brain import Brain


class Spreader(Brain):
    """
    TRIES TO STAY AWAY FROM OTHER CHARACTERS?
    """
    def __init__(self, body):
        """
                Creates a new spreader brain for the given body.
                Parameter body is the character whose actions the brain is supposed to control: Character
                Parameter neighbour is the nearest character: Character (any type)
                The spreader tries to avoid human contact (in order to decrease
                the risk of infecting other people):
                """
        super(Spreader, self).__init__(body)

        # self.neighbour_location = self.body.get_neighbour_location()

        self.body.infected = True
        self.body.susceptible = False
        self.eliminated = False
        self.neighbour_location = None
        self.duration = 0
        self.disease_length = 0
        self.brain = self

        # SimulationWorld.get_characters -> loop through it?

    def is_infected(self):
        self.body.infected = True
        return True

    # def is_susceptible(self):
    #    self.susceptible = False
    #    return self.susceptible

    def is_recovered(self):
        self.body.recovered = True
        return True

    def move_body(self):
        """
        Moves the given "body", i.e., the character given as a parameter. A spreader tries to stay away from other people,
        since we assume here that spreaders know that they are infected. If there is a wall or another character in the
        chosen direction, the spreader either finds the next possible option or will stay at the current square.

        The path of movement is chosen as follows. First the spreader calculates its distance to its neighbour in both x
        and y dimension. It moves one square at a time so that either x or y distance increases by one, depending on
        which one is smaller. The smaller of the two is incremented. In the case that the distances are equal, x is
        incremented. The spreader only moves one square per turn. When moving a spreader turns to face the
        direction it is moving in.

        This method assumes that it is called only if the spreader is not deceased.
        """

        self.duration += 1
        location = self.body.get_location()
        next_direction = self.determine_direction(location)
        if next_direction:
            self.body.move(next_direction)

    def get_duration(self):

        return self.duration

    def get_disease_length(self):

        return self.disease_length

    def determine_direction(self, current_location):
        """
        Determines the direction the spreader will attempt to move in.
        Parameter current_location is the spreader's current location: Coordinates
        Returns the preferred direction of movement: tuple
        See move_body()
        """
        # see square and get neighbour
        current_square = self.body.get_location_square()
        current_coord = self.body.get_location()

        neighbour_location = self.body.get_neighbour_location()

        if neighbour_location is not None and current_location is not None:
            distance_x = neighbour_location.get_x() - current_location.get_x()
            distance_y = neighbour_location.get_y() - current_location.get_y()

            if math.fabs(distance_x) >= math.fabs(distance_y):
                print()
                if distance_x >= 1:
                    return Direction.WEST
                elif distance_x <= -1:
                    return Direction.EAST
            else:
                if distance_y >= 1:
                    return Direction.NORTH
                elif distance_y <= -1:
                    return Direction.SOUTH
        return None


