#!/usr/bin/env python
#spline
from shapes import *

class CubicBezier(Shape):
    def __init__(self,p0,p1,p2,p3):
        self.p0 = asarray(p0)
        self.p1 = asarray(p1)
        self.p2 = asarray(p2)
        self.p3 = asarray(p3)
        key = (p0[0],p0[1],p1[0],p1[1],p2[0],p2[1],p3[0],p3[1])
        Shape.__init__('spline',key)
    def __repr__(self):
        return 'CubicBezier['+','.join(['[%f,%f]'%tuple(p) for p in [self.p0,self.p1,self.p2,self.p3]]) + ']'
    def mirror(self,p,v): 
        p0 = mirror_p(self.p0,p,v)
        p1 = mirror_p(self.p1,p,v)
        p2 = mirror_p(self.p2,p,v)
        p3 = mirror_p(self.p3,p,v)
        return CubicBezier(p0,p1,p2,p3)
    def rotate(self,p,t): 
        p0 = rotate_p(self.p0,p,t)
        p1 = rotate_p(self.p1,p,t)
        p2 = rotate_p(self.p2,p,t)
        p3 = rotate_p(self.p3,p,t)
        return CubicBezier(p0,p1,p2,p3)
    def translate(self,v): 
        v = asarray(v)
        return CubicBezier(self.p0+v,self.p1+v,self.p2+v,self.p3+v)
    def evaluate(self,t=.5):
        return self.p0*(1-t)**3 + self.p1*(3*t*(1-t)**2) + self.p2*(3*(1-t)*t**2) + self.p3*t**3;
    def to_polyline(self,res=100):
        t = arange(0,1.,1./res).reshape(-1,1)
        p = self.evaluate(t)
        return Polyline(p,False)
    def length(self):
        raise NotImplementedError
    def strarray(self,s):
        return ["  <path d=\"M%f,%f C%f,%f, %f,%f, %f,%f\" />\n" %\
                (self.p0[0],self.p0[1],self.p1[0],self.p1[1],self.p2[0],self.p2[1],self.p3[0],self.p3[1])]

