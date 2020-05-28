"""
Simple tuple arithmetic including adding, subtraction, mutiplication, and reverse
for working with robot's directions and navigation
"""

from myconstants import HOME


def add_tuple(tuple1, tuple2):
    """
    Tuple arithmetic addition. Example: (1,0) + (2,3) = (3,3)
    """
    return tuple(x + y for x, y in zip(tuple1, tuple2))


def sub_tuple(tuple1, tuple2):
    """
    Tuple arithmetic subtraction
    """
    return tuple(x - y for x, y in zip(tuple1, tuple2))


def mult_tuple(tuple1, multiplier):
    """
    Tuple arithmetic: Multiple all members with an integer
    """
    return tuple(x * multiplier for x in tuple1)


def rev(tuple1):
    """
    Reverse direction
    """
    return mult_tuple(tuple1, -1)


def distance_2points(point1, point2):
    """
    Calculate distance betwwen two points
    """
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def IPS_coordinates(rA, rC, rD):
    x1, y1 = HOME[0]
    x2, y2 = HOME[2]
    x3, y3 = HOME[3]

    x = ((-(y2 - y3)*((y2**2 - y1**2) +
            (x2**2 - x1**2)+(rA**2 - rC**2)) +
            (y1 - y2) * ((y3**2 - y2**2)+(x3**2 - x2**2) +
            (rC**2 - rD**2))) /
        (2 * ((x1 - x2) * (y2 - y3) - (x2 - x3) * (y1 - y2))))
    y = (-(x2 - x3)*((x2**2 - x1**2) + (y2**2 - y1**2) + (rA**2 - rC**2))+((x1-x2) *
                                                                           ((x3**2-x2**2)+(y3**2-y2**2)+(rC**2-rD**2))))/(2*((y1-y2)*(x2-x3) - (y2-y3)*(x1-x2)))
    return (x, y)