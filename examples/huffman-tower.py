#!/usr/bin/env python
from shapes import *

scene = Scene('huffman-tower',4.,2.,'in')
mtn = Layer('mountain',(0,0,255),scene)
val = Layer('valley',(255,0,0),scene)
cut = Layer('cut',(255,0,255),scene)

n = 6 #number of segments
l = 1. #segment length
h = l*sqrt(3)/2

c1 = asarray([l,0.])
a1 = Arc(c1,l,2*pi/3,pi)
c2 = .5*c1
a2 = Arc(c2,.25*l,pi/2,pi)
l1 = Line([0,h],[.5*l,h])
l2 = Line([.5*l,h],[.5*l,1.5*h])

g = Group({a1:mtn,a2:val,l1:val,l2:mtn})
g = g.rotate(.5*c2,pi,copy=True)
g = g.mirror(c2,asarray([0,1]),copy=True)
g = g.translate(l*arange(-n/2,n/2).reshape(-1,1) * array([[1,0]]))
scene.add_group(g)

outline = [Line([-n*l/2,1.5*h],[n*l/2,1.5*h]),\
		Line([n*l/2,1.5*h],[n*l/2,-1.5*h]),\
		Line([n*l/2,-1.5*h],[-n*l/2,-1.5*h]),\
		Line([-n*l/2,-1.5*h],[-n*l/2,1.5*h])]
cut.add(outline)
scene.remove_duplicates()
scene.write_svg()
scene.display()
#scene.convert('.dxf')