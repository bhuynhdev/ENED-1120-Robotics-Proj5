"""
Module for combing backend and frontend, creating some actions
with visual representation, acting as building block for more complex
sequences
"""

from tuplemath import *
from myconstants import *
import matplotlib.pyplot as plt
from myfrontend import InvisibleArtist
from mybackend import Backend


class Simulation:
    """
    Simulation class to combine frontend and backend, creating real-looking
    simulated actions
    """

    def __init__(self, start_pos, correct_barcode):
        """
        Initiate new game with a robot and an invisible artist
        """
        self.frontend = InvisibleArtist(correct_barcode)
        self.backend = Backend(correct_barcode)
        self.target_code = correct_barcode
        self.finished = False
        self.start_pos = start_pos

    def set_robot_start(self):
        """
        Set the starting position and direction for robot,
        given the game inputted starting position
        """
        self.backend.robot.center = self.start_pos
        if self.start_pos == (6, -6) or self.start_pos == (102, -6):
            start_direction = UP
        else:
            start_direction = DOWN
        self.backend.robot.head = add_tuple(self.backend.robot.center,
                                            mult_tuple(start_direction, 3))
        self.frontend.render_surface(self.backend.robot)

    def robot_forward(self, numsteps):
        """
        Make robot step forward with visual representation
        """
        for _ in range(numsteps):
            self.backend.robot.step_forward()
            self.backend.update_digital_board()
            self.frontend.render_surface(self.backend.robot)
            plt.pause(0.03)

    def robot_backward(self, numsteps):
        """
        Make robot step backward with visual representation
        """
        for _ in range(numsteps):
            self.backend.robot.step_backward()
            self.backend.update_digital_board()
            self.frontend.render_surface(self.backend.robot)
            plt.pause(0.03)

    def robot_turn_right(self):
        """
        Make robot turn right (clockwise) with visual representation
        """
        self.backend.robot.turn_right_90()
        self.backend.update_digital_board()
        self.frontend.render_surface(self.backend.robot)
        plt.pause(0.1)

    def robot_turn_left(self):
        """
        Make robot turn left (counter-clockwise) with visual representation
        """
        self.backend.robot.turn_left_90()
        self.backend.update_digital_board()
        self.frontend.render_surface(self.backend.robot)
        plt.pause(0.1)

    def robot_become_direction(self, direction_to_become):
        """
        Rotate the robot into a desired direction
        """
        current_direction = self.backend.robot.get_direction()
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
        current_y = self.backend.robot.center[1]
        if yval_to_go > current_y:
            self.robot_become_direction(UP)
        elif yval_to_go < current_y:
            self.robot_become_direction(DOWN)
        self.robot_forward(abs(yval_to_go - current_y))

    def robot_goto_x(self, xval_to_go):
        """
        Control robot to go to a specific y_value
        """
        current_x = self.backend.robot.center[0]
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
        direction = self.backend.robot.get_direction()
        x_store, y_store = self.backend.robot.storage
        x_box = x_store
        if direction == UP:
            y_box = y_store + 5 # 12 = DISPLACEMENT diff between Python and matplot
        else:
            y_box = y_store - 5

        # Remove the box from the background
        self.backend.remove_box((x_box, y_box))
        # Update robot's storage area
        self.backend.robot.store_box()
        # Update digital board
        self.backend.update_digital_board()
        # Frontend: Rerender both background and surface
        self.frontend.render_background(self.backend.box_list)
        self.frontend.render_surface(self.backend.robot)
        plt.pause(0.5)

if __name__ == "__main__":
    target_barcode = BARCODE[1]
    game = Simulation(HOME[1], target_barcode)
    game.set_robot_start()

    game.frontend.render_background(game.backend.box_list)
    game.frontend.render_surface(game.backend.robot)
    plt.pause(5)

# print("Center", game.backend.robot.center)
# print("Head", game.backend.robot.head)
# print(game.backend.robot.get_rectangle_coor())
# print(game.backend.robot.storage)
# print(game.backend.robot.ultrasonic)