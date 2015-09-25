"""
Tetris-like game with LEDs for the SenseHat / UnicornHat / AstroPi!

Adapted from Stephen Blythe's Tetris clone for the Ciseco PiLite.
pygame used for colours, collision detection, timing and keyboard handling.

Controls (sticking with the Sense Hat joystick-to-keyboard mappings):
    Joystick left   /  Left Arrow  - Move left
    Joystick right  /  Right Arrow - Move right
    Joystick up     /  Up Arrow    - Rotate anti-clockwise
    Joystick down   /  Down Arrow  - Rotate clockwise
    Joystick press  /  Return key  - Drop current block

Stephen Blythe 2014 (Originial PiLite implementation)
Andrew Richards 2015 (Sense Hat implementation)
--------------------------------------------------------------------------
"""

import sys, pygame, random, sense_hat, math
from pygame.color import Color

WIDTH = 8
WORKAREA_HEIGHT = 12  # ACTUAL_SIZE of display + max height of a block
WORKAREA_SIZE = WIDTH, WORKAREA_HEIGHT
ACTUAL_HEIGHT = 8  # The actual number of pixels vertically on the display
ACTUAL_SIZE = WIDTH, ACTUAL_HEIGHT
TOTAL_LEDS = WIDTH * ACTUAL_HEIGHT
CLEAR = (0, 0, 0, 0)
THRESHOLD = 10  # Colour intensity over which a pixel/LED counts as 'on'.
FRAME_RATE = 10  # Frames per second
sense = sense_hat.SenseHat()


def sensehat_display(surface):
    """Transfer a pygame Surface to the Sense Hat LEDs.

    This function builds a frame-buffer fb of (r,g,b) values suitable for the
    Hat's set_pixels method. It does this by extracting these values from
    pygame's (r,g,b,a) values, treating the final value as intensity.
    """
    fb = []
    w, h = surface.get_size()
    for y in range(h):
        row = ""
        for x in range(w):
            r, g, b, a = surface.get_at((x, y))
            red = int(r * a / 255)
            green = int(g * a / 255)
            blue = int(b * a / 255)
            fb.append((red, green, blue))
    # Display only the physical pixels that the Hat actually has,
    sense.set_pixels(fb[-TOTAL_LEDS:])


def blank_canvas(size=WORKAREA_SIZE):
    """Setup and return a pygame.Surface with all pixels turned off"""
    s = pygame.Surface(size, pygame.SRCALPHA)
    s.fill(CLEAR)
    return s


def make_block(pattern, colour):
    """
    Returns a pygame.Surface object according to the supplied pattern and colour.
    The pattern is a list of rows, each row is a list of 1s and 0s.
    """
    height = len(pattern)  # Number of rows
    width = (max(len(row) for row in pattern))
    block = pygame.Surface((width, height), pygame.SRCALPHA)
    block.fill(CLEAR)
    for y, row in enumerate(pattern):
        for x, element in enumerate(row):
            if element:
                block.set_at((x, y), colour)
    return block


def blocks_list():
    """
    Create a surface for each block and put it in an array. Given small display,
    some smaller blocks used.
    """
    bl = []
    bl.append(make_block([[1, 1], [1, 1]], Color('magenta')))
    bl.append(make_block([[1, 1, 0], [0, 1, 1]], Color('blue')))
    bl.append(make_block([[0, 1, 1], [1, 1, 0]], Color('darkorange4')))
    bl.append(make_block([[0, 1, 0], [1, 1, 1]], Color('red')))
    bl.append(make_block([[1, 0, 0], [1, 1, 1]], Color('cyan')))
    bl.append(make_block([[0, 0, 1], [1, 1, 1]], Color('salmon')))
    bl.append(make_block([[1, 1, 1]], Color('yellow')))
    return bl


def block_mask(block, x, y):
    """Return a pygame.mask for the specified block and position"""
    block_canvas = blank_canvas()
    block_canvas.blit(block, [x, y], special_flags=pygame.BLEND_RGBA_ADD)
    return pygame.mask.from_surface(block_canvas, THRESHOLD)


def game_over(frames):
    """Print score etc, exit cleanly"""
    score = int(frames/10)  # Tweak as desired
    print("Game over, score: {0}".format(score))
    # Draw a red cross on the Hat, wait a bit, then display the score there,
    hat_canvas = blank_canvas(ACTUAL_SIZE)
    pygame.draw.line(hat_canvas, Color('red'), (0, 0), (WIDTH - 1, ACTUAL_HEIGHT-1))
    pygame.draw.line(hat_canvas, Color('red'), (WIDTH - 1, 0), (0, ACTUAL_HEIGHT-1))
    sensehat_display(hat_canvas)
    pygame.time.wait(2000)
    sense.show_message("Score: "+str(score), text_colour = Color('navyblue')[:3])


