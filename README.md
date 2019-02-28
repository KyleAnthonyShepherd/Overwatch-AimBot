# Overwatch-AimBot
A python based aimbot that identifies targets though screen analysis. Enemies are outlined in Red during the game, so this program finds the red outline and places the crosshair in the center. 

Overwatch aim bot program<br>
<br>
This code runs in the background of your computer as you play Overwatch.<br>
It identifies the location of enemies through image analysis.<br>
Specifically, in Overwatch, each enemy is outlined in Red.<br>
This program takes a screenshot, identifies red pixels on the screen, and moves<br>
your cursor to the center of the red pixels.<br>
<br>
I have not searched for the best thesholds to use to identify the red lines and<br>
just the red lines<br>
<br>
If this script is run by itself, the Main function is run using these values<br>
key = 0x42 #b key<br>
xbbox = 200<br>
ybbox = 200<br>
FPS=30<br>
AutoAdjust=True<br>
Debug=False<br>
<br>
Function ScreenGrab(sct,bbox) gets the screenshot<br>
Function GetOutline(im,bbox) get the red lines<br>
Function PrintScreenGrab(im) and PrintOutline(im,xloc,yloc,bbox) are uses when<br>
debugging is on, to see what is being captured and identified as a red line<br>
Function CursorSnap(xloc,yloc,bbox) moves the cursor based on the red line information<br>
Function Main has an infinite loop, and listens for a key to run the above functions<br>
<br>
Virtual key codes can be found by googling "windows Virtual-Key Codes"<br>
<br>
For this code to work, your computer must be beefy enough to run overwatch at a<br>
fast frame rate, to reduce input lag. Otherwise, this program will aim<br>
behind your target.<br>
<br>
###<br>
Code Written by:<br>
Kyle Shepherd<br>
kyleanthonyshepherd@gmail.com<br>
Sep 23, 2016<br>
###<br>
