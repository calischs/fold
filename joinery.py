#!/usr/bin/env python
#joinery
from numpy import *
from geom import *
from shapes import *
from scene import *

#TODO: write polyline offseting with intelligent normals
#TODO: then write zipper in terms of offsets to keep the exact
#metric of the polyline


class Zipper():
	def __init__(self,l,mat_thick,outer,inner):
		self.l = l
		self.mat_thick = mat_thick
		self.outer = outer #cut layer
		self.inner = inner #internal layer

	#this division is kind of artificial.
	def unit(self,base,along,inward):
		along = asarray(along)/mag(along)
		inward = asarray(inward)/mag(inward)
		base = asarray(base)
		i = Line(base,base+.75*self.l*along)
		ci = Circle(base+self.mat_thick*inward + self.l*along,.5*self.mat_thick)
		o = Line(base+inward*self.mat_thick, base+.75*self.l*along+inward*self.mat_thick)
		co = Circle(base+self.mat_thick*inward,.5*self.mat_thick)
		return Group({	i:self.inner, ci:self.inner, \
						o:self.outer, co:self.outer})
	def run_along(self,pl,side='left'):
		#run a zipper along a polyline
		g = Group(None)
		n = int(pl.length()/self.l)
		ds = self.l/(pl.length()+.5)
		start = .5*(pl.length()-n*self.l) #start
		for i in range(n-1):
			base = pl.point(start + i*ds)
			along = pl.point(start + (i+1)*ds) - base
			inward = array([-along[1],along[0]] if side=='left' else [along[1],-along[0]]) 
			g.add_group(self.unit(base,along,inward))
		return g