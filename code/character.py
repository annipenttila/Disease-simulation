import math
import random

from direction import Direction
# from square import Square
# from simulation_world import SimulationWorld

class Character():

    """ A character is equipped with the various capabilities:
     - It can sense its own surroundings (location, facing, the world that it is in).
     - It can move forward.
     - It can spin around in any one of the four main compass directions.

    When a character's take_turn() method is called, it uses its "brain" to figure
    out what to do (move, turn about, etc.). Characters with different kinds of brains behave
    differently.

    """
    def __init__(self):
        """
        Creates a new simulation character with the given name. The newly
        created character is initially just a "dumb shell" until
        it's given a brain later using the method
        set_brain().

        If the given name is None or an empty
        string, the name is set to "Incognito".

        See set_brain(Brain)
        """
        # self.set_name(name)
        self.world = None           # fixed value
        self.location = None        # most-recent holder
        self.eliminated = False     # flag
        self.deceased = False       # flag
        self.infected = False
        self.recovered = False
        self.susceptible = True

        self.age = None
        self.brain = None           # most-recent holder
        self.facing = None          # most-recent holder
        # self.nearest_neighbour_location = None   # most-recent holder, see get_neighbour_location

    def get_age(self):

        return self.age

    def set_brain(self, new_brain):
        """
        Sets a "brain" (or AI) for the character (replacing any brain
        previously set, if any): spreader, susceptible, recovered, ...

        Parameter new_brain is the artificial intelligence that controls the character
        """
        self.brain = new_brain

    def get_brain(self):
        """
        Returns the "brain" (or AI) of the character: spreader, susceptible, recovered/... object
        """
        return self.brain

    def get_world(self):
        """
        Returns the world in which the character is, or None if the character has not been placed in any world:
        SimulationWorld
        """
        return self.world

    def get_location(self):
        """
        Returns the current location of the character in the simulation world, or None if the character has not been
        placed in the simulation: Coordinates

        See get_location_square()
        """
        return self.location

    def get_location_square(self):
        """
        Returns the square that the character is in: Square

        See get_location()
        """
        return self.get_world().get_square(self.get_location())

    def get_facing(self):
        """
        Returns the direction the character is facing: tuple
        """
        return self.facing

    def eliminate(self):
        """
        Eliminates the deceased character. From there the character should be eliminated?
        See Square
        See take_turn()
        """
        self.infected = False
        self.eliminated = True
        self.brain = None
        # self.brain = None

    def set_world(self, world,  location,  facing):
        """
        Places the character in the given world at the specified
        coordinates. Note! This method is supposed to be used from the
        addCharacter method in the SimulationWorld class,
        which makes sure that the character is appropriately recorded as
        being part of the simulation world.

        Parameter world is the simulation world in which the character is placed: SimulationWorld

        Parameter location is the coordinates at which the character is placed: Coordinates

        Parameter facing is the direction the character is facing initially : tuple

        Returns False if the square at the given location is not empty or the character is already located in some world
        (the given one or some other world), True otherwise: boolean

        See SimulationWorld.add_character(Character, Coordinates, Direction)
        """
        target_square = world.get_square(location)
        if not target_square.is_empty() or self.get_world() is not None:
            return False

        else:
            self.world = world
            self.location = location
            self.facing = facing
            return True

    def is_infected(self):
        return self.infected

    def infect(self):
        self.infected = True
        self.susceptible = False
        return self.infected

    def is_susceptible(self):
        return self.susceptible

    def is_recovered(self):
        return self.recovered

    def cure(self):
        self.infected = False
        self.recovered = True

    def is_deceased(self):
        """
        Returns the boolean value which states whether the character is deceased or
        not or is it lacking a brain: boolean
        """
        return self.eliminated or self.get_brain() is None

    def is_stuck(self):

        """
        Determines whether the character is stuck or not, i.e., are there any
        squares that the character could move into. This is done by
        examining the four adjacent squares (diagonally adjacent squares are
        not considered). If there is a wall in all directions, the character is
        considered stuck. Also, if the character has not yet been placed in any
        simulation world, it is considered to be stuck.

        Returns a boolean value that states whether the bot is stuck or not: boolean
        
        See take_turn()
        """
        world = self.get_world()
        if world is None:
            return True

        for value in Direction.get_values():  # most-recent holder
            if not world.get_square(self.get_location().get_neighbor(value)).is_square_wall():
                return False
        return True

    def move(self, direction):
        """
        Changes the place of the character within its current world
        from the current square to the square next to it in the
        given direction.

        The direction does not necessarily have
        to be the same one that the character is originally facing in.
        This method changes the character to face the direction it
        moves in.

        Parameter direction is the direction to move in: tuple
        Returns a boolean value indicating if the movement was successful: boolean
        """

        if self.is_deceased():  # if self.eliminated is True or self.get_brain in None
            return False

        target = self.get_location().get_neighbor(direction)
        current_square = self.get_location_square()
        target_square = self.get_world().get_square(target)
        self.spin(direction)

        if target_square.is_empty() and not target_square.is_square_wall():
            current_square.remove_character()
            self.location = target
            target_square.set_character(self)
            return True

        # if self is infected and the target square is wall
        elif self.infected and target_square.is_square_wall():

            self.spin(random.choice([Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.NORTH]))
            target = self.get_location().get_neighbor(self.facing)  # new target square
            target_square = self.get_world().get_square(target)

            if target_square.is_empty() and not target_square.is_square_wall():
                current_square.remove_character()
                self.location = target
                target_square.set_character(self)
                return True
            else:
                return False
        else:
            return False

    def move_forward(self):
        """
        Moves the character forward one square. This is equivalent to calling self.move(self.get_facing()).
        See move(Direction)
        Returns a boolean value indicating if the movement was successful: boolean
        """
        return self.move(self.get_facing())

    def spin(self, new_facing):
        """
        Turns the character in the specified direction, if the
        character is intact. If the character is deceased, the method does nothing.

        Parameter new_facing is the new facing direction of the character: tuple
        """
        if not self.eliminated:
            self.facing = new_facing

    def take_turn(self):
        """
        Gives the character a turn to act. An unstuck character, however, consults its brain to
        find out what to do. This is done by calling the brain's method move_body().
        Here is a general outline of what happens during a character's turn:
         1. The character checks its sensors to see if it is stuck or deceased?. (If it is, it doesn't do anything.)
         2. If not, it call's it's brain's move_body() method, leaving it up to the brain to decide
            what happens next.
         3. The move_body() method will then determine how the character behaves, usually calling
            various methods of the character's body (i.e., the Character object whose turn it is),
            e.g. move, spin. However, it is not up to the Character object
            to decide which of its methods get called - that depends on the implementation of the character's brain.


        See is_stuck()

        See Brain.move_body()
        """
        if not self.is_stuck() and not self.is_deceased():
            self.brain.move_body()

    def __str__(self):
        return self.get_name() + ' at location ' + str(self.get_location())

    def get_neighbour_location(self):

        # finds the coordinates of the nearest neighbour in the world
        neighbour_location = None
        shortest_dist = math.inf
        current_dist = None

        for character in self.get_world().get_characters():
            current_dist = self.calculate_distance(character)
            if current_dist < shortest_dist and current_dist != 0:
                neighbour_location = character.get_location()
                shortest_dist = current_dist

        return neighbour_location

    def calculate_distance(self, character):

        # calculates the distance between the given character objects

        location1 = self.get_location()
        location2 = character.get_location()
        squared_dist_x = math.pow(location2.get_x() - location1.get_x(), 2)
        squared_dist_y = math.pow(location2.get_y() - location1.get_y(), 2)
        distance = math.sqrt(squared_dist_x + squared_dist_y)

        return distance

