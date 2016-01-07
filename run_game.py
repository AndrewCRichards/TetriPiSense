"""
Wrapper program to call TetriPiSense

Controls (sticking with the Sense Hat joystick-to-keyboard mappings):
    Any joystick key: Start game
    Ctrl-C or Esc: Quit game (remote keyboard or local USB keyboard resp.)

Andrew Richards 2015
--------------------------------------------------------------------------
"""

import sys, pygame, random, sense_hat, math, tetripisense, subprocess, atexit
from pygame.color import Color

sense = sense_hat.SenseHat()

def start_screen_fb_list():
    """Returns images to display at start in Sense Hat framebuffer format"""
    z = (0,0,0); g = (180,180,180); r = (255,0,0)
    pr =     [g, g, g, z, z, z, z, z,
              g, z, z, g, z, z, z, z,
              g, z, z, g, z, g, z, g,
              g, g, g, z, z, g, g, z,
              g, z, z, z, z, g, z, z,
              g, z, z, z, z, g, z, z,
              g, z, z, z, z, g, z, z,
              z, z, z, z, z, z, z, z ]
    ess =    [z, z, z, z, z, z, z, z,
              z, z, z, z, z, z, z, z,
              g, g, z, g, g, z, g, g,
              g, z, z, g, z, z, g, z,
              g, g, z, g, g, z, g, g,
              g, z, z, z, g, z, z, g,
              g, g, z, g, g, z, g, g,
              z, z, z, z, z, z, z, z ]
    button = [z, z, z, z, z, z, z, z,
              z, z, z, g, g, z, z, z,
              z, z, z, g, g, z, z, z,
              z, z, z, g, g, z, z, z,
              z, r, r, g, g, r, r, z,
              r, r, r, r, r, r, r, r,
              z, z, r, r, r, r, z, z,
              z, z, z, z, z, z, z, z]
    return [pr, ess, button]


def startgame_loop():
    sense.clear()
    pygame.init()
    # pygame.display not used, but needed to capture keyboard events
    pygame.display.set_mode((1, 1))
    clock = pygame.time.Clock()
    images = start_screen_fb_list()
    index = 0
    try:
        while True:
            image_list_pointer = (int (index / 10)) % len(images)
            sense.set_pixels(images[image_list_pointer])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        return
                    sense.clear()
                    tetripisense.run_game()
            clock.tick(10)
            index += 1
            if sense.get_accelerometer_raw()['z'] < -0.7:  # Inverted Hat[+Pi]
                sense.show_message("Shutting down...  ")
                subprocess.call("shutdown -h now", shell=True, stdout=open("/dev/null"))
                return
    except KeyboardInterrupt:
        return

def cleanup():
    sense.clear()
    pygame.quit()

if __name__ == '__main__':
    atexit.register(cleanup)
    startgame_loop()
