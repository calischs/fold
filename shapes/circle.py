#!/usr/bin/env python
#circle
from shapes import *

class Circle(Shape):
    def __init__(self,center,radius):
        self.center = center
        self.radius = radius
        key = (center[0], center[1], radius)
        Shape.__init__('circle',key)
    def __repr__(self):
        return 'Circle([%f,%f],%f)'%(self.center[0],self.center[1],self.radius)
    def translate(self,v): 
        return Circle(asarray(self.center)+asarray(v),self.radius)
    def rotate(self,p,t): 
        return Circle(rotate_p(asarray(self.center),p,t),self.radius)
    def mirror(self,p,v): 
        return Circle(mirror_p(self.center,p,v),self.radius)
    def strarray(self,s):
        return ["  <circle cx=\"%f\" cy=\"%f\" r=\"%f\"/>\n" %\
                (self.center[0],self.center[1],self.radius)]
    def length(self):
        return 2*pi*self.radius
    def offset(self,d,side='left'):
        diff = d if side=='right' else -d
        return Circle(self.center,self.radius + d)