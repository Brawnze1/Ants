#!/usr/bin/env python
from random import shuffle
from ants import *
from random import randrange

class Movement():
    def __init__(self):
        self.orders = {}
        self.targets = {}


    # track all moves, prevent collisions
    def do_move_direction(self, loc, direction, ants):
        new_loc = ants.destination(loc[0], loc[1], direction)
        if (ants.unoccupied(new_loc[0], new_loc[1]) and new_loc not in self.orders):
            ants.issue_order((loc[0], loc[1], direction))
            self.orders[new_loc] = loc
            return True
        else:
            return False


    #Move to specific location
    def do_move_location(self, loc, dest, ants):
        directions = ants.direction(loc[0], loc[1], dest[0], dest[1])
        for direction in directions:
            if self.do_move_direction(loc, direction, ants):
                self.targets[dest] = loc
                return True
        return False


    def reset(self):
        self.orders = {}
        self.targets = {}