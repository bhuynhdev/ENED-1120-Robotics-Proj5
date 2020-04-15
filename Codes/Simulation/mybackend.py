"""
My module for backend-related logics, including
robot's movement logic, data scanning, ultrasonic detection, box generation, etc.
"""

import random
from tuplemath import add_tuple, sub_tuple, mult_tuple, rev
from myconstants import *
from myobjects import Robot, Box


# Digital respresentation
ROBOT = 15
EDGE = 10


class Backend:
    """
    Backend class to deal with data accessing and processing for robot
    Representated as a 2D array of data points
    """

    def __init__(self, target_barcode):
        self.row = 108      # Row corresponds to matplot x-axis
        self.col = 132      # Col cooresoinds to matplot y-axis
        self.board = self.create_empty_board()
        self.box_list = self.generate_all_boxes(target_barcode)
        self.robot = Robot()
        self.digitalize_boxes()
        self.update_digital_board()

    def create_empty_board(self):
        """
        Create 2D array filled with 0 based on row and column numbers
        """
        board = [[0 for _ in range(self.col + 1)] for _ in range(self.row + 1)]
        return board

    def generate_all_boxes(self, target_barcode):
        """
        Randomize and return the box tuple coordinates of all 32 boxes
        """
        # Project 5 specifies that boxes's bottomlefts
        # can only be in rows (12, 20, 36, 44, 60, 68, 84, 92)
        # 4 boxes on each row, divided into 2 regions: A-C (col 12-48) and B-D(col 60-96)
        # In each sub-region, on each row, there are 2 boxes
        # These 2-boxes-pair's positions on a particular row is random,
        # as long as they don't overlap each other

        all_boxes = []
        for y in (12, 20, 36, 44, 60, 68, 84, 92):
            # Generate two boxes until their bottomlefts are 4in apart (each box is 4in wide)
            # Region A-C: column 12-44
            # Region B-D: column 60-92
            for region_range in [(12, 44), (60, 92)]:
                while True:
                    x1, x2 = (random.randrange(*region_range, 1)
                              for _ in range(2))
                    if abs(x1 - x2) >= 8:
                        break

                box_temp1 = Box((x1, y, x1 + 4, y + 4), random.choice(BARCODE))
                box_temp2 = Box((x2, y, x2 + 4, y + 4), random.choice(BARCODE))
                if box_temp1.barcode == target_barcode:
                    box_temp1.wanted = True
                if box_temp2.barcode == target_barcode:
                    box_temp2.wanted = True
                all_boxes.append(box_temp1)
                all_boxes.append(box_temp2)
        return all_boxes

    def remove_box(self, btmleft_of_box_to_remove):
        """
        Remove the box from the box_list, and consequently, frontend
        when the box is picked up
        """
        for index, box in enumerate(self.box_list):
            if box.get_bottomleft() == btmleft_of_box_to_remove:
                del self.box_list[index]
                print(f"A box at {box.get_bottomleft()} deleted")
                break
            if add_tuple(box.get_bottomleft(), (1, 0)) == btmleft_of_box_to_remove:
                del self.box_list[index]
                print(
                    f"A box at {add_tuple(box.get_bottomleft(), (1, 0))} deleted")
                break
            if add_tuple(box.get_bottomleft(), (-1, 0)) == btmleft_of_box_to_remove:
                del self.box_list[index]
                print(
                    f"A box at {add_tuple(box.get_bottomleft(), (-1, 0))} deleted")
                break

    def digitalize_boxes(self):
        """
        Assigning 10s indicicating box edge onto the 2D array
        """
        for box in self.box_list:
            bottomleft = box.get_bottomleft()
            if bottomleft[1] in (12, 36, 60, 84):
                x, y = bottomleft[0], bottomleft[1] + DISPLACEMENT
                # Assign the box's edge with 10s
                for i in range(4):
                    self.board[x + i][y] = EDGE
                # Assigning the barcode onto the box
                for i in range(4):
                    self.board[x + i][y + 1] = box.barcode[i]

            elif bottomleft[1] in (20, 44, 68, 92):
                x, y = bottomleft[0] + 4, bottomleft[1] + 4 + DISPLACEMENT
                # Assign the box's edge with 10s
                for i in range(4):
                    self.board[x - i][y] = EDGE
                # Assigning the barcode onto the box
                for i in range(4):
                    self.board[x - i][y - 1] = box.barcode[i]

    def digitalize_robot(self):
        """
        Assign 5s indicating the robot onto the 2d Array
        """
        # whole_rectangle = self.robot.get_whole_rectangle_coor()
        btmleft = self.robot.get_bottomleft()
        direction = self.robot.get_direction()
        x_val, y_val = btmleft[0], btmleft[1] + DISPLACEMENT
        if direction in (UP, DOWN):
            for x in range(x_val, x_val + 4, 1):
                for y in range(y_val, y_val + 6, 1):
                    self.board[x][y] = ROBOT
        elif direction in (LEFT, RIGHT):
            for x in range(x_val, x_val + 6, 1):
                for y in range(y_val, y_val + 4, 1):
                    self.board[x][y] = ROBOT

    def update_digital_board(self):
        """
        Update the digital board if any changes happen to the robot,
        or the boxes
        """
        # Refresh the board
        self.board = self.create_empty_board()
        # Update boxes
        self.digitalize_boxes()
        # Update the robot (since it is always in continuous movement)
        self.digitalize_robot()
