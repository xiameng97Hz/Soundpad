# recordandplay.py
#
# Author: Weiyi Sun
# Date: 12/04/2019
# Description: Functions for recording and playback

import os

def record():	# Record for 3 seconds
    cmd1='arecord -D "plughw:1,0" -d 3 /home/pi/soundpad/record/00-cyan-record.wav &'
    os.system(cmd1)
    print("recording...")
    
def play(): 
    cmd2='omxplayer -o local /home/pi/soundpad/record/00-cyan-record.wav'
    os.system(cmd2)
    print("playing...")
