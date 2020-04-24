"""
Consists of constants, information and convention pertaining to
how the simulation will be implemented
"""

# General info:
# POSITIONING COORDINATES CONVENTION
# Becase Python and Matlab has Row-major 2-d array indexing,
# the map has BOTTOM-LEFT corner as (0, 0)
# x-axis follows the ↑ direction, y-axis follows the → direction
# A position tuple is a (x, y) tuple

# The directions are therefore as followed:
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIAG_UP_RIGHT = (1, 1)
DIAG_UP_LEFT = (-1, 1)
DIAG_DOWN_RIGHT = (1, -1)
DIAG_DOWN_LEFT = (-1, -1)

# DIRECTION DETERMINATION
# This dictionary's value is the key's direction if rotated clockwise (turn right 90 degree)
# For example: If begin in DOWN direction, turn 90 degree will be LEFT direction
# The dictionary will be used later to calculate position-/direction-related data
CLOCKWISE = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
COUNTER_CLOCKWISE = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}

# BARCODE LIST: 4 barcode types. 1 = Black, 2 = White
BARCODE = [(1, 2, 2, 2)]#, (1, 2, 1, 2), (1, 1, 2, 2), (1, 2, 2, 1)]


# BTMLEFT_INDEX:
# Used to determine bottom left index of objects, given the object's
# (right-of-head, right-of-tail, left-of-tail, left-of-head) position list
# This dictionary shows the index of the bottom left position on the board
# given the robot's direction
# Btmleft position can then be used to draw rectangles, or calculate navigation
# Example: If robot is in UP direction: index = 2 means `left-of-tail` is the bottom left
BTMLEFT_INDEX = {UP: 2, DOWN: 0, LEFT: 3, RIGHT: 1}


# Because Python 2D array is Ox ↓ Oy →
# But matplotlib plane is Ox → Oy ↑
# So think of the backend array 90 degree clockwise version of the matplot
# The coordinate system still works fine
# However, when accessing the 2D array, y-coordinates must always plus +12
# because the matplot Oy is (-12, 120), but 2d Array column is (0, 132)
DISPLACEMENT = 12

# Robot's length
LENGTH = 6
HLENGTH = 3 # Half-length = distance between center and head
WIDTH = 4


# HOME locations: Dont add DISPLACEMENT because these locations do not concern
# the digital board in anyway
HOME = [(6, -6), (102, -6), (6, 114), (102, 114)]

# Quads' starting and ending locations:
QUAD_START = [(12, 7), (59, 7), (49, 101), (97, 101)]
QUAD_END = [(9, 53), (57, 53), (51, 55), (99, 55)]

# Quads' x and y limit
QUAD_Y_LIMIT = [(7, 53), (7, 53), (55, 103), (55, 103)]
QUAD_X_LIMIT = [(7, 53), (55, 103), (7, 53), (55, 103)]

# Quad's starting direction:
QUAD_START_DIRCT = [UP, UP, DOWN, DOWN]

# Number of rocks wanted on field
NUM_ROCKS = 6

# List of x limits for vertical hallways
# Make sure generated rocks only lie in vertical hallways
VERT_HALLWAY = [(7, 9), (48, 54), (54, 57), (96, 102)]

# List of y limits for horizonal hallways
# Make sure not too many rocks concentrated in 1 horizonal hallways
HORI_HALLWAY = [(12, 21), (36, 45), (60, 69), (84, 99)]

# A zone is an intersection between a vertical hallway and a horizontal hallway
# Therefore, there are 16 zones. Zones are used to contain rocks, and
# control that not too many rocks are in 1 zone
def generate_zones():
    """
    Permuatate VERT_HALLWAY and HORI_HALLWAY to generate zones
    """
    # Intialize zones full of zero
    num_vert_hall = len(VERT_HALLWAY)
    num_hori_hall = len(HORI_HALLWAY)
    zones = [[0 for x in range(num_vert_hall)] for x in range(num_hori_hall)]
    for i in range(num_hori_hall):
        for j in range(num_vert_hall):
            zones[i][j] = [VERT_HALLWAY[j], HORI_HALLWAY[i]]
    return zones

ZONES = generate_zones()
