#!/usr/bin/env python
from shapes import *

#Ron Resch tesselation

l = 1.25 #triangle circumradius
n = 3 #twice number in height
m = 3 #twice number in width
#r = l/40. #radius of thickened slits
r = .025
print 'radius=',r
print 'dimensions=%.2fx%.2f'%(3*(m)*l,sqrt(3)*(n+.5)*l)

def Thick(p0,p1,r,f=1.):
	p0 = asarray(p0)
	p1 = asarray(p1)
	v = p1-p0
	l = mag(v)
	v = v/l
	p0 = p0 + .5*(1-f)*v*l
	p1 = p1 - .5*(1-f)*v*l
	p = array([-v[1],v[0]])
	l1 = Line(p0+r*p,p1+r*p)
	l2 = Line(p0-r*p,p1-r*p)
	l3 = Line(p0-r*p,p0+r*p)
	l4 = Line(p1-r*p,p1+r*p)
#	a1 = Arc.from_3_points(p0+r*p, p1-r*v, p1-r*p)
#	a2 = Arc.from_3_points(p1-r*p, p1+r*v, p1+r*p)
	return (l1,l2,l3,l4)

scene = Scene('resch',3*(m+.5)*l,sqrt(3)*(n+1)*l,'in',.01)
mountain = Layer('mountain',(0,0,255),scene)
cut = Layer('cut',(255,0,255),scene)
valley = Layer('valley',(0,255,0),scene)

p0 = l*array([-1., 0.])
p1 = l*array([0., sqrt(3)/3.])
p2 = l*array([-1/2., -sqrt(3)/6.])

cap0 = Thick(p0,p1,r,.7)
cap1 = Thick(p1,p2,r,.8)
cap2 = Thick(p0,p2,r,.8)
g = Group({	cap0[0]:valley,cap0[1]:valley,cap0[2]:valley,cap0[3]:valley,\
			cap1[0]:mountain,cap1[1]:mountain,cap1[2]:mountain,cap1[3]:mountain,\
			cap2[0]:mountain,cap2[1]:mountain,cap2[2]:mountain,cap2[3]:mountain})
g = g.rotates([0,0],2*pi*arange(3)/3.)
g = g.mirror(p0,p1-p0,copy=True)
g = g.mirror([.5*l,0],[0,1],copy=True)
tn = sqrt(3)*l*(arange(n)-n/2.+.25).reshape(1,-1,1)*array([[0,1]])
tm = 3*l*(arange(m)-m/2.+.25).reshape(-1,1,1)*array([[1,0]])
g = g.translate((tn+tm).reshape(-1,2))

scene.add_group(g)

pts = 1.5*l*(arange(2*m+1)-m-.1666).reshape(-1,1)*array([1,0]) + .5*sqrt(3)*(l*((arange(2*m+1)+1)%2-n-.5)).reshape(-1,1)*array([0,1]) 
pts2 = pts + sqrt(3)*n*l*array([0,1])
pts = vstack((pts,pts2[::-1]))
outline = Group({Line(pts[i],pts[(i+1)%len(pts)]):cut for i in range(len(pts))})
scene.add_group(outline)

#scene.remove_duplicates()
scene.write_svg()
scene.display()

#make cut files
cut1 = Scene.from_scene(scene,'resch-cut1')
cut1.add_layers([mountain,cut])
cut1.write_svg()
cut1.convert('.dxf')

cut2 = Scene.from_scene(scene,'resch-cut2')
valley.mirror([0,0],[1,0]) #mirror about horizontal for material flip
cut.mirror([0,0],[1,0])
cut2.add_layers([valley,cut]) 
cut2.write_svg()
cut2.convert('.dxf')