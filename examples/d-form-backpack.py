#!/usr/bin/env python
from shapes import *

#this script generates flexures to exhibit a stress-strain step function.  They 
#are designed to be flexible within a prescribed strain range, then the stress
#should spike.  In order to eliminate out-of-plane behavior, the parameter t should
#be less than material thickness, say half.

ma = 18 #length of semimajor axis
mi = 12 #length of semiminor axis

scene = Scene('d-form-backpack',2*ma,2*mi,'in',.01)
cut = Layer('cut',(255,0,255),scene)

ell = Ellipse([0,0],ma,mi,0)
cut.add(ell)

#calculate zipper length
h = (ma-mi)/(ma+mi)
p = pi*(ma+mi)*(1+3*h/(10+sqrt(4-3*h))) #Ramanujan's approximation of elliptic perimeter

scene.write_svg()
scene.display()
print "Zipper length = %f" % p
scene.convert('.dxf')