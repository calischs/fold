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