#!/usr/bin/env python
#joinery abstract class and children
from numpy import *
from geom import *
from shapes import *
from scene import *

class Joinery():
	def __init__(self,l,mat_thick,outer,inner,connect_offset):
		self.l = l
		self.mat_thick = mat_thick
		self.outer = outer #cut layer
		self.inner = inner #internal layer	
		self.connect_offset = connect_offset
	def unit(self):
		#a unit of the joinery in a coordinate system
		# x->offset, y->along (in units of l)
		return Group(None)
	def run(self,pl,side='left',mirror=False):
		#run joinery along a polyline
		n = int(pl.length()/self.l)
		ds = self.l/pl.length()
		start = .5*(pl.length()-n*self.l)/pl.length()
		g = Group(None)
		unit = self.unit()
		if mirror:
			unit = unit.mirror([0,.5],[1,0])
		for j in range(n):
			t = start + j*ds
			for item,layer in unit.items.iteritems():
				assert(item.type == 'polyline') #for now
				np = len(item.points)
				for i in range(np if item.closed else np-1):
					p0 = item.points[i]
					p1 = item.points[(i+1)%np]
					d = p1 - p0
					if d[0]==0:
						s = t+ds*p0[1]
						e = t+ds*p1[1]
						sub_pl = pl.sub(s, e).offset(p0[0],side)
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
		if self.connect_offset:
			pl_sub = pl.sub(0.,start).offset(self.connect_offset,side)
			g.add({pl_sub:self.outer})
			t = start + (n)*ds
			pl_sub = pl.sub(t,1.).offset(self.connect_offset,side)
			g.add({pl_sub:self.outer})
		return g

	def runs(self,pls,sides='left',mirrors=False):
		g = Group(None)
		if type(sides)==list and type(mirrors)==list:
			for pl,side,mir in zip(pls,sides,mirrors):
				g.add_group(self.run(pl,side,mir))
		else:
			#no mixing and matching	
			side = sides
			mir = mirrors
			for pl in pls:
				g.add_group(self.run(pl,side,mir))
		return g

#Zipper edge-type joinery
class EdgeZipper(Joinery):
	def __init__(self,l,mat_thick,outer,inner):
		Joinery.__init__(self,l,mat_thick,outer,inner,-.5*mat_thick)
	def unit(self):
		m = self.mat_thick
		pl = Polyline(asarray([	
			[-.5*m,0],
			[-.5*m,.1],
			[1.*m,.1],
			[1.*m,.4],
			[-.5*m,.4],
			[-.5*m,.53],
			[2.*m,.53],
			[2.*m,.97],
			[-.5*m,.97],
			[-.5*m,1.]]),
			False
			)
		pl2 = Polyline(asarray([
			[-.5*m,.6],
			[.5*m,.6],
			[.5*m,.9],
			[-.5*m,.9]]),
			closed=True
			)
		return Group({pl:self.outer,pl2:self.inner})

#zipper face-time joinery
class FaceZipper(Joinery):
	def __init__(self,l,mat_thick,outer,inner):
		Joinery.__init__(self,l,mat_thick,outer,inner,None)
	def unit(self):
		m = self.mat_thick
		hole = Polyline(asarray([	
			[-.5*m,.1],
			[.5*m,.1],
			[.5*m,.4],
			[-.5*m,.4]]),
			closed=True)
		tab_hole = Polyline(asarray([
			[1.5*m,.52],
			[-.5*m,.52],
			[-.5*m,.6],
			[.5*m,.6],
			[.5*m,.9],
			[-.5*m,.9],
			[-.5*m,.98],
			[1.5*m,.98],
			]),
			closed=True)
		return Group({hole:self.inner, tab_hole:self.inner})	






