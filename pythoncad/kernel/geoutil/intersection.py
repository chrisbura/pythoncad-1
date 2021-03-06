#
# Copyright (c) 2002, 2003, 2006 Art Haas
#
# Copyright (c) 2010 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# code to calculate if or where two objects intersect
#

# from __future__ import division

import math

from kernel.geoentity.point       import Point
from kernel.geoentity.segment     import Segment
from kernel.geoentity.arc         import Arc
from kernel.geoentity.cline       import CLine
from kernel.geoentity.ccircle     import CCircle
from kernel.geoentity.polyline    import Polyline
from kernel.geoentity.ellipse     import Ellipse
from kernel.geoutil.geolib        import Vector
#
# common constants
#

_dtr = math.pi/180.0
_rtd = 180.0/math.pi

_zero = 0.0 - 1e-10
_one = 1.0 + 1e-10

#
# the following functions are used to calculate the
# intersection of two line segments
#
# see comp.graphics.algorithms FAQ for details
#

def denom(p1, p2, p3, p4):
    if not isinstance(p1, Point):
        raise TypeError, "Invalid argument to denom(): " + `type(p1)`
    if not isinstance(p2, Point):
        raise TypeError, "Invalid argument to denom(): " + `type(p2)`
    if not isinstance(p3, Point):
        raise TypeError, "Invalid argument to denom(): " + `type(p3)`
    if not isinstance(p4, Point):
        raise TypeError, "Invalid argument to denom(): " + `type(p4)`
    _p1x, _p1y = p1.getCoords()
    _p2x, _p2y = p2.getCoords()
    _p3x, _p3y = p3.getCoords()
    _p4x, _p4y = p4.getCoords()
    return ((_p2x - _p1x)*(_p4y - _p3y)) - ((_p2y - _p1y)*(_p4x - _p3x))

def rnum(p1, p2, p3, p4):
    if not isinstance(p1, Point):
        raise TypeError, "Invalid argument to rnum(): " + `type(p1)`
    if not isinstance(p2, Point):
        raise TypeError, "Invalid argument to rnum(): " + `type(p2)`
    if not isinstance(p3, Point):
        raise TypeError, "Invalid argument to rnum(): " + `type(p3)`
    if not isinstance(p4, Point):
        raise TypeError, "Invalid argument to rnum(): " + `type(p4)`
    _p1x, _p1y = p1.getCoords()
    _p2x, _p2y = p2.getCoords()
    _p3x, _p3y = p3.getCoords()
    _p4x, _p4y = p4.getCoords()
    return ((_p1y - _p3y)*(_p4x - _p3x)) - ((_p1x - _p3x)*(_p4y - _p3y))

def snum(p1, p2, p3, p4):
    if not isinstance(p1, Point):
        raise TypeError, "Invalid argument to snum(): " + `type(p1)`
    if not isinstance(p2, Point):
        raise TypeError, "Invalid argument to snum(): " + `type(p2)`
    if not isinstance(p3, Point):
        raise TypeError, "Invalid argument to snum(): " + `type(p3)`
    if not isinstance(p4, Point):
        raise TypeError, "Invalid argument to snum(): " + `type(p4)`
    _p1x, _p1y = p1.getCoords()
    _p2x, _p2y = p2.getCoords()
    _p3x, _p3y = p3.getCoords()
    _p4x, _p4y = p4.getCoords()
    return ((_p1y - _p3y)*(_p2x - _p1x)) - ((_p1x - _p3x)*(_p2y - _p1y))




#
# intersection functions
#

def _null_intfunc(ipts, obja, objb):
    print "invoked _null_intfunc()"
    print "obja: " + `obja`
    print "objb: " + `objb`

def _non_intersecting(ipts, obja, objb):
    pass
#
# Ellipse intersection function
#
def _sympy_intersection(ipts, obj1, obj2):
    """
        calculate the intersection beteen polyline and segment
    """
    from sympy.geometry import Point as sPoint
    from sympy.geometry import intersection as sIntersection
    sympySegment=obj1.getSympy()
    sympyObj2=obj2.getSympy()
    #print "try intersect ", sympySegment, sympyObj2
    iObjs=sIntersection(sympySegment, sympyObj2 )
    #print "iObjs", iObjs
    for p in iObjs:
        if isinstance(p, sPoint):
            ipts.append((float(p[0]),float(p[1])))
    #print "Intersection",ipts
def _pol_obj_intersection(ipts, pol, obj):
    """
        calculate the intersection beteen polyline and a generic object
    """
    for seg in pol.getSegments():
        tempIpts=[]
        _sympy_intersection(tempIpts,  seg,  obj)
        if len(tempIpts)>0:
            ipts=tempIpts
            break

def _pol_pol_intersection(ipts, pol1, pol2):
    """
        found an intersection between polyline and other object
    """
    if isinstance(pol1, Polyline):
        if isinstance(pol2, Polyline):
            for seg1 in pol1.getSegments():
                for seg2 in pol2.getSegments():
                    tempIpts=[]
                    _sympy_intersection(tempIpts,  seg1,  seg2)
                    if len(tempIpts)>0:
                        ipts=tempIpts
                        break

def find_intersections(obja, objb):
    """
        Find intersection points
    """
    _ipts=[]
    if isinstance(obja,Polyline) or isinstance(objb,Polyline):
        if isinstance(obja,Polyline) and isinstance(objb,Polyline):
            _pol_pol_intersection(_ipts, obja, objb)
        else:
            if isinstance(objb,Polyline):
                sp=obja
                obja=objb
                objb=sp
            _pol_obj_intersection(_ipts, obja, objb)

    else:
            try:
                _sympy_intersection(_ipts, obja, objb)
            except:
                print "find_intersections: problem with sympy intersection",obja,objb
    return _ipts

def findSegmentExtendedIntersection(obja, objb):
    """
        Extend the segment intersection on a cline intersection
        Return an [(x,y),(x1,y1),...]
    """
    if isinstance(obja, Segment):
        p1, p2=obja.getEndpoints()
        arg={"CLINE_0":p1, "CLINE_1":p2}
        obja=CLine(arg)
    if isinstance(objb, Segment):
        p1, p2=objb.getEndpoints()
        arg={"CLINE_0":p1, "CLINE_1":p2}
        objb=CLine(arg)
    return find_intersections(obja, objb)

def findSegmentExtendedIntersectionPoint(obja, objb):
    """
        xtend the segment intersection on a cline intersection
        Return a [Point,Point,..]
    """
    return [Point(x, y) for x, y in findSegmentExtendedIntersection(obja, objb)]

