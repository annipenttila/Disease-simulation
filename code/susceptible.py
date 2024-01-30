from direction import Direction
from character import Character
from brain import Brain


class Susceptible(Brain):
    """
            Moves the given "body", i.e., the character given as a parameter. A Susceptible first looks at the next square in the
            direction of its nose. If that square is empty, it moves there and ends its turn. If the square was not empty,
            it turns its nose 90 degrees clockwise and tries again, moving if possible, etc. If the character makes a full 360
            turnabout without finding a suitable square to move in, it ends its turn without moving. As a susceptible always
            looks where it's going, so it can never collide with anything during its own turn.
    """

    def __init__(self, body):
        """
                Creates a new spreader brain for the given body.
                Parameter body is the character whose actions the brain is supposed to control: Character
                Parameter neighbour is the nearest character: Character (any type)
                The spreader tries to avoid human contact (in order to decrease
                the risk of infecting other people):
                """
        super(Susceptible, self).__init__(body)

        self.infected = False
        self.susceptible = True
        # self.infected = self.is_infected()
        # SimulationWorld.get_characters -> loop through it?

    def is_infected(self):
        self.infected = False
        return self.infected

    def is_susceptible(self):
        self.susceptible = True
        return self.susceptible

    def is_recovered(self):
        return False

    def move_body(self):

        turned = 0

        while turned < 360:
            position = self.body.get_location()
            facing = self.body.get_facing()
            next_coordinate = position.get_neighbor(facing)
            next_square = self.body.get_world().get_square(next_coordinate)

            if next_square.is_empty() and not next_square.is_square_wall():
                self.body.move_forward()
                return
            else:
                facing = Direction.get_next_clockwise(facing)
                self.body.spin(facing)
                turned += 90


