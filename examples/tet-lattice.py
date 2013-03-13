#!/usr/bin/env python
from shapes import *
from joinery import EdgeZipper,FaceZipper

l = 1.
res=200
w = 2.
#mid_w = 1.
mat_thick = .0625 + .03
#frac = .2 #percent of radius for inner
zip_length = 1.55


def tp(o=0,i=0):
	t = 2*pi*i/3.
	return o+l*dstack((cos(t),sin(t)))

def closure(r0,r1,os):
	end0 = r0.offset_p(1,os)
	end1 = r1.offset_p(1,-os)
	start0 = r0.offset_p(0,os)
	start1 = r1.offset_p(0,-os)

	return Group({	Line(end0,end1):outside,
				Line(start0,start1):outside
				})
def zip_rails(r0,r1,z):
	scene.add_group(z.run(r0,'left',False))
	scene.add_group(z.run(r1,'right',True))


scene = Scene('tet-lattice',4*l,2*l,'in',.005)
outside = Layer('outside',(0,0,255),scene)
inside = Layer('inside',(255,0,255),scene)
z = EdgeZipper(zip_length,mat_thick,outside,inside)


l1 = Polyline([
		[-l*(1+cos(pi/3)),l*sin(pi/3)],
		[-l,0],
		[0,0],
		[l,0],
		[l*(1+cos(pi/3)),l*sin(pi/3)]
		])

outside.add(l1)

#zip_rails(s0,s1,z)
#scene.add_group(closure(s0,s1,z.connect_offset))


#test
#test = Polyline([[.125*w,0],[.125*w,zip_length+.001]])
#test2 = test.mirror([0,0],[0,1])
#test = test.translate([-w,0])
#test2 = test2.translate([-w,0])


#curf
#outside.offset(.010,'left')
#inside.offset(.010,'right')


scene.write_svg()
#scene.convert('.dxf')
scene.display()
