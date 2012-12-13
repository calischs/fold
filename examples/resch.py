#!/usr/bin/env python
from shapes import *
#Ron Resch tesselation

l = .5 #triangle circumradius
n = 6 #twice number in height
m = 6 #twice number in width

scene = Scene('resch',3*(m+.5)*l,sqrt(3)*(n+1)*l,'in',.01)
mountain = Layer('mountain',(0,0,255),scene)
cut = Layer('cut',(255,0,255),scene)
valley = Layer('valley',(0,255,0),scene)

p0 = l*array([-1., 0.])
p1 = l*array([0., sqrt(3)/3.])
p2 = l*array([-1/2., -sqrt(3)/6.])

lin0 = Line(p0,p1)
lin1 = Line(p1,p2)
lin2 = Line(p0,p2)
g = Group({lin0:valley,lin1:mountain,lin2:mountain})
g = g.rotates([0,0],2*pi*arange(3)/3.)
g = g.mirror(p0,p1-p0,copy=True)
g = g.mirror([.5*l,0],[0,1],copy=True)
tn = sqrt(3)*l*(arange(n)-n/2+.25).reshape(1,-1,1)*array([[0,1]])
tm = 3*l*(arange(m)-m/2+.25).reshape(-1,1,1)*array([[1,0]])
g = g.translate((tn+tm).reshape(-1,2))

scene.add_group(g)

pts = [[(-1.5*m-.25)*l,.5*sqrt(3)*(n+.5)*l],
		[(1.5*m-.25)*l,.5*sqrt(3)*(n+.5)*l],
		[(1.5*m-.25)*l,-.5*sqrt(3)*(n+.5)*l],
		[(-1.5*m-.25)*l,-.5*sqrt(3)*(n+.5)*l]]
outline = Group({Line(pts[i],pts[(i+1)%len(pts)]):cut for i in range(len(pts))})
scene.add_group(outline)

scene.remove_duplicates()
scene.write_svg()
scene.display()

#make cut files
cut1 = Scene.from_scene(scene,'resch-cut1')
cut1.add_layers([mountain,cut])
cut1.write_svg()

cut2 = Scene.from_scene(scene,'resch-cut2')
valley.mirror([0,0],[1,0]) #mirror about horizontal for material flip
cut2.add_layers([valley]) 
cut2.write_svg()
