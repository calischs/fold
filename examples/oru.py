#!/usr/bin/env python
from shapes import *

#this is the worst script ever written.  need to introduce structure

def mirror_x(p):
	return mirror_p(p,[0,0],[1,0])
def mirror_y(p):
	return mirror_p(p,[0,0],[0,1])

scene = Scene('oru',5.,10.,'in')
mtn = Layer('mountain',(0,0,255),scene)
val = Layer('valley',(255,0,0),scene)
cut = Layer('cut',(255,0,255),scene)

cockpit_hl = 1.
keel_tri_l = 1.75
keel_tri_w = .5
chine_w = .25
gunwale_w = .5
deck_hw = .5

fore_chine_dart_angle = 5.*pi/180.
fore_gunwhale_dart_angle = 5.*pi/180.
aft_chine_dart_angle = 10.*pi/180.
aft_gunwhale_dart_angle = 10.*pi/180.

fore_stem_pos = 4.
fore_stem_base = .75
fore_stem_height = .75
aft_stem_pos = 4.25
aft_stem_base = .5
aft_stem_height = .5
stem_undercut = .15

deck_tab_w = 1./12

p1 = array([.5*keel_tri_w,cockpit_hl])
p2 = p1 + array([chine_w,0.])
p3 = p2 + array([gunwale_w,0.])
p4 = p3 + array([deck_hw,0.])

p5 = array([0.,cockpit_hl+keel_tri_l]) #apex
p6 = array([0.,fore_stem_pos])
p6_aft = array([0.,-aft_stem_pos])
p7 = p6 + array([0.,fore_stem_base-stem_undercut])
p7_aft = p6_aft - array([0.,aft_stem_base-stem_undercut])
p8 = p7 + array([fore_stem_height,stem_undercut])
p8_aft = p7_aft - array([-aft_stem_height,stem_undercut])

apex = Line(p1,p5)
inner = Line(p7,p8)
inner_aft = Line(p7_aft,p8_aft)
nose = Line(p6,inner.midpoint(.9))
nose_aft = Line(p6_aft,inner_aft.midpoint(.9))
outer = Line(p4,p8) #this won't actually be in pattern
outer_aft = Line(mirror_x(p4),p8_aft)

chine = Arc.from_2_points_R(inner.midpoint(.95),p3,15.)
chine_aft = Arc.from_2_points_R(mirror_x(p3),inner_aft.midpoint(.95),15.)
gunwhale = Arc.from_2_points_R(nose.midpoint(),p2,30.)
gunwhale_aft = Arc.from_2_points_R(mirror_x(p2),nose_aft.midpoint(),30.)
apex_aft = apex.mirror([0,0],[1,0])

vert = Group({
	Line(p1,mirror_x(p1)):val,
	Line(p2,mirror_x(p2)):val,
	Line(p3,mirror_x(p3)):val,
	apex:val,
	apex_aft:val,
	Line(p5,p6):val,
	Line(mirror_x(p5),p6_aft):val,
	Line(p6,p7):mtn,
	Line(p6_aft,p7_aft):mtn,
	nose:val,
	nose_aft:val,
	chine:val,
	chine_aft:val,
	gunwhale:val,
	gunwhale_aft:val,
	})

p9 = line_circle_intersection(p2,array([cos(fore_chine_dart_angle),sin(fore_chine_dart_angle)]),chine.center,chine.radius)
p10 = line_circle_intersection(p2,array([cos(.5*fore_chine_dart_angle),sin(.5*fore_chine_dart_angle)]),chine.center,chine.radius)

p11 = line_line_intersection(p9,array([cos(fore_chine_dart_angle+fore_gunwhale_dart_angle),sin(fore_chine_dart_angle+fore_gunwhale_dart_angle)]),outer.start,outer.end-outer.start)
p12 = line_line_intersection(p10,array([cos(.5*fore_chine_dart_angle+.5*fore_gunwhale_dart_angle),sin(.5*fore_chine_dart_angle+.5*fore_gunwhale_dart_angle)]),outer.start,outer.end-outer.start)

dart_fore_11 = Line(p2,p9)
dart_fore_12 = Line(p9,p11)
dart_fore_21 = Line(p2,p10)
dart_fore_22 = Line(p10,p12)
dart_fore_22 = Line(p10,dart_fore_22.midpoint(.95))


