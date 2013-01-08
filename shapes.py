#!/usr/bin/env python
#shape primitives
from scene import *
from geom import *
from math import pi,sin,cos,atan
from numpy import *


class Line():
    def __init__(self,start,end):
        self.type = 'line'
        self.start = asarray(start) 
        self.end = asarray(end)    
        return
    def key(self):
        return (self.type, self.start[0], self.start[1], self.end[0], self.end[1])
    def __repr__(self):
        return 'Line([%f,%f],[%f,%f])'%(self.start[0],self.start[1],self.end[0],self.end[1])
    def mirror(self,p,v): 
        return Line(mirror_p(self.start,p,v),mirror_p(self.end,p,v))
    def rotate(self,p,t): 
        return Line(rotate_p(asarray(self.start),p,t),rotate_p(asarray(self.end),p,t))
    def translate(self,v): 
        return Line(asarray(self.start)+asarray(v),asarray(self.end)+asarray(v))

    def midpoint(self,t=.5):
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

    def strarray(self,s):
        return ["  <line x1=\"%f\" y1=\"%f\" x2=\"%f\" y2=\"%f\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]

class Circle():
    def __init__(self,center,radius):
        self.type = 'circle'
        self.center = center
        self.radius = radius
        return
    def key(self):
        return (self.type, self.center[0], self.center[1], self.radius)
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

class Ellipse():
    def __init__(self,center,xr,yr,rot):
        self.type = 'ellipse'
        self.center = center
        self.xr  = xr
        self.yr = yr
        self.rot = rot
        return
    def key(self):
        return (self.type, self.center[0], self.center[1], self.xr, self.yr, self.rot)
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

class Arc():
    #draws an arc with center, radius, ccw from th1 to th2
    #right now, angles must be in [-pi,pi)
    def __init__(self,center,radius,th1,th2):
        self.type = 'arc'
        self.center = asarray(center)
        self.radius = radius
        self.th1 = th1
        self.th2 = th2
    def key(self):
        return (self.type, self.center[0], self.center[1], self.radius, self.th1, self.th2)
    def __repr__(self):
        return 'Arc([%f,%f],%f,%f,%f)'%(self.center[0],self.center[1],self.radius,self.th1,self.th2)
    def translate(self,v): 
        return Arc(asarray(self.center)+asarray(v),self.radius,self.th1,self.th2)
    def rotate(self,p,t): 
        return Arc(rotate_p(asarray(self.center),p,t),self.radius,self.th1+t,self.th2+t)
    def mirror(self,p,v): 
        vth = angle_between([1,0],v)
        return Arc(mirror_p(self.center,p,v),self.radius,2*vth-self.th2,2*vth-self.th1)
    def midpoint(self,t=.5):
        t = (1-t)*asarray(self.th1) + t*asarray(self.th2)
        return self.center + self.radius*array([cos(t),sin(t)])
    def length(self):
        return self.radius*(self.th2-self.th1)

    #reflect a point p about the arc at point b.
    def invert(self,p,b):
        b = asarray(b)
        r = b-self.center
        t = array([-r[1],r[0]])
        return mirror_p(p,b,t)

    @classmethod
    def from_3_points(cls,a,b,c): #in ccw order
        #adapted from Joseph O'Rourke, http://www.ics.uci.edu/~eppstein/junkyard/circumcenter.html
        def thing0(aa,bb,cc):
            return (aa[0]**2 + aa[1]**2)*(bb[1]-cc[1])
        def thing1(aa,bb,cc):
            return (aa[0]**2 + aa[1]**2)*(cc[0]-bb[0])
        D = 2*(cross(a,b) + cross(b,c) + cross(c,a))
        cen0 =(thing0(a,b,c) + thing0(b,c,a) + thing0(c,a,b))/D
        cen1 =(thing1(a,b,c) + thing1(b,c,a) + thing1(c,a,b))/D
        R = sqrt((a[0] - cen0)**2 + (a[1] - cen1)**2)
        center = array([cen0,cen1])
        th1 = angle_between(asarray([1,0])-center,asarray(a)-center)
        th2 = angle_between(asarray([1,0])-center,asarray(c)-center)
        return cls([cen0,cen1],R,th1,th2)

    @classmethod
    #constructor from start point, end point, and radius.
    def from_2_points_R(cls,a,b,R):
        a = asarray(a)
        b = asarray(b)
        v = b-a
        n = array([-v[1],v[0]])
        l = R**2 - .25*mag(v)**2
        if l<0: #check if radius to small
            raise(GeometryError())
        l = sqrt(l)
        n *= l/mag(n)
        c = a+.5*v + n
        aa = a-c
        bb = b-c
        th1 = atan2(aa[1],aa[0])
        th2 = atan2(bb[1],bb[0])
        return cls(c,R,th1,th2)

    def strarray(self,s):
        start = [self.center[0]+self.radius*cos(self.th1), self.center[1]+self.radius*sin(self.th1)]
        end = [self.center[0]+self.radius*cos(self.th2), self.center[1]+self.radius*sin(self.th2)]
        large_arc_flag = 0 if self.th2-self.th1 > -pi or self.th1-self.th2 > -pi else 1
        sweep_flag = 1
        return ["  <path d=\"m%f,%f A%f,%f 0 %d,%d %f,%f\"/>\n"%\
                (   start[0],start[1],\
                    self.radius,self.radius,\
                    large_arc_flag, sweep_flag,\
                    end[0],end[1])]

#test
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

