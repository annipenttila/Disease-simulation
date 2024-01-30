import math
import random
from direction import Direction
from brain import Brain


class Recovered(Brain):

    def __init__(self, body, random_seed):
        """
        Creates a brain for a recovered individual.
        Each Recovered has its own unique Random object (a random number generator). Recovered does not create a
        new Random number generator every time this method is called.

        See the documentation of random (in https://docs.python.org/3.4/library/random.html).
        Parameter body is the character whose actions the brain is supposed to control: Character
        Parameter random_seed is the seed that feeds the random generator that guides the bot: int
        """
        super(Recovered, self).__init__(body)
        self.random = random.Random(random_seed)

    def is_recovered(self):
        self.recovered = True
        return self.recovered

    def move_body(self):
        """
        Moves the character. A recovered character selects a random direction and tries to move to the adjacent square in that
        direction. If there is a wall or another character in that square, the character will collide (and does not move). If
        the character collides with something, it remains facing whatever it collided with and ends its turn there. If
        the character did not collide with anything, it turns in a new direction after moving. The new facing is again
        selected at random. Note: this means that assuming that the character did not collide, it picks two random
        directions per turn, one to move in and one to face in.

        The character selects a random direction using the following algorithm:

        - Get all the direction constants in a list, in the order defined by the direction module.

        - Select a random list item (for example, using random.choice(sequence)).

        - Use the direction found.

        See direction.get_values()

        See random.choice()
        """
        if self.body.move(self.get_random_direction()):
            self.body.spin(self.get_random_direction())

    def get_random_direction(self):
        """
        Selects a random direction.

        Returns: random direction: tuple
        """
        directions = Direction.get_values()
        return self.random.choice(directions)
