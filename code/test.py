import unittest

from simulation_world import SimulationWorld
from character import Character
from coordinates import Coordinates
from direction import Direction
from spreader import Spreader


class Test(unittest.TestCase):

    def setUp(self):
        self.test_world = SimulationWorld(5, 5)

        first_location = Coordinates(4, 3)
        first_body = Character()
        first_brain = Spreader(first_body)
        first_body.set_brain(first_brain)
        self.test_world.add_character(first_body, first_location, Direction.EAST)
        self.first_body = first_body

        new_location = Coordinates(4, 4)
        new_body = Character()
        new_brain = Spreader(new_body)
        new_body.set_brain(new_brain)
        self.test_world.add_character(new_body, new_location, Direction.WEST)
        self.new_body = new_body

    def test_Spreader(self):

        self.assertEqual('(4, 4)', str(self.test_world.get_characters()[1].get_location()),
                         "the spreader should be in (4, 4)")

    def test_character_list(self):

        self.assertEqual(2, self.test_world.get_number_of_characters(), "the number should be 2")

    def test_SimulationWorld_functions(self):

        self.assertEqual([self.first_body, self.new_body], self.test_world.get_characters())


if __name__ == "__main__":
    unittest.main()