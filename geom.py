#!/usr/bin/env python
#geom utils
from numpy import *
from numpy import arctan2 as atan2

def cross(a,b):
    return a[0]*b[1] - a[1]*b[0]
def dot(a,b):
    return a[0]*b[0] + a[1]*b[1]
def angle_between(a,b):
    return atan2(cross(a,b),dot(a,b))
def mag(v):
    return sqrt(dot(v,v))
def mag_squared(v):
    return dot(v,v)
def mirror_p(a,p,v): #mirror point a about a line through point p along vector v
    a = asarray(a)
    p = asarray(p)
    v = asarray(v)/mag(v)
    return -a + 2*p + 2*v*(dot(a-p,v))
def rotate_p(a,p,t):
    p = asarray(p)
    a = asarray(a)-p
    a = [a[0]*cos(t)-a[1]*sin(t), a[0]*sin(t)+a[1]*cos(t)]
    return a+p

def close(p1,p2,tol):
    return (abs(p1-p2)<tol).all()

#compute line-line intersection
def line_line_intersection(p0,v0,p1,v1):
    if v0[1] - v0[0]*v1[1]/v1[0] == 0:
        return None #no intersection
    elif v1[0] != 0:
        s = (p1[1]-p0[1] + v1[1]/v1[0]*(p0[0]-p1[0]))/(v0[1]-v0[0]*v1[1]/v1[0])
        return p0+s*v0
    else:
        t = (p1[0]-p0[0] + v1[0]/v1[1]*(p0[1]-p1[1]))/(v0[0]-v0[1]*v1[0]/v1[1])
        return p0+t*v0
#compute line p->v intersection with circle of radius r centered at c
def line_circle_intersection(p,v,c,r):
    p = asarray(p)
    v = asarray(v)
    c = asarray(c)
    f = p-c
    a = mag_squared(v)
    b = 2*dot(f,v)
    c = mag_squared(f) - r*r
    discrim = b*b - 4*a*c
    if discrim<0:
        return None
    else:
        discrim = sqrt(discrim)
        #return min ray distance answer
        t = [(-b + discrim)/(2*a),(-b - discrim)/(2*a)]
        t = min(t)
        return p+t*v


class GeometryError(Exception):
    """Exception raised for illegal geometry construction -- mostly test at this point
    """
    def __init__(self):
        pass


