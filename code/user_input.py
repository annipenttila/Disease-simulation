from simulation_world import SimulationWorld
from character import Character
from susceptible import Susceptible
from spreader import Spreader
from coordinates import Coordinates
from direction import Direction

import random
import math


def user_input():
    """
    Prompts the user for input to configure a disease simulation.
    Returns: A tuple containing the simulation world object and the size of the world grid.
    """

    print("This is a disease simulation.")
    name = input("Enter the name of the disease: ")

    prompts = False
    while not prompts:
        try:
            population_size = int(input("Enter the size of the population: "))
            number_of_spreaders = int(input("Enter the number of spreaders: "))
            duration = int(input("Enter the average duration of the disease (in days): "))
            mortality_rate = int(input("Enter the mortality rate of the disease (%): "))

            if population_size < 0 or number_of_spreaders < 0 or mortality_rate < 0:
                print("The simulation parameters must be positive integers.")
            elif population_size < number_of_spreaders:
                print("The size of the population must be larger than the number of spreaders.")
            elif mortality_rate < 0 or mortality_rate > 100:
                print("The mortality rate must be an integer between 0 and 100.")
            else:
                prompts = True

        except ValueError:
            print("The simulation parameters must be positive integers.")

    print("\n")
    print("The probability of getting infected (when in contact with a spreader) varies between different age groups.")
    print("The age groups are: \nYOUNG: 0-17 (25% infection rate)\nADULTS: 18-64 (50% infection rate)\nELDERLY: 65+ (75% infection rate)")
    print("In the simulation the spreaders are red, susceptible people are yellow/orange, recovered green and deceased black.")

    young = 1  # lower chance of getting infected
    adult = 2  # moderate chance of getting infected
    elderly = 3  # high chance of getting infected

    number_of_susceptible = population_size - number_of_spreaders

    if population_size >= 100:
        grid_size = math.sqrt(10 * population_size)
        size = math.ceil(grid_size)
    elif population_size >= 50:
        grid_size = math.sqrt(7.5 * population_size)
        size = math.ceil(grid_size)
    elif population_size >= 15:
        grid_size = math.sqrt(5 * population_size)
        size = math.ceil(grid_size)
    else:
        size = math.ceil(population_size*1.5)

    world = SimulationWorld(size, size)
    world.name = name
    world.set_mortality_rate(mortality_rate)

    for i in range(0, number_of_spreaders):

        flag = True
        location = None

        while flag:
            x = random.randrange(size)
            y = random.randrange(size)
            location = Coordinates(x, y)
            square = world.get_square(location)
            if square.is_empty():
                flag = False

        spreader_body = Character()
        spreader_body.infected = True
        spreader_body.age = random.choice([young, adult, elderly])
        spreader_brain = Spreader(spreader_body)
        spreader_body.set_brain(spreader_brain)
        spreader_brain.disease_length = duration

        if random.random() <= 0.25:
            world.add_character(spreader_body, location, Direction.EAST)
        elif 0.25 < random.random() <= 0.5:
            world.add_character(spreader_body, location, Direction.SOUTH)
        elif 0.5 < random.random() <= 0.75:
            world.add_character(spreader_body, location, Direction.WEST)
        else:
            world.add_character(spreader_body, location, Direction.NORTH)

    for i in range(0, number_of_susceptible):

        flag = True
        location = None

        while flag:
            x = random.randrange(size)
            y = random.randrange(size)
            location = Coordinates(x, y)
            square = world.get_square(location)
            if square.is_empty():
                flag = False

        susceptible_body = Character()
        susceptible_brain = Susceptible(susceptible_body)
        susceptible_body.set_brain(susceptible_brain)
        susceptible_body.age = random.choice([young, adult, elderly])

        if random.random() <= 0.25:
            world.add_character(susceptible_body, location, Direction.EAST)
        elif 0.25 < random.random() <= 0.5:
            world.add_character(susceptible_body, location, Direction.SOUTH)
        elif 0.5 < random.random() <= 0.75:
            world.add_character(susceptible_body, location, Direction.WEST)
        else:
            world.add_character(susceptible_body, location, Direction.NORTH)

    return world, size






