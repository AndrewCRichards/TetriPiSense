# Ideas on how this program could be improved

## Rotation

Rotating blocks could be better in 2 ways:

 - The axis of rotation: Consider the linear 3-unit block. When
   rotated, it rotates by its left end. It would probably feel
   more 'natural' to rotate around its centre, but this does
   complicate how the block's vertical position is tracked.

 - At the sides of the display: Sometimes rotation is not
   permitted because part of the rotated block would extend
   beyond the display. It may feel more 'natural', when this
   occurs, to try to rotate the block whilst moving it one
   unit inwards.

One possible enhancement re. rotation could be to pre-compute all the
possible rotated shapes, and store not just the shape itself but also
its rotated versions in a list which could then be accessed by using
list indexing.

## Sound
Currently there's no sound included; it would be good to have sound
provided (listen with headphones or an external speaker). Even better
would be to have the music gradually get more hectic as the game itself
speeds up. pygame.mixer.music might be helpful for providing sound.

## Object Orientation

I feel that I've not achieved the level of Object Orientation I would
like with this program - in particular it feels like the falling block
could benefit from being a separate object/ class, but the attempts
I've made in this direction get awkward quickly: Whilst moving left,
right and down seem not to create any difficulties, rotation is
problematic, although the idea above about pre-computing rotated
shapes might be useful in addressing this.

## Automatically starting the game

I love the idea of the Raspberry Pi with the Sense Hat and a battery
being self-contained without the need for a separate keyboard or
screen. The run_game.py program is provided for this. Possible
enhancements would be to provide more features in this wrapper
program, perhaps offer additional games (Snake is available as an
example program for the Sense Hat / Astro Pi for example), or allow
the user to adjust the difficulty of the game.
