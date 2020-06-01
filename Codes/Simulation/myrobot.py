"""
A module containing Robot
"""

from tuplemath import *
from myconstants import *


class Robot:
    """Robot class"""
    # Half-Length = length from center to head
    HLENGTH = 3 # Half length
    LENGTH = 2 * HLENGTH
    # Width is full width, 4 inch from left side to right side
    WIDTH = 4

    def __init__(self):
        """
        Intialize new robot with a head, a center, an ultrasonic vision field,
        a color sensor, and a storage area for the box
        Default starting center is (0,0), direction UP

        Also has attributes: head, storage, colorsensor, ultrasonic
        implemented through @propery decorator
        """
        # A robot has a center and a head
        # Center indicates its position on board, and Head incates direction
        # Center and Head is always same row or same column
        # Head = Center + Direction * Half-Length
        self.center = (0, 0)
        self.head = add_tuple(self.center, mult_tuple(UP, HLENGTH))

        # If the box is picked, the storage_empty will become False
        self.storage_empty = True


    @property # Property decorator to turn into class attribute
    def direction(self):
        """
        Deduct the robot's current direction based on relationship
        between center's and head's coordinates
        """
        # Calculate self.head[row] - self.center[row] and self.head[col] - self.center[col]
        subtracted = sub_tuple(self.head, self.center)
        x_diff, y_diff = subtracted
        # If y_diff = 0, meaning Robot is on horizontal direction
        if y_diff == 0:
            return RIGHT if (x_diff > 0) else LEFT
        # If x_diff = 0, meaning Robot is on vertical direction
        if x_diff == 0:
            return UP if (y_diff > 0) else DOWN

    @property
    def rectangle_coor(self):
        """
        Derive the coordinates of 4 rectangle corners using center and head
        """
        # `Move` the head in a clockwise manner, we will have 4 coordinates sequentially:
        # (right-of-head, right-of-tail, left-of-tail, left-of-head)
        current_direction = self.direction
        # First go clockwise WIDTH/2 inch from the head to get right-of-head
        # Second go clockwise LENGTH inch (robot's body length) to get right-of-tail
        # Third, go clockwise WIDTH inch (robot's width) to get left-of-tail
        # Fourth, go clockwise LENGTH inch (robot's body length) to get left-of-head
        displacement = (int(WIDTH / 2), LENGTH, WIDTH, LENGTH)
        robot_corners = []
        corner_coor = self.head
        for d in displacement:
            next_clockwise_direction = CLOCKWISE[current_direction]
            corner_coor = add_tuple(
                corner_coor, mult_tuple(next_clockwise_direction, d))
            robot_corners.append(corner_coor)
            current_direction = next_clockwise_direction
        return robot_corners

    @property
    def bottomleft(self):
        """
        Return bottom left coordinate of robot
        """
        rectangle_coor = self.rectangle_coor
        direction = self.direction
        bottomleft_index = BTMLEFT_INDEX[direction]
        return rectangle_coor[bottomleft_index]

    @property
    def ultrasonic(self):
        """
        Generate representation of robot's ultrasonic vision, which includes
        a 1x2 rectangular field in front of storage area (1 inch in front of head)
        (Actually will create a 2x2 field but will only draw the top part)
        Returns the bottom left coordinate of this field
        """
        rectangle_coor = self.rectangle_coor
        direction = self.direction
        right_of_head = rectangle_coor[0]
        right_of_ultra_bottom = add_tuple(
            right_of_head, COUNTER_CLOCKWISE[direction])
        left_of_head = rectangle_coor[3]
        left_of_ultra_bottom = add_tuple(
            left_of_head, CLOCKWISE[direction])

        # 2 is a hard-coded value since ultrasonic is 2 inch away from the ultra_bottom
        right_of_ultra_top = add_tuple(
            right_of_ultra_bottom, mult_tuple(direction, 2))
        left_of_ultra_top = add_tuple(
            left_of_ultra_bottom, mult_tuple(direction, 2))

        ultra_coor = list((right_of_ultra_top, left_of_ultra_top))
        return ultra_coor

    @property
    def colorsensor(self):
        """
        Generate color sensor coordinates
        Color sensor is depicted by 1 point at the left-of-head position
        """
        # Colorsensor is a point at the left-of-head
        direction = self.direction
        bottomleft_body = self.bottomleft
        if direction == UP:
            return add_tuple(bottomleft_body, (0, LENGTH))
        if direction == DOWN:
            # the second -1 is a hard-coded value since color sensor is of width/height 1
            return add_tuple(bottomleft_body, (WIDTH - 1, -1))
        if direction == RIGHT:
            return add_tuple(bottomleft_body, (LENGTH, WIDTH - 1))
        if direction == LEFT:
            # the -1 is a hard-coded value since color sensor is of width/height 1
            return add_tuple(bottomleft_body, (-1, 0))

    @property
    def storage(self):
        """
        Return the bottom left coordinate of the robot's storage area, which
        is a 4x4 field not exceeding of the head
        """
        direction = self.direction
        bottomleft_body = self.bottomleft
        # The 2s below are hard-coded values
        if direction == UP:
            return add_tuple(bottomleft_body, (0, 2))
        elif direction == DOWN:
            return add_tuple(bottomleft_body, (0, 0))
        elif direction == RIGHT:
            return add_tuple(bottomleft_body, (2, 0))
        else:
            return add_tuple(bottomleft_body, (0, 0))

    @property
    def quad(self):
        """
        Determine quad number from coordinates:
        """
        x_robot, y_robot = self.center
        # print("Getting quad num", end=". ")
        # print(f"Center: {self.center}", end=". ")
        for quad in range(4):
            x_limit = QUAD_X_LIMIT[quad]
            y_limit = QUAD_Y_LIMIT[quad]
            if x_limit[0] <= x_robot <= x_limit[1] and y_limit[0] <= y_robot <= y_limit[1]:
                print(f"Quad {quad}")
                return quad
        print("Quad 4")
        return 4  # return 4 otherwise (neutral hallway)

    def get_dodging_direction(self):
        """
        Return the dodging direction when meeting a rock
        """
        current_col = self.center[0]
        if (6 <= current_col <= 15 or 54 <= current_col <= 65):
            return LEFT
        else:
            return RIGHT


    def step_forward(self):
        """
        Make robot step forward 1 step toward current direcion
        """
        current_direction = self.direction
        self.center = add_tuple(self.center, current_direction)
        self.head = add_tuple(self.head, current_direction)

    def step_backward(self):
        """
        Make robot step backward 1 step against current direcion
        """
        # Backward direction = current_direction * (-1)
        reversed_direction = rev(self.direction)
        self.center = add_tuple(self.center, reversed_direction)
        self.head = add_tuple(self.head, reversed_direction)

    def turn_right_90(self):
        """
        Make robot turn right 90 degree (or clockwise)
        """
        current_direction = self.direction
        next_direction = CLOCKWISE[current_direction]
        self.head = add_tuple(self.center, mult_tuple(next_direction, HLENGTH))

    def turn_left_90(self):
        """
        Make robot turn left 90 degree (or counter-clockwise)
        """
        current_direction = self.direction
        next_direction = COUNTER_CLOCKWISE[current_direction]
        self.head = add_tuple(self.center, mult_tuple(next_direction, HLENGTH))

    def ultrasonic_detection(self, field):
        """
        Detect if there is anything on the `field` that is within the robot's
        ultrasonic vision
        """
        for point in self.ultrasonic:
            x, y = point
            if field[x][y + DISPLACEMENT] > 0:  # Emtpy spaces will be encoded as 0 in the field
                print(f"{x},{y} detected {field[x][y + DISPLACEMENT]}")
                return True
        return False

    def scan_color_bit(self, field):
        """
        The color sensor can only scan one quare at a time
        Therefore, the 1/4th barcode returned will the of the same x-coor as the color sensor
        """
        direction = self.direction
        x_color, y_color = self.colorsensor
        x_to_scan = x_color
        for i in range(1, 8, 1):  # Shoot a color beam of length 7 to detect barcode color (if any)
            if direction == UP:
                y_to_scan = y_color + i + DISPLACEMENT # DISPLACEMENT = 12: diff between Python and matplot
            else:
                y_to_scan = y_color - i + DISPLACEMENT
            if 0 < field[x_to_scan][y_to_scan] < 10:
                return field[x_to_scan][y_to_scan]
        return -1  # Meaning no barcode detected

    def store_box(self):
        """
        Simulating storing a box
        """
        self.storage_empty = False

    def set_robot_start(self, start_pos):
        """
        Set the starting position and direction for robot,
        given the game inputted starting position
        """
        self.center = start_pos
        if start_pos == (6, -6) or start_pos == (102, -6):
            start_direction = UP
        else:
            start_direction = DOWN
        self.head = add_tuple(self.center, mult_tuple(start_direction, HLENGTH))
