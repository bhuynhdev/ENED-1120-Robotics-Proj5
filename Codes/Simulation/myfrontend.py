"""
My module for Invisible Artist class
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from tuplemath import *
from myconstants import *

# Digital reporesentation
# Robot is encoded as 5s, box's edges are encoded as 10s
ROBOT = 15
EDGE = 10

class InvisibleArtist:
    """An invisible hand that draws Robots, Boxes, and Shelves"""

    def __init__(self, target_barcode):
        """
        Intialize a blank canvas to draw on
        """
        self.fig = plt.figure(figsize=(6, 6))
        self.background = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        self.background.set_xlim(0, 132)
        self.background.set_ylim(-12, 120)
        self.background.set_title("Team 271")

        self.surface = self.background.twiny()
        self.surface.set_xticks([])
        self.surface.set_xlim(0, 132)
        self.target_barcode = target_barcode

    def write_IPS(self, robot):
        """
        Write IPS info to background
        """        
        self.surface.text(110, 90, f"{robot.center}")
        # Distance to A
        rA = distance_2points(robot.center, HOME[0])
        self.surface.text(110, 76, f"{rA:.0f}")
        # Distance to C
        rC = distance_2points(robot.center, HOME[2])
        self.surface.text(110, 66, f"{rC:.0f}")
        # Distance to D
        rD = distance_2points(robot.center, HOME[3])
        self.surface.text(110, 56, f"{rD:.0f}")
        # Calculated cooridnates using Blackboard algorithm
        x_calc, y_calc = IPS_coordinates(rA, rC, rD)
        self.surface.text(110, 41, f"({x_calc:.0f}, {y_calc:.0f})")

    
    def clear_IPS(self):
        """
        Clear text from surface
        """
        for text in self.surface.texts:
            text.remove()

    def create_robot_body(self, robot):
        """
        Generate patches for robot's main body
        """
        body_patches = []
        # Draw vertical rectangle if robot is in vertical direction
        direction = robot.direction
        bottomleft_body = robot.bottomleft
        if direction in (UP, DOWN):
            bottomleft_body = add_tuple(robot.center, (-int(WIDTH / 2), -HLENGTH))
            rect = patches.Rectangle(
                bottomleft_body, 4, 6, linewidth=1, edgecolor='black', facecolor='orange')
        # Draw horizontal rectangle if robot is in horizontal direction
        else:
            bottomleft_body = add_tuple(robot.center, (-HLENGTH, -int(WIDTH / 2)))
            rect = patches.Rectangle(
                bottomleft_body, 6, 4, linewidth=1, edgecolor='black', facecolor='orange')
        body_patches.append(rect)
        """
        # Draw a smaller blue rectangle to indicate the head
        if direction == UP:
            bottomleft_head = add_tuple(bottomleft_body, (0, 8))
            headrect = patches.Rectangle(
                bottomleft_head, 4, 1, linewidth=1, edgecolor='black', facecolor='blue')
        elif direction == DOWN:
            bottomleft_head = add_tuple(bottomleft_body, (0, 1))
            headrect = patches.Rectangle(
                bottomleft_head, 4, 1, linewidth=1, edgecolor='black', facecolor='blue')
        elif direction == RIGHT:
            bottomleft_head = add_tuple(bottomleft_body, (8, 0))
            headrect = patches.Rectangle(
                bottomleft_head, 1, 4, linewidth=1, edgecolor='black', facecolor='blue')
        elif direction == LEFT:
            bottomleft_head = add_tuple(bottomleft_body, (1, 0))
            headrect = patches.Rectangle(
                bottomleft_head, 1, 4, linewidth=1, edgecolor='black', facecolor='blue')
        body_patches.append(headrect)
        """

        return body_patches

    def create_robot_accessories(self, robot):
        """
        Generate patches for robot's other accessories, including
        ultrasonic field and box (if is being stored)
        """
        direction = robot.direction
        # Create ultrasonic field patches
        ultra_btmleft = (robot.ultrasonic[0] if direction in (RIGHT, DOWN)
                    else robot.ultrasonic[1])
        if direction in (LEFT, RIGHT):
            ultra_field = patches.Rectangle(
                ultra_btmleft, 1, 2, linewidth=1, facecolor='red')
        else:
            ultra_field = patches.Rectangle(
                ultra_btmleft, 2, 1, linewidth=1, facecolor='red')

        # Create stored box patches if robot's storage are is not empty
        if not(robot.storage_empty):
            storage_area = patches.Rectangle(
                robot.storage, 4, 4, edgecolor='black', linewidth=2, facecolor='none')
        else:
            storage_area = patches.Rectangle(
                robot.storage, 4, 4, edgecolor='black', linestyle="--", linewidth=1, facecolor='none')
        
        # Create color sensor patches
        color_sensor = patches.Rectangle(robot.colorsensor, 1, 1, facecolor='blue')
        return [ultra_field, storage_area, color_sensor]

    def draw_robot(self, robot):
        """
        Generate all robot-related patches and draw them all
        """
        robot_patches = []
        robot_patches.extend(self.create_robot_body(robot))
        robot_patches.extend(self.create_robot_accessories(robot))
        robot_patch_collection = PatchCollection(robot_patches, True, zorder=10)
        self.surface.add_collection(robot_patch_collection)

    def clear_robot(self):
        """
        Clear robot's visual patches
        """
        for patch in self.surface.collections:
            patch.remove()

    def draw_many_boxes(self, box_list):
        """
        Draw all boxes's patch (using Patch Collection). Draw boxes with
        target_barcode a bit diffrently
        """
        box_patches = []
        for box in box_list:
            bottomleft = box.bottomleft
            square = patches.Rectangle(
                bottomleft, 4, 4, linewidth=1, facecolor="lightgrey",
                edgecolor="red" if box.barcode == self.target_barcode else "black")
            box_patches.append(square)

        box_patch_collection = PatchCollection(box_patches, True)
        self.background.add_collection(box_patch_collection)

    def draw_shelves(self):
        """
        Hard-coding drawing shelves
        """
        shelf_patches = []
        # Zone A Shelves
        rect = patches.Rectangle(
            (12, 12), 36, 12, linewidth=1, edgecolor='black', facecolor='none')
        shelf_patches.append(rect)
        rect = patches.Rectangle(
            (12, 36), 36, 12, linewidth=1, edgecolor='black', facecolor='none')
        shelf_patches.append(rect)
        # Zone B Shelves
        rect = patches.Rectangle(
            (60, 12), 36, 12, linewidth=1, edgecolor='black', facecolor='none')
        shelf_patches.append(rect)
        rect = patches.Rectangle(
            (60, 36), 36, 12, linewidth=1, edgecolor='black', facecolor='none')
        shelf_patches.append(rect)
        # Zone C Shelves
        rect = patches.Rectangle(
            (12, 60), 36, 12, linewidth=1, edgecolor='black', facecolor='none')
        shelf_patches.append(rect)
        rect = patches.Rectangle(
            (12, 84), 36, 12, linewidth=1, edgecolor='black', facecolor='none')
        shelf_patches.append(rect)
        # Zone D Shelves
        rect = patches.Rectangle(
            (60, 60), 36, 12, linewidth=1, edgecolor='black', facecolor='none')
        shelf_patches.append(rect)
        rect = patches.Rectangle(
            (60, 84), 36, 12, linewidth=1, edgecolor='black', facecolor='none')
        shelf_patches.append(rect)

        shelf_collection = PatchCollection(shelf_patches, True)
        self.background.add_collection(shelf_collection)

    def draw_boundaries(self):
        """
        Hard-coding drawing the area boundaries, excluding A,B,C,D beacon
        """
        all_bound = patches.Rectangle((0, 0), 108, 108,
                                      linewidth=2, edgecolor='green', facecolor='none')
        self.surface.add_patch(all_bound)
        # Quad A imaginary bound
        quad_bound = patches.Rectangle((8, 8), 43, 43, linestyle="--",
                                       linewidth=1, edgecolor='green', facecolor='none')
        self.surface.add_patch(quad_bound)
        # Quad B imaginary bound
        quad_bound = patches.Rectangle((59, 8), 43, 43, linestyle="--",
                                       linewidth=1, edgecolor='green', facecolor='none')
        self.surface.add_patch(quad_bound)
        # Quad C imaginary bound
        quad_bound = patches.Rectangle((8, 59), 43, 43, linestyle="--",
                                       linewidth=1, edgecolor='green', facecolor='none')
        self.surface.add_patch(quad_bound)
        # Quad D imaginary bound
        quad_bound = patches.Rectangle((59, 59), 43, 43, linestyle="--",
                                       linewidth=1, edgecolor='green', facecolor='none')
        self.surface.add_patch(quad_bound)

    def draw_homebases(self):
        """
        Hard-coding drawing the homebases A, B, C, D as circles
        """
        for home_pos in HOME:
            home_circle = patches.Circle(home_pos, 6, facecolor='lavender', edgecolor='violet')
            self.surface.add_patch(home_circle)

    def draw_many_rocks(self, rock_list):
        """
        Draw all the rocks onto background
        """
        rock_patches = []
        for rock in rock_list:
            bottomleft = rock.bottomleft
            square_rock = patches.Rectangle(
                bottomleft, rock.size, rock.size, linewidth=1, facecolor="brown", edgecolor="black")
            rock_patches.append(square_rock)

        rock_patch_collection = PatchCollection(rock_patches, True)
        self.background.add_collection(rock_patch_collection)

    def clear_background(self):
        """
        Empty the background, ready for redraw
        """
        for patch in self.background.patches:
            patch.remove()
        for collection in self.background.collections:
            collection.remove()

    def render_background(self, box_list, rock_list):
        """
        Render the background, including the boxes and the shelves
        """
        self.clear_background()
        self.draw_many_boxes(box_list)
        self.draw_many_rocks(rock_list)
        self.draw_shelves()
        self.draw_boundaries()
        self.draw_homebases()
        self.background.text(110, 110, "IPS info")
        self.background.text(110, 100, "Simulation")
        self.background.text(110, 95, "coordinates")
        self.background.text(110, 80, "Distance to A")
        self.background.text(110, 70, "Distance to C")
        self.background.text(110, 60, "Distance to D")
        self.background.text(110, 50, "Calculated")
        self.background.text(110, 45, "coordinates")

    def render_surface(self, robot):
        """
        Render the surface, including the robot
        """
        self.clear_robot()
        self.draw_robot(robot)
        self.clear_IPS()
        self.write_IPS(robot)