#!/usr/bin/env python
#shape primitives
#from scene import *
#from geom import *
from math import pi,sin,cos,atan
from numpy import *

class Shape():
    def __init__(self,t,key):
        self.type = t
        self.key = tuple(t)+key
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
