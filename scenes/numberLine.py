import numpy as np
import pyglet

import sys
sys.path.append('..')
import animation
import colors
sys.path.append('../geometry')
import lines
sys.path.append('../image')
import image

def setupScene(width, height):
    global myNumberLine
    myNumberLine = lines.NumberLine()

    global openInterval, closedInterval, clopenInterval
    openInterval = lines.Interval([-2,4], myNumberLine, True, True, color=colors.RED)
    closedInterval = lines.Interval([-3,1], myNumberLine, False, False, color=colors.GREEN)
    clopenInterval = lines.Interval([-1,2], myNumberLine, False, True, color=colors.BLUE)

    clopenInterval.resize([-1, 1], 2, 4)
    closedInterval.resize([-2, 4], 4.5, 7)
    openInterval.resize([-4, 4.5], 7, 10)

def drawScene(elapsedTime):
    myNumberLine.draw()
    for interval in [openInterval, closedInterval, clopenInterval]:
        interval.aBracket.sprite.draw()
        interval.bBracket.sprite.draw()
    
    if elapsedTime > 11:
        pyglet.app.exit()