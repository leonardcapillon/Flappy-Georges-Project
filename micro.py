#!/usr/bin/python
# VU meter written in Python (www.python.org) by Tim Howlett 1st April 2013, 
# Does not work with Python 2.7.3 or 2.7.4 Does work with 3.2.3
# Requires the Pygame module (www.pygame.org)and the Pyaudio module (http://people.csail.mit.edu/hubert/pyaudio/)

import sys, pygame, pyaudio, wave, audioop, math
from pygame.locals import *

# set up a bunch of constants 
BGCOLOR = (0, 0, 0)
WINDOWWIDTH = 85
WINDOWHEIGHT = 500

# setup code
pygame.init()
pygame.mixer.quit() # stops unwanted audio output on some computers
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), HWSURFACE)
pygame.display.set_caption('VU Meter')
fontSmall = pygame.font.Font('freesansbold.ttf', 12)
pa = pyaudio.PyAudio()

info = pa.get_default_input_device_info()
RATE = int(info['defaultSampleRate'])

# open stream 
stream = pa.open(format = pyaudio.paInt16,
            channels = 1,
            rate = RATE,
            input = True,
            frames_per_buffer = 1024)
            
def level():
    data = stream.read(1024)
    ldata = audioop.tomono(data, 2, 1, 0)
    amplitudel = ((audioop.max(ldata, 2))/32767)
    LevelLa = (int(41+(20*(math.log10(amplitudel+(1e-40))))))	
    return LevelLa;            

while True: # main application loop
    # event handling loop for quit events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    # Read the data and calcualte the left and right levels
    LevelL = level()
    
    # Fill the screen to draw from a blank state and draw the clock face
    DISPLAYSURF.fill(BGCOLOR)

    # Write the scale and draw in the lines
    for dB in range (0, 60, 4):
        number = str(dB)
        text = fontSmall.render("-"+number, 1, (255, 255, 255))
        textpos = text.get_rect()
        DISPLAYSURF.blit(text, (55, (12*dB)))
        pygame.draw.line(DISPLAYSURF, (255, 255, 255), (40,5+(12*dB)), (50,5+(12*dB)), 1)

    # Draw the boxes
    for i in range (0, LevelL):
        if i < 20: 
            pygame.draw.rect(DISPLAYSURF, (0, 192, 0), (10, (475-i*12), 30, 10))
        elif i >= 20 and i < 30:
            pygame.draw.rect(DISPLAYSURF, (255, 255, 0), (10, (475-i*12), 30, 10))
        else:
            pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (10, (475-i*12), 30, 10))
    mic=0  
    for i in range (0, LevelL):
     if  i < 30:
         mic=0
     else:
         mic=1   
    print(mic)
    pygame.display.update()
