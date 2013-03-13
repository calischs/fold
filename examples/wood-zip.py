#!/usr/bin/env python
from shapes import *
from joinery import EdgeZipper,FaceZipper

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

res=200
l = 12.
w = 2.
mid_w = 1.
mat_thick = .0625 + .03
frac = .2 #percent of radius for inner
zip_length = 1.55


scene = Scene('zip',5*w,l+1,'in',.005)
outside = Layer('outside',(0,0,255),scene)
inside = Layer('inside',(255,0,255),scene)



p0 = asarray([.5*w,-.5*l])
p1 = asarray([.5*mid_w,0])
p2 = p1
p3 = asarray([.5*w,.5*l])
s0 = CubicBezier(p0,p1,p2,p3).to_polyline(res)

p0 = asarray([frac*.5*w,-.5*l])
p1 = asarray([frac*.5*mid_w,0])
p2 = p1
p3 = asarray([frac*.5*w,.5*l])
i0 = CubicBezier(p0,p1,p2,p3).to_polyline(res)

p0 = asarray([(1-frac)*.25*w,-.5*l])
p1 = asarray([(1-frac)*.25*mid_w,0])
p2 = p1
p3 = asarray([(1-frac)*.25*w,.5*l])
t0 = CubicBezier(p0,p1,p2,p3).to_polyline(res)

s1 = s0.mirror([0,0],[0,1])
i1 = i0.mirror([0,0],[0,1])
t1 = t0.mirror([0,0],[0,1])

t0 = t0.translate([w,0])
t1 = t1.translate([w,0])



z = EdgeZipper(zip_length,mat_thick,outside,inside)
zf = FaceZipper(zip_length,mat_thick,outside,inside)
ze = EdgeZipper(zip_length,mat_thick,outside,inside)

zip_rails(s0,s1,z)
zip_rails(i0,i1,zf)
zip_rails(t0,t1,ze)

#test
test = Polyline([[.125*w,0],[.125*w,zip_length+.001]])
test2 = test.mirror([0,0],[0,1])
test = test.translate([-w,0])
test2 = test2.translate([-w,0])

zip_rails(test,test2,z)
scene.add_group(closure(test,test2,z.connect_offset))

scene.add_group(closure(s0,s1,z.connect_offset))
scene.add_group(closure(t0,t1,z.connect_offset))

#curf
#outside.offset(.010,'left')
#inside.offset(.010,'right')


scene.write_svg()
scene.convert('.dxf')
scene.display()

sys.exit(0)

