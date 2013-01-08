#!/usr/bin/env python
from shapes import *

def mirror_x(p):
	return mirror_p(p,[0,0],[1,0])
def mirror_y(p):
	return mirror_p(p,[0,0],[0,1])

scene = Scene('oru',5.,10.,'in')
mtn = Layer('mountain',(0,0,255),scene)
val = Layer('valley',(255,0,0),scene)
cut = Layer('cut',(255,0,255),scene)

cockpit_hl = 1.
keel_tri_l = 2.
keel_tri_w = .5
chine_w = .5
gunwale_w = .5
deck_hw = .75

chine_dart_angle = 10.*pi/180.
gunwhale_dart_angle = 10.*pi/180.

stem_pos = 4.
stem_base = .75
stem_height = .75

p1 = array([.5*keel_tri_w,cockpit_hl])
p2 = p1 + array([chine_w,0.])
p3 = p2 + array([gunwale_w,0.])
p4 = p3 + array([deck_hw,0.])

p5 = array([0.,cockpit_hl+keel_tri_l]) #apex
p6 = array([0.,stem_pos])
p7 = p6 + array([0.,stem_base])
p8 = p7 + array([stem_height,0.])

nose = Line(p6,p8)
apex = Line(p1,p5)
outer = Line(p4,p8)

chine = Arc.from_2_points_R(p8,p3,15.)
gunwhale = Arc.from_2_points_R(nose.midpoint(),p2,30.)

vert = Group({
	Line(p1,mirror_x(p1)):val,
	Line(p2,mirror_x(p2)):val,
	Line(p3,mirror_x(p3)):val,
	apex:val,
	Line(p5,p6):val,
	Line(p6,p7):val,
	nose:val,
	Line(p7,p8):val,
	chine:val,
	gunwhale:val,
	outer:cut,
	Line(p4,mirror_x(p4)):cut
	})

p9 = line_circle_intersection(p2,array([cos(chine_dart_angle),sin(chine_dart_angle)]),chine.center,chine.radius)
p10 = line_circle_intersection(p2,array([cos(.5*chine_dart_angle),sin(.5*chine_dart_angle)]),chine.center,chine.radius)

p11 = line_line_intersection(p9,array([cos(chine_dart_angle+gunwhale_dart_angle),sin(chine_dart_angle+gunwhale_dart_angle)]),outer.start,outer.end-outer.start)
p12 = line_line_intersection(p10,array([cos(.5*chine_dart_angle+.5*gunwhale_dart_angle),sin(.5*chine_dart_angle+.5*gunwhale_dart_angle)]),outer.start,outer.end-outer.start)

dart11 = Line(p2,p9)
dart12 = Line(p9,p11)
dart21 = Line(p2,p10)
dart22 = Line(p10,p12)


hor = Group({
	Line(p1,mirror_y(p1)):val,
	Line(p1,p2):val,
	Line(p2,p3):mtn,
	Line(p3,p4):mtn,
	dart11:mtn,
	dart12:mtn,
	dart21:val,
	dart22:val,
	apex.perp_to(outer,1.):val
	})

g = vert
g.add_group(hor)

g = g.mirror([0,0],[1,0],copy=True)
g = g.mirror([0,0],[0,1],copy=True)

scene.add_group(g)
scene.write_svg()
scene.display()
#scene.convert('.dxf')