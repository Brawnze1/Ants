#!/usr/bin/env python
from random import shuffle
from ants import *
from Movement import Movement
from random import randrange

class StarterBot():
    def __init__(self):
        self.hills = []
        self.unseen = []
        self.Movement = Movement()


    def do_setup(self, ants):
        self.hills = []

        self.unseen = []
        for row in range(ants.rows):
            for col in range(ants.cols):
                self.unseen.append((row, col))


    def do_turn(self, ants):
        self.Movement.reset()

        # prevent stepping on own hill
        for hill_loc in ants.my_hills():
            self.Movement.orders[hill_loc] = None

        # find close food
        ant_dist = []
        for food_loc in ants.food():
            for ant_loc in ants.my_ants():
                dist = ants.distance(ant_loc[0], ant_loc[1], food_loc[0], food_loc[1])
                ant_dist.append((dist, ant_loc, food_loc))
        ant_dist.sort()
        for dist, ant_loc, food_loc in ant_dist:
            if food_loc not in self.Movement.targets and ant_loc not in self.Movement.targets.values():
                self.Movement.do_move_location(ant_loc, food_loc, ants)

        # attack hills
        for hill_loc, hill_owner in ants.enemy_hills():
            if hill_loc not in self.hills:
                self.hills.append(hill_loc)        
        ant_dist = []
        for hill_loc in self.hills:
            for ant_loc in ants.my_ants():
                if ant_loc not in self.Movement.orders.values():
                    dist = ants.distance(ant_loc[0], ant_loc[1], hill_loc[0], hill_loc[1])
                    ant_dist.append((dist, ant_loc, hill_loc))
        ant_dist.sort()
        for dist, ant_loc, hill_loc in ant_dist:
            self.Movement.do_move_location(ant_loc, hill_loc, ants)

        # explore unseen areas
        for loc in self.unseen[:]:
            if ants.visible(loc):
                self.unseen.remove(loc)
        for ant_loc in ants.my_ants():
            if ant_loc not in self.Movement.orders.values():
                unseen_dist = []
                for unseen_loc in self.unseen:
                    dist = ants.distance(ant_loc[0], ant_loc[1], unseen_loc[0], unseen_loc[1])
                    unseen_dist.append((dist, unseen_loc))
                unseen_dist.sort()
                for dist, unseen_loc in unseen_dist:
                    if self.Movement.do_move_location(ant_loc, unseen_loc, ants):
                        break

        # unblock own hill
        for hill_loc in ants.my_hills():
            if hill_loc in ants.my_ants() and hill_loc not in self.Movement.orders.values():
                for direction in ('s','e','w','n'):
                    if self.Movement.do_move_direction(hill_loc, direction, ants):
                        break

                         
        # default move
        for ant_loc in ants.my_ants():
            directions = ['n','e','s','w']
            random.shuffle(directions)
            for direction in directions:
                if self.Movement.do_move_direction(ant_loc, direction, ants):
                    break

if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    try:
        Ants.run(StarterBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
