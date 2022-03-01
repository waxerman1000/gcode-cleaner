# gcode Cleaner
There are several files in here and each to different things. Amazing, right?

## gcode_pore_wall_remover.py
This is the final program that removes the wall inside the pores and some
infill lines.

## gcode_pore_inserter.py
This is the original program that I started making and later pushed aside since
it started becoming too slow and the like.

## object_mover.py
I made this to test flashprint gcodes on my personal printer.
Moves every X and Y coordinate in the file ~ +155.

## extrusion_check.py
I made this to test my output files to check and see if there's any
overextrusion or underextrusion without actually printing the file.

## poredcube.gcode
The gcode file that's been used for testing.

# What's important?
The primary file in here is gcode_pore_wall_remover. It's the what the final
product was supposed to be.

# What's wrong with it?
Known issues include:

## Removed Extrusion
Any Extrusion that is removed currently doesn't add properly to the global
extrusion_removed variable (at least, on line 148).

## Infill "Wall" Removal
The current strategy to remove walls is to simulate a moving print head.
If the program says that the print head only moved on one axis while printing
the infill, it removes the movement.
The plan was to have it move anyways (just remove the extrusion) but I was never
able to figure out the extrusion_removed variable from before.

# Anything else I should know?
Good luck.
