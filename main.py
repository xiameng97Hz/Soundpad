# main.py
#
# Author: Xiameng Chen
# Date: 12/04/2019
# Description: This is the main program. It creates the GUI and calls functions as user selects on touchscreen

import pygame
from pygame.locals import*  #for event MOUSE variables
import os
import RPi.GPIO as GPIO
import time
import play_sound
import voice_recognition
import recordandplay

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)

os.putenv('SDL_VIDEODRIVER','fbcon')  #Display on piTFT
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')     #Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

def GPIO27_callback(channel):
	global code_running
	print ("falling edge detected on 27")
	code_running = False

GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback)


# Pygame initialization
pygame.init()
pygame.mouse.set_visible(False)	# Set to False when display on piTFT

WHITE=255,255,255
BLACK=0,0,0

size=width,height=320,240
screen=pygame.display.set_mode((width,height))

background=pygame.image.load("/home/pi/soundpad/background.jpg")
ai_background=pygame.image.load("/home/pi/soundpad/voice_background.jpg")
backrect=background.get_rect()
backrect2=ai_background.get_rect()
title_font=pygame.font.Font(None,30)
button_font=pygame.font.Font(None,20)

flag_main = True
flag_preset = False
flag_ai = False
flag_record = False

context = ""

# Initialize main menu
def main_menu():
	screen.fill(BLACK)
	screen.blit(background,backrect)

	title_text={'Soundpad':(160,25)}
	button_text={'Preset mode':(50,220),'AI mode':(160,220),'Record mode':(270,220)}
	for my_text,text_pos in title_text.items():
		text_surface=title_font.render(my_text,True,WHITE)
		rect=text_surface.get_rect(center=text_pos)
		screen.blit(text_surface,rect)
	for my_text,text_pos in button_text.items():
		text_surface=button_font.render(my_text,True,WHITE)
		rect=text_surface.get_rect(center=text_pos)
		screen.blit(text_surface,rect)

	pygame.display.flip()


# Initialize preset mode screen
def preset_menu():
	screen.fill(BLACK)
	screen.blit(background,backrect)
	
	title_text={'Preset Mode':(160,25)}
	button_text={'Back':(270,220)}
	for my_text,text_pos in title_text.items():
		text_surface=title_font.render(my_text,True,WHITE)
		rect=text_surface.get_rect(center=text_pos)
		screen.blit(text_surface,rect)
	for my_text,text_pos in button_text.items():
		text_surface=button_font.render(my_text,True,WHITE)
		rect=text_surface.get_rect(center=text_pos)
		screen.blit(text_surface,rect)

	pygame.display.flip()
	
	
# Initialize preset mode screen
def ai_menu(string):
	screen.fill(BLACK)
	screen.blit(ai_background,backrect2)
	
	title_text={'AI Mode':(160,25)}
	button_text={'Start':(50,220),'Confirm':(160,220),'Back':(270,220)}
	for my_text,text_pos in title_text.items():
		text_surface=title_font.render(my_text,True,WHITE)
		rect=text_surface.get_rect(center=text_pos)
		screen.blit(text_surface,rect)
	for my_text,text_pos in button_text.items():
		text_surface=button_font.render(my_text,True,WHITE)
		rect=text_surface.get_rect(center=text_pos)
		screen.blit(text_surface,rect)
		
	text=button_font.render(string,True,WHITE)
	textRect=text.get_rect()
	textRect.center=(160,120)
	#screen.blit(text_surface,rect)
	screen.blit(text,textRect)
				
	pygame.display.flip()
	

# Initialize record mode screen
def record_menu(string):
	screen.fill(BLACK)
	screen.blit(background,backrect)
	
	title_text={'Record Mode':(160,25)}
	button_text={'Start':(50,220),'Play':(120,220),'Load':(200,220),'Back':(270,220)}
	for my_text,text_pos in title_text.items():
		text_surface=title_font.render(my_text,True,WHITE)
		rect=text_surface.get_rect(center=text_pos)
		screen.blit(text_surface,rect)
	for my_text,text_pos in button_text.items():
		text_surface=button_font.render(my_text,True,WHITE)
		rect=text_surface.get_rect(center=text_pos)
		screen.blit(text_surface,rect)
		
	text=button_font.render(string,True,WHITE)
	textRect=text.get_rect()
	textRect.center=(160,180)
	#screen.blit(text_surface,rect)
	screen.blit(text,textRect)

	pygame.display.flip()
	

code_running = True	
main_menu()
while code_running:
	if flag_main:
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP):
				pos=pygame.mouse.get_pos()
				x,y=pos
				if y>200:
					if x<80:	# preset mode is selected
						flag_main = False
						flag_preset = True
						preset_menu()
						# Actions to initializaing preset menu
						status = play_sound.run("sounds")
						if status==0:
							flag_main = True
							flag_preset = False
							main_menu()
							
					elif x>140 and x<180:		# ai mode is selected
						flag_main = False
						flag_ai = True
						ai_menu("")
						
					elif x>240:		# record mode is selected
						flag_main = False
						flag_record = True
						record_menu("")
	
	if flag_preset:
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP):
				pos=pygame.mouse.get_pos()
				x,y=pos
				if y>200:
					if x>240:	# back to main menu
						flag_main = True
						flag_preset = False
						main_menu()
	
	if flag_ai:
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP):
				pos=pygame.mouse.get_pos()
				x,y=pos
				if y>200:
					if x<80:	# start recognizing human voice
						ai_menu("Start to speak")
						context = voice_recognition.run()		# call voice recognition
						print("Requesting "+context)
						ai_menu(context)
					elif x>140 and x<180:		# confirm the result
						if context=="":
							ai_menu("Please specify instrument first:)")
						else:
							ai_menu("Now playing " + context + "...")
							status = play_sound.run(context)		# loading specific sound packs
							if status==0:
								context = ""
								flag_main = True
								flag_ai = False
								main_menu()
							elif status==1:
								ai_menu("Start to speak")
						
					elif x>240:	# back to main menu
						flag_main = True
						flag_ai = False
						main_menu()
						
	if flag_record:
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP):
				pos=pygame.mouse.get_pos()
				x,y=pos
				if y>200:
					if x<80:	# start recording
						print("Start recording...")
						record_menu("Recording...")
						# add recording code
						recordandplay.record()
						time.sleep(3.0)
						record_menu("Finish")
						
					elif x>100 and x<140: # playback
						print("Playback...")
						record_menu("Playing...")
						# add playback code
						recordandplay.play()
						record_menu("Finish")
						
					elif x>180 and x<220: # load
						print("Loading to Neotrellis...")
						record_menu("Loaded^_^")
						# add playback code
						status = play_sound.run("record")
						
						
					elif x>240:	# back to main menu
						flag_main = True
						flag_record = False
						main_menu()

					
GPIO.cleanup()			