p2_aft = mirror_x(p2)
cc_aft = mirror_x(chine.center)
p9_aft = line_circle_intersection(p2_aft,array([cos(-aft_chine_dart_angle),sin(-aft_chine_dart_angle)]),cc_aft,chine.radius)
p10_aft = line_circle_intersection(p2_aft,array([cos(-.5*aft_chine_dart_angle),sin(-.5*aft_chine_dart_angle)]),cc_aft,chine.radius)

os_aft = mirror_x(outer.start)
oe_aft = mirror_x(outer.end)
p11_aft = line_line_intersection(p9_aft,array([cos(-aft_chine_dart_angle-aft_gunwhale_dart_angle),sin(-aft_chine_dart_angle-aft_gunwhale_dart_angle)]),os_aft,oe_aft-os_aft)
p12_aft = line_line_intersection(p10_aft,array([cos(-.5*aft_chine_dart_angle-.5*aft_gunwhale_dart_angle),sin(-.5*aft_chine_dart_angle-.5*aft_gunwhale_dart_angle)]),os_aft,oe_aft-os_aft)


dart_aft_11 = Line(p2_aft,p9_aft)
dart_aft_12 = Line(p9_aft,p11_aft)
dart_aft_21 = Line(p2_aft,p10_aft)
dart_aft_22 = Line(p10_aft,p12_aft)
dart_aft_22 = Line(p10_aft,dart_aft_22.midpoint(.95))

darts = Group({
		dart_fore_11:mtn,
		dart_fore_12:mtn,
		dart_fore_21:val,
		dart_fore_22:val,
		dart_aft_11:mtn,
		dart_aft_12:mtn,
		dart_aft_21:val,
		dart_aft_22:val
		})

tab_n_fore = rotate_p(p8-p12,0,-pi/2)
tab_n_aft = rotate_p(p8_aft-p12_aft,0,pi/2)
tab_n_fore *= deck_tab_w/mag(tab_n_fore)
tab_n_aft *= deck_tab_w/mag(tab_n_aft)


hor = Group({
	Line(p1,mirror_y(p1)):val,
	Line(p1,mirror_y(p1)).mirror([0,0],[1,0]):val,
	Line(p1,p2):val,
	Line(p1,p2).mirror([0,0],[1,0]):val,
	Line(p2,p3):mtn,
	Line(p2,p3).mirror([0,0],[1,0]):mtn,
	Line(p3,p4):mtn,
	Line(p3,p4).mirror([0,0],[1,0]):mtn,
	apex.perp_to(outer,1.):val,
	apex_aft.perp_to(outer_aft,1.):val
	})

mid_fore_deck = Line(dart_fore_12.end,p8)
mid_fore_deck_tab = mid_fore_deck.translate(tab_n_fore)
mid_aft_deck = Line(dart_aft_12.end,p8_aft)
mid_aft_deck_tab = mid_aft_deck.translate(tab_n_aft)
mid_coam = Line(p4,mirror_x(p4))

p4_aft = mirror_x(p4)
c = Group({
	Line(p4,dart_fore_22.end):cut,
	Line(p4_aft,dart_aft_22.end):cut,
	Line(dart_fore_22.end,dart_fore_12.end):cut,
	Line(dart_aft_22.end,dart_aft_12.end):cut,
	mid_fore_deck:val,
	mid_aft_deck:val,
	mid_fore_deck_tab:cut,
	mid_aft_deck_tab:cut,
	Line(mid_fore_deck.start,mid_fore_deck_tab.start):cut,
	Line(mid_aft_deck.start,mid_aft_deck_tab.start):cut,
	Line(mid_fore_deck.end,mid_fore_deck_tab.end):cut,
	Line(mid_aft_deck.end,mid_aft_deck_tab.end):cut,
	inner:cut,
	inner_aft:cut
	})


#make groups
g = vert
g.add_group(hor)
#g = g.mirror([0,0],[1,0],copy=True)
g.add_group(c)
g.add_group(darts)

c1 = mid_coam.midpoint(.05)
c2 = mid_coam.midpoint(.95)
coam = CubicBezier(c1,c1+array([-.25,0.]),c2+array([-.75,0.]),c2)
coaming = Group({
	coam:cut,
	Line(c1,p4):cut,
	Line(c2,mirror_x(p4)):cut
	})

g.add_group(coaming)

g = g.mirror([0,0],[0,1],copy=True)

scene.add_group(g)
scene.remove_duplicates()
scene.write_svg()
scene.display()
scene.convert('.dxf')