class MyPlayarea:
    """Class to keep track of game 'Surface' and current falling block."""


    def __init__(self, size=WORKAREA_SIZE):
        pygame.init()  # In case not already called
        self.background = blank_canvas()  # For blocks that have landed
        self.width = size[0]
        self.height = size[1]
        self.blocks = blocks_list()
        self.new_block()


    def new_block(self):
        """Create a new block (select the shape randomly) and give it
        co-ordinates at the top of the current display/'Surface'.
        Check that there is actually space in this location for the
        block; return False if there's no space; otherwise return
        True and set up the block attributes."""
        block = self.blocks[random.randrange(0, len(self.blocks))]
        new_x = 3
        new_y = WORKAREA_HEIGHT - ACTUAL_HEIGHT - block.get_height()
        if self.can_place_block_here(block, new_x, new_y):
            self.block = block
            self.block_x = new_x
            self.block_y = new_y
            return True
        else:
            return False


    def can_place_block_here(self, block, x, y):
        """
        Check if having block at (x,y) would exceed the borders of workarea.
        Check for no collision with the existing contents of workarea if block
        is placed at position (x,y).
        """
        border_violation = x < 0 or y < 0 or \
            x + block.get_width() > self.width or \
            y + block.get_height() > self.height
        background_mask = pygame.mask.from_surface(self.background, THRESHOLD)
        collision = background_mask.overlap(block_mask(block, x, y), (0, 0))
        return not (border_violation or collision)


    def block_move(self, dx, dy):
        """
        See if there is empty space available if the current falling block
        moves by (dx, dy) pixels.
        """
        if self.can_place_block_here(self.block, self.block_x+dx, self.block_y+dy):
            self.block_x = self.block_x + dx
            self.block_y = self.block_y + dy
            return True
        else:
            return False


    def block_rotate(self, angle):
        """
        See if there is empty space available if the current falling block
        is rotate by angle degrees (angle should be a multiple of 90).
        """
        rotated_block = pygame.transform.rotate(self.block, angle)
        if self.can_place_block_here(rotated_block, self.block_x, self.block_y):
            self.block = rotated_block
            return True
        else:
            return False


    def add_block_to_background(self):
        """
        Add the current falling block at its current position to the background.
        """
        self.background.blit(self.block, [self.block_x, self.block_y], special_flags=pygame.BLEND_RGBA_ADD)


    def render(self):
        '''Renders background and block in current position'''
        screen = blank_canvas()
        screen.fill(CLEAR)
        screen.blit(self.background, (0, 0))
        screen.blit(self.block, [self.block_x, self.block_y], special_flags=pygame.BLEND_RGBA_ADD)
        sensehat_display(screen)


    def remove_full_lines(self):
        """
        Remove any complete horizontal lines in workarea; move content above the
        removed line down into the space created by the line removal.
        """
        background_mask = pygame.mask.from_surface(self.background, THRESHOLD)
        for row in range(self.height):
            check_area = blank_canvas()
            pygame.draw.line(check_area, Color('white'), (0, row), (self.width - 1, row))
            check_area_mask = pygame.mask.from_surface(check_area, THRESHOLD)
            if background_mask.overlap_area(check_area_mask, (0, 0)) == self.width:
                # Remove full lines by setting the clipping area to be a rectangle
                # from the top to the line to be removed, and scrolling down,
                self.background.set_clip(pygame.Rect((0, 0), (self.width, row + 1)))
                self.background.scroll(0, 1)
                self.background.set_clip(None)
                background_mask = pygame.mask.from_surface(self.background, THRESHOLD)


def tetripisense():
    sense.clear()
    pygame.init()

    # pygame.display not used, but needed to capture keyboard events
    pygame.display.set_mode((1, 1))

    clock = pygame.time.Clock()
    s = MyPlayarea()
    frames = 0
    frames_before_drop = 10
    drop_block = False
    try:
        while True:
            frames += 1
            # One move event per frame simplifies collision detection and plays better
            moved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if drop_block and event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    drop_block = False
                    #moved = True
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        return
                    if not drop_block and not moved:
                        if event.key == pygame.K_LEFT:
                            moved = s.block_move(-1,0)
                        if event.key == pygame.K_RIGHT:
                            moved = s.block_move(1,0)
                        if event.key == pygame.K_UP:
                            moved = s.block_rotate(90)
                        if event.key == pygame.K_DOWN:
                            moved = s.block_rotate(-90)
                        if event.key == pygame.K_RETURN:
                            drop_block = True
            frames_before_drop -= 1
            if frames_before_drop == 0:
                if s.block_move(0, 1): # Move down
                    pass
                else: # Collision downwards at pos_y+1
                    s.add_block_to_background()
                    s.remove_full_lines()
                    if not s.new_block():
                        break # New block collides with existing blocks
                    drop_block = False
                # Progressively reduce to make game harder,
                frames_before_drop = 10 - int(math.log(frames,5))
            s.render()
            if drop_block:
                clock.tick(FRAME_RATE*10)  # Fast descent
            else:
                clock.tick(FRAME_RATE)
    except KeyboardInterrupt:
        return
    game_over(frames)


if __name__ == '__main__':
    tetripisense()
    sense.clear()
    pygame.quit()
    sys.exit()
