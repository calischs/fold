#!/usr/bin/env python
"""\
SVG.py - Construct/display SVG scenes.

Adapted from:
http://code.activestate.com/recipes/325823-draw-svg-images-in-python/
"""

import os,sys
from math import pi,sin,cos,atan
from numpy import *
from geom import *

def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

class Scene:
    def __init__(self,name="svg",height=11,width=8.5,units="in"):
        self.name = name
        self.layers = []
        self.height = height
        self.width = width
        self.units = units
        return

    def add_layer(self,layer): 
        self.layers.append(layer)

    def add_group(self,group):
        for item,layer in group.items.iteritems():
            layer.add(item)

    def strarray(self):
        var = ["<?xml version=\"1.0\" ?>\n",
               "<svg xmlns=\"http://www.w3.org/2000/svg\"\n",
               "  height=\"%f%s\" width=\"%f%s\" \n" % (self.height,self.units,self.width,self.units),
               "  units=\"%s\"\n"%(self.units),
               "  viewBox=\"0 0 %f %f\">\n"%(self.width,self.height),
               " <g fill=\"none\" stroke-width=\"%f\"\n"%(self.width/1000),
               "    transform=\"translate(%f,%f) scale(1, -1)\">\n"%\
               (.5*self.width,.5*self.height)]
        for layer in self.layers: 
            var += layer.strarray()
        var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return

    def display(self,prog='display'):
        os.system("%s %s &" % (prog,self.svgname))
        return

    def convert(self,format='.ps'):
        if format=='.ps':
            os.system('inkscape %s.svg -P %s.ps' % (self.name,self.name) )
        if format=='.dxf':
            os.system('inkscape %s.svg -P %s.tmp.ps' % (self.name,self.name) )
            os.system('pstoedit %s.tmp.ps -f dxf:-ctl %s.dxf' % (self.name,self.name) )
            os.system('rm %s.tmp.ps' % (self.name))
        return 


#layers will hold groups of shapes with same attributes
class Layer:
    def __init__(self,name,color,scene):
        self.color = color
        self.items = []
        self.name = name
        self.scene = scene
        scene.add_layer(self)
    def __repr__(self):
        return self.name

    def add(self,item): 
        try: self.items.extend(item)
        except(TypeError):
            self.items.append(item)

    def strarray(self):
        var = ["<g stroke=\"%s\">\n" % colorstr(self.color)]
        for item in self.items: var += item.strarray(self.scene)
        var += [" </g>\n"]
        return var

#this will allow instancing, transforms, etc. on a group
class Group:
    def __init__(self,items=None):
        self.items={}
        if items:
            for item,layer in items.iteritems():
                self.items[item] = layer

    def add(self,items):
        for item,layer in items.iteritems():
            self.items[item] = layer

    def mirror(self,p,v,copy=False):
        new = {}
        if copy:
            new.update(self.items)
        for item,layer in self.items.iteritems():
            new[item.mirror(p,v)] = layer
        return Group(new)

    def rotate(self,p,t,copy=False):
        new = {}
        if copy:
            new.update(self.items)
        for item,layer in self.items.iteritems():
                new[item.rotate(p,t)] = layer
        return Group(new)

    def translate(self,ts,copy=False):
        new = {}
        if copy:
            new.update(self.items)
        for t in ts:
            for item,layer in self.items.iteritems():
                new[item.translate(t)] = layer
        return Group(new)

#shape primitives
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
        return Circle(mirror_p(self.center,p,v),radius)

    def strarray(self,s):
        return ["  <circle cx=\"%f\" cy=\"%f\" r=\"%f\"/>\n" %\
                (self.center[0],self.center[1],self.radius)]

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
    cut = Layer('cut',(255,0,255),scene)

    mtn.add(Line([0,0],[1,1]))
    mtn.add(Line([0,0],[-1,1]))
    mtn.add(Line([0,0],[-1,-1]))
    val.add(Line([0,0],[1,-1]))
    mtn.add(Circle([0,0],1))
    val.add(Circle([1,0],.5))
    val.add(Circle([0,1],.5))
    val.add(Arc([0,0],1.25,pi/4,3*pi/4))
    cut.add(Arc.from_3_points([sqrt(3),1],[0.,2.],[-sqrt(3),1]))
    cut.add(Arc.from_3_points([-sqrt(3),1],[-2.,0.],[-sqrt(3),-1]))
    cut.add(Arc.from_3_points([-sqrt(3),-1],[0.,-2.],[sqrt(3),-1]))
    cut.add(Arc.from_3_points([sqrt(3),-1],[2.,0.],[sqrt(3),1]))
    mtn.add(Circle([0,0],2.))
    cut.add(Line([-1,-1],[-1,1]))
    l = Line([-4,0],[4,-4])
    cut.add(l)
    cut.add(l.mirror([0,0],[0,1]))
    scene.write_svg()
    scene.display()
    scene.convert()
    return

if __name__ == '__main__': test()


