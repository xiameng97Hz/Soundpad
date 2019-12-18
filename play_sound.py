# play_sound.py
#
# Author: Xiameng Chen
# Date: 12/04/2019
# Description: Set button color and play sound when detecting button press
# Reference: NeoTrellis Soundbox Remix - Noe and Pedro Ruiz, code by Mike Barela

import pygame
from pygame.locals import*  #for event MOUSE variables

import time
import os
import random
import board
from board import SCL, SDA
import digitalio
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

# Color definitions
OFF = (0, 0, 0)
RED = (25, 0, 0)
YELLOW = (25, 15, 0)
GREEN = (0, 25, 0)
CYAN = (0, 25, 25)
BLUE = (0, 0, 25)
PURPLE = (18, 0, 25)
WHITE = (127, 127, 127)

# Instrument
instru = ""

# Path
path = ""

# Create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

# Create the trellis
trellis = NeoTrellis(i2c_bus,False,addr=0x2F)

print("NeoTrellis created")

audio_file = None

PUSH_COLOR = GREEN
ANIM_COLOR = WHITE

COLORS = ["RED", "YELLOW", "GREEN", "CYAN", "BLUE", "PURPLE", "WHITE"]
COLOR_TUPLES = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE]

buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
button_colors = [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF,
				OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF]
shuffled_colors = list(button_colors)
Shuffled = False

wavnames = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
shuffled_names = list(wavnames)  # Duplicate list, wavnames is our reference



def play_file(audio_filename):
    global audio_file  # pylint: disable=global-statement
    if audio_file:
        audio_file.close()
    audio_name = path+audio_filename
    print(audio_file)
    audio_file = open(path+audio_filename, "rb")
    print("Playing "+audio_filename+".")
    os.system('omxplayer '+audio_name+' &')


# this will be called when button events are received
def blink(event):
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:  # Trellis button pushed
        print("Button "+str(event.number)+" pushed")
        if event.number > 15:
            print("Event number out of range: ", event.number)
        trellis.pixels[event.number] = WHITE
        if shuffled_names[event.number] != "":
            play_file(shuffled_names[event.number])

    # turn the LED off when a rising edge is detected (button released)
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = shuffled_colors[event.number]



def run(instru):
	global path,wavnames,shuffled_names,buttons,button_colors,shuffled_colors,Shuffled
	path = "/home/pi/soundpad/"+instru+"/"
	wavnames = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
	shuffled_names = list(wavnames)  # Duplicate list, wavnames is our reference
	
	buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	button_colors = [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF,
				OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF]
	shuffled_colors = list(button_colors)
	Shuffled = False

	# Process wav files in the flash drive sounds directory
	wavefiles = [file for file in os.listdir(path)
				if (file.endswith(".wav") and not file.startswith("._"))]
	if len(wavefiles) < 1:
		print("No wav files found in sounds directory")
	else:
		print("Audio files found: ", wavefiles)
	
	# Time to process the filenames using the special file name syntax
	# Currently nn-color-name.wav where nn = 2 digit number 0 to 15
	# color is lower or upper case color name from above and
	# name can be anything. BUT these all must be separated by a "-"
	# Example 02-blue-firetruck.wav is valid. Note leading 0 for 0 to 9
	shuffled = False
	for soundfile in wavefiles:
		print("Processing "+soundfile)
		pos = int(soundfile[0:2])
		if pos >= 0 and pos < 16:      # Valid filenames start with 00 to 15
			wavnames[pos] = soundfile  # Store soundfile in proper index
			shuffled_names[pos] = soundfile
			skip = soundfile[3:].find('-') + 3
			user_color = soundfile[3:skip].upper()  # Detect file color
			print("For file "+soundfile+", color is "+user_color+".")
			file_color = COLOR_TUPLES[COLORS.index(user_color)]
			button_colors[pos] = file_color
			shuffled_colors[pos] = file_color
		else:
			print("Filenames must start with a number from 00 to 15 - "+soundfile)
		
	for i in range(16):
		# activate rising edge events on all keys
		trellis.activate_key(i, NeoTrellis.EDGE_RISING)
		# activate falling edge events on all keysshuff
		trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
		# set all keys to trigger the blink callback
		trellis.callbacks[i] = blink

		# cycle the LEDs on startup
		trellis.pixels[i] = ANIM_COLOR
		time.sleep(.05)

	# On start, set the pixels on trellis to the file name colors chosen
	for i in range(16):
		trellis.pixels[i] = shuffled_colors[i]
		time.sleep(.05)


	while True:
		# call the sync function call any triggered callbacks
		trellis.sync()
		# the trellis can only be read every 17 milliseconds or so
		time.sleep(.02)
		
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP):
				pos=pygame.mouse.get_pos()
				x,y=pos
				if y>200:
					if x<80:
						return 1
					
					elif x>200:	# back to main menu
						for i in range(16):
							trellis.pixels[i] = OFF
						return 0
