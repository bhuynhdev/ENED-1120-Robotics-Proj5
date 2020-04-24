"""
Module for Rock class and RockFactory
"""

import random
from myconstants import VERT_HALLWAY, HORI_HALLWAY, ZONES


class Rock:
    """
    Rock class as representation for obstacles
    """

    def __init__(self, position: tuple, size: int):
        """
        Intialize a new rock at position, which will also be bottomleft cooridnates
        """
        self.bottomleft = position
        self.size = size


class RockFactory:
    """
    Comprises of methods to generate rocks
    """
    
    def randomize_rocks(self, num_rocks: int) -> list:
        """
        Generate a `num_rocks` amount of rocks
        """
        rocklist = []
        # Num_rocks_per_zone to ensure not too many rocks in one zone
        num_rocks_per_zone = [[0 for _ in range(len(VERT_HALLWAY))] for _ in range(len(HORI_HALLWAY))]
        for _ in range(num_rocks):
            # Randomize a size
            random_size = random.randint(2, 3)
            # Choose a vertical hallway to be in, but making sure
            # not choosing the same zone too many times
            # A vertical hallway should only have (num_rocks/2) rocks
            while True:
                # Choose a zone
                index_vert = random.randrange(0, len(VERT_HALLWAY))
                index_hori = random.randrange(0, len(HORI_HALLWAY))
                if (num_rocks_per_zone[index_hori][index_vert] == 0):
                    num_rocks_per_zone[index_hori][index_vert] += 1
                    break
            # Randomize x and y in the chosen zone
            x_limit = ZONES[index_hori][index_vert][0]
            y_limit = ZONES[index_hori][index_vert][1]
            random_x = random.randint(*x_limit)
            random_y = random.randint(*y_limit)

            # Create a rock
            temp = Rock((random_x, random_y), random_size)
            rocklist.append(temp)
        return rocklist
