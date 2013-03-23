#!/usr/bin/env python
#ellipse
from shapes import *

class Ellipse(Shape):
    def __init__(self,center,xr,yr,rot):
        self.center = center
        self.xr  = xr
        self.yr = yr
        self.rot = rot
        key = (center[0], center[1], xr, yr, rot)
        Shape.__init__('ellipse',key)
    def __repr__(self):
        return 'Ellipse([%f,%f],%f,%f,%f)'%(self.center[0],self.center[1],self.xr,self.yr,self.rot)
    def translate(self,v):
        return Ellipse(asarray(self.center)+asarray(v),self.xr,self.yr,self.rot)
    def rotate(self,p,t): 
        return Ellipse(rotate_p(asarray(self.center),p,t),self.xr,self.yr,self.rot+t)
    def mirror(self,p,v):
        return Ellipse(mirror_p(self.center,p,v),self.xr,self.yr, pi - self.rot)

    def strarray(self,s):
        return ["  <ellipse transform=\"rotate(-%f)\" cx=\"%f\" cy=\"%f\" rx=\"%f\" ry=\"%f\"/>\n" %\
                (self.rot,self.center[0],self.center[1],self.xr,self.yr)]
