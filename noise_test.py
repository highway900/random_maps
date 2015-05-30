#!/bin/env python

import sys
import noise
import png
import random

WIDTH = 256
HEIGHT = 256


def clamp(x, a, b):
    return min(max(float(x), float(a)), float(b))

def scaleVal(val, inlow, inhigh, outlow, outhigh):
    return ((val - float(inlow)) / (float(inhigh) - float(inlow))) * (float(outhigh) - float(outlow)) + float(outlow)
   
img = []
for y in range(HEIGHT):
    t = tuple()
    for x in range(WIDTH):
        nx = scaleVal(x, 0, WIDTH, -1.0, 1.0)
        ny = scaleVal(y, 0, HEIGHT, -1.0, 1.0)
        val = noise.pnoise3(nx, ny, 1, octaves=int(sys.argv[1]), persistence=int(sys.argv[2]), lacunarity=float(sys.argv[3]), repeatx=256, repeaty=256, base=int(sys.argv[4]))
        
        nval = int(scaleVal(val, -1.0, 1.0, 0, 255))
        
        #nval = clamp(nval, 155, 255)
       
        if nval < 140:
            nval = 10
        else:
            nval = 255

        t += (nval, nval, nval,)
    img.append(t)

if img:
    with open('random_map_pnoise.png', 'wb') as f:
        w = png.Writer(WIDTH, HEIGHT)
        w.write(f, img)
 
