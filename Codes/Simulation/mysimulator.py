"""
Module for combing backend and frontend, creating some actions
with visual representation, acting as building block for more complex
sequences
"""

import matplotlib.pyplot as plt
from tuplemath import *
from myconstants import *
from myfrontend import InvisibleArtist
from mybackend import Backend


class Simulator:
    """
    Simulator class to combine frontend and backend, creating real-looking
    simulated actions
    """

    def __init__(self, start_pos, correct_barcode):
        """
        Initiate new game with a backend(robot, boxes) and frontend(invisible artist)
        """
        self.frontend = InvisibleArtist(correct_barcode)
        self.backend = Backend(correct_barcode)
        # Just call out a robot instance because robot is used a lot
        self.robot = self.backend.robot
        # Set starting position for robot
        self.robot.set_robot_start(start_pos)
        self.target_code = correct_barcode

    def robot_forward(self, numsteps):
        """
        Make robot step forward with visual representation
        """
        for _ in range(numsteps):
            self.robot.step_forward()
            self.backend.update_digital_board()
            self.frontend.render_surface(self.robot)
            plt.pause(0.00001)

    def robot_backward(self, numsteps):
        """
        Make robot step backward with visual representation
        """
        for _ in range(numsteps):
            self.robot.step_backward()
            self.backend.update_digital_board()
            self.frontend.render_surface(self.robot)
            plt.pause(0.00001)

    def robot_turn_right(self):
        """
        Make robot turn right (clockwise) with visual representation
        """
        self.robot.turn_right_90()
        self.backend.update_digital_board()
        self.frontend.render_surface(self.robot)
        plt.pause(0.05)

    def robot_turn_left(self):
        """
        Make robot turn left (counter-clockwise) with visual representation
        """
        self.robot.turn_left_90()
        self.backend.update_digital_board()
        self.frontend.render_surface(self.robot)
        plt.pause(0.05)

    def robot_become_direction(self, direction_to_become):
        """
        Rotate the robot into a desired direction
        """
        current_direction = self.robot.direction
        if direction_to_become == CLOCKWISE[current_direction]:
            self.robot_turn_right()
        elif direction_to_become == COUNTER_CLOCKWISE[current_direction]:
            self.robot_turn_left()
        elif direction_to_become == rev(current_direction):
            self.robot_turn_left()
            self.robot_turn_left()

    def robot_goto_y(self, yval_to_go):
        """
        Control robot to go to a specific y_value
        """
        current_y = self.robot.center[1]
        if yval_to_go > current_y:
            self.robot_become_direction(UP)
        elif yval_to_go < current_y:
            self.robot_become_direction(DOWN)
        self.robot_forward(abs(yval_to_go - current_y))

    def robot_goto_x(self, xval_to_go):
        """
        Control robot to go to a specific y_value
        """
        current_x = self.robot.center[0]
        if xval_to_go > current_x:
            self.robot_become_direction(RIGHT)
        elif xval_to_go < current_x:
            self.robot_become_direction(LEFT)
        self.robot_forward(abs(xval_to_go - current_x))

    def robot_goto_point(self, point_to_go):
        """
        Navigate robot to specific point
        Only works perfectly in hallway areas
        Don't use if in shelves area"""
        x_togo, y_togo = point_to_go
        self.robot_goto_y(y_togo)
        self.robot_goto_x(x_togo)

    def robot_pick_box(self):
        """
        Make robot pick up box by filling the storage area and remove box
        from the shelf
        To stimulate real environment, the box_to_pick should be at same row as
        robot's storage cooridnates
        """
        direction = self.robot.direction
        x_store, y_store = self.robot.storage
        x_box = x_store
        if direction == UP:
            y_box = y_store + 5 # 12 = DISPLACEMENT diff between Python and matplot
        else:
            y_box = y_store - 5

        # Remove the box from the background
        self.backend.remove_box((x_box, y_box))
        # Update robot's storage area
        self.robot.store_box()
        # Update digital board
        self.backend.update_digital_board()
        # Frontend: Rerender both background and surface
        self.frontend.render_background(self.backend.box_list)
        self.frontend.render_surface(self.robot)
        plt.pause(0.4)

    def scan_full_barcode(self):
        """
        4-step sequence to scan the 4 color-bit of a barcode
        """
        # Start scanning the 4 bits of the bardcode
        full_code = []
        for _ in range(4):
            temp_bit = self.robot.scan_color_bit(self.backend.board)
            if temp_bit > 0:
                full_code.append(temp_bit)
            else:
                print("Code scanning weird")
            self.robot_turn_right()
            self.robot_forward(1)
            self.robot_turn_left()
            plt.pause(0.007)
        # Visual bug: If direction is DOWN (corresponsinding to LEFT scanning direction)
        # must go 1 more step (reason explained in another "Visual Bug" comment above)
        if self.robot.direction == DOWN:
            self.robot_turn_right()
            self.robot_forward(1)
            self.robot_turn_left()
        return full_code

    # More complicated and full-flex sequences of simulation below
    def backtrack_scanning(self):
        """
        Backtrack scanning algorithm when robot has met a box
        """
        scanning_direction = self.get_scanning_direction()
        # After colliding with the box, the robot will step backward 1 step at a time
        # while also turning to check if the box is still there.
        # After some back steps, the box is not detected any more, meaning the robot
        # has reached the leftmost edge of the box.
        # Then it begins scanning in the scanning direction

        # Backward until box is no longer seen
        backward_steps = 0 # steps count to control how long robot has backwarded
        while self.robot.ultrasonic_detection(self.backend.board):
            backward_steps += 1
            self.robot_turn_right()
            self.robot_backward(1)
            self.robot_turn_left()
            plt.pause(0.02)
        print(f"Back steps: {backward_steps}")                
          
        # If it needs to go backward more than 4 steps, there are 2 boxes
        # next to each other: The "adjacent boxes" problem
        # Therefore, activate "forward-tracking scan" sequence
        if backward_steps > 4:
            print("Adjacent boxes found")
            self.robot_turn_right()
            self.robot_forward(10)
            self.robot_turn_left()
            # Forward till no longer see box
            while self.robot.ultrasonic_detection(self.backend.board):
                self.robot_turn_right()
                self.robot_forward(1)
                self.robot_turn_left()
                plt.pause(0.02)
            # When the box is no longer seen, the ultrasonic field is at the box's
            # rightmost edge. Now turn right, preparing to backward to scanning position
            # Visual Bug: If robot is going RIGHT, needs to backward 3 steps for
            # the colorsensor to align with the first barcode bit of box II
            # If robot is going LEFT, needs 4 steps instead
            self.robot_turn_right()
            self.robot_backward(3 if scanning_direction == RIGHT else 4)
        else:
            # If there is one box isolated, there are no concerns
            # When the box is no longer seen, the ultrasonic field is at the box's
            # leftmost edge. Now turn right, preparing to forward to scanning position
            self.robot_turn_right()
            # Visual Bug: If robot is going RIGHT, needs to forward 4 steps for
            # the colorsensor to align with the first barcode bit
            # If robot is going LEFT, only needs 3 steps
            self.robot_forward(4 if scanning_direction == RIGHT else 3)
        self.robot_turn_left()
        plt.pause(0.05)

        full_code = self.scan_full_barcode()
        print(f"Barcode result: {full_code}")
        plt.pause(0.5)
        return full_code

    def search_shelf(self):
        """
        In this sequence, the robot scan a whole shelf line to search the right box,
        turning inside every 4 inches to check for box.
        Go into hallway after finished searching the shelf.
        Invoke this sequence only when robot has been near a shelf,
        facing towards the boxes
        """
        scanning_direction = self.get_scanning_direction()
        x_begin = self.robot.center[0]
        x_end = x_begin + 38 * scanning_direction[0]


        print(f"Scanning seq start with {x_begin}, {x_end}")
        while min(x_begin, x_end) <= self.robot.head[0] <= max(x_begin, x_end):
            # Only continue searching if has not found the right box (storage is empty) 
            if self.robot.storage_empty:
                box_detected = self.robot.ultrasonic_detection(self.backend.board)
                if box_detected:
                    full_code = self.backtrack_scanning()
                    plt.pause(0.007)
                    # If barcode is correct, proceed to get into position to store box
                    if tuple(full_code) == self.target_code:
                        # Go a bit backward to place the robot right in middle of box
                        self.robot_turn_right()
                        self.robot_backward(3)
                        self.robot_turn_left()
                        # Get close to the box
                        self.robot_forward(1)
                        # Pick up the box and move backward
                        self.robot_pick_box()
                        self.robot_backward(1)
                        self.robot_turn_right()
                else:
                    self.robot_turn_right()
                    # Forward 4 inch then turn back in to see if any boxes appear
                    self.robot_forward(4)
                    self.robot_turn_left()
            # If a box is found and picked up already, just go:
            else:
                self.robot_forward(1)
        print(f"Scanning seq ended. Robot currently at {self.robot.center}")

        # Go to hall way
        self.robot_goto_point(add_tuple(tuple((x_end, self.robot.center[1])),
                                        mult_tuple(scanning_direction, 2)))
        print(f"Went into hallway at {self.robot.center}")

    def where_to_go_next(self):
        """
        Find out what is the next location to take
        based on current location
        """
        current_quad = self.robot.quad
        quad_original_direction = QUAD_START_DIRCT[current_quad]
        current_point = self.robot.center
        current_row = current_point[1]
        current_scan_direction = self.get_scanning_direction()
    
        if current_row not in (53, 55): # If not in quad-end positions
            if current_row in (7, 31, 77, 101):
                step_to_take = 22
            elif current_row in (29, 79):
                step_to_take = 2
            # next_direct = rev(curr_quad_direction)

            # Move along the hallway past the shelf width
            next_pt = add_tuple(current_point,
                                mult_tuple(quad_original_direction, step_to_take))
            # From hallway step into position to start searching shelf
            # The next scan direction will be opposite of current scan direction
            next_pt = add_tuple(next_pt,
                                mult_tuple(rev(current_scan_direction), 2))
            next_scan_direction = rev(self.get_scanning_direction())
        else:
            next_quad = current_quad + 1 if current_quad < 3 else current_quad - 3
            next_pt = QUAD_START[next_quad]
            next_scan_direction = CLOCKWISE[QUAD_START_DIRCT[next_quad]]
            print(f"Arriving to quad {next_quad}")
            # print(f"DIRECTION {next_direct}")
        return (next_pt, next_scan_direction)

    def get_scanning_direction(self):
        """
        Get the scanning direction
        """
        if self.robot.center[1] in (7, 31, 55, 79):
            return RIGHT
        else:
            return LEFT

    def escape_home(self):
        """
        Robot departs from home page
        """
        start_pos = self.robot.center
        home_number = HOME.index(start_pos)
        self.robot_forward(13)
        # If starting at A or D, robot turns right into hallway
        # and get to starting point
        if home_number in (0, 3): # If starting at A or D
            self.robot_turn_right()
            self.robot_forward(4)
            self.robot_turn_left()
        # If starting at B or C, robot turns left into hallway
        # and get to starting point
        else:
            self.robot_turn_left()
            self.robot_forward(43)
            self.robot_turn_right()

    def go_home(self, start_pos):
        """
        Go straight to home base after having the box
        """
        self.robot_goto_point(start_pos)
        print("Finished. Box retrieved")

    def search_entire_area(self):
        """
        Combine other sequences into a whole box search sequence on entire field
        """
        game_finished = False
        num_quad_finished = 0
        starting_position = self.robot.center
        while not game_finished:
            # Depart from home
            self.escape_home()
            plt.pause(0.5)

            # Make first search
            self.search_shelf()
            #print(f"Current quad is: {self.robot.quad}")
            # Continuously do subsequenct searches if necessary
            while self.robot.storage_empty and num_quad_finished < 4:
                next_point, next_scan_direction = self.where_to_go_next()
                print(next_point, next_scan_direction)
                # Move into next spot
                self.robot_goto_point(next_point)
                self.robot_become_direction(COUNTER_CLOCKWISE[next_scan_direction])
                
                # Scan a shelf line
                self.search_shelf()
                #print(f"Current quad is: {self.robot.quad}")
                if self.robot.center in QUAD_END:
                    num_quad_finished += 1
                    print(f"Finished quad {self.robot.quad}")

            # If carrying a box, initiate go_home sequence
            if not self.robot.storage_empty:
                self.go_home(starting_position)
                game_finished = True
            else: # Meaning no box found
                print("Searched 4 quads but no boxes found")
                game_finished = True


if __name__ == "__main__":
    target_barcode = BARCODE[1]
    game = Simulator(HOME[1], target_barcode)

    game.frontend.render_background(game.backend.box_list)
    game.frontend.render_surface(game.backend.robot)
    plt.pause(10)

# print("Center", game.backend.robot.center)
# print("Head", game.backend.robot.head)
# print(game.backend.robot.rectangle_coor)
# print(game.backend.robot.storage)
# print(game.backend.robot.ultrasonic)
