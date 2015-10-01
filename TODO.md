# Ideas on how this program could be improved

## Rotation

Rotating blocks could be better: Consider the linear 3-unit block.
When rotated, it rotates by its left end. It would probably feel
more 'natural' to rotate around its centre, but this does complicate
how the block's vertical position is tracked.

## Sound

Currently there's no sound included; it would be good to have sound
provided (listen with headphones or an external speaker). Even better
would be to have the music gradually get more hectic as the game itself
speeds up. `pygame.mixer.music` might be helpful for providing sound.
Tetronimo has an easy approach that might be a quick fix here - just
kick off a music file, nothing further to do.

## Object Orientation (OO)

I feel that I've not achieved the level of OO I would like with this
program; I'm hopeful that someone with better OO skills will take a
closer look and improve what's here.

## Automatically starting the game

I love the idea of the Raspberry Pi with the Sense Hat and a battery
being self-contained without the need for a separate keyboard or
screen. The `run_game.py` program is provided for this. Possible
enhancements would be to provide more features in this wrapper
program, perhaps offer additional games (Snake is available as an
example program for the Sense Hat / Astro Pi for example), or to allow
the user to adjust the difficulty of the game.
