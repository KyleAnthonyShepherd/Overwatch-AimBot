'''
Overwatch aim bot program

This code runs in the background of your computer as you play Overwatch.
It identifies the location of enemies through image analysis.
Specifically, in Overwatch, each enemy is outlined in Red.
This program takes a screenshot, identifies red pixels on the screen, and moves
your cursor to the center of the red pixels.

I have not searched for the best thesholds to use to identify the red lines and
just the red lines

If this script is run by itself, the Main function is run using these values
key = 0x42 #b key
xbbox = 200
ybbox = 200
FPS=30
AutoAdjust=True
Debug=False

Function ScreenGrab(sct,bbox) gets the screenshot
Function GetOutline(im,bbox) get the red lines
Function PrintScreenGrab(im) and PrintOutline(im,xloc,yloc,bbox) are uses when
debugging is on, to see what is being captured and identified as a red line
Function CursorSnap(xloc,yloc,bbox) moves the cursor based on the red line information
Function Main has an infinite loop, and listens for a key to run the above functions

Virtual key codes can be found by googling "windows Virtual-Key Codes"

For this code to work, your computer must be beefy enough to run overwatch at a
fast frame rate, to reduce input lag. Otherwise, this program will aim
behind your target.

###
Code Written by:
Kyle Shepherd
kyleanthonyshepherd@gmail.com
Sep 23, 2016
###
'''
#### Import BLock ####
# the import block imports needed modules, and spits out a json file with
# version numbers so the code can be repeatable
file = open("ModuleVersions.json", 'w')
modules = {}

import os
import time

import sys
modules['Python'] = dict([('version', sys.version_info)])

import json
modules['json'] = dict([('version', json.__version__)])

import numpy
modules['numpy'] = dict([('version', numpy.__version__)])

import PIL
modules['PIL'] = dict([('version', PIL.__version__)])
from PIL import Image

import mss
modules['mss'] = dict([('version', mss.__version__)])
from mss.windows import MSS as mss

import ctypes
modules['ctypes'] = dict([('version', ctypes.__version__)])

json.dump(modules, file, indent=4, sort_keys=True)
file.close()
#### END Import Block ####

def ScreenGrab(bbox):
	'''
This function captures the current monitor screen using mss

Inputs:
###
bbox: the area of the screen to capture
format: dictionary {'width':,'left':,'height':,'top':}
Example:
bbox={'width':100,'left':100,'height':100,'top':100}
###

It returns an Pil Image object
	'''
	im=mss().grab(bbox)
	im=Image.frombytes("RGB", im.size, im.bgra, "raw", "BGRX")
	return im

