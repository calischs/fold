#!/usr/bin/env python
#joinery abstract class and children
from numpy import *
from geom import *
from shapes import *
from scene import *

class Joinery():
	def __init__(self,l,mat_thick,outer,inner):
		self.l = l
		self.mat_thick = mat_thick
		self.outer = outer #cut layer
		self.inner = inner #internal layer	
	def unit(self):
		#a unit of the joinery in a coordinate system
		# x->offset, y->along (in units of l)
		return Group(None)
	def run(self,pl,side='left'):
		#run joinery along a polyline
		n = int(pl.length()/self.l)
		ds = self.l/pl.length()
		start = .5*(pl.length()-n*self.l)
		g = Group(None)
		for j in range(n-1):
			t = start + j*ds
			for item,layer in self.unit().items.iteritems():
				assert(item.type == 'polyline') #for now
				np = len(item.points)
				for i in range(np):
					#this will only work for unit consisting
					#of horizontal and vertical line segments...
					p0 = item.points[i]
					p1 = item.points[(i+1)%np]
					d = p1 - p0
					if d[0]==0:
						s = t+ds*p0[1]
						e = t+ds*p1[1]
						print j,s,e
						sub_pl = pl.sub(s, e)
						sub_pl = sub_pl.offset(p0[0],side)
						#this is sloppy at edges...
						g.add({sub_pl:layer})
					elif d[1]==0:
						q0 = pl.offset_p( t+ds*p0[1],p0[0],side)
						q1 = pl.offset_p( t+ds*p1[1],p1[0],side)
						g.add({Line(q0,q1):layer})
					else:
						#maybe assume these are small and
						#just offset the endpoints?
						raise NotImplementedError
		return g

#Zipper edge-type joinery
class Zipper(Joinery):
	def __init__(self,l,mat_thick,outer,inner):
		Joinery.__init__(self,l,mat_thick,outer,inner)
	def unit(self):
		m = self.mat_thick
		pl = Polyline(asarray([	[-.5*m,.2],\
								[.5*m,.2],\
								[.5*m,.3],\
								[0,.3],\
								[0,.7],\
								[.5*m,.7],\
								[.5*m,.8],\
								[-.5*m,.8]]),
					closed=True
					)
		return Group({pl:self.inner})

#zipper face-time joinery
class FaceZipper(Joinery):
	def __init__(self,l,mat_thick,outer,inner):
		Joinery.__init__(self,l,mat_thick,outer,inner)
	def unit(self):
		m = self.mat_thick
		pl = Polyline(asarray([	[-.5*m,.2],\
								[.5*m,.2],\
								[.5*m,.3],\
								[0,.3],\
								[0,.7],\
								[.5*m,.7],\
								[.5*m,.8],\
								[-.5*m,.8]]),
					closed=True
					)
		return Group({pl:self.inner})	


#other: gear joinery, ben's zipper, ...





