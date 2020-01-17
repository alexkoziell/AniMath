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
    myNumberLine = lines.NumberLine(color=colors.RED)

    global openInterval, closedInterval, clopenInterval
    openInterval = lines.Interval([-3,4], myNumberLine, True, True)
    closedInterval = lines.Interval([-2,3], myNumberLine, False, False)
    clopenInterval = lines.Interval([-1,1], myNumberLine, False, True)

def drawScene(elapsedTime):
    myNumberLine.draw()
    for interval in [openInterval, closedInterval, clopenInterval]:
        interval.aBracket.sprite.draw()
        interval.bBracket.sprite.draw()