def GetOutline(im,bbox):
	'''
This function finds the pixels that contain the red outline
Using HSV pixel values, hue and saturation threshholds are set

Inputs:
###
im: the image to analyze
Format: Pil Image object

bbox: the area of the screen to capture
format: dictionary {'width':,'left':,'height':,'top':}
Example:
bbox={'width':100,'left':100,'height':100,'top':100}
###

It returns a tuple containing (xloc,yloc,OutlineFound)
xloc=x coordinates of the pixels with a red outline, list
yloc=y coordinates of the pixels with a red outline, list
OutlineFound=bool if any red outline was found
	'''
	color=list(im.getdata().convert('HSV')) #convert to HSV for cleaner thresholds
	xbbox=bbox['width']/2
	xloc = []
	yloc = []

	for i in range(0,len(color)):

		if color[i][0] < 8  and color[i][1]>135: # thesholds for red line
			xloc.append(i % (xbbox*2))
			yloc.append(i // (xbbox*2))

	if len(xloc)!=0: # checks to see if red line was found
		OutlineFound=True
	else:
		OutlineFound=False

	return (xloc,yloc,OutlineFound)

def PrintScreenGrab(im):
	'''
This function displays the captured area of the screen using PIL image show

Inputs:
###
im: the image to analyze
Format: Pil Image object
###
	'''
	im.show()

def PrintOutline(im,xloc,yloc,bbox):
	'''
This function displays where the red outline was detected.

Inputs:
###
im: the image to analyze
Format: Pil Image object

xloc: the x coordinates of the pixels containing the red outline
Format: List

yloc: the x coordinates of the pixels containing the red outline
Format: List

bbox: the area of the screen to capture
format: dictionary {'width':,'left':,'height':,'top':}
Example:
bbox={'width':100,'left':100,'height':100,'top':100}
###
	'''
	color=list(im.getdata().convert('HSV'))
	xbbox=int(bbox['width']/2)

	for i in range(0,len(color)):
		im.putpixel((i % (xbbox*2),i // (xbbox*2)),(0, 0, 0)) # makes image black
	for i in range(0,len(xloc)):
		im.putpixel((int(xloc[i]),int(yloc[i])),(255, 0, 0)) # makes pixels red where line exists
	im.show()

def CursorSnap(xloc,yloc,bbox):
	'''
This function performes a relative mouse movement based on the location of the
red outline.
It finds the average x and y coordinate, and moves the mouse there

Inputs:
###
xloc: the x coordinates of the pixels containing the red outline
Format: List

yloc: the x coordinates of the pixels containing the red outline
Format: List

bbox: the area of the screen to capture
format: dictionary {'width':,'left':,'height':,'top':}
Example:
bbox={'width':100,'left':100,'height':100,'top':100}
###
	'''
	xavg=sum(xloc)/len(xloc)
	yavg=sum(yloc)/len(yloc)
	# does the acutal cursor move
	ctypes.windll.user32.mouse_event(1, int(xavg-bbox['width']/2), int(yavg-bbox['height']/2), 0,0)

def Main(key,xbbox,ybbox,FPS=30,AutoAdjust=True,Debug=False):
	'''
This function will run in a loop.
It checks for when the given key is pressed. When the key is pressed, the AimBot
program is activated, and the above functions are called to take a screenshot
and find the enemy

Inputs:
###
key: the virtural key code of the keyboard key to activate the aimbot
Format: windows virtual key code
Example: 0x42
for the b key

xbbox: the width of the screenshot to take
Format: integer
Example: 150
larger values require more processing time, and may cause two enemies to be in
view at the same time.

ybbox: the height of the screenshot to take
Format: integer
Example: 150
larger values require more processing time, and may cause two enemies to be in
view at the same time.

FPS: the Frames Per Second that Overwatch runs on your system
When AutoAdjust is turned on, the size of the screenshot is dynamically adjusted
so that the image processing time is the same length of time as a frame
Format: integer
Example: 30

AutoAdjust: switch to turn on autoadjusting frame size
Format: bool
Example: True

Debug: Switch to output images of the captured screenshot
Format: bool
Example: False
###
	'''
	sct = mss()
	mon=sct.monitors #gets monitor size, so the center can be found
	bbox={'width':int(xbbox*2),'left':int(mon[0]['width']/2-xbbox),'height':int(ybbox*2),'top':int(mon[0]['height']/2-ybbox)}
	while 1==1: # infinite loop
		if ctypes.windll.user32.GetKeyState(key)>1: # listens for key
			t=time.time() # for timing the loop, for autoadjust
			im=ScreenGrab(bbox) # calls ScreenGrab
			(xloc,yloc,OutlineFound)=GetOutline(im,bbox) # calls GetOutline

			if Debug:
				PrintScreenGrab(im)
				PrintOutline(im,xloc,yloc,bbox)

			if OutlineFound:
				CursorSnap(xloc,yloc,bbox)

			if AutoAdjust:
				dTtime=1/FPS-(time.time()-t)
				xbbox = xbbox+numpy.sign(dTtime)*10 # adjusts the frame size by 10 pixels at a time
				ybbox = ybbox+numpy.sign(dTtime)*10
				xbbox=max([xbbox,50]) # floors the frame size, so negatives do not occur
				ybbox=max([ybbox,50])
				bbox={'width':int(xbbox*2),'left':int(mon[0]['width']/2-xbbox),'height':int(ybbox*2),'top':int(mon[0]['height']/2-ybbox)}

			else:
				time.sleep(1/FPS-(time.time()-t)) # makes sure each loop is as long as a frame

if __name__ == "__main__":
	key = 0x42 #b key
	xbbox = 200
	ybbox = 200
	FPS=30
	AutoAdjust=True
	Debug=False
	Main(key,xbbox,ybbox,FPS=FPS,AutoAdjust=AutoAdjust,Debug=Debug)
