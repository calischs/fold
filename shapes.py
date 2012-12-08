#!/usr/bin/env python
#shape primitives
from scene import *
from geom import *
from math import pi,sin,cos,atan
from numpy import *

class Line:
    def __init__(self,start,end):
        self.start = start 
        self.end = end    
        return

    def mirror(self,p,v): #mirror about line through point p along vector v
        return Line(mirror_p(self.start,p,v),mirror_p(self.end,p,v))
    def rotate(self,p,t): #rotate about p by t radians
        return Line(rotate_p(asarray(self.start),p,t),rotate_p(asarray(self.end),p,t))
    def translate(self,v): #translate along v
        return Line(asarray(self.start)+asarray(v),asarray(self.end)+asarray(v))

    def strarray(self,s):
        return ["  <line x1=\"%f\" y1=\"%f\" x2=\"%f\" y2=\"%f\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]

class Circle:
    def __init__(self,center,radius):
        self.center = center
        self.radius = radius
        return

    def translate(self,v): #translate along v
        return Circle(asarray(self.center)+asarray(v),self.radius)
    def rotate(self,p,t): #rotate about p by t radians
        return Circle(rotate_p(asarray(self.center),p,t),self.radius)
    def mirror(self,p,v): #mirror about line through point p along vector v
        return Circle(mirror_p(self.center,p,v),self.radius)

    def strarray(self,s):
        return ["  <circle cx=\"%f\" cy=\"%f\" r=\"%f\"/>\n" %\
                (self.center[0],self.center[1],self.radius)]

class Ellipse:
    def __init__(self,center,xr,yr,rot):
        self.center = center
        self.xr  = xr
        self.yr = yr
        self.rot = rot
        return

    def translate(self,v): #translate along v
        return Ellipse(asarray(self.center)+asarray(v),self.xr,self.yr,self.rot)
    def rotate(self,p,t): #rotate about p by t radians
        return Ellipse(rotate_p(asarray(self.center),p,t),self.xr,self.yr,self.rot+t)
    def mirror(self,p,v): #mirror about line through point p along vector v
        return Ellipse(mirror_p(self.center,p,v),self.xr,self.yr, pi - self.rot)

    def strarray(self,s):
        return ["  <ellipse transform=\"rotate(-%f)\" cx=\"%f\" cy=\"%f\" rx=\"%f\" ry=\"%f\"/>\n" %\
                (self.rot,self.center[0],self.center[1],self.xr,self.yr)]

class Arc:
    #draws an arc with center, radius, ccw from th1 to th2
    #right now, angles must be in [-pi,pi)
    def __init__(self,center,radius,th1,th2):
        self.center = center
        self.radius = radius
        self.th1 = th1
        self.th2 = th2

    def translate(self,v): #translate along v
        return Arc(asarray(self.center)+asarray(v),self.radius,self.th1,self.th2)
    def rotate(self,p,t): #rotate about p by t radians
        return Arc(rotate_p(asarray(self.center),p,t),self.radius,self.th1+t,self.th2+t)
    def mirror(self,p,v): #mirror about line through point p along vector v
        vth = angle_between([1,0],v)
        return Arc(mirror_p(self.center,p,v),self.radius,2*vth-self.th2,2*vth-self.th1)

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

#test routine
def test():
    scene = Scene('origami-test',8.5,8.5,'in')
    mtn = Layer('mountain',(0,0,255),scene)
    val = Layer('valley',(255,0,0),scene)
    l = Line([0,0],[1,1])
    c = Circle([0,0],sqrt(2))
    g = Group({l:mtn, c:val})
    t = 2*pi*arange(6)/6.
    g = g.translate(2*sqrt(2)*dstack((cos(t),sin(t)))[0])
    scene.add_group(g)
    scene.write_svg()
    scene.display()
    return

if __name__ == '__main__': test()


