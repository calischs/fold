#!/usr/bin/env python
#shape primitives
from scene import *
from geom import *
from math import pi,sin,cos,atan
from numpy import *

class Shape():
    def __init__(self,t,key):
        self.type = t
        self.key = t+key
    def __repr__(self):
        return 'Shape'
    def mirror(self,p,v):
        raise NotImplementedError
    def rotate(self,p,t):
        raise NotImplementedError
    def translate(self,v):
        raise NotImplementedError
    def evaluate(self,t=.5):
        raise NotImplementedError
    def length(self):
        raise NotImplementedError
    def strarray(self,s):
        raise NotImplementedError


#test
'''
if __name__ == '__main__': 
    scene = Scene('origami-test',8.5,8.5,'in')
    mtn = Layer('mountain',(0,0,255),scene)
    val = Layer('valley',(255,0,0),scene)
    l = Line([0,0],[1,1])
    c = Circle([0,0],sqrt(2))
    g = Group({l:mtn, c:val})
    t = 2*pi*arange(6)/6.
    g = g.translate(2*sqrt(2)*dstack((cos(t),sin(t)))[0])
    scene.add_group(g)
    scene.remove_duplicates()
    scene.write_svg()
    scene.display()
'''