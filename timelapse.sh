#!/bin/bash

# run raspistill with no arguments to see all parameters
# (-t 0): Total run time. When set to 0 the timelapse will run until ctrl+c or other interrupt is input by user.
# (-tl 5000): Timelapse with frame rate of 5s.
# (-o /home/pi/Pictures/.jpeg) Signifies output file path and format. Can also use (-e png,jpeg,raw) for format.
# (-ts) Appends a unix timestamp to the file name. Can use (-dt) for utc datetime or add %04d to filename for image sequence.
# (-n) Preview mode disabled.
# (-md) Used to change sensor mode (0-7). 0 = default, 1 = 1920x1080, 2 = 3280x2464, etc.
# (-w) and (-h) Used to change custom width and height of image.
# (-q) Image quality from 0-100.
# (-rot) Rotate image 0-359 degrees.

echo 'Starting Timelapse'
raspistill -t 0 -tl 5000 -o -q 100 -rot 180 /home/pi/Pictures/img_%04d.jpeg -ts -n