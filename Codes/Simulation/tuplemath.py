"""
Simple tuple arithmetic including adding, subtraction, mutiplication, and reverse
for working with robot's directions and navigation
"""

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