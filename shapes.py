#!/usr/bin/env python
"""\
SVG.py - Construct/display SVG scenes.

Adapted from:
http://code.activestate.com/recipes/325823-draw-svg-images-in-python/
"""

import os,sys
from math import pi,sin,cos
display_prog = 'display' # Command to execute to display images.

class Scene:
    def __init__(self,name="svg",height=11,width=8.5,units="in"):
        self.name = name
        self.layers = []
        self.height = height
        self.width = width
        self.units = units
        return

    def add_layer(self,layer): 
        print 'adding layer:',layer
        self.layers.append(layer)

    def strarray(self):
        var = ["<?xml version=\"1.0\" ?>\n",
               "<svg xmlns=\"http://www.w3.org/2000/svg\"\n",
               "  height=\"%f%s\" width=\"%f%s\" \n" % (self.height,self.units,self.width,self.units),
               "  units=\"%s\"\n"%(self.units),
               "  viewBox=\"0 0 %f %f\">\n"%(self.width,self.height),
               " <g fill=\"none\" stroke-width=\"%f\"\n"%(self.width/1000),
               "    transform=\"translate(%f,%f) scale(1, -1)\">\n"%\
               (.5*self.width,.5*self.height)]
        print 'writing',self.layers
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

    def display(self,prog=display_prog):
        os.system("%s %s" % (prog,self.svgname))
        return

def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)


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

    def add(self,item): self.items.append(item)

    def strarray(self):
#        var = ["<g style=\"stroke:%s;\">\n" % colorstr(self.color)]
        var = ["<g stroke=\"%s\">\n" % colorstr(self.color)]
        for item in self.items: var += item.strarray(self.scene)
        var += [" </g>\n"]
        return var


#shape primitives
class Line:
    def __init__(self,start,end):
        self.start = start #xy tuple
        self.end = end     #xy tuple
        return

    def strarray(self,s):
        return ["  <line x1=\"%f\" y1=\"%f\" x2=\"%f\" y2=\"%f\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]

class Circle:
    def __init__(self,center,radius):
        self.center = center #xy tuple
        self.radius = radius #xy tuple
        return

    def strarray(self,s):
        return ["  <circle cx=\"%f\" cy=\"%f\" r=\"%f\"/>\n" %\
                (self.center[0],self.center[1],self.radius)]

class Arc:
    #draws an arc with center, radius, ccw from th1 to th2
    #right now, angles must be in [0,2*pi)
    def __init__(self,center,radius,th1,th2):
        self.center = center
        self.radius = radius
        self.th1 = th1
        self.th2 = th2

    def strarray(self,s):
        start = [self.center[0]+self.radius*cos(self.th1), self.center[1]+self.radius*sin(self.th1)]
        end = [self.center[0]+self.radius*cos(self.th2), self.center[1]+self.radius*sin(self.th2)]
        large_arc_flag = 0 if self.th2-self.th1 < pi else 1
        sweep_flag = 1
        return ["  <path d=\"M%f,%f A%f,%f 0 %d,%d %f,%f\"/>\n"%\
                (   start[0],start[1],\
                    self.radius,self.radius,\
                    large_arc_flag, sweep_flag,\
                    end[0],end[1]),
                "  <circle cx=\"%f\" cy=\"%f\" r=\".125\"/>\n" %\
                (start[0],start[1]),
                "  <circle cx=\"%f\" cy=\"%f\" r=\".25\"/>\n" %\
                (end[0],end[1]),]

#test routine
def test():
    scene = Scene('origami-test',11,8.5,'in')
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
#    val.add(Circle([-1,0],.5))
#    val.add(Circle([0,-1],.5))
    val.add(Arc([0,0],1.25,pi/4,3*pi/4))
    cut.add(Line([-1,-1],[-1,1]))
    scene.write_svg()
    scene.display()
    return

if __name__ == '__main__': test()


