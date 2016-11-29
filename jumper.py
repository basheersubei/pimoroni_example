#!/usr/bin/env python

import random
import sys
import time

import alsaaudio
import audioop
import unicornhat as unicorn

class Game(object):

    GRAVITY = 0.01
    JUMP_VELOCITY = -0.3
    FRAME_RATE = 60
    # Create list of coordinates to make a big X on screen.
    BIG_X1 = [[i,i] for i in range(8)]
    BIG_X2 = [[i,7-i] for i in range(8)]
    BIG_X = BIG_X1 + BIG_X2

    def __init__(self):

        self.setup_microphone()
        self.reset_game()
        random.seed(0)

    def reset_game(self):
        self.player = Player([1.0, 6.0])
        self.grounds = [Ground([1.0 * x, 7.0]) for x in range(8)]
        self.obstacles = [Obstacle([7.0, 6.0])]
        # How fast the game progresses (independent of the framerate).
        self.tempo = 0.1
        self.score = 0

    def draw(self):
        # Clear all pixels
        unicorn.clear()

        # Draw each obstacle.
        for o in self.obstacles:
            pos = tuple([int(round(p)) for p in o.position])
            unicorn.set_pixel(*(pos + tuple(o.color)))

        # Draw the ground .
        for g in self.grounds:
            pos = tuple([int(round(p)) for p in g.position])
            unicorn.set_pixel(*(pos + tuple(g.color)))
        
        # Draw player.
        if self.player.alive:
            pos = tuple([int(round(p)) for p in self.player.position])
            unicorn.set_pixel(*(pos + tuple(self.player.color)))
            
        unicorn.show()

    def do_physics(self):
        # Move all the obstacles based on the tempo.
        for o in self.obstacles:
            o.position[0] -= self.tempo

        # Gravity effect on player (change velocity).
        self.player.velocity[1] += Game.GRAVITY

        # Update position of player.
        self.player.position[1] += self.player.velocity[1]

        # Check for collision and react accordingly.
        # if collided, reset velocity and position
        if self.player.position[1] >= 6.0:
            self.player.position[1] = 6.0
            self.player.velocity[1] = 0.0

        player_pos = [int(round(x)) for x in self.player.position]
        for o in self.obstacles:
            obs_pos = [int(round(x)) for x in o.position]
            if (player_pos == obs_pos):
                self.game_over()
                self.reset_game()
                return

        # Cleanup obstacles that are out of screen.
        for o in self.obstacles:
            if self.out_of_bounds(o.position):
                self.obstacles.remove(o)

    def run(self):
        # Run for a random amount of time, before spawning another obstacle, then continue.
        while True:
            rand_secs = random.uniform(1, max(5 - (10 * self.tempo), 2))
            self.run_n(Game.FRAME_RATE, rand_secs)
            self.spawn_obstacle()

            self.tempo += 0.01  # Make the game more difficult (faster obstacles as we go)
            self.score += 1

    def run_n(self, frame_rate, num_seconds):
        for x in range(int(round(num_seconds * Game.FRAME_RATE))):
            # check for user input
            self.check_user_input()
            # Update positions and redraw everything
            self.do_physics()
            self.draw()
            time.sleep(1.0 / Game.FRAME_RATE)

    # If mike amplitude is >20000, then make player jump
    def check_user_input(self):
        l,data = self.inp.read()
        if l == 640:
            val = audioop.max(data, 2)
            if val > 20000:
                self.player.jump()

    def out_of_bounds(self, position):
        return position[0] < 0.0 or position[0] > 7.0 or position[1] < 0.0 or position[1] > 7.0

    def spawn_obstacle(self):
        self.obstacles.append(Obstacle([7.0, 6.0]))

    def setup_unicorn(self):
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(0)
        unicorn.brightness(0.5)

    # Taken from http://stackoverflow.com/a/1937058/341505
    def setup_microphone(self):
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device="Device", cardindex=1)
        self.inp.setchannels(1)
        self.inp.setrate(8000)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.inp.setperiodsize(640)

    def game_over(self):
        print("Game over! Your score is: " + str(self.score))
        # Clear all objects first
        self.obstacles = list()
        self.player.alive = False
        self.grounds = list()
        # Now display a flashing X
        x_obstacles = [Obstacle(x) for x in Game.BIG_X]

        for i in range(6):
            if i % 2 == 0:
                self.obstacles = list()
            else:
                self.obstacles = x_obstacles

            self.draw()
            time.sleep(0.5)


class Thing(object):
    def __init__(self, position):
        self.position = position

class Player(Thing):
    def __init__(self, position):
        super(Player, self).__init__(position)
        self.velocity = [0.0, 0.0]
        self.color = [255, 255, 255]
        self.alive = True

    def jump(self):
        if self.position[1] == 6.0:
            self.velocity[1] += Game.JUMP_VELOCITY

class Obstacle(Thing):
    def __init__(self, position):
        super(Obstacle, self).__init__(position)
        self.velocity = [0.0, 0.0]
        self.color = [255, 0, 0]

class Ground(Thing):
    def __init__(self, position):
        super(Ground, self).__init__(position)
        self.velocity = [0.0, 0.0]
        self.color = [0, 255, 0]

if __name__ == '__main__':
    g = Game()
    g.run()
