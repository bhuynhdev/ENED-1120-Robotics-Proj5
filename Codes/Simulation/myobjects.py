"""
A module containig objecte necessary for simulation: Robot and Box
"""

from tuplemath import *
from myconstants import *


class Robot:
    """Robot class"""

    def __init__(self):
        """
        Intialize new robot with a head, a center, an ultrasonic vision field,
        and a storage area for the box
        Default starting center is (0,0), direction UP
        """
        # A robot has a center and a head
        # Center indicates its position on board, and Head incates direction
        # Center and Head is always same row or same column
        # Robot's main length is 2x the length from head to center (2x3 = 6)
        self.center = (0,0)
        self.head = add_tuple(self.center, mult_tuple(UP, 3))

        # Ultrasonic field represents the ultrasonic sensor's vision
        # This vision is represented as the bottomleft point of a 2x2 field in front of head
        self.ultrasonic = self.generate_ultrasonic()

        # Storage field represent the storage are for the box
        # The storage are is also representated by a box tuple (like a box)
        # If the box is pickedup, the box's tuple will be the storage area's tuple
        self.storage = self.generate_storage()
        self.storage_empty = True
        # The color sensor is representated by a 1x1 field at the left-of-head
        self.colorsensor = self.generate_colorsensor()

    def get_direction(self):
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

    def get_rectangle_coor(self):
        """
        Derive the coordinates of 4 rectangle corners using center and head
        """
        # `Move` the head in a clockwise manner, we will have 4 coordinates sequentially:
        # (right-of-head, right-of-tail, left-of-tail, left-of-head)
        current_direction = self.get_direction()
        # First go clockwise 2 inch (robot's half width because the head aligns with the center)
        # from the head to get right-of-head
        # Second go clockwise 6 inch (robot's body length) to get right-of-tail
        # Third, go clockwise 4 inch (robot's width) to get left-of-tail
        # Fourth, go clockwise 6 inch (robot's body length) to get left-of-head
        displacement = (2, 6, 4, 6)
        robot_corners = []
        corner_coor = self.head
        for d in displacement:
            next_clockwise_direction = CLOCKWISE[current_direction]
            corner_coor = add_tuple(
                corner_coor, mult_tuple(next_clockwise_direction, d))
            robot_corners.append(corner_coor)
            current_direction = next_clockwise_direction
        return robot_corners

    def get_whole_rectangle_coor(self):
        """
        Get the rectangle coordinates of the entire robot, including the main body
        and the storage area in front (excluding the ultrasonic vision)
        """
        # Get rectangle coor (right-head, right-tail, left-tail, left-head)
        rectangle = self.get_rectangle_coor()
        direction = self.get_direction()
        # Extend right of head to include right of storage area
        rectangle[0] = add_tuple(rectangle[0], mult_tuple(direction, 4))
        # Extend left of head to include right of storage area
        rectangle[3] = add_tuple(rectangle[3], mult_tuple(direction, 4))
        # Return the modifed rectangle coor list
        return rectangle

    def get_bottomleft(self):
        """
        Return bottom left coordinate of robot
        """
        rectangle_coor = self.get_rectangle_coor()
        direction = self.get_direction()
        bottomleft_index = BTMLEFT_INDEX[direction]
        return rectangle_coor[bottomleft_index]

    def generate_ultrasonic(self):
        """
        Generate representation of robot's ultrasonic vision, which includes
        a 1x2 rectangular field in front of storage area (1 inch in front of head)
        Returns the bottom left coordinate of this field
        """
        rectangle_coor = self.get_rectangle_coor()
        direction = self.get_direction()
        right_of_head = rectangle_coor[0]
        right_of_ultra_bottom = add_tuple(
            right_of_head, COUNTER_CLOCKWISE[direction])
        left_of_head = rectangle_coor[3]
        left_of_ultra_bottom = add_tuple(
            left_of_head, CLOCKWISE[direction])

        right_of_ultra_top = add_tuple(
            right_of_ultra_bottom, mult_tuple(direction, 2))
        left_of_ultra_top = add_tuple(
            left_of_ultra_bottom, mult_tuple(direction, 2))

        ultra_coor = list((right_of_ultra_top, left_of_ultra_top))
        return ultra_coor

    def generate_colorsensor(self):
        """
        Generate color sensor coordinates
        """
        # Colorsensor is a point at the left-of-head
        direction = self.get_direction()
        bottomleft_body = self.get_bottomleft()
        if direction == UP:
            return add_tuple(bottomleft_body, (0, 6))
        elif direction == DOWN:
            return add_tuple(bottomleft_body, (3, -1))
        elif direction == RIGHT:
            return add_tuple(bottomleft_body, (6, 3))
        else:
            return add_tuple(bottomleft_body, (-1, 0))

    def generate_storage(self):
        """
        Return the bottom left coordinate of the robot's storage area, which
        is a 4x4 field not exceeding of the head
        """
        direction = self.get_direction()
        bottomleft_body = self.get_bottomleft()
        if direction == UP:
            return add_tuple(bottomleft_body, (0, 2))
        elif direction == DOWN:
            return add_tuple(bottomleft_body, (0, 0))
        elif direction == RIGHT:
            return add_tuple(bottomleft_body, (2, 0))
        else:
            return add_tuple(bottomleft_body, (0, 0))

    def get_quad_num(self):
        """
        Determine quad number from coordinates:
        """
        x, y = self.head
        if 8 <= x <= 53:
            if 8 <= y <= 53:
                return 0  # means quad A
            if 55 <= y <= 102:
                return 2  # 2 means quad C
        elif 55 <= x <= 102:
            if 8 <= y <= 53:
                return 1  # means quad B
            if 55 <= y <= 102:
                return 3  # 2 means quad D
        return -1  # return -1 otherwise (neutral hallway)

    def step_forward(self):
        """
        Make robot step forward 1 step toward current direcion
        """
        direction = self.get_direction()
        self.center = add_tuple(self.center, direction)
        self.head = add_tuple(self.head, direction)
        self.storage = self.generate_storage()
        self.colorsensor = self.generate_colorsensor()
        self.ultrasonic = self.generate_ultrasonic()

    def step_backward(self):
        """
        Make robot step backward 1 step against current direcion
        """
        # Backward direction = current_direction * (-1)
        direction = rev(self.get_direction())
        self.center = add_tuple(self.center, direction)
        self.head = add_tuple(self.head, direction)
        self.storage = self.generate_storage()
        self.colorsensor = self.generate_colorsensor()
        self.ultrasonic = self.generate_ultrasonic()

    def turn_right_90(self):
        """
        Make robot turn right 90 degree (or clockwise)
        """
        current_direction = self.get_direction()
        next_direction = CLOCKWISE[current_direction]
        self.head = add_tuple(self.center, mult_tuple(next_direction, 3))
        self.storage = self.generate_storage()
        self.ultrasonic = self.generate_ultrasonic()
        self.colorsensor = self.generate_colorsensor()

    def turn_left_90(self):
        """
        Make robot turn left 90 degree (or counter-clockwise)
        """
        current_direction = self.get_direction()
        next_direction = COUNTER_CLOCKWISE[current_direction]
        self.head = add_tuple(self.center, mult_tuple(next_direction, 3))
        self.storage = self.generate_storage()
        self.ultrasonic = self.generate_ultrasonic()
        self.colorsensor = self.generate_colorsensor()

    def ultrasonic_detection(self, field):
        """
        Detect if there is anything on the `field` that is within the robot's
        ultrasonic vision
        """
        for point in self.ultrasonic:
            x, y = point
            if field[x][y + 12] > 0:  # Emtpy spaces will be encoded as 0 in the field
                print(f"{x},{y} detected {field[x][y+12]}")
                return True
        return False

    def scan_barcode(self, field):
        """
        The color sensor can only scan one quare at a time
        Therefore, the 1/4th barcode returned will the of the same x-coor as the color sensor
        """
        direction = self.get_direction()
        x_color, y_color = self.colorsensor
        x_to_scan = x_color
        for i in range(1, 8, 1):  # Shoot a color beam of length 7 to detect barcode color (if any)
            if direction == UP:
                y_to_scan = y_color + i + 12  # 12 = DISPLACEMENT diff between Python and matplot
            else:
                y_to_scan = y_color - i + 12
            if 0 < field[x_to_scan][y_to_scan] < 10:
                return field[x_to_scan][y_to_scan]
        return -1  # Meaning no barcode detected

    def store_box(self):
        """
        Simulating storing a box
        """
        self.storage_empty = False


class Box:
    """
    Box class
    """

    def __init__(self, box_tuple, barcode):
        """
        Intialize a new square box with side 4"
        """
        self.side = 4
        self.barcode = barcode
        # Since a box is 4 innch long, it will not have a whole integer center
        # So a box tuple (bottom, left, top, right)
        self.box_tuple = box_tuple
        self.wanted = False

    def get_bottomleft(self):
        """
        Get a box's bottom left coordinate for matplotlib to draw rectangle
        """
        return (self.box_tuple[0], self.box_tuple[1])
