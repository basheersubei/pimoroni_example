#!/usr/bin/env python

import sys
import time

import unicornhat as unicorn

class Game(object):

    GRAVITY = -0.1

    def __init__(self):

        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(0)
        unicorn.brightness(0.5)
        self.width, self.height = unicorn.get_shape()

        self.player = Player([4.0, 4.0])
        self.obstacles = [Obstacle([1.0 * x, 0.0]) for x in range(8)]

    def draw(self):

        # Clear all pixels
        unicorn.clear()

        for o in self.obstacles:
            # Draw each obstacle.
            pos = tuple([int(round(p)) for p in o.position])
            unicorn.set_pixel(*(pos + tuple(o.color)))
        
        # Draw player.
        pos = tuple([int(round(p)) for p in self.player.position])
        unicorn.set_pixel(*(pos + tuple(self.player.color)))
            
        unicorn.show()

    def do_physics(self):
        # Gravity effect on player (change velocity).
        self.player.velocity[1] += Game.GRAVITY

        # Update position of player.
        self.player.position[1] += self.player.velocity[1]

        # Check for collision and react accordingly.
        # if collided, reset velocity and position
        if self.player.position[1] <= 1.0:
            self.player.position[1] = 1.0

    def run(self):
        #for x in range(width):
            #unicorn.set_pixel(x,0,255,255,255)
            #unicorn.show()
            #time.sleep(0.5)


        while True:
            self.draw()
            self.do_physics()
            time.sleep(0.5)


        time.sleep(3)
        return 0


    def print_intsructions():
        print("""oh hai TODO """) 


class Thing(object):
    def __init__(self, position):
        self.position = position

class Player(Thing):
    def __init__(self, position):
        super(Player, self).__init__(position)
        self.velocity = [0.0, 0.0]
        self.color = [255, 255, 255]

class Obstacle(Thing):
    def __init__(self, position):
        super(Obstacle, self).__init__(position)
        self.velocity = [0.0, 0.0]
        self.color = [255, 0, 0]


if __name__ == '__main__':
    g = Game()
    sys.exit(g.run())
