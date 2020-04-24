"""
Module for Rock class and RockFactory
"""

import random


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
    # List of x limits for vertical hallways
    # Make sure generated rocks only lie in vertical hallways
    VERT_HALLWAY = [(0, 12), (48, 60), (96, 108)]

    # List of y limits for horizonal hallways
    # Make sure not too many rocks concentrated in 1 horizonal hallways
    HORI_HALLWAY = [(0, 36), (36, 60), (60, 84), (84, 102)]

    def __init__(self):
        """
        Factory does not contain any attributes
        """
        pass

    def randomize_rocks(self, num_rocks: int) -> list:
        """
        Generate a `num_rocks` amount of rocks
        """
        rocklist = []
        # Num_rocks_per_zone to ensure not too many rocks in one horizontal/vertical hallway
        num_rocks_per_hori = [0 for _ in range(len(RockFactory.HORI_HALLWAY))]
        num_rocks_per_vert = [0 for _ in range(len(RockFactory.VERT_HALLWAY))]
        for _ in range(num_rocks):
            # Randomize a size
            random_size = random.randint(2, 5)
            # Choose a vertical hallway to be in, but making sure
            # not choosing the same vertical hallway too many times
            # A vertical hallway should only have (num_rocks/2) rocks
            while True:
                vert_hall_index = random.randrange(0, len(RockFactory.VERT_HALLWAY))
                vert_hall = RockFactory.VERT_HALLWAY[vert_hall_index]
                num_rocks_per_vert[vert_hall_index] += 1
                if (num_rocks_per_vert[vert_hall_index] <= int(num_rocks / 2) or
                    num_rocks_per_vert[vert_hall_index] <= 1):
                    break
            # Randomize x in the chosen vertical hallway
            while True:
                random_x = random.randint(0, 108)
                if vert_hall[0] <= random_x <= vert_hall[1] - random_size:
                    break

            # Choose a horizontal hallway to be in, but making sure
            # not choosing the same horizontal hallway too many times
            # A horizontal hallway should only have (num_rocks/2) rocks
            while True:
                hori_hall_index = random.randrange(0, len(RockFactory.HORI_HALLWAY))
                hori_hall = RockFactory.HORI_HALLWAY[hori_hall_index]
                num_rocks_per_hori[hori_hall_index] += 1
                if (num_rocks_per_hori[hori_hall_index] <= int(num_rocks / 2) or
                    num_rocks_per_hori[hori_hall_index] <= 1):
                    break
            # Randomize x in the chosen vertical hallway
            while True:
                random_y = random.randint(0, 108)
                if hori_hall[0] <= random_y <= hori_hall[1] - random_size:
                    break
            
            # Create a rock
            temp = Rock((random_x, random_y), random_size)
            rocklist.append(temp)
        return rocklist
