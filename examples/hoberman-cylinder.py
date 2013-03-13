#!/usr/bin/env python
from shapes import *

scene = Scene('hoberman-cylinder',15,9,'in',.02)
mountain = Layer('mountain',(0,0,255),scene)
cut = Layer('cut',(255,0,255),scene)
valley = Layer('valley',(0,255,0),scene)

th1 = 60 *pi/180.
th2 = 75 *pi/180.
w = .275
h = .5
gap = 1.5
nx = 4
ny = 6

x = asarray([1,0])
y = asarray([0,1])

o = 0*x
p1 = w*x
p2 = x*h/tan(th1) + h*y
p3 = p1 + x*h/tan(th2) + y*h

l1 = Line(o,p1)
l2 = Line(o,p2)
l3 = Line(p2,p3)
l4 = Line(p1,p3)
l5 = Line(p3,p3+p1)
l6 = Line(p1,p3-p2+p1)
l7 = Line(p3-p2+p1,p3+p1)

g = Group({
	l1:mountain,
	l2:valley,
	l3:valley,
	l4:mountain,
	l5:mountain,
	l6:valley,
	l7:valley
	})

if gap>0:
	l8 = Line(p3-p2+p1,p3-p2+p1+x*gap)
	l9 = Line(p3+p1,p3+p1+x*gap)
	l10 = Line(p3-p2+p1+x*gap, p3+p1+x*gap) #redundant
	l11 = Line(p3-p2+p1, p3+p1) #redundant
	#g.add({l8:mountain, l9:valley, l10:valley, l11:valley})
	gaps = Group({l8:mountain, l9:valley, l10:valley, l11:valley})


g = g.mirror(p2,[1,0],copy=True)
gaps = gaps.mirror(p2,[1,0],copy=True)
tot_w = (p3-p2+p1)[0]+gap
t = dstack(meshgrid(tot_w*arange(nx)-.5*nx*tot_w,2*h*arange(ny)-ny*h)).reshape(-1,2)
g = g.translate(t)
t_gaps = dstack(meshgrid(tot_w*arange(-1,nx)-.5*nx*tot_w,2*h*arange(ny)-ny*h)).reshape(-1,2)
gaps = gaps.translate(t_gaps)

scene.add_group(g)
scene.add_group(gaps)

scene.write_svg()
scene.display()