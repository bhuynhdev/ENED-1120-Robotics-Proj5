"""
Module for class Box
"""
class Box:
    """
    Box class
    """
    SIDE = 4

    def __init__(self, box_tuple, barcode):
        """
        Intialize a new square box with side 4"
        """
        self.barcode = barcode
        # Since a box is 4 innch long, it will not have a whole integer center
        # So a box tuple (bottom, left, top, right)
        self.box_tuple = box_tuple
        self.wanted = False

    @property
    def bottomleft(self):
        """
        Get a box's bottom left coordinate for matplotlib to draw rectangle
        """
        return (self.box_tuple[0], self.box_tuple[1])
