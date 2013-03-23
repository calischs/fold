#!/usr/bin/env python
#line
from shapes import *

class Line(Shape):
    def __init__(self,start,end):
        self.start = asarray(start) 
        self.end = asarray(end)    
        key = (start[0], start[1], end[0], end[1])
        Shape.__init__(self,'line',key)
    def __repr__(self):
        return 'Line([%f,%f],[%f,%f])'%(self.start[0],self.start[1],self.end[0],self.end[1])
    def mirror(self,p,v): 
        return Line(mirror_p(self.start,p,v),mirror_p(self.end,p,v))
    def rotate(self,p,t): 
        return Line(rotate_p(asarray(self.start),p,t),rotate_p(asarray(self.end),p,t))
    def translate(self,v): 
        return Line(asarray(self.start)+asarray(v),asarray(self.end)+asarray(v))

    def evaluate(self,t=.5):
        return (1-t)*asarray(self.start) + t*asarray(self.end)
    def length(self):
        return mag(self.end-self.start)
    def perp_thru(self,p):
        pp = asarray(p) - self.start
        v = self.end - self.start
        pp = dot(pp,v)*v/mag_squared(v)
        return Line(p,pp+self.start)
    def perp_to(self,l,t): #perp to self at param t, intersecting another line l
        v = self.end - self.start
        n = array([-v[1],v[0]])
        p0 = self.midpoint(t)
        p = line_line_intersection(p0,n,l.start,l.end-l.start)
        return Line(p0,p)

    def offset(self,d,side='left'):
        n = self.end - self.start
        angle = pi/2 if side=='left' else -pi/2
        n = rotate_p(n,[0,0],angle)
        n /= mag(n)
        return Line(self.start+d*n, self.end+d*n)
    def to_polyline(self):
        return Polyline([self.start,self.end],False)
    def slope(self):
        v = self.end - self.start
        if v[0]==0 and v[1] == 0:
            return float('nan')
        elif v[0]==0 and v[1] != 0:
            return float('inf')
        else:
            return v[1]/v[0]
    def merge(self,other,tol=.001):
        #attempt to merge another line into self.  
        #on success return true, on fail return false
        #TODO: test for partial overlap
        #TODO: make tol commesurate
        parallel = abs(self.slope() - other.slope())<tol
        if parallel:
            if close(self.start, other.start, tol) and close(self.end, other.end, tol):
                return True
            elif close(self.end, other.start, tol):
                self.end = other.end
                return True
            elif close(other.end, self.start, tol): 
                self.start = other.start
                return True
            else:
                return False
        else:
            return False

    def strarray(self,s):
        return ["  <line x1=\"%f\" y1=\"%f\" x2=\"%f\" y2=\"%f\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]

