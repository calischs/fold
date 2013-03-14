#!/usr/bin/env python
from shapes import *
from joinery import EdgeZipper,FaceZipper

l = 2.
res=50
w = .5
#mid_w = 1.
mat_thick = .015
frac = .5 #percent of l for split
zip_length = .49
smooth_a = 1.
smooth_n = 100

def closure_start(r0,r1,os):
	start0 = r0.offset_p(0,os)
	start1 = r1.offset_p(0,-os)

	return Group({Line(start0,start1):outside})
def closure_end(r0,r1,os):
	end0 = r0.offset_p(1,os)
	end1 = r1.offset_p(1,-os)
	return Group({Line(end0,end1):outside})

def zip_rails(r0,r1,z):
	scene.add_group(z.run(r0,'left',False))
	scene.add_group(z.run(r1,'right',True))


scene = Scene('tet-lattice',4*l,3*l,'in',.002)
outside = Layer('outside',(0,0,255),scene)
inside = Layer('inside',(255,0,255),scene)
#other = Layer('other',(0,255,0),scene)
z = EdgeZipper(zip_length,mat_thick,outside,inside)


l1 = Polyline([
		[-l*(1+.5*cos(pi/3)),.5*l*sin(pi/3)],
		[-l,0],
		[-.5*l,0]
		])
l2 = Polyline([
	[-l*(1+.5*cos(pi/3)),.5*l*sin(pi/3)],
	[-l*(1+1.5*cos(pi/3)),1.5*l*sin(pi/3)],

	])		
#other.add(l1)

l1 = l1.offset(.5*w,'right')
l2 = l2.offset(.5*w,'right')
l1 = l1.refine(res).smooth(smooth_a,smooth_n)
l2 = l2.refine(.5*res).smooth(smooth_a,smooth_n)
g = z.run(l1,'right',False)
g = g.rotates([-l,0],[0,2*pi/3,4*pi/3])
h = z.run(l2,'right',False)
h.add_group(z.run(l2.offset(w,'left'),'left',True))
mid = h.rotate([-l,0],-2*pi/3,copy=True)

g.add_group( h)


p11 = l1.offset_p(0,-z.connect_offset)
p12 = l1.rotate([-l,0],2*pi/3).offset_p(1,-z.connect_offset)
l1 = Line(p11,p12).rotate([-l,0],2*pi/3)
p21 = l2.offset_p(1,-z.connect_offset)
p22 = l2.offset(w,'left').offset_p(1,z.connect_offset)

h = Group({l1:outside,Line(p21,p22):outside})
g.add_group(h)

g = g.rotate([0,0],pi,copy=True)
g.add_group(mid)
scene.add_group(g)

#scene.remove_duplicates()
scene.write_svg()
scene.convert('.dxf')
scene.display()
