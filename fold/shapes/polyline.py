#!/usr/bin/env python
#polyline
from shape import *
from .. geom import *

class Polyline(Shape):
    def __init__(self,points,closed=False):
        self.points = asarray(points)
        self.closed = closed
        key = tuple(list(ravel(self.points)))
        Shape.__init__(self,'polyline',key)
    def __repr__(self):
        return 'Polyline['+','.join(['[%f,%f]'%tuple(p) for p in self.points]) + ']'
    def mirror(self,p,v): 
        new_points = []
        for pp in self.points:
            new_points.append(mirror_p(pp,p,v))
        return Polyline(new_points,self.closed)
    def rotate(self,p,t): 
        new_points = []
        for pp in self.points:
            new_points.append(rotate_p(pp,p,t))
        return Polyline(new_points,self.closed)
    def translate(self,v): 
        v = asarray(v)
        return Polyline(v+self.points,self.closed)

    def length(self):
        l = 0
        for i in range(len(self.points)-1):
            l += mag(self.points[i+1]-self.points[i])
        if self.closed:
            l += mag(self.points[-1]-self.points[0])
        return l  
    def evaluate(self,t=0):
        assert(0<=t<=1)
        if t==0:
            return self.points[0]
        elif t==1:
            return self.points[-1]
        else:
            t *= self.length()
            n = len(self.points)
            cum = 0
            for i in range(n if self.closed else n-1):
                li = mag(self.points[(i+1)%n]-self.points[i])
                if cum+li>t:
                    a = (t-cum)/li
                    return (1-a)*self.points[i]+a*self.points[(i+1)%n]
                else:
                    cum += li
    def refine(self,res=100):
        p = [self.evaluate(t) for t in linspace(0,1.,res)]
        return Polyline(p,self.closed)
    def segment(self,t):
        #return the index of line segment in which t lies
        assert(0<=t<=1)
        t *= self.length()
        n = len(self.points)
        cum = 0
        for i in range(n if self.closed else n-1):
            li = mag(self.points[(i+1)%n]-self.points[i])
            if cum+li>=t:
                return i
            else:
                cum += li
    def add_points(self,new_pts):
        if len(self.points) == 0:
            self.points = asarray(new_pts)
        else:
            self.points = vstack((self.points,asarray(new_pts)))
    def sub(self,start,end):
        #return a sub-polyline between parameters start and end
        if end<start:
            tmp = end
            end = start
            start = tmp
        if not 0<=start<=end<=1:
            print 'start=',start, 'end=',end
            assert(False)
        p_start = self.evaluate(start)
        i_start = self.segment(start)
        p_end = self.evaluate(end)
        i_end = self.segment(end)
        new_points = vstack(([p_start],self.points[i_start+1 : i_end],[p_end]))
        return Polyline(new_points,False)

    def normals(self,side='left'):
        #return a list of unit normal vectors at the vertices.  
        norms = []
        angle = -pi/2 if side=='left' else pi/2
        n = len(self.points)
        for i in range(n):
            if i==0 and not self.closed:
                p = self.points[(i+1)%n] - self.points[i]
            elif i==n-1 and not self.closed:
                p = self.points[i] - self.points[(i+n-1)%n]
            else: 
                #central difference when possible   
                p = self.points[(i+1)%n] - self.points[(i+n-1)%n]
            p = rotate_p(p,[0,0],angle)
            #if mag(p)==0:
            #    print 'zero mag',self.points
            p /= mag(p)
            norms.append(p)
        return norms

    def offset(self,d,side='left'):
        ns = self.normals(side)
        new_points = [p+d*n for p,n in zip(self.points,ns)]
        return Polyline(new_points,self.closed)
    def incremental_offset(self,d,side='left',n=10):
        p = self
        for i in range(n):
            p = p.offset(d/n,side)
        return p
    def smooth(self,a=.5,n=1):
        p = self.points
        for trial in range(n):
            for i in range(1,len(p)-1):
                p[i] += a*(.5*(p[i-1]+p[i+1]) - p[i])
        return Polyline(p,self.closed)

    def offset_p(self,t,d,side='left'):
        #offset a point parameterized by t a distance d
        si = self.segment(t)
        n = len(self.points)
        angle = -pi/2 if side=='left' else pi/2
        #not handling open pl
        norm = self.points[(si+1)%n] - self.points[si]
        norm = rotate_p(norm,[0,0],angle)
        norm /= mag(norm)
        return self.evaluate(t) + d*norm


    def strarray(self,s):
        return ["  <path d=\"M%f,%f"%tuple(self.points[0]) + \
                    ''.join([" L%f,%f"%tuple(p) for p in self.points[1:-1]]) +\
                    " L%f,%f"%tuple(self.points[-1]) + \
                    "%s\" />\n"%('Z' if self.closed else '')
                ]

def from_box(pmin,pmax):
    return Polyline([
        pmin,
        [pmax[0],pmin[1]],
        pmax,
        [pmin[0],pmax[1]]
        ],closed=True)


