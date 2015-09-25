TetriPiSense - A Tetris-y game for the Sense Hat / Astro Pi / Unicorn Hat
=========================================================================

Andrew Richards, September 2015.

# Introduction
8 rows of 8 LEDs, teensy joystick... I found Snake as mentioned in the blurb
for the AstroPi, but no Tetris. So here's TetriPiSense, my motivation for
getting to grips with my Sense Hat... and indeed GitHub too.

# Description
The program uses the [sense_hat](https://pythonhosted.org/sense-hat/api/)
and [pygame](http://www.pygame.org/docs/) libraries to provide much of the
underlying functionality. The Sense Hat joystick is mapped to keyboard keys,
so for the Unicorn Hat (with no joystick), this program should still work -
just use your keyboard's arrow keys and Return key (also Esc key to quit).

# Installation
You'll need the pygame and sense_hat libraries installed on your Pi. pygame is
probably already installed; and if you've not already installed the sense_hat
library,

    sudo apt-get install sense-hat

# Usage
If you're directly connected (keyboard, mouse, monitor) to the Raspberry Pi
with Sense Hat, you should be able to launch the game like this (although
writing with Python 3 in mind, Python 2.7 seems to work fine too, I don't
know about earlier versions of Python),

    python tetripisense.py

The joystick controls the block: Move left/right, rotate anticlockwise/
clockwise, press to drop the current block; all of these are also available
via the keyboard (USB-connected to Pi) using the arrow keys and the Return key,
as well as the Esc key to exit the game.

If you're accessing the Raspberry Pi remotely (e.g. via ssh),

    export DISPLAY=0:0; sudo python tetripisense.py

Note that this runs the program with full administrator privileges, and makes
your Raspberry Pi system much more exposed and vulnerable to anything dodgy
that the game might try to do to your Pi. Note that the [ssh] keyboard doesn't
control the game when you're connected like this (although Ctrl-C will quit).

# Getting the game to startup automatically
It's fun to get the game to start automatically when the Pi is switched on,
without having to call it from a keyboard; indeed not having a monitor or
keyboard connected makes this an entertaining handheld gadget. The run_game.py
program is provided to wrap around the main game; it can be added to
/etc/rc.local so as to run the game when the Pi starts.

# Authors
Original PiLite implementation: Stephen Blythe
This Sense Hat implementation: Andrew Richards

# Website

    http://free.acrconsulting.co.uk/other/tetripisense.html

# License
Gnu General Public License, version 3 and above: Please see the included
LICENSE file.

# Known issues
Rotation: Please see TODO.md: Rotation uses pygame and rotates around an
axis of the top-left of the shape. Which is mostly fine, but for a long
narrow block, rotating around the centre of the block might look a bit more
polished.

# Origins of the program
Possible starting points were Tetromino written by Al Sweigart included
within Raspbian, and Stephen Blythe's implementation for Ciseco's PiLite.
I chose to adapt the latter since it was aimed at a similar grid-of-LEDs
display so should map well to the Hat - indeed, my initial hacks to get
it working on the Sense Hat didn't require much work, although I did then
spend a fair amount of time polishing the code and ironing out a few bugs.

# Some notes on the code
Having only 8 vertical LEDs makes it harder to achieve a reasonably playable
game, so I added another 'virtual' row of pixels for the behind-the-scenes
pygame.Surface, which gives the sense of the new block emerging at the top
of the display, rather than the whole block suddenly appearing at the top of
the display - this gives the player a bit more time to manoevre the new block
and results in the game feeling a bit more polished.

I've tried to move some chunks of code into functions where possible to make
the logic clearer; unfortunately the main game loop still contains quite a lot
of code but is hopefully reasonably straightforward. Most of the manipulation
of the falling block and the background is done with pygame functions; actually
displaying the game uses the sensehat_display() function which converts from
the pygame representation of the display to the representation used by
sense_hat's set_pixels() method.

The falling block and/or the [virtual] pixel matrix (pygame.Surface) feel like
they could become proper objects in a more object-oriented implementation, but
I've not found time for that and probably won't. Anyone?

Unit or other tests are also conspicuously absent here but would be very
worthwhile, even if only part of the code lends itself to this.


# Getting your Pi to run game this at startup
It's fun to have the Pi run this game on its own without a mouse, keyboard,
screen - a sort of minimal handheld games console, powered by an external
battery, such as the now fairly widely available external battery packs for
phones that provide power via USB cables.

To do this, the Pi will need to respond to the Hat's joystick when it starts
up. Given this is mapped to the keyboard, just add run_game.py to the Pi's
customisable startup script to wait for the joystick button (mapped to the
Return key) to be pressed (in fact any keypress, so moving the joystick
works too): Add the following line before the final "exit 0" line in
/etc/rc.local,

    python /home/pi/tetripisense/run_game.py

assuming run_game.py and tetripisense.py are in the directory above.
Also note that this will be running run_game.py and tetripisense.py
with administrator privileges which is poor practice.
