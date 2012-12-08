#!/usr/bin/env python
from shapes import *

#this script generates flexures to exhibit a stress-strain step function.  They 
#are designed to be flexible within a prescribed strain range, then the stress
#should spike.  In order to eliminate out-of-plane behavior, the parameter t should
#be less than material thickness, say half.

m = 10 #number of rows thetally
n=m+2 #number of rows axially, should be even.
l = .75 #base length
scene = Scene('stent',n*l+1,m*l+1,'in',.01)
mountain = Layer('mountain',(0,0,255),scene)
cut = Layer('cut',(255,0,255),scene)
valley = Layer('valley',(0,255,0),scene)
holes = Layer('holes',(255,0,255),scene)

lin1 = Line([0,0],[.5*l,0])
lin2 = Line([0,.5*l],[.5*l,0])
lin3 = Line([0,0],[0,.5*l])
lin4 = Line([0,.5*l],[.5*l,.5*l])
g = Group({lin1:mountain,lin2:valley,lin3:mountain,lin4:mountain})

g = g.mirror([.5*l,0],[0,1],copy=True)
g = g.translate(array([[0,0],[l,.5*l]]))
g = g.mirror([0,.5*l],[1,0],copy=True)

na = 2*l*(arange(n/2)-n/4.).reshape(-1,1) * array([1,0])
ma = l*(arange(m)-m/2).reshape(-1,1,1) * array([0,1])
t = (na+ma).reshape(-1,2)
g = g.translate( t)

scene.add_group(g)

pts = [[-.5*n*l,-.5*m*l],
		[.5*n*l,-.5*m*l],
		[.5*n*l,.5*m*l],
		[-.5*n*l,.5*m*l]]
outline = Group({Line(pts[i],pts[(i+1)%len(pts)]):cut for i in range(len(pts))})
scene.add_group(outline)

#make lacing holes
hole_diam = .020 
hole = Group({Circle([0,0],.5*hole_diam):holes})
hole = hole.translate(array([[.15*l,0],[.35*l,0]]))
hole = hole.mirror([0,0],[0,1],copy=True)
hole = hole.translate( l*(arange(n)-n/2+.5).reshape(-1,1)*array([[1,0]]) )
hole = hole.translate((.5*l*m-.05)*array([[0,1],[0,-1]]))
scene.add_group(hole)

scene.remove_duplicates()
scene.write_svg()
scene.display()

#make cut files
cut1 = Scene.from_scene(scene,'stent-cut1')
cut1.add_layers([mountain,cut,holes])
cut1.write_svg()

cut2 = Scene.from_scene(scene,'stent-cut2')
valley.mirror([0,0],[1,0]) #mirror about horizontal for material flip
holes.mirror([0,0],[1,0])
cut2.add_layers([valley,holes]) 
cut2.write_svg()
