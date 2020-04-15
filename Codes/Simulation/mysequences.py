"""
Module for writing action sequence for robot to simulate specific tasks
"""

from tuplemath import *
from myconstants import *
from mysimulation import *
from matplotlib.pyplot import pause


def backtrack_scanning_seq(simulation):
    """
    Backtrack scanning algorithm when robot has met an obstacle (a box)
    """
    # First, deactivate ultrasonic sensor's continuous movement mode
    # After colliding with the box, the robot will step backward 1 step at a time
    # while also turning to check if the box is still there.
    # After some back steps, the box is not detected any more, meaning the robot
    # has reached the leftmost edge of the box.
    # Then it begin scanning in the scanning direction

    # Backward until box is no longer seen
    while simulation.backend.robot.ultrasonic_detection(simulation.backend.board):
        simulation.robot_turn_right()
        simulation.robot_backward(1)
        simulation.robot_turn_left()
        pause(0.5)
    # When the box is no longer seen, the ultrasonic field is at the box's
    # leftmost edge, meaning the colorsensor
    # is 3 inch away from the first barcode bit
    simulation.robot_turn_right()
    simulation.robot_forward(4 if simulation.backend.robot.get_direction() == RIGHT else 3)
    simulation.robot_turn_left()
    pause(0.3)
    full_code = []
    temp_bit = simulation.backend.robot.scan_barcode(simulation.backend.board)
    if temp_bit > 0:
        full_code.append(temp_bit)
    for _ in range(3):
        simulation.robot_turn_right()
        simulation.robot_forward(1)
        simulation.robot_turn_left()
        pause(0.3)
        temp_bit = simulation.backend.robot.scan_barcode(simulation.backend.board)
        if temp_bit > 0:
            full_code.append(temp_bit)
        else:
            print("Code scanning weird")
    # Visual bug?: If direction is DOWN must somehow go 1 more step
    if simulation.backend.robot.get_direction() == DOWN:
        simulation.robot_turn_right()
        simulation.robot_forward(1)
        simulation.robot_turn_left()
    return full_code

def search_shelf_seq(simulation, start_x, stop_x):
    """
    In this sequence, the robot scan a whole shelf line to search the right box,
    turning inside every 1 inch to check for box.
    Invoke this sequence only when robot has been in a critical point,
    facing towards the boxes
    """

    while min(start_x, stop_x) <= simulation.backend.robot.head[0] <= max(start_x, stop_x):
        if simulation.backend.robot.storage_empty:
            box_detected = simulation.backend.robot.ultrasonic_detection(simulation.backend.board)
            if box_detected:
                full_code = backtrack_scanning_seq(simulation)
                pause(0.06)
                # If barcode is correct, proceed to get into position to store box
                if tuple(full_code) == simulation.target_code:
                    # Go a bit backward to place the robot right in middle of box
                    simulation.robot_turn_right()
                    simulation.robot_backward(3)
                    simulation.robot_turn_left()
                    # Get close to the box
                    simulation.robot_forward(1)
                    # Pick up the box and move backward
                    simulation.robot_pick_box()
                    simulation.robot_backward(1)
                    simulation.robot_turn_right()
            else:
                simulation.robot_turn_right()
                # Forward 4 inch then turn back in to see if any boxes appear
                simulation.robot_forward(4)
                simulation.robot_turn_left()
        # If carrying a box already, just go:
        else:
            simulation.robot_forward(1)

def generate_next_point_to_go(simulation, curr_quad_direction):
    """
    Find out what is the next location to take
    based on current location
    """
    quad_num = simulation.backend.robot.get_quad_num()
    quad_original_direction = QUAD_START_DIRCT[quad_num]
    current_point = simulation.backend.robot.center
    current_row = current_point[1]
    curr_quad = simulation.backend.robot.get_quad_num()
    if current_row not in (53, 55):
        if current_row in (7, 31, 77, 101):
            step_to_take = 22
        elif current_row in (29, 79):
            step_to_take = 2
        next_direct = rev(curr_quad_direction)
        next_pt = add_tuple(current_point,
                            mult_tuple(quad_original_direction, step_to_take))
        next_pt = add_tuple(next_pt,
                            mult_tuple(CLOCKWISE[next_direct], 2))
    else:
        next_quad = curr_quad + 1 if curr_quad <= 2 else curr_quad - 3
        next_pt = QUAD_START[next_quad]
        next_direct = QUAD_START_DIRCT[next_quad]
        print(f"Arriving to quad {next_quad}. DIRECTION {next_direct}")
    return (next_pt, next_direct)

def escape_home_seq(simulation):
    """
    In this sequence, Robot departs from homebase as required
    """
    start_pos = simulation.backend.robot.center
    home_number = HOME.index(start_pos)
    simulation.robot_forward(13)
    # If starting at A or D, robot turns right into hallway
    # and get to starting point
    if home_number in (0, 3):
        simulation.robot_turn_right()
        simulation.robot_forward(4)
        simulation.robot_turn_left()
    # If starting at B or C, robot turns left into hallway
    # and get to starting point
    else:
        simulation.robot_turn_left()
        simulation.robot_forward(43)
        simulation.robot_turn_right()

def go_home_seq(simulation):
    """
    Go straight to home base after having the box
    """
    simulation.robot_goto_point(simulation.start_pos)
    simulation.finished = True
    print("Finished. Box retrieved")
