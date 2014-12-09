#!/usr/bin/env python

import sys
import os
import string
import types
import math
import time
import base64
from curves import *

try:
    # New Python 2.6 way of spawning subprocesses
    import subprocess
    def popen2(command):
        p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, \
                                 stdout=subprocess.PIPE, close_fds=True)
        return (p.stdin, p.stdout)
except ImportError, e:
    # Old-style fallback, deprecated in 2.6
    from os import popen2

class GlyphContext:
    def __init__(self):
        self.curves = {}
        self.curveid = 0
        self.canvas = self # simplest thing :-)
        self.extra = self.before = ""

        # Scale in units per inch. 1900 happens to be the scale at
        # which I drew most of these glyphs; unhelpfully, the real
        # scale used by Lilypond (and Mus) is 3600.
        self.scale = 1900 # default unless otherwise specified
        # Location of the glyph's origin, in output coordinates
        # (i.e. the location in the glyph's own coordinates will be
        # this, divided by 3600, multiplied by self.scale).
        self.origin = 1000, 1000
        # Default size of canvas (in glyph coordinates) on which we
        # will display the image.
        self.canvas_size = 1000, 1000
        # Default extra resolution factor over the glyph coordinates
        # used for rendering to potrace.
        self.trace_res = 4
        # Default number of points to interpolate along each curve.
        self.curve_res = 1001
    def create_line(self, *args, **kw):
        return None
    def delete(self, *args, **kw):
        pass
    def makeps(self):
        out = "gsave 1 setlinecap\n"
        out = out + self.before + "\n"
        for cid, curve in self.curves.items():
            for it in range(self.curve_res):
                t = it / float(self.curve_res-1)
                x, y = curve.compute_point(t)
                nib = curve.compute_nib(t)
                if type(nib) == types.TupleType:
                    radius, angle, fdist, bdist = nib
                    c = cos(angle)
                    s = -sin(angle)
                    out = out + "newpath %g %g moveto %g %g lineto %g setlinewidth stroke\n" % \
                    (x+c*fdist, y+s*fdist, x-c*bdist, y-s*bdist, 2*radius)
                elif nib != 0:
                    out = out + "newpath %g %g %g 0 360 arc fill\n" % (x, y, nib)
        e = self.extra
        if not (type(e) == types.TupleType or type(e) == types.ListType):
            e = (e,)
        for ee in e:
            if type(ee) == types.StringType:
                out = out + ee + "\n"
            else:
                out = out + ee.makeps()
        out = out + "\ngrestore\n"
        return out
    def testdraw(self):
        print "gsave clippath flattenpath pathbbox 0 exch translate"
        print "1 -1 scale pop pop pop"
        print self.makeps()
        print "grestore showpage"

# Python doesn't have the ?: operator, bah.
def qc(cond,t,f):
    if cond:
        return t
    else:
        return f

# UTF-7 encoding, ad-hocked to do it the way Fontforge wants it done
# (encoding control characters and double quotes, in particular).
def utf7_encode(s):
    out = ""
    b64 = ""
    # Characters we encode directly: RFC 2152's Set D, plus space.
    ok = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'(),-./:? "
    for c in s + "\0":
        assert ord(c) < 128 # we support ASCII only
        if not (c in ok):
            b64 = b64 + "\0" + c
        else:
            if b64 != "":
                b64 = base64.b64encode(b64)
                b64 = string.replace(b64, "\n", "") # just in case
                b64 = string.replace(b64, "=", "")
                out = out + "+" + b64 + "-"
                b64 = ""
            if c != '\0':
                out = out + c
        
    return out

# 2x2 matrix multiplication.
def matmul((a,b,c,d),(e,f,g,h)):
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)
# 2x2 matrix inversion.
def matinv((a,b,c,d)):
    det = a*d-b*c
    return (d/det, -b/det, -c/det, a/det)

# Turn a straight line from (0,0) to (1,1) into a quadratic curve
# hitting the same two points but passing through (1/2,1/2-k)
# instead of (1/2,1/2).
def depress(t,k):
    return t - t*(1-t)*4*k

# Nib helper function which sets up a chisel nib with one end on the
# curve and the other end at a specified other point.
def ptp_nib(c,x,y,t,theta,x1,y1,nr):
    angle = atan2(y-y1, x1-x)
    dist = sqrt((y-y1)**2 + (x1-x)**2)
    return nr, angle, dist, 0

# Nib helper function which sets up a chisel nib with one end
# following the curve and the other end following a completely
# different curve or chain of curves.
def follow_curveset_nib(c,x,y,t,theta,carray,i,n,r):
    tt = (t + i) * len(carray) / n
    ti = int(tt)
    if ti == len(carray):
        ti = ti - 1
    x1, y1 = carray[ti].compute_point(tt-ti)
    return ptp_nib(c,x,y,t,theta,x1,y1,r)

# Function which draws a blob on the end of a line.
def blob(curve, end, whichside, radius, shrink, nibradius=None):
    if nibradius == None:
        nibradius = curve.compute_nib(end)
        assert type(nibradius) != types.TupleType
    x, y = curve.compute_point(end)
    dx, dy = curve.compute_direction(end)
    if end == 0:
        dx, dy = -dx, -dy
    dlen = sqrt(dx*dx + dy*dy)
    dx, dy = dx/dlen, dy/dlen
    if whichside == 'r':
        nx, ny = -dy, dx
    elif whichside == 'l':
        nx, ny = dy, -dx
    # We want to draw a near-circle which is essentially a single
    # involute going all the way round, so that its radius shrinks
    # from 'radius' to (radius-shrink) on the way round. That means
    # it needs to unwind once round a circle of circumference
    # 'shrink'.
    r = shrink/(2*pi)
    cx = x + radius*nx - r*dx
    cy = y + radius*ny - r*dy
    for i in range(4):
        if whichside == 'r':
            newnx, newny = -ny, nx
        elif whichside == 'l':
            newnx, newny = ny, -nx
        radius = radius - shrink/4.
        newx = cx - r*nx - radius*newnx
        newy = cy - r*ny - radius*newny
        newcurve = CircleInvolute(curve.cont, x, y, dx, dy, newx, newy, nx, ny)
        x, y, dx, dy, nx, ny = newx, newy, nx, ny, newnx, newny
        newcurve.nib = lambda c,x,y,t,theta: ptp_nib(c,x,y,t,theta,cx,cy,nibradius)

# Construct a PostScript path description which follows the centre
# of some series of curve objects and visits other points in
# between. Used to arrange that one quaver tail doesn't go past
# another.
def clippath(elements):
    coords = []
    for e in elements:
        if type(e) == types.InstanceType:
            # Curve.
            for it in range(e.cont.curve_res):
                t = it / float(e.cont.curve_res-1)
                coords.append(e.compute_point(t))
        else:
            # Plain coordinate pair.
            coords.append(e)
    for i in range(len(coords)):
        if i == 0:
            coords[i] = "%g %g moveto" % coords[i]
        else:
            coords[i] = "%g %g lineto" % coords[i]
    coords.append("closepath")
    return " ".join(coords)

def update_bbox(bbox, x, y):
    x0,y0,x1,y1 = bbox
    if x0 == None:
        x0,y0,x1,y1 = x,y,x,y
    else:
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, x)
        y1 = max(y1, y)
    return x0,y0,x1,y1

def bezfn(x0, x1, x2, x3, t):
    return x0*(1-t)**3 + 3*x1*(1-t)**2*t + 3*x2*(1-t)*t**2 + x3*t**3

def break_curve(x0,y0, x1,y1, x2,y2, x3,y3):
    # We must differentiate the separate cubics for the curve's x and
    # y coordinates, find any stationary points in [0,1], and break
    # the curve at those points.
    #
    # A single coordinate of a Bezier curve has the equation
    #
    #  x = x0 (1-t)^3 + 3 x1 (1-t)^2 t + 3 x2 (1-t) t^2 + x3 t^3
    #    = x0 (1-3t+3t^2-t^3) + 3 x1 (t-2t^2+t^3) + 3 x2 (t^2-t^3) + x3 t^3
    #    = t^3 (x3-3x2+3x1-x0) + t^2 (3x2-6x1+3x0) + t (3x1-3x0) + x0
    #
    # and hence its derivative is at^2+bt+c where
    #  a = 3(x3-3x2+3x1-x0)
    #  b = 6(x2-2x1+x0)
    #  c = 3(x1-x0)
    breakpts = [(0,0),(1,0)]
    for (axis,c0,c1,c2,c3) in ((1,x0,x1,x2,x3),(2,y0,y1,y2,y3)):
        a = 3*(c3-3*c2+3*c1-c0)
        b = 6*(c2-2*c1+c0)
        c = 3*(c1-c0)
        #sys.stderr.write("%d: a=%g b=%g c=%g\n" % (axis, a, b, c))
        tlist = ()
        if a == 0:
            if b != 0:
                breakpts.append((-c/b,axis))
        else:
            disc = b*b-4*a*c
            if disc >= 0:
                rdisc = math.sqrt(disc)
                breakpts.append(((-b + rdisc)/(2*a),axis))
                breakpts.append(((-b - rdisc)/(2*a),axis))
    breakpts.sort()
    curves = []
    #sys.stderr.write("break %g,%g %g,%g %g,%g %g,%g:\n" % (x0,y0,x1,y1,x2,y2,x3,y3))
    #sys.stderr.write("   at %s\n" % repr(breakpts))
    for i in range(len(breakpts)-1):
        (t0, axis0) = breakpts[i]
        (t1, axis1) = breakpts[i+1]
        if 0 <= t0 and t0 < t1 and t1 <= 1:
            nx0 = bezfn(x0,x1,x2,x3,t0)
            ny0 = bezfn(y0,y1,y2,y3,t0)
            nx3 = bezfn(x0,x1,x2,x3,t1)
            ny3 = bezfn(y0,y1,y2,y3,t1)
            nx1 = nx0 + (t1-t0) * ((x3-3*x2+3*x1-x0)*t0**2 + 2*(x2-2*x1+x0)*t0 + (x1-x0))
            ny1 = ny0 + (t1-t0) * ((y3-3*y2+3*y1-y0)*t0**2 + 2*(y2-2*y1+y0)*t0 + (y1-y0))
            nx2 = nx3 - (t1-t0) * ((x3-3*x2+3*x1-x0)*t1**2 + 2*(x2-2*x1+x0)*t1 + (x1-x0))
            ny2 = ny3 - (t1-t0) * ((y3-3*y2+3*y1-y0)*t1**2 + 2*(y2-2*y1+y0)*t1 + (y1-y0))
            if axis0 == 1:
                nx1 = nx0
            elif axis0 == 2:
                ny1 = ny0
            if axis1 == 1:
                nx2 = nx3
            elif axis1 == 2:
                ny2 = ny3
            curves.append((nx0,ny0,nx1,ny1,nx2,ny2,nx3,ny3))
            #sys.stderr.write("  got %g,%g %g,%g %g,%g %g,%g\n" % curves[-1])
    return curves

# Use potrace to compute the PS path outline of any glyph.
def get_ps_path(char, debug=None):
    path = []
    xsize, ysize = char.canvas_size
    res = char.trace_res
    if debug == None:
        tee1 = tee2 = ""
    else:
        tee1 = " | tee z1.%s" % debug
        tee2 = " | tee z2.%s" % debug
    fin, fout = popen2("gs -sDEVICE=pbm -sOutputFile=- -g%dx%d -r%d -dBATCH -dNOPAUSE -q -%s | potrace -b ps -c -q -W 1in -H 1in -r 4000 -M 1000 -O 1 -o - -%s" % (xsize*res, ysize*res, 72*res, tee1, tee2))
    fin.write("0 %d translate 1 -1 scale\n" % ysize)
    fin.write(char.makeps())
    fin.write("showpage")
    fin.close()
    # Now we read and parse potrace's PostScript output. This is easy
    # enough if we've configured potrace to output as simply as
    # possible (which we did) and are also ignoring most of the fiddly
    # bits, which we are. I happen to know that potrace (as of v1.8 at
    # least) transforms its coordinate system into one based on tenths
    # of a pixel measured up and right from the lower left corner, so
    # I'm going to ignore the scale and translate commands and just
    # skip straight to parsing the actual lines and curves on that
    # basis.
    psstack = []
    pscurrentpoint = None, None
    output = "newpath"
    scale = 4.0 / char.trace_res
    while 1:
        s = fout.readline()
        if s == "": break
        if s[:1] == "%":
            continue # comment
        ss = string.split(s)
        for word in ss:
            if word[:1] in "-0123456789":
                psstack.append(float(word))
            elif word == "gsave":
                pass # ignore
            elif word == "grestore":
                pass # ignore
            elif word == "showpage":
                pass # ignore
            elif word == "scale":
                psstack.pop(); psstack.pop() # ignore
            elif word == "translate":
                psstack.pop(); psstack.pop() # ignore
            elif word == "setgray":
                psstack.pop() # ignore
            elif word == "newpath":
                pscurrentpoint = None, None
            elif word == "moveto" or word == "rmoveto":
                y1 = psstack.pop(); x1 = psstack.pop()

                x0, y0 = pscurrentpoint
                if word == "moveto":
                    x1, y1 = x1, y1
                else:
                    assert x0 != None
                    x1, y1 = x1 + x0, y1 + y0
                pscurrentpoint = x1, y1
                path.append(('m', x1*scale, y1*scale))
            elif word == "lineto" or word == "rlineto":
                y1 = psstack.pop(); x1 = psstack.pop()

                x0, y0 = pscurrentpoint
                if word == "moveto":
                    x1, y1 = x1, y1
                else:
                    assert x0 != None
                    x1, y1 = x1 + x0, y1 + y0
                pscurrentpoint = x1, y1
                path.append(('l', x0*scale, y0*scale, x1*scale, y1*scale))
            elif word == "curveto" or word == "rcurveto":
                y3 = psstack.pop(); x3 = psstack.pop()
                y2 = psstack.pop(); x2 = psstack.pop()
                y1 = psstack.pop(); x1 = psstack.pop()
                x0, y0 = pscurrentpoint
                assert x0 != None
                if word == "curveto":
                    x1, y1 = x1, y1
                    x2, y2 = x2, y2
                    x3, y3 = x3, y3
                else:
                    x1, y1 = x1 + x0, y1 + y0
                    x2, y2 = x2 + x0, y2 + y0
                    x3, y3 = x3 + x0, y3 + y0
                pscurrentpoint = x3, y3
                for c in break_curve(x0*scale,y0*scale,x1*scale,y1*scale,\
                x2*scale,y2*scale,x3*scale,y3*scale):
                    path.append(('c',) + c)
            elif word == "closepath":
                path.append(('cp',))
    fout.close()
    bbox = None, None, None, None
    for c in path:
        if c[0] != 'cp':
            bbox = update_bbox(bbox, c[-2], c[-1])
    return bbox, path

# Wrapper on os.system() that enforces a success return.
def system(cmd):
    ret = os.system(cmd)
    assert ret == 0

# ----------------------------------------------------------------------
# G clef (treble).
#
# The G clef is drawn in two parts. First, we have a connected
# sequence of curves which draws the main outline of the clef (with
# varying stroke width as detailed below). But at the very top of
# the clef, the two edges of the thick stroke diverge: the outside
# of the curve is pointy, but the inside curves round smoothly. So
# we have a secondary context containing an alternative version of
# the top two curves (c6,c7), used as the inner smooth curve. The
# actual drawing uses the main context, but with an exciting nib
# function for c6 and c7 which moves one end of the nib along the
# main curve while the other tracks the curves in the secondary
# context.

def tmpfn():
    # Secondary curves.
    tmp = cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 603, 161, -0.33035, -0.943858, 563, 145, -0.943858, 0.33035)
    c1 = CircleInvolute(cont, 563, 145, -0.943858, 0.33035, 504.709, 289.062, 0.208758, 0.977967)
    c0.weld_to(1, c1, 0)
    # End saved data
    tc0, tc1 = c0, c1

    # Main context.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 528, 654, -0.90286, -0.429934, 569, 507, 1, 0)
    c1 = CircleInvolute(cont, 569, 507, 1, 0, 666, 607, 0, 1)
    c2 = CircleInvolute(cont, 666, 607, 0, 1, 549, 715, -1, 0)
    c3 = CircleInvolute(cont, 549, 715, -1, 0, 437, 470, 0.581238, -0.813733)
    c4 = CircleInvolute(cont, 437, 470, 0.581238, -0.813733, 536, 357, 0.731055, -0.682318)
    c5 = CircleInvolute(cont, 536, 357, 0.731055, -0.682318, 603, 161, -0.33035, -0.943858)
    c6 = CircleInvolute(cont, 603, 161, -0.33035, -0.943858, 559, 90, -0.83205, -0.5547)
    c7 = CircleInvolute(cont, 559, 90, -0.77193, 0.635707, 500, 267, 0.211282, 0.977425)
    c8 = StraightLine(cont, 500, 267, 605.66, 762)
    c9 = ExponentialInvolute(cont, 606, 762, 0.211282, 0.977425, 598, 856, -0.514496, 0.857493)
    c10 = CircleInvolute(cont, 598, 856, -0.514496, 0.857493, 446, 865, -0.633238, -0.773957)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c6, 0)
    c6.weld_to(1, c7, 0, 1)
    c7.weld_to(1, c8, 0)
    c8.weld_to(1, c9, 0)
    c9.weld_to(1, c10, 0)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: 17+11*cos(theta-c.nibdir(t))
    c0.nibdir = c1.nibdir = c2.nibdir = lambda t: 0
    phi = c4.compute_theta(1)
    c3.nibdir = lambda t: phi*t
    c4.nibdir = lambda t: phi
    gamma = c5.compute_theta(1) - pi
    c5.nibdir = lambda t: phi + (gamma-phi)*t
    c5.nib = lambda c,x,y,t,theta: 18+10*cos(theta-c.nibdir(t))
    c6.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[tc0,tc1],0,2,8)
    c7.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[tc0,tc1],1,2,8)
    c8.nib = c9.nib = c10.nib = 8
    blob(c10, 1, 'r', 45, 9)

    # I drew this one at a silly scale for some reason
    cont.scale = 1736
    cont.origin = 800, 822

    cont.hy = 1000 - (cont.origin[1] * cont.scale / 3600.) # I should probably work this out better

    return cont
clefG = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = ".8 dup scale", clefG
    cont.scale = clefG.scale
    cont.origin = clefG.origin
    cont.hy = .8 * clefG.hy
    return cont
clefGsmall = tmpfn()

# ----------------------------------------------------------------------
# F clef (bass).

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 534, 761, 0.964764, -0.263117, 783, 479, 0, -1)
    c1 = CircleInvolute(cont, 783, 479, 0, -1, 662, 352, -0.999133, -0.0416305)
    c2 = CircleInvolute(cont, 662, 352, -0.999133, -0.0416305, 585, 510, 0.993884, 0.110432)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: ((c.nibmax+6) + (c.nibmax-6)*cos(2*(theta-c.nibdir(t))))/2

    theta0 = c0.compute_theta(0)
    theta1 = c1.compute_theta(0)
    c0.nib = lambda c,x,y,t,theta: (34 + (6-34)*abs((theta-theta1)/(theta0-theta1))**1.4)
    c1.nibdir = lambda t: theta1
    c1.nibmax = 34
    c2.nibdir = lambda t: theta1
    c2.nibmax = 12
    blob(c2, 1, 'l', 47, 3)

    # The two dots.
    cont.extra = "newpath 857 417 20 0 360 arc fill " + \
    "newpath 857 542 20 0 360 arc fill";

    # The hot-spot y coordinate is precisely half-way between the
    # two dots.
    cont.hy = (417+542)/2.0

    return cont
clefF = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = ".8 dup scale", clefF
    cont.hy = .8 * clefF.hy
    return cont
clefFsmall = tmpfn()

# ----------------------------------------------------------------------
# C clef (alto, tenor).
#
# This one took considerable thinking! The sharp point between c3
# and c4 is difficult to achieve, and I eventually did it by having
# the nib narrow to 2 pixels at that point - so it isn't actually
# perfectly sharp, but I can't bring myself to care. So what happens
# is simply that the backward C shape is drawn with a nib function
# that narrows to a near-point, and then turns a corner to go down
# to the centreline via c4. Meanwhile, tc0 defines a cutoff line at
# which the plain circular nib going along c3 suddenly shifts to
# being a point-to-point nib of the same radius with its other end
# at the end of tc0 on the centreline.
#
# (Note that, due to the nontrivial nib width at the point where the
# cutoff occurs, the actual edge that ends up drawn will not run
# precisely along tc0. Again, I don't care.)

def tmpfn():
    # Secondary context.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 698, 474, 744, 398)
    c1 = StraightLine(cont, 698, 474, 744, 550)
    # End saved data
    tc0, tc1 = c0, c1

    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 698, 242, 0.707107, -0.707107, 762, 216, 1, 0)
    c1 = CircleInvolute(cont, 762, 216, 1, 0, 870, 324, 0, 1)
    c2 = CircleInvolute(cont, 870, 324, 0, 1, 773, 436, -1, 0)
    c3 = CircleInvolute(cont, 773, 436, -1, 0, 705, 355, -0.0434372, -0.999056)
    c4 = CircleInvolute(cont, 705, 355, -0.220261, 0.975441, 635, 474, -0.894427, 0.447214)
    c5 = CircleInvolute(cont, 698, 706, 0.707107, 0.707107, 762, 732, 1, 0)
    c6 = CircleInvolute(cont, 762, 732, 1, 0, 870, 624, 0, -1)
    c7 = CircleInvolute(cont, 870, 624, 0, -1, 773, 512, -1, -0)
    c8 = CircleInvolute(cont, 773, 512, -1, -0, 705, 593, -0.0434372, 0.999056)
    c9 = CircleInvolute(cont, 705, 593, -0.220261, -0.975441, 635, 474, -0.894427, -0.447214)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0, 1)
    c5.weld_to(1, c6, 0)
    c6.weld_to(1, c7, 0)
    c7.weld_to(1, c8, 0)
    c8.weld_to(1, c9, 0, 1)
    # End saved data

    def mad_cclef_points(c,x,y,t,theta,nibfn,cutoffline):
        # Get the ordinary nib width which the normal nib function
        # would specify for this point on the curve.
        nw = nibfn(c,x,y,t,theta)
        # If we're to the left of the cutoff line, do a PTP nib
        # pointing to the start point of the cutoff line.
        cx0, cy0, cx1, cy1 = cutoffline.inparams
        cx = cx0 + (cx1-cx0) * (y-cy0) / (cy1-cy0)
        if x < cx:
            return ptp_nib(c,x,y,t,theta,cx0,cy0,nw)
        else:
            return nw
    c0.nib = lambda c,x,y,t,theta: 6
    c1.nib = c2.nib = lambda c,x,y,t,theta: (lambda x1,x2: ((lambda k: (6, pi, k, 0))(44*((x-min(x1,x2))/abs(x2-x1))**2)))(c.compute_x(0),c.compute_x(1))
    c3.nib = lambda c,x,y,t,theta: mad_cclef_points(c,x,y,t,theta,c0.nib,tc0)
    cx0,cy0 = tc0.compute_point(0)
    r0 = c3.compute_nib(1)[0]
    c4.nib = lambda c,x,y,t,theta: ptp_nib(c,x,y,t,theta,cx0,cy0,r0)

    c5.nib = lambda c,x,y,t,theta: 6
    c6.nib = c7.nib = lambda c,x,y,t,theta: (lambda x1,x2: ((lambda k: (6, pi, k, 0))(44*((x-min(x1,x2))/abs(x2-x1))**2)))(c.compute_x(0),c.compute_x(1))
    c8.nib = lambda c,x,y,t,theta: mad_cclef_points(c,x,y,t,theta,c5.nib,tc1)
    cx1,cy1 = tc1.compute_point(0)
    r1 = c8.compute_nib(1)[0]
    c9.nib = lambda c,x,y,t,theta: ptp_nib(c,x,y,t,theta,cx1,cy1,r1)

    blob(c0, 0, 'l', 28, 6)
    blob(c5, 0, 'r', 28, 6)

    cont.extra = \
    "/box { newpath 3 index 3 index moveto 3 index 1 index lineto 1 index 1 index lineto 1 index 3 index lineto closepath fill pop pop pop } def " + \
    "537 206 601 742 box " + \
    "625 206 641 742 box "

    return cont
clefC = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = ".8 dup scale", clefC
    return cont
clefCsmall = tmpfn()

# ----------------------------------------------------------------------
# Percussion 'clef'.

def tmpfn():
    cont = GlyphContext()
    cont.extra = \
    "newpath 410 368 moveto 410 632 lineto " + \
    "470 632 lineto 470 368 lineto closepath fill " + \
    "newpath 530 368 moveto 530 632 lineto " + \
    "590 632 lineto 590 368 lineto closepath fill "
    return cont
clefperc = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = ".8 dup scale", clefperc
    return cont
clefpercsmall = tmpfn()

# ----------------------------------------------------------------------
# Tablature 'clef': just the letters "TAB", written vertically in a
# vaguely calligraphic style.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 100, 104, 900, 104)
    c1 = StraightLine(cont, 100, 368, 900, 368)
    c2 = StraightLine(cont, 100, 632, 900, 632)
    c3 = StraightLine(cont, 100, 896, 900, 896)
    c4 = CircleInvolute(cont, 354, 153, 0.564684, -0.825307, 443, 128, 0.964764, 0.263117)
    c5 = CircleInvolute(cont, 443, 128, 0.964764, 0.263117, 555, 118, 0.83205, -0.5547)
    c6 = CircleInvolute(cont, 463, 136, 0.110432, 0.993884, 434, 313, -0.571064, 0.820905)
    c7 = CircleInvolute(cont, 434, 313, -0.571064, 0.820905, 376, 334, -0.83205, -0.5547)
    c8 = CircleInvolute(cont, 333, 603, 0.98387, 0.178885, 486, 384, 0.0416305, -0.999133)
    c9 = CircleInvolute(cont, 486, 384, 0.110432, 0.993884, 527, 572, 0.398726, 0.91707)
    c10 = CircleInvolute(cont, 527, 572, 0.398726, 0.91707, 572, 605, 0.963518, -0.267644)
    c11 = CircleInvolute(cont, 441, 541, 0.724999, 0.688749, 482, 555, 0.977176, -0.21243)
    c12 = CircleInvolute(cont, 355, 698, 0.5547, -0.83205, 464, 648, 0.998168, -0.0604951)
    c13 = CircleInvolute(cont, 464, 648, 0.998168, -0.0604951, 551, 700, 0, 1)
    c14 = CircleInvolute(cont, 551, 700, 0, 1, 475, 756, -0.995634, 0.0933407)
    c15 = CircleInvolute(cont, 475, 756, 0.98995, 0.141421, 555, 822, 0.0416305, 0.999133)
    c16 = CircleInvolute(cont, 555, 822, 0.0416305, 0.999133, 427, 856, -0.815507, -0.578747)
    c17 = CircleInvolute(cont, 446, 667, 0.119145, 0.992877, 417, 815, -0.447214, 0.894427)
    c18 = CircleInvolute(cont, 417, 815, -0.447214, 0.894427, 342, 858, -0.876812, -0.480833)
    c4.weld_to(1, c5, 0)
    c6.weld_to(1, c7, 0)
    c8.weld_to(1, c9, 0, 1)
    c9.weld_to(1, c10, 0)
    c12.weld_to(1, c13, 0)
    c13.weld_to(1, c14, 0)
    c14.weld_to(1, c15, 0, 1)
    c15.weld_to(1, c16, 0)
    c17.weld_to(1, c18, 0)
    # End saved data

    # Stave lines as guides used when I was drawing it
    c0.nib = c1.nib = c2.nib = c3.nib = 0
    cont.default_nib = lambda c,x,y,t,theta: 12+10*sin(theta)**2

    # Vertical of T needs not to overlap top of T
    c6.nib = lambda c,x,y,t,theta: (12, theta+pi/2, 10*sin(theta)**2, 10*sin(theta)**2)

    # Special nib for crossbar of A
    c11.nib = lambda c,x,y,t,theta: 12-6*t

    cont.hy = (c1.compute_y(0) + c2.compute_y(0)) / 2.0

    return cont
clefTAB = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = ".8 dup scale", clefTAB
    cont.hy = .8 * clefTAB.hy
    return cont
clefTABsmall = tmpfn()

# ----------------------------------------------------------------------
# Quaver tails.

# Vertical space between multiple tails, which after some
# experimentation I decided should be different between the up- and
# down-pointing stems.
#
# For down stems (so that the tails have to fit under the note
# head), it's about 80% of the spacing between adjacent stave lines
# (which is, in this coordinate system, 250 * 1900/3600 = 132 minus
# 1/18. For up stems, it's a bit more than that: closer to 87%.
quavertaildispdn = 105
quavertaildispup = 115

def clipup(tail):
    # Clipped version of an up-quaver-tail designed to fit above
    # another identical tail and stop where it crosses the latter.
    cont = GlyphContext()
    clip = clippath([tail.c0, tail.c1, (900,1900), (900,100), (100,100), (100,1900)])
    cont.extra = "gsave 0 %g translate newpath" % quavertaildispup, clip, \
    "clip 0 -%g translate" % quavertaildispup, tail, "grestore"
    cont.ox = tail.ox
    cont.oy = tail.oy
    return cont

def clipdn(tail):
    # Clipped version of a down-quaver-tail designed to fit below
    # another identical tail and stop where it crosses the latter.
    cont = GlyphContext()
    clip = clippath([tail.c0, tail.c1, (900,100), (900,1900), (100,1900), (100,900)])
    cont.extra = "gsave 0 -%g translate newpath" % quavertaildispdn, clip, \
    "clip 0 %g translate" % quavertaildispdn, tail, "grestore"
    cont.ox = tailquaverdn.ox
    cont.oy = tailquaverdn.oy
    return cont

def multiup(n, tail):
    # Up-pointing multitail.
    short = clipup(tail)
    cont = GlyphContext()
    # To make room for the five-tailed quasihemidemisemiquaver, we
    # translate downwards a bit. 95 (== 5*19) in glyph coordinates
    # equals 128 (== 5*36) in output coordinates.
    cont.extra = ("0 95 translate", tail,) + ("0 -%g translate" % quavertaildispup, short) * (n-1)
    cont.ox = tail.ox
    cont.oy = tail.oy - quavertaildispup*(n-1) + 95
    cont.origin = tail.origin
    cont.origin = (cont.origin[0], cont.origin[1] + quavertaildispup*(n-1)*3600./cont.scale - 180)
    return cont

def multidn(n, tail):
    # Down-pointing multitail.
    short = clipdn(tail)
    cont = GlyphContext()
    cont.extra = (tail,) + ("0 %g translate" % quavertaildispdn, short) * (n-1)
    cont.ox = tail.ox
    cont.oy = tail.oy + quavertaildispdn*(n-1)
    cont.origin = tail.origin
    cont.origin = (cont.origin[0], cont.origin[1] - quavertaildispdn*(n-1)*3600./cont.scale)
    return cont

def tmpfn():
    # Full-size tail for a quaver with an up-pointing stem.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 567, 0.948683, 0.316228, 611, 607, 0.7282, 0.685365)
    c1 = CircleInvolute(cont, 611, 607, 0.7282, 0.685365, 606, 840, -0.661622, 0.749838)
    c2 = CircleInvolute(cont, 535, 465, 0.233373, 0.972387, 605, 581, 0.73994, 0.672673)
    c3 = CircleInvolute(cont, 605, 581, 0.73994, 0.672673, 606, 840, -0.661622, 0.749838)
    c4 = StraightLine(cont, 660, 875, 660, 506)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) - c2.compute_nib(0)[0] - 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 9)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
tailquaverup = tmpfn()

def tmpfn():
    # Single tail for an up-pointing semiquaver.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 556, 1, 0, 602, 571, 0.825307, 0.564684)
    c1 = CircleInvolute(cont, 602, 571, 0.825307, 0.564684, 617, 779, -0.661622, 0.749838)
    c2 = CircleInvolute(cont, 535, 465, 0.371391, 0.928477, 613, 566, 0.732793, 0.680451)
    c3 = CircleInvolute(cont, 613, 566, 0.732793, 0.680451, 617, 779, -0.661622, 0.749838)
    c4 = StraightLine(cont, 660, 783.16, 660, 496.816)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # Make sure the tail length matches what it should be.
    assert round(c1.compute_y(1) - (840 + 54 - quavertaildispup*1)) == 0

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) - c2.compute_nib(0)[0] - 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 9)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
tailsemiup = multiup(2, tmpfn())

def tmpfn():
    # Single tail for an up-pointing demisemiquaver.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 555, 0.998868, -0.0475651, 586, 561, 0.913812, 0.406138)
    c1 = CircleInvolute(cont, 586, 561, 0.913812, 0.406138, 621, 800, -0.536875, 0.843662)
    c2 = CircleInvolute(cont, 535, 465, 0.416655, 0.909065, 608, 555, 0.734803, 0.67828)
    c3 = CircleInvolute(cont, 608, 555, 0.734803, 0.67828, 621, 800, -0.536875, 0.843662)
    c4 = StraightLine(cont, 660, 835.64, 660, 502.064)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # Make sure the tail length matches what it should be.
    assert round(c1.compute_y(1) - (840 + 58 - quavertaildispup*2 + 132)) == 0

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) - c2.compute_nib(0)[0] - 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 9)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
taildemiup = multiup(3, tmpfn())

def tmpfn():
    # Single tail for an up-pointing hemidemisemiquaver.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 555, 0.853282, -0.52145, 577, 552, 0.894427, 0.447214)
    c1 = CircleInvolute(cont, 577, 552, 0.894427, 0.447214, 640, 753, -0.447214, 0.894427)
    c2 = CircleInvolute(cont, 535, 465, 0.28, 0.96, 592, 545, 0.77193, 0.635707)
    c3 = CircleInvolute(cont, 592, 545, 0.77193, 0.635707, 640, 753, -0.447214, 0.894427)
    c4 = StraightLine(cont, 660, 815.96, 660, 500.096)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # Make sure the tail length matches what it should be.
    assert round(c1.compute_y(1) - (840 + 60 - quavertaildispup*3 + 132*1.5)) == 0

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) - c2.compute_nib(0)[0] - 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 9)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
tailhemiup = multiup(4, tmpfn())

def tmpfn():
    # Single tail for an up-pointing quasihemidemisemiquaver.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 546, 0.996546, 0.0830455, 607, 575, 0.707107, 0.707107)
    c1 = CircleInvolute(cont, 607, 575, 0.707107, 0.707107, 629, 772, -0.611448, 0.791285)
    c2 = CircleInvolute(cont, 535, 465, 0.371391, 0.928477, 595, 544, 0.707107, 0.707107)
    c3 = CircleInvolute(cont, 595, 544, 0.707107, 0.707107, 629, 772, -0.611448, 0.791285)
    c4 = StraightLine(cont, 660, 868.44, 660, 505.344)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # Make sure the tail length matches what it should be.
    assert round(c1.compute_y(1) - (840 + 62 - quavertaildispup*4 + 132*2.5)) == 0

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) - c2.compute_nib(0)[0] - 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 9)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
tailquasiup = multiup(5, tmpfn())

def tmpfn():
    # Full-size tail for a quaver with a down-pointing stem.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 363, 0.999201, -0.039968, 585, 354, 0.948683, -0.316228)
    c1 = CircleInvolute(cont, 585, 354, 0.948683, -0.316228, 635, 90, -0.563337, -0.826227)
    c2 = CircleInvolute(cont, 535, 465, 0.338427, -0.940993, 627, 349, 0.742268, -0.670103)
    c3 = CircleInvolute(cont, 627, 349, 0.742268, -0.670103, 635, 90, -0.563337, -0.826227)
    c4 = StraightLine(cont, 680, 55, 680, 424)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) + c2.compute_nib(0)[0] + 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 8)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
tailquaverdn = tmpfn()

def tmpfn():
    # Single tail for a down-pointing semiquaver.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 378, 0.99083, -0.135113, 611, 356, 0.868243, -0.496139)
    c1 = CircleInvolute(cont, 611, 356, 0.868243, -0.496139, 663, 195, -0.447214, -0.894427)
    c2 = CircleInvolute(cont, 535, 465, 0.467531, -0.883977, 620, 363, 0.768221, -0.640184)
    c3 = CircleInvolute(cont, 620, 363, 0.768221, -0.640184, 663, 195, -0.447214, -0.894427)
    c4 = StraightLine(cont, 680, 186.2, 680, 437.12)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # Make sure the tail length matches what it should be.
    assert round(c1.compute_y(1) - (90 + quavertaildispdn*1)) == 0

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) + c2.compute_nib(0)[0] + 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 8)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
tailsemidn = multidn(2, tmpfn())

def tmpfn():
    # Single tail for a down-pointing demisemiquaver.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 380, 0.9916, -0.129339, 615, 354, 0.861934, -0.50702)
    c1 = CircleInvolute(cont, 615, 354, 0.861934, -0.50702, 653, 168, -0.536875, -0.843662)
    c2 = CircleInvolute(cont, 535, 465, 0.450869, -0.89259, 616, 376, 0.789352, -0.613941)
    c3 = CircleInvolute(cont, 616, 376, 0.789352, -0.613941, 653, 168, -0.536875, -0.843662)
    c4 = StraightLine(cont, 680, 173.08, 680, 435.808)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # Make sure the tail length matches what it should be.
    assert round(c1.compute_y(1) - (90 + quavertaildispdn*2 - 132)) == 0

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) + c2.compute_nib(0)[0] + 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 8)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
taildemidn = multidn(3, tmpfn())

def tmpfn():
    # Single tail for a down-pointing hemidemisemiquaver.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 534, 382, 0.999133, -0.0416305, 605, 369, 0.921635, -0.388057)
    c1 = CircleInvolute(cont, 605, 369, 0.921635, -0.388057, 646, 207, -0.784883, -0.619644)
    c2 = CircleInvolute(cont, 535, 465, 0.338719, -0.940888, 630, 363, 0.825307, -0.564684)
    c3 = CircleInvolute(cont, 630, 363, 0.825307, -0.564684, 646, 207, -0.784883, -0.619644)
    c4 = StraightLine(cont, 680, 232.12, 680, 441.712)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # Make sure the tail length matches what it should be.
    assert round(c1.compute_y(1) - (90 + quavertaildispdn*3 - 132*1.5)) == 0

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) + c2.compute_nib(0)[0] + 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 8)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
tailhemidn = multidn(4, tmpfn())

def tmpfn():
    # Single tail for a down-pointing quasihemidemisemiquaver.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 384, 0.982007, -0.188847, 608, 357, 0.885547, -0.464549)
    c1 = CircleInvolute(cont, 608, 357, 0.885547, -0.464549, 653, 180, -0.606043, -0.795432)
    c2 = CircleInvolute(cont, 535, 465, 0.338719, -0.940888, 633, 348, 0.768221, -0.640184)
    c3 = CircleInvolute(cont, 633, 348, 0.768221, -0.640184, 653, 180, -0.606043, -0.795432)
    c4 = StraightLine(cont, 680, 219, 680, 440.4)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c3, 1, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # Make sure the tail length matches what it should be.
    assert round(c1.compute_y(1) - (90 + quavertaildispdn*4 - 132*2.5)) == 0

    c4.nib = 0 # guide line to get the width the same across all versions

    c0.nib = c1.nib = 0
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],0,2,8)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c0,c1],1,2,8)

    cont.c0 = c0 # for tailshortdn
    cont.c1 = c1 # for tailshortdn

    cont.oy = c2.compute_y(0) + c2.compute_nib(0)[0] + 2

    cx = c2.compute_x(0) + c2.compute_nib(0)[0]
    cont.ox = cx
    cont.extra = "gsave newpath %g 0 moveto 0 1000 rlineto -100 0 rlineto 0 -1000 rlineto closepath 1 setgray fill grestore" % (cx - 8)

    cont.origin = cx * 3600. / cont.scale - 12, (1000-cont.oy) * 3600. / cont.scale

    return cont
tailquasidn = multidn(5, tmpfn())

# ----------------------------------------------------------------------
# Minim note head.
#
# A minim head has an elliptical outline, and then a long thin
# elliptical hole in the middle.

def tmpfn():
    cont = GlyphContext()
    # Parameters: a unit vector giving the direction of the ellipse's
    # long axis, the squash ratio (short axis divided by long).
    angle = 37
    sq = 0.35
    # The long and short axes as unit vectors.
    lx, ly = cos(angle*(pi/180)), -sin(angle*(pi/180))
    sx, sy = -sin(angle*(pi/180)), -cos(angle*(pi/180))
    # We want to find an ellipse, centred on the origin, which is large
    # enough to be just tangent to the outline ellipse. To do this, we
    # transform the coordinate system so that the new ellipse is
    # circular, then construct the image of the outline ellipse and find
    # its closest approach to the origin. The circle of that radius,
    # transformed back again, is the ellipse we want.
    #
    # Our original ellipse, discounting translation, is the unit circle
    # fed through a 2x2 matrix transform. We have a second 2x2 matrix
    # transform here, so we multiply the two to construct the matrix
    # which transforms the coordinate system in which the note outline
    # is a circle into the one in which the hole in the middle is a
    # circle.
    mat1 = (1,-.3,0,1) # the shear matrix from the head outline
    mat2 = (76,0,0,67) # the scaling matrix from the head outline
    mat3 = (lx,ly,sx,sy) # rotate so that our desired axes become i,j
    mat4 = (1,0,0,1/sq) # unsquash in the s-axis
    imat = matmul(matmul(mat4,mat3), matmul(mat2,mat1))
    mat = matinv(imat)
    # The equation of the outline ellipse in the new coordinate system
    # is given by transforming (x,y) by the above matrix and then
    # setting the sum of the squares of the transformed coordinates
    # equal to 1. In other words, we have
    #
    #          (x y) (a c) (a b) (x) = 1
    #                (b d) (c d) (y)
    #
    # => (x y) (a^2+c^2  ab+cd ) (x) = 1
    #          ( ba+dc  b^2+d^2) (y)
    #
    # and then the matrix in the middle is symmetric, which means we can
    # decompose it into an orthogonal eigenvector matrix and a diagonal
    # eigenvalue matrix, giving us
    #
    #    (x y) (p q) (u 0) (p r) (x) = 1
    #          (r s) (0 v) (q s) (y)
    #
    # Now the eigenvector matrix rotates our coordinate system into one
    # which has the basis vectors aligned with the axes of the ellipse,
    # so in that coordinate system the equation of the ellipse is merely
    # u x^2 + v y^2 = 1. Thus u and v are the squared reciprocals of the
    # lengths of our major and minor axes, so sqrt(min(1/u,1/v)) is the
    # closest approach to the origin of the ellipse in question.
    #
    # (We don't even bother calculating the eigenvector matrix, though
    # we could if we wanted to.)
    matO = (mat[0]*mat[0]+mat[2]*mat[2], mat[1]*mat[0]+mat[3]*mat[2],
    mat[0]*mat[1]+mat[2]*mat[3], mat[1]*mat[1]+mat[3]*mat[3])
    # Characteristic equation of a 2x2 matrix is
    #    (m0-lambda)(m3-lambda) - m1*m2 = 0
    # => lambda^2 - (m0+m3)lambda + (m0*m3-m1*m2) = 0
    # So the eigenvalues are the solutions of that quadratic, i.e.
    #    (m0+m3 +- sqrt((m0-m3)^2+4*m1*m2)) / 2
    u = (matO[0] + matO[3] + sqrt((matO[0]-matO[3])**2 + 4*matO[1]*matO[2]))/2
    v = (matO[0] + matO[3] - sqrt((matO[0]-matO[3])**2 + 4*matO[1]*matO[2]))/2
    r = sqrt(min(1/u, 1/v)) * 0.999 # small hedge against rounding glitches
    # And now we can draw our ellipse: it's the circle about the origin
    # of radius r, squashed in the y-direction by sq, rotated by angle.
    cont.extra = \
    "gsave 527 472 translate newpath " + \
    "matrix currentmatrix 76 67 scale [1 0 -.3 1 0 0] concat 1 0 moveto 0 0 1 0 360 arc closepath setmatrix " + \
    "matrix currentmatrix -%g rotate 1 %g scale %g 0 moveto 0 0 %g 360 0 arcn closepath setmatrix " % (angle,sq,r,r) + \
    "gsave fill grestore 8 setlinewidth stroke grestore"

    # Incidentally, another useful datum output from all of this is
    # that we can compute the exact point on the outer ellipse at
    # which the tangent is vertical, which is where we'll have to
    # put a note stem. This is given by reconstituting the elements
    # of the outer ellipse's transformation matrix into a quadratic
    # in x,y of the form
    #
    #     ax^2 + bxy + cy^2 = 1
    #
    # From this we can differentiate with respect to y to get
    #
    #     2ax dx/dy + bx + by dx/dy + 2cy = 0
    #
    # and then solve for dx/dy to give
    #
    #     dx/dy = -(bx + 2cy) / (2ax + by)
    #
    # which is zero iff its denominator is zero, i.e. y = -bx/2c.
    # Substituting that back into the original equation gives
    #
    #       ax^2 + bx(-bx/2c) + c(bx/2c)^2 = 1
    # =>  ax^2 - (b^2/2c)x^2 + (b^2/4c)x^2 = 1
    # =>                   (a - b^2/4c)x^2 = 1
    # =>                                 x = 1/sqrt(a - b^2/4c)
    #
    # Substituting that into the expression for y and rearranging a
    # bit gives us
    #
    #   x = (2*sqrt(c)) / sqrt(4ac-b^2)
    #   y = (-b/sqrt(c)) / sqrt(4ac-b^2)
    #
    # (Of course, that's on the outer elliptical _path_, which isn't
    # the very outside of the note shape due to the stroke width; so
    # another (currentlinewidth/2) pixels are needed to get to
    # there. But the y-position is correct.)
    matK = matinv(matmul(mat2,mat1))
    matL = (matK[0]*matK[0]+matK[2]*matK[2], matK[1]*matK[0]+matK[3]*matK[2],
    matK[0]*matK[1]+matK[2]*matK[3], matK[1]*matK[1]+matK[3]*matK[3])
    a, b, c = matL[0], matL[1]+matL[2], matL[3]
    denom = sqrt(4*a*c-b*b)
    #sys.stderr.write("%.17f, %.17f\n" % (2*sqrt(c)/denom, -b/sqrt(c)/denom))
    cont.ay = 472 - b/sqrt(c)/denom

    return cont
headminim = tmpfn()

# ----------------------------------------------------------------------
# Filled note head, for crotchet/quaver/semiquaver/etc.
#
# This is identical to the minim head but without the inner hole.

def tmpfn():
    cont = GlyphContext()
    cont.extra = \
    "gsave 527 472 translate newpath " + \
    "matrix currentmatrix 76 67 scale [1 0 -.3 1 0 0] concat 1 0 moveto 0 0 1 0 360 arc closepath setmatrix " + \
    "gsave fill grestore 8 setlinewidth stroke grestore"
    cont.ay = headminim.ay
    return cont
headcrotchet = tmpfn()

# ----------------------------------------------------------------------
# Semibreve head. This is another nested pair of ellipses. The outer
# ellipse is unskewed and half again as wide as the crotchet/minim
# head; the inner one is at a totally different angle.

def tmpfn():
    cont = GlyphContext()
    angle = 120
    sq = 0.75
    # Everything below is repaated from the minim head.
    lx, ly = cos(angle*(pi/180)), -sin(angle*(pi/180))
    sx, sy = -sin(angle*(pi/180)), -cos(angle*(pi/180))
    mat2 = (116,0,0,67) # the scaling matrix from the head outline
    mat3 = (lx,ly,sx,sy) # rotate so that our desired axes become i,j
    mat4 = (1,0,0,1/sq) # unsquash in the s-axis
    imat = matmul(matmul(mat4,mat3), mat2)
    mat = matinv(imat)
    mat2 = (mat[0]*mat[0]+mat[2]*mat[2], mat[1]*mat[0]+mat[3]*mat[2],
    mat[0]*mat[1]+mat[2]*mat[3], mat[1]*mat[1]+mat[3]*mat[3])
    u = (mat2[0] + mat2[3] + sqrt((mat2[0]-mat2[3])**2 + 4*mat2[1]*mat2[2]))/2
    v = (mat2[0] + mat2[3] - sqrt((mat2[0]-mat2[3])**2 + 4*mat2[1]*mat2[2]))/2
    r = sqrt(min(1/u, 1/v))
    cont.extra = \
    "gsave 527 472 translate newpath " + \
    "matrix currentmatrix 116 67 scale 1 0 moveto 0 0 1 0 360 arc closepath setmatrix " + \
    "matrix currentmatrix -%g rotate 1 %g scale %g 0 moveto 0 0 %g 360 0 arcn closepath setmatrix " % (angle,sq,r,r) + \
    "gsave fill grestore 8 setlinewidth stroke grestore"
    return cont
semibreve = tmpfn()

# A breve is just a semibreve with bars down the sides.
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 398, 390, 398, 554)
    c1 = StraightLine(cont, 656, 390, 656, 554)
    c2 = StraightLine(cont, 362, 390, 362, 554)
    c3 = StraightLine(cont, 692, 390, 692, 554)
    # End saved data

    cont.default_nib = 10

    cont.extra = semibreve
    return cont
breve = tmpfn()

# ----------------------------------------------------------------------
# Shaped note heads used for drum and other notation.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 411, 472, 0.970536, 0.240956, 527, 539, 0.633646, 0.773623)
    c1 = CircleInvolute(cont, 527, 539, 0.633646, -0.773623, 643, 472, 0.970536, -0.240956)
    c2 = CircleInvolute(cont, 643, 472, -0.970536, -0.240956, 527, 405, -0.633646, -0.773623)
    c3 = CircleInvolute(cont, 527, 405, -0.633646, 0.773623, 411, 472, -0.970536, 0.240956)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c3, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: (6, 0, (527-x)/3, 0)

    return cont
diamondsemi = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 448, 472, 0.939517, 0.342501, 527, 539, 0.487147, 0.87332)
    c1 = CircleInvolute(cont, 527, 539, 0.487147, -0.87332, 606, 472, 0.939517, -0.342501)
    c2 = CircleInvolute(cont, 606, 472, -0.939517, -0.342501, 527, 405, -0.487147, -0.87332)
    c3 = CircleInvolute(cont, 527, 405, -0.487147, 0.87332, 448, 472, -0.939517, 0.342501)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c3, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    # End saved data

    cont.default_nib = 6
    c1.nib = lambda c,x,y,t,theta: (6, 127*pi/180, min(12, 300*t, 100*(1-t)), 0)
    c3.nib = lambda c,x,y,t,theta: (6, -53*pi/180, min(12, 300*t, 100*(1-t)), 0)

    return cont
diamondminim = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 448, 472, 0.939517, 0.342501, 527, 539, 0.487147, 0.87332)
    c1 = CircleInvolute(cont, 527, 539, 0.487147, -0.87332, 606, 472, 0.939517, -0.342501)
    c2 = CircleInvolute(cont, 606, 472, -0.939517, -0.342501, 527, 405, -0.487147, -0.87332)
    c3 = CircleInvolute(cont, 527, 405, -0.487147, 0.87332, 448, 472, -0.939517, 0.342501)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c3, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    # End saved data

    # Fill the diamond.
    cont.default_nib = lambda c,x,y,t,theta: ptp_nib(c,x,y,t,theta,527,472,6)

    return cont
diamondcrotchet = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 411, 550, 0.944497, -0.328521, 643, 550, 0.944497, 0.328521)
    c1 = CircleInvolute(cont, 643, 550, -0.784883, -0.619644, 527, 405, -0.519947, -0.854199)
    c2 = CircleInvolute(cont, 527, 405, -0.519947, 0.854199, 411, 550, -0.784883, 0.619644)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c2, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    # End saved data

    c0.nib = 6
    angle = abs(1/tan(c0.compute_theta(0) + pi/30))
    ybase = c0.compute_y(0)
    c1.nib = lambda c,x,y,t,theta: (6, 0, 0, min((x-527)/3, (ybase-y)*angle))
    c2.nib = lambda c,x,y,t,theta: (6, 0, min((527-x)/3, (ybase-y)*angle), 0)

    return cont
trianglesemi = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 448, 550, 0.890571, -0.454844, 606, 550, 0.890571, 0.454844)
    c1 = CircleInvolute(cont, 606, 550, -0.65319, -0.757194, 527, 405, -0.382943, -0.923772)
    c2 = CircleInvolute(cont, 527, 405, -0.382943, 0.923772, 448, 550, -0.65319, 0.757194)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c2, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    # End saved data

    c1.nib = 6
    angle = 127*pi/180
    vx, vy = cos(angle), -sin(angle)
    vdist = lambda x1,y1,x2,y2: abs(vx*(x1-x2) + vy*(y1-y2))
    x0, y0 = c0.compute_point(0)
    c0.nib = lambda c,x,y,t,theta: (6, angle, vdist(x0,y0,x,y)/3, 0)
    c2.nib = lambda c,x,y,t,theta: (6, angle, 0, min(vdist(x0,y0,x,y)/3, 350*t))

    cont.ay = c0.compute_y(0)
    cont.iy = 2*472 - cont.ay

    return cont
triangleminim = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 448, 550, 0.890571, -0.454844, 606, 550, 0.890571, 0.454844)
    c1 = CircleInvolute(cont, 606, 550, -0.65319, -0.757194, 527, 405, -0.382943, -0.923772)
    c2 = CircleInvolute(cont, 527, 405, -0.382943, 0.923772, 448, 550, -0.65319, 0.757194)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c2, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    # End saved data

    # Fill the triangle.
    cont.default_nib = lambda c,x,y,t,theta: ptp_nib(c,x,y,t,theta,527,472,6)

    cont.ay = c0.compute_y(0)
    cont.iy = 2*472 - cont.ay
    return cont
trianglecrotchet = tmpfn()
def tmpfn():
    cont = GlyphContext()
    outerw = 9
    innerr = 12
    outerr = innerr + 2*outerw
    ax, ay = 116 - outerr, 70 - outerr
    cont.extra = ["gsave 527 472 translate",
    "newpath %g %g 1 index neg 1 index neg moveto 1 index 1 index lineto 1 index neg 1 index moveto neg lineto" % (ax,ay),
    "gsave %g setlinewidth stroke grestore %g setlinewidth 1 setgray stroke" % (2*outerr, 2*innerr),
    "grestore"]
    cont.ay = ay
    return cont
crosssemi = tmpfn()
def tmpfn():
    cont = GlyphContext()
    outerw = 9
    innerr = 10
    outerr = innerr + 2*outerw
    ax, ay = 79 - outerr, 70 - outerr
    cont.extra = ["gsave 527 472 translate",
    "newpath %g %g 1 index neg 1 index neg moveto 1 index 1 index lineto 1 index neg 1 index moveto neg lineto" % (ax,ay),
    "gsave %g setlinewidth stroke grestore %g setlinewidth 1 setgray stroke" % (2*outerr, 2*innerr),
    "grestore"]
    cont.ay = 472 - ay
    return cont
crossminim = tmpfn()
def tmpfn():
    cont = GlyphContext()
    r = 12
    ax, ay = 79 - r, 70 - r
    cont.extra = ["gsave 527 472 translate",
    "newpath %g %g 1 index neg 1 index neg moveto 1 index 1 index lineto 1 index neg 1 index moveto neg lineto" % (ax,ay),
    "%g setlinewidth stroke" % (2*r),
    "grestore"]
    cont.ay = 472 - ay
    return cont
crosscrotchet = tmpfn()
def tmpfn():
    cont = GlyphContext()
    r = 12
    ax, ay = 70 - r, 70 - r
    cont.extra = ["gsave 527 472 translate",
    "newpath %g %g 1 index neg 1 index neg moveto 1 index 1 index lineto 1 index neg 1 index moveto neg lineto" % (ax,ay),
    "%g dup 0 moveto 0 exch 0 exch 0 360 arc" % (sqrt(ax*ax+ay*ay)),
    "%g setlinewidth stroke" % (2*r),
    "grestore"]
    return cont
crosscircle = tmpfn()

def tmpfn():
    cont = GlyphContext()
    r = 12
    xouter = 116 - r
    xwidth = 160
    ay = 130 - r
    cont.extra = ["gsave 527 472 translate",
    "newpath %g %g moveto %g %g lineto %g %g lineto %g %g lineto closepath" % (xouter,-ay,xouter-xwidth,-ay,-xouter,ay,-xouter+xwidth,ay),
    "%g setlinewidth 1 setlinejoin stroke" % (2*r),
    "grestore"]
    cont.ay = 472 - ay
    return cont
slashsemi = tmpfn()
def tmpfn():
    cont = GlyphContext()
    r = 12
    xouter = 76 - r
    xwidth = 80
    ay = 130 - r
    cont.extra = ["gsave 527 472 translate",
    "newpath %g %g moveto %g %g lineto %g %g lineto %g %g lineto closepath" % (xouter,-ay,xouter-xwidth,-ay,-xouter,ay,-xouter+xwidth,ay),
    "%g setlinewidth 1 setlinejoin stroke" % (2*r),
    "grestore"]
    cont.ay = 472 - ay
    return cont
slashminim = tmpfn()
def tmpfn():
    cont = GlyphContext()
    r = 12
    xouter = 56 - r
    xwidth = 40
    ay = 130 - r
    cont.extra = ["gsave 527 472 translate",
    "newpath %g %g moveto %g %g lineto %g %g lineto %g %g lineto closepath" % (xouter,-ay,xouter-xwidth,-ay,-xouter,ay,-xouter+xwidth,ay),
    "gsave %g setlinewidth 1 setlinejoin stroke grestore fill" % (2*r),
    "grestore"]
    cont.ay = 472 - ay
    return cont
slashcrotchet = tmpfn()

# ----------------------------------------------------------------------
# Trill sign. There seem to be two standard-ish designs for this:
# one flowery one in which there are loops all over the place as if
# it's been drawn in several strokes by somebody who didn't bother
# taking the pen off the paper between them (e.g. Euterpe,
# Lilypond), and one simpler one that just looks like 'tr' written
# in an italic font and squashed together. Mine follows the latter
# model, but has a more chisel-nib-calligraphy look than other
# examples I've seen. (I drew it like that as an experiment and
# found I liked it more than the one I was comparing to!)

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 497, 274, 452, 425)
    c1 = CircleInvolute(cont, 452, 425, -0.285601, 0.958349, 488, 456, 0.860055, -0.510202)
    c2 = StraightLine(cont, 488, 456, 547, 421)
    c3 = StraightLine(cont, 413, 344, 488, 343)
    c4 = CircleInvolute(cont, 488, 343, 0.999911, -0.0133321, 559, 335, 0.974222, -0.225592)
    c5 = CircleInvolute(cont, 559, 335, 0.974222, -0.225592, 573, 345, -0.290482, 0.956881)
    c6 = StraightLine(cont, 573, 345, 539, 457)
    c7 = CircleInvolute(cont, 561.107, 382, 0.274721, -0.961524, 621, 332, 1, 0)
    c8 = CircleInvolute(cont, 621, 332, 1, 0, 636, 356, -0.242536, 0.970142)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c6, 0)
    c7.weld_to(1, c8, 0)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: (3, c.nibdir(t), 17, 17)

    k2 = c4.compute_theta(1)
    c3.nibdir = c4.nibdir = c5.nibdir = c6.nibdir = lambda t: k2
    c7.nibdir = c8.nibdir = c3.nibdir

    topy = c0.compute_y(0)
    c0.nib = lambda c,x,y,t,theta: qc(t>0.5, 20, (3, 0, 17, min(17,-17+(y-topy)*1.2)))
    theta0 = c0.compute_theta(0)
    theta2 = c2.compute_theta(0)
    c1.nib = c2.nib = lambda c,x,y,t,theta: 14+6*cos(pi*(theta-theta0)/(theta2-theta0))

    return cont
trill = tmpfn()

# ----------------------------------------------------------------------
# Crotchet rest. The top section is done by curve-following, drawing
# the two sides of the stroke independently; the bottom section is a
# single curve on the right, with the nib width varying in such a
# way as to present a nice curve on the left.

def tmpfn():
    cont = GlyphContext()

    # Secondary curve set.
    # Saved data from gui.py
    c0 = StraightLine(cont, 502, 276, 589, 352)
    c1 = CircleInvolute(cont, 589, 352, -0.585491, 0.810679, 592, 535, 0.74783, 0.66389)
    c0.weld_to(1, c1, 0, 1)
    # End saved data
    tc0, tc1 = c0, c1

    cont = GlyphContext()
    # Primary curve set.
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 502, 276, 0.753113, 0.657892, 494, 448, -0.613941, 0.789352)
    c1 = StraightLine(cont, 494, 448, 592, 535)
    c2 = CircleInvolute(cont, 592, 535, -0.952424, -0.304776, 524, 569, -0.378633, 0.925547)
    c3 = CircleInvolute(cont, 524, 569, -0.378633, 0.925547, 547, 649, 0.745241, 0.666795)
    c0.weld_to(1, c1, 0, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # Dependencies between the above: tc0 and c0 must start at the
    # same place heading in the same direction, and tc1 and c1 must
    # end at the same place heading in the same direction.

    c0.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[tc0,tc1],0,2,6)
    c1.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[tc0,tc1],1,2,6)
    phi0 = c2.compute_theta(0)
    phi1 = c3.compute_theta(1) + pi
    phia = (phi0 + phi1) / 2
    c2.nib = lambda c,x,y,t,theta: (6, phia, (1-(1-t)**2)*40, 0)
    c3.nib = lambda c,x,y,t,theta: (6, phia, (1-t**2)*40, 0)
    return cont
restcrotchet = tmpfn()

# ----------------------------------------------------------------------
# Quaver rest and friends.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 531, 271, 588, 81)
    c1 = CircleInvolute(cont, 588, 81, -0.347314, 0.937749, 480, 125, -0.784883, -0.619644)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    cont.default_nib = 8

    blob(c1, 1, 'r', 33, 3)
    cont.cy = c1.compute_y(1) - 33*sin(c1.compute_theta(1)-pi/2) + 76

    cont.origin = 1000, ((1000-cont.cy) * 3600 / cont.scale)

    return cont
restquaver = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 492, 401, 588, 81)
    c1 = CircleInvolute(cont, 588, 81, -0.347314, 0.937749, 480, 125, -0.784883, -0.619644)
    c2 = CircleInvolute(cont, 549, 211, -0.347314, 0.937749, 441, 255, -0.784883, -0.619644)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    cont.default_nib = 8

    blob(c1, 1, 'r', 33, 3)
    blob(c2, 1, 'r', 33, 3)
    cont.cy = c1.compute_y(1) - 33*sin(c1.compute_theta(1)-pi/2) + 76

    cont.origin = 1000-(39*1800/cont.scale), ((1000-cont.cy) * 3600 / cont.scale)

    return cont
restsemi = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 453, 531, 588, 81)
    c1 = CircleInvolute(cont, 588, 81, -0.347314, 0.937749, 480, 125, -0.784883, -0.619644)
    c2 = CircleInvolute(cont, 549, 211, -0.347314, 0.937749, 441, 255, -0.784883, -0.619644)
    c3 = CircleInvolute(cont, 510, 341, -0.347314, 0.937749, 402, 385, -0.784883, -0.619644)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    cont.default_nib = 8

    blob(c1, 1, 'r', 33, 3)
    blob(c2, 1, 'r', 33, 3)
    blob(c3, 1, 'r', 33, 3)
    cont.cy = c2.compute_y(1) - 33*sin(c1.compute_theta(1)-pi/2) + 76

    cont.origin = 1000-(39*2*1800/cont.scale), ((1000-cont.cy) * 3600 / cont.scale)

    return cont
restdemi = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 414, 661, 588, 81)
    c1 = CircleInvolute(cont, 588, 81, -0.347314, 0.937749, 480, 125, -0.784883, -0.619644)
    c2 = CircleInvolute(cont, 549, 211, -0.347314, 0.937749, 441, 255, -0.784883, -0.619644)
    c3 = CircleInvolute(cont, 510, 341, -0.347314, 0.937749, 402, 385, -0.784883, -0.619644)
    c4 = CircleInvolute(cont, 471, 471, -0.347314, 0.937749, 363, 515, -0.784883, -0.619644)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    cont.default_nib = 8

    blob(c1, 1, 'r', 33, 3)
    blob(c2, 1, 'r', 33, 3)
    blob(c3, 1, 'r', 33, 3)
    blob(c4, 1, 'r', 33, 3)
    cont.cy = c2.compute_y(1) - 33*sin(c1.compute_theta(1)-pi/2) + 76

    cont.origin = 1000-(39*3*1800/cont.scale), ((1000-cont.cy) * 3600 / cont.scale)

    return cont
resthemi = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 375, 791, 588, 81)
    c1 = CircleInvolute(cont, 588, 81, -0.347314, 0.937749, 480, 125, -0.784883, -0.619644)
    c2 = CircleInvolute(cont, 549, 211, -0.347314, 0.937749, 441, 255, -0.784883, -0.619644)
    c3 = CircleInvolute(cont, 510, 341, -0.347314, 0.937749, 402, 385, -0.784883, -0.619644)
    c4 = CircleInvolute(cont, 471, 471, -0.347314, 0.937749, 363, 515, -0.784883, -0.619644)
    c5 = CircleInvolute(cont, 432, 601, -0.347314, 0.937749, 324, 645, -0.784883, -0.619644)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    cont.default_nib = 8

    blob(c1, 1, 'r', 33, 3)
    blob(c2, 1, 'r', 33, 3)
    blob(c3, 1, 'r', 33, 3)
    blob(c4, 1, 'r', 33, 3)
    blob(c5, 1, 'r', 33, 3)
    cont.cy = c3.compute_y(1) - 33*sin(c1.compute_theta(1)-pi/2) + 76

    cont.origin = 1000-(39*4*1800/cont.scale), ((1000-cont.cy) * 3600 / cont.scale)

    return cont
restquasi = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.before = "1000 0 translate -1 1 scale"
    cont.extra = restquaver

    return cont
restcrotchetx = tmpfn()

# ----------------------------------------------------------------------
# Rectangular rests (minim/semibreve, breve, longa, double longa).

def tmpfn():
    cont = GlyphContext()

    cont.extra = \
    "newpath 440 439 moveto 440 505 lineto 614 505 lineto 614 439 lineto closepath fill "

    return cont
restminim = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = \
    "newpath 452 406 moveto 452 538 lineto 602 538 lineto 602 406 lineto closepath fill "

    return cont
restbreve = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = \
    "newpath 452 406 moveto 452 670 lineto 602 670 lineto 602 406 lineto closepath fill "

    return cont
restlonga = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = restlonga, "-300 0 translate", restlonga

    return cont
restdbllonga = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = restminim, \
    "newpath 390 505 moveto 664 505 lineto 12 setlinewidth 1 setlinecap stroke"

    cont.oy = 505

    return cont
restminimo = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = restminim, \
    "newpath 390 439 moveto 664 439 lineto 12 setlinewidth 1 setlinecap stroke"

    cont.oy = 439

    return cont
restsemibreveo = tmpfn()

# ----------------------------------------------------------------------
# Digits for time signatures.

def tmpfn(): # zero
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 528, 253, 1, 0, 572, 273, 0.60745, 0.794358)
    c1 = CircleInvolute(cont, 572, 273, 0.60745, 0.794358, 597, 362, 0, 1)
    c2 = CircleInvolute(cont, 597, 362, 0, 1, 572, 451, -0.60745, 0.794358)
    c3 = CircleInvolute(cont, 572, 451, -0.60745, 0.794358, 528, 471, -1, 0)
    c4 = CircleInvolute(cont, 528, 471, -1, 0, 484, 451, -0.60745, -0.794358)
    c5 = CircleInvolute(cont, 484, 451, -0.60745, -0.794358, 459, 362, 0, -1)
    c6 = CircleInvolute(cont, 459, 362, 0, -1, 484, 273, 0.60745, -0.794358)
    c7 = CircleInvolute(cont, 484, 273, 0.60745, -0.794358, 528, 253, 1, 0)
    c0.weld_to(1, c1, 0)
    c0.weld_to(0, c7, 1)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c6, 0)
    c6.weld_to(1, c7, 0)
    # End saved data

    ymid = float(c1.compute_y(1))
    yext = abs(ymid - c0.compute_y(0))
    cont.default_nib = lambda c,x,y,t,theta: (6, 0, 25*(1-abs((y-ymid)/yext)**2.5), 25*(1-abs((y-ymid)/yext)**2.5))

    return cont
big0 = tmpfn()
def tmpfn(): # one
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 467, 342, 513, 257)
    c1 = StraightLine(cont, 538, 257, 538, 467)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: (6, 0, 10*t, 0)

    y2 = c1.compute_y(1)
    y1 = y2-50 # this value is the same as is used for the serif on the 4
    serif = lambda y: qc(y<y1,0,26*((y-y1)/(y2-y1))**4)
    c1.nib = lambda c,x,y,t,theta: (6, 0, 25+serif(y), 25+serif(y))

    return cont
big1 = tmpfn()
def tmpfn(): # two

    # At the top of the 2 I use the same hack as I did for the 3 to
    # get the inner curve. See below. 

    # Secondary context.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 615, 419, -0.26963, 0.962964, 560, 424, -0.865426, -0.501036)
    c1 = CircleInvolute(cont, 560, 424, -0.865426, -0.501036, 449, 467, -0.419058, 0.907959)
    c0.weld_to(1, c1, 0)
    # End saved data
    tc0, tc1 = c0, c1

    # Primary context.
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 615, 419, -0.26963, 0.962964, 548, 468, -0.83205, -0.5547)
    c1 = CircleInvolute(cont, 548, 468, -0.83205, -0.5547, 449, 467, -0.419058, 0.907959)
    c2 = CircleInvolute(cont, 449, 467, 0, -1, 523, 381, 0.94299, -0.33282)
    c3 = CircleInvolute(cont, 523, 381, 0.94299, -0.33282, 583, 307, 0, -1)
    c4 = CircleInvolute(cont, 583, 307, 0, -1, 530, 253, -1, 0)
    c5 = CircleInvolute(cont, 530, 253, -1, 0, 467, 275, -0.7282, 0.685365)
    c6 = CircleInvolute(cont, 561, 307, 0, -1, 512, 261, -1, 0)
    c7 = CircleInvolute(cont, 512, 261, -1, 0, 467, 275, -0.7282, 0.685365)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c6.weld_to(1, c7, 0)
    # End saved data

    cont.default_nib = 6

    xr = c0.compute_x(0)
    xl = c1.compute_x(1)
    c0.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[tc0,tc1],0,2,6)
    c1.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[tc0,tc1],1,2,6)
    c4.nib = lambda c,x,y,t,theta: (lambda x1,x2: ((lambda k: (6, 0, k, k))(22*((x-min(x1,x2))/abs(x2-x1)))))(c.compute_x(0),c.compute_x(1))
    c3.nib = c2.nib = lambda c,x,y,t,theta: (lambda x1,x2: ((lambda k: (6, 0, k, k))(22*((x-min(x1,x2))/abs(x2-x1)))))(c2.compute_x(0),c3.compute_x(1))

    blob(c5, 1, 'l', 25, 4)

    return cont
big2 = tmpfn()
def tmpfn(): # three
    cont = GlyphContext()

    # Bit of a hack here. The x-based formula I use for the nib
    # thickness of the right-hand curves c1-c4 leaves a nasty corner
    # at the very top and bottom, which I solve by drawing an
    # independent inner curve at each end (c6-c9). Normally I would
    # solve this using follow_curveset_nib, filling the area between
    # c6-c7 and c0-c1 and that between c8-c9 and c2-c3; however,
    # that gets the inner curve right but destroys the outer curve
    # from the x-based formula. So instead I just do the simplest
    # possible thing: draw c1-c4 with the nib thickness formula as
    # before, but then draw c6-c9 over the top at constant
    # thickness, relying on the fact that they never separate far
    # enough from what would otherwise be the inner curve to open a
    # gap between them.

    # Saved data from gui.py
    c0 = CircleInvolute(cont, 462, 446, 0.7282, 0.685365, 525, 471, 1, 0)
    c1 = CircleInvolute(cont, 525, 471, 1, 0, 580, 416, 0, -1)
    c2 = CircleInvolute(cont, 580, 416, 0, -1, 504, 352, -1, 0)
    c3 = CircleInvolute(cont, 504, 352, 1, 0, 578, 303, 0, -1)
    c4 = CircleInvolute(cont, 578, 303, 0, -1, 525, 253, -1, 0)
    c5 = CircleInvolute(cont, 525, 253, -1, 0, 462, 276, -0.7282, 0.685365)
    c6 = CircleInvolute(cont, 462, 446, 0.7282, 0.685365, 510, 464, 1, 0)
    c7 = CircleInvolute(cont, 510, 464, 1, 0, 558, 416, 0, -1)
    c8 = CircleInvolute(cont, 556, 303, 0, -1, 511, 261, -1, 0)
    c9 = CircleInvolute(cont, 511, 261, -1, 0, 462, 276, -0.7282, 0.685365)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0, 1)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c6.weld_to(1, c7, 0)
    c8.weld_to(1, c9, 0)
    # End saved data

    cont.default_nib = 6

    c1.nib = c2.nib = c3.nib = c4.nib = lambda c,x,y,t,theta: (lambda x1,x2: ((lambda k: (6, 0, k, k))(22*((x-min(x1,x2))/abs(x2-x1)))))(c.compute_x(0),c.compute_x(1))

    blob(c0, 0, 'r', 25, 4)

    blob(c5, 1, 'l', 25, 4)

    return cont
big3 = tmpfn()
def tmpfn(): # four
    # Secondary context
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 496, 257, 0, 1, 432, 413, -0.665255, 0.746617)
    # End saved data
    tc0 = c0

    # Primary context
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 571, 257, 432, 413)
    c1 = StraightLine(cont, 432, 413, 514, 413)
    c2 = StraightLine(cont, 551, 299, 551, 467)
    c3 = StraightLine(cont, 450, 411, 599, 411)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[tc0],0,1,6)
    c1.nib = 6
    gradient = tan(c0.compute_theta(0))
    y0 = c2.compute_y(0)
    y2 = c2.compute_y(1)
    y1 = y2-50 # this value is the same as is used for the serif on the 1
    serif = lambda y: qc(y<y1,0,26*((y-y1)/(y2-y1))**4)
    c2.nib = lambda c,x,y,t,theta: (6, 0, 25+serif(y), min(25+serif(y), -25+(y-y0)/gradient))
    c3.nib = 8

    # Top line and baseline of the digits are defined by the 4.
    cont.ty = c0.compute_y(0) - c0.compute_nib(0)[0]
    cont.by = c2.compute_y(1) + c2.compute_nib(1)[0]
    # Icky glitch-handling stuff (see -lily section).
    cont.gy = (cont.ty + cont.by) / 2 + (250*cont.scale/3600.0)

    return cont
big4 = tmpfn()
def tmpfn(): # five
    cont = GlyphContext()

    # At the bottom of the 5 I use the same hack as I did for the 3
    # to get the inner curve. See below.

    # Saved data from gui.py
    c0 = CircleInvolute(cont, 461, 442, 0.7282, 0.685365, 524, 471, 1, 0)
    c1 = CircleInvolute(cont, 524, 471, 1, 0, 579, 400, 0, -1)
    c2 = CircleInvolute(cont, 579, 400, 0, -1, 520, 332, -1, 0)
    c3 = CircleInvolute(cont, 520, 332, -1, 0, 461, 351, -0.795432, 0.606043)
    c4 = StraightLine(cont, 461, 351, 469, 257)
    c5 = CircleInvolute(cont, 469, 257, 0.938343, 0.345705, 596, 257, 0.953583, -0.301131)
    c6 = CircleInvolute(cont, 461, 442, 0.7282, 0.685365, 506, 463, 1, 0)
    c7 = CircleInvolute(cont, 506, 463, 1, 0, 557, 400, 0, -1)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0, 1)
    c4.weld_to(1, c5, 0, 1)
    c6.weld_to(1, c7, 0)
    # End saved data

    cont.default_nib = 6

    c1.nib = c2.nib = lambda c,x,y,t,theta: (lambda x1,x2: ((lambda k: (6, 0, k, k))(22*((x-min(x1,x2))/abs(x2-x1)))))(c.compute_x(0),c.compute_x(1))

    xr = c5.compute_x(1)
    xl = c5.compute_x(0)
    taper = lambda x: (qc(x>0, (lambda t: t**4), (lambda t: 0)))(x)
    xm = xl + 0.5*(xr-xl)
    c5.nib = lambda c,x,y,t,theta: (6,-pi/2,32*(1-taper((x-xm)/(xr-xm))),0)

    blob(c0, 0, 'r', 25, 4)

    return cont
big5 = tmpfn()
def tmpfn(): # six
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 535, 471, -1, 0, 479, 408, 0, -1)
    c1 = CircleInvolute(cont, 479, 408, 0, -1, 535, 349, 1, 0)
    c2 = CircleInvolute(cont, 535, 349, 1, 0, 591, 408, 0, 1)
    c3 = CircleInvolute(cont, 591, 408, 0, 1, 535, 471, -1, 0)
    c4 = CircleInvolute(cont, 535, 471, -1, 0, 491, 446, -0.60745, -0.794358)
    c5 = CircleInvolute(cont, 491, 446, -0.60745, -0.794358, 466, 360, 0, -1)
    c6 = CircleInvolute(cont, 466, 360, 0, -1, 493, 277, 0.658505, -0.752577)
    c7 = CircleInvolute(cont, 493, 277, 0.658505, -0.752577, 546, 253, 1, 0)
    c8 = CircleInvolute(cont, 546, 253, 1, 0, 598, 275, 0.7282, 0.685365)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c6, 0)
    c6.weld_to(1, c7, 0)
    c7.weld_to(1, c8, 0)
    # End saved data

    ymid = float(c5.compute_y(1))
    yext = abs(ymid - c4.compute_y(0))
    cont.default_nib = lambda c,x,y,t,theta: (6, 0, 25*(1-abs((y-ymid)/yext)**2.5), 25*(1-abs((y-ymid)/yext)**2.5))

    ytop2 = c2.compute_y(0)
    ybot2 = c3.compute_y(1)
    ymid2 = (ytop2+ybot2)/2
    yext2 = abs(ymid2 - ytop2)
    c2.nib = c3.nib = lambda c,x,y,t,theta: (6, 0, 22*(1-abs((y-ymid2)/yext2)**2.5), 22*(1-abs((y-ymid2)/yext2)**2.5))

    ythreshold = c1.compute_y(0.5)
    c0.nib = c1.nib = lambda c,x,y,t,theta: (6, 0, 22*(1-abs((y-ymid2)/yext2)**2.5), qc(y>ythreshold, 0, 22*(1-abs((y-ymid2)/yext2)**2.5)))

    c8.nib = 6
    blob(c8, 1, 'r', 25, 4)

    # FIXME: consider redoing this using the x-based formula I used
    # on the 3.

    return cont
big6 = tmpfn()
def tmpfn(): # seven

    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 538, 467, 0, -1, 568, 353, 0.544988, -0.838444)
    c1 = CircleInvolute(cont, 568, 353, 0.544988, -0.838444, 604, 257, 0.233373, -0.972387)
    c2 = CircleInvolute(cont, 604, 257, -0.546268, 0.837611, 491, 284, -0.7282, -0.685365)
    c3 = CircleInvolute(cont, 491, 284, -0.7282, -0.685365, 444, 283, -0.563337, 0.826227)
    c4 = CircleInvolute(cont, 479, 467, 0, -1, 545, 345, 0.759257, -0.650791)
    c5 = CircleInvolute(cont, 545, 345, 0.759257, -0.650791, 604, 257, 0.233373, -0.972387)
    c6 = CircleInvolute(cont, 604, 257, -0.563337, 0.826227, 558, 273, -0.768221, -0.640184)
    c7 = CircleInvolute(cont, 558, 273, -0.768221, -0.640184, 444, 283, -0.563337, 0.826227)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c6, 0, 1)
    c6.weld_to(1, c7, 0)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c4,c5,c6,c7],0,4,6)
    c1.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c4,c5,c6,c7],1,4,6)
    c2.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c4,c5,c6,c7],2,4,6)
    c3.nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,[c4,c5,c6,c7],3,4,6)
    c4.nib = c5.nib = c6.nib = c7.nib = 1 # essentially ignore these
    x2 = c7.compute_x(1)
    x0 = c7.compute_x(0)
    x1 = x2 + 0.4 * (x0-x2)
    serif = lambda x: qc(x>x1,0,26*((x-x1)/(x2-x1))**4)
    xc3 = eval(c3.serialise())
    xc7 = eval(c7.serialise())
    xc3.nib = xc7.nib = lambda c,x,y,t,theta: (lambda k: (6,pi/2,k,k))(serif(x))

    return cont
big7 = tmpfn()
def tmpfn(): # eight

    # The traditional 8 just contains _too_ many ellipse-like curves
    # to draw sensibly using involutes, so I resorted to squashing
    # the x-axis down by 3/4 so that the ellipses became more
    # circular.

    # This glyph is designed so that its _exterior_ outline is
    # mirror-symmetric. To this end, constraints currently
    # unenforced by gui.py are:
    #  - c4 should be an exact mirror image of c3
    #  - c2 should be an exact mirror image of c7
    #
    # Also, of course, c0 must join up precisely to c3 just as c4
    # does, and likewise c2 to c7 just like c6.

    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 529, 255, -1, 0, 490, 293, 0.485643, 0.874157, mx=(0.75, 0, 0, 1))
    c1 = CircleInvolute(cont, 490, 293, 0.485643, 0.874157, 575, 353, 0.925547, 0.378633, mx=(0.75, 0, 0, 1))
    c2 = CircleInvolute(cont, 575, 353, 0.925547, 0.378633, 529, 469, -1, 0, mx=(0.75, 0, 0, 1))
    c3 = CircleInvolute(cont, 559, 365, 0.942302, -0.334765, 529, 255, -1, 0, mx=(0.75, 0, 0, 1))
    c4 = CircleInvolute(cont, 529, 255, -1, 0, 499, 365, 0.942302, 0.334765, mx=(0.75, 0, 0, 1))
    c5 = CircleInvolute(cont, 499, 365, 0.942302, 0.334765, 576, 427, 0.263117, 0.964764, mx=(0.75, 0, 0, 1))
    c6 = CircleInvolute(cont, 576, 427, 0.263117, 0.964764, 529, 469, -1, 0, mx=(0.75, 0, 0, 1))
    c7 = CircleInvolute(cont, 529, 469, -1, 0, 483, 353, 0.925547, -0.378633, mx=(0.75, 0, 0, 1))
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c6, 0)
    c6.weld_to(1, c7, 0)
    # End saved data
    tcurves = c0,c1,c2
    curves = c4,c5,c6

    for i in range(len(tcurves)):
        tcurves[i].nib = 0
    for i in range(len(curves)):
        curves[i].i = i
        curves[i].nib = lambda c,x,y,t,theta: follow_curveset_nib(c,x,y,t,theta,tcurves,c.i,len(curves),8)

    c3.nib = lambda c,x,y,t,theta: (lambda x1,x2: ((lambda k: (8, 0, 0, k))(9*((x-min(x1,x2))/abs(x2-x1)))))(c.compute_x(0),c.compute_x(1))
    c7.nib = lambda c,x,y,t,theta: (lambda x1,x2: ((lambda k: (8, 0, k, 0))(9*((max(x1,x2)-x)/abs(x2-x1)))))(c.compute_x(0),c.compute_x(1))

    return cont
big8 = tmpfn()
def tmpfn(): # nine
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 522, 253, 1, 0, 578, 316, 0, 1)
    c1 = CircleInvolute(cont, 578, 316, 0, 1, 522, 375, -1, 0)
    c2 = CircleInvolute(cont, 522, 375, -1, 0, 466, 316, 0, -1)
    c3 = CircleInvolute(cont, 466, 316, 0, -1, 522, 253, 1, 0)
    c4 = CircleInvolute(cont, 522, 253, 1, 0, 566, 278, 0.60745, 0.794358)
    c5 = CircleInvolute(cont, 566, 278, 0.60745, 0.794358, 591, 364, 0, 1)
    c6 = CircleInvolute(cont, 591, 364, 0, 1, 564, 447, -0.658505, 0.752577)
    c7 = CircleInvolute(cont, 564, 447, -0.658505, 0.752577, 511, 471, -1, 0)
    c8 = CircleInvolute(cont, 511, 471, -1, 0, 459, 449, -0.7282, -0.685365)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c6, 0)
    c6.weld_to(1, c7, 0)
    c7.weld_to(1, c8, 0)
    # End saved data

    ymid = float(c5.compute_y(1))
    yext = abs(ymid - c4.compute_y(0))
    cont.default_nib = lambda c,x,y,t,theta: (6, 0, 25*(1-abs((y-ymid)/yext)**2.5), 25*(1-abs((y-ymid)/yext)**2.5))

    ytop2 = c2.compute_y(0)
    ybot2 = c3.compute_y(1)
    ymid2 = (ytop2+ybot2)/2
    yext2 = abs(ymid2 - ytop2)
    c2.nib = c3.nib = lambda c,x,y,t,theta: (6, 0, 22*(1-abs((y-ymid2)/yext2)**2.5), 22*(1-abs((y-ymid2)/yext2)**2.5))

    ythreshold = c1.compute_y(0.5)
    c0.nib = c1.nib = lambda c,x,y,t,theta: (6, 0, qc(y<ythreshold, 0, 22*(1-abs((y-ymid2)/yext2)**2.5)), 22*(1-abs((y-ymid2)/yext2)**2.5))

    c8.nib = 6
    blob(c8, 1, 'r', 25, 4)

    # FIXME: consider redoing this using the x-based formula I used
    # on the 3. (Well, recopying from the 6 if I do.)

    return cont
big9 = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 500, 362, 600, 362)
    c1 = StraightLine(cont, 550, 312, 550, 412)
    # End saved data

    cont.default_nib = 12

    return cont
asciiplus = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 500, 362, 600, 362)
    # End saved data

    cont.default_nib = 12

    return cont
asciiminus = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 573, 435, 0.843662, 0.536875, 548, 535, -0.894427, 0.447214)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: 4+25*cos(pi/2*t)**2

    blob(c0, 0, 'l', 5, 0)

    return cont
asciicomma = tmpfn()
def tmpfn():
    cont = GlyphContext()

    cont.extra = "newpath 500 439 34 0 360 arc fill"

    return cont
asciiperiod = tmpfn()
for x in big0,big1,big2,big3,big5,big6,big7,big8,big9,\
         asciiplus,asciiminus,asciicomma,asciiperiod:
    x.ty,x.by,x.gy = big4.ty,big4.by,big4.gy

# ----------------------------------------------------------------------
# The small digits used for ntuplets and fingering marks. Scaled and
# sheared versions of the big time-signature digits.

def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big0, "grestore"
    return cont
small0 = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big1, "grestore"
    return cont
small1 = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big2, "grestore"
    return cont
small2 = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big3, "grestore"
    return cont
small3 = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big4, "grestore"
    return cont
small4 = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big5, "grestore"
    return cont
small5 = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big6, "grestore"
    return cont
small6 = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big7, "grestore"
    return cont
small7 = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big8, "grestore"
    return cont
small8 = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 480 480 translate 0.6 0.72 scale [1 0 -.3 1 0 0] concat -480 -480 translate", big9, "grestore"
    return cont
small9 = tmpfn()

# ----------------------------------------------------------------------
# The big C for common time signature.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 732, 391, -0.5547, -0.83205, 659, 353, -1, 0)
    c1 = CircleInvolute(cont, 659, 353, -1, 0, 538, 470, 0, 1)
    c2 = CircleInvolute(cont, 538, 470, 0, 1, 650, 587, 1, 0)
    c3 = CircleInvolute(cont, 650, 587, 1, 0, 742, 508, 0.135113, -0.99083)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    # End saved data

    c0.nib = c3.nib = 6
    c1.nib = c2.nib = lambda c,x,y,t,theta: (lambda x1,x2: ((lambda k: (6, 0, k, 0))(44*((x-max(x1,x2))/abs(x2-x1))**2)))(c.compute_x(0),c.compute_x(1))

    blob(c0, 0, 'r', 32, 8)

    return cont
timeC = tmpfn()
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 648, 272, 648, 672)
    # End saved data

    cont.default_nib = 8

    cont.extra = timeC

    return cont
timeCbar = tmpfn()

# ----------------------------------------------------------------------
# Dynamics marks (f,m,p,s,z).

def tmpfn(): # m (we do this one first to define the baseline)
    cont = GlyphContext()

    # Saved data from gui.py
    c0 = CircleInvolute(cont, 539, 378, 0.328521, -0.944497, 585, 331, 1, 0)
    c1 = CircleInvolute(cont, 585, 331, 1, 0, 606, 360, -0.287348, 0.957826)
    c2 = StraightLine(cont, 606, 360, 576, 460)
    c3 = CircleInvolute(cont, 621, 360, 0.287348, -0.957826, 648, 331, 1, 0)
    c4 = CircleInvolute(cont, 648, 331, 1, 0, 669, 360, -0.287348, 0.957826)
    c5 = StraightLine(cont, 669, 360, 639, 460)
    c6 = CircleInvolute(cont, 684, 360, 0.287348, -0.957826, 711, 331, 1, 0)
    c7 = CircleInvolute(cont, 711, 331, 1, 0, 732, 360, -0.286206, 0.958168)
    c8 = StraightLine(cont, 732, 360, 709, 437)
    c9 = CircleInvolute(cont, 709, 437, -0.286206, 0.958168, 726, 463, 1, 0)
    c10 = CircleInvolute(cont, 726, 463, 1, 0, 773, 415, 0.328521, -0.944497)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c6.weld_to(1, c7, 0)
    c7.weld_to(1, c8, 0)
    c8.weld_to(1, c9, 0)
    c9.weld_to(1, c10, 0)
    # End saved data

    cont.default_nib = 4
    c2.nib = c5.nib = c8.nib = (4,0,15,15)
    phi = c1.compute_theta(1)
    psi = c0.compute_theta(0)
    c0.nib = c1.nib = c3.nib = c4.nib = c6.nib = c7.nib = c9.nib = c10.nib = lambda c,x,y,t,theta: (lambda k: 4+k)(15*cos(pi/2*(theta-phi)/(psi-phi))**2)

    cont.lby = c2.compute_y(1)
    cont.by = c2.compute_y(1) + c2.compute_nib(1)[0]
    cont.lx = 557 + (-41.38 - 34.62) * cont.scale / 3600.0
    cont.rx = 751 - (-49.53 - -87.53) * cont.scale / 3600.0

    return cont
dynamicm = tmpfn()
def tmpfn(): # f
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 720, 269, -0.60745, -0.794358, 690, 254, -1, 0)
    c1 = CircleInvolute(cont, 690, 254, -1, 0, 600, 359, -0.21243, 0.977176)
    c2 = CircleInvolute(cont, 600, 359, -0.21243, 0.977176, 550, 506, -0.462566, 0.886585)
    c3 = CircleInvolute(cont, 550, 506, -0.462566, 0.886585, 490, 552, -1, 0)
    c4 = CircleInvolute(cont, 490, 552, -1, 0, 463, 516, 0.301131, -0.953583)
    c5 = StraightLine(cont, 540, 349, 661, 349)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0)
    # End saved data

    cont.default_nib = 8

    yt = c1.compute_y(0)
    yb = c3.compute_y(1)
    m = 0.6

    # Construct a quintic which is 0 with derivative 0 at both 0 and
    # 1, and 1 with derivative 0 at m. Second derivative at 0 is
    # non-negative iff m <= 0.6, so we require 0.4 <= m <= 0.6 for
    # the values on [0,1] to be contained within [0,1].
    denom = m*m*m*(-1+m*(3+m*(-3+m)))
    a = (2-4*m)/denom
    b = (-4+m*(5+m*5))/denom
    c = (2+m*(2+m*-10))/denom
    d = (m*(-3+m*5))/denom
    quintic = lambda x: x*x*(d+x*(c+x*(b+x*a)))

    c1.nib = c2.nib = c3.nib = lambda c,x,y,t,theta: (8+20*quintic((y-yb)/(yt-yb))**0.3)
    #cos(pi/2 * ((theta % (2*pi))-phi)/(psi-phi))**2)

    c5.nib = 10

    blob(c0, 0, 'r', 20, 8)
    blob(c4, 1, 'r', 20, 8)

    cont.by = dynamicm.by
    cont.lx = 496.7 + (-81.74 - -86.74) * cont.scale / 3600.0
    cont.rx = 657.7 - (-139.36 - -165.36) * cont.scale / 3600.0

    return cont
dynamicf = tmpfn()
def tmpfn(): # p
    cont = GlyphContext()

    # Saved data from gui.py
    c0 = CircleInvolute(cont, 539, 378, 0.328521, -0.944497, 585, 331, 1, 0)
    c1 = CircleInvolute(cont, 585, 331, 1, 0, 606, 360, -0.289177, 0.957276)
    c2 = StraightLine(cont, 606, 360, 548, 552)
    c3 = CircleInvolute(cont, 607, 428, 0, -1, 669, 336, 1, 0)
    c4 = CircleInvolute(cont, 669, 336, 1, 0, 697, 370, 0, 1)
    c5 = CircleInvolute(cont, 697, 370, 0, 1, 633, 464, -1, 0)
    c6 = CircleInvolute(cont, 633, 464, -1, 0, 607, 428, 0, -1)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c3.weld_to(1, c4, 0)
    c3.weld_to(0, c6, 1)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c6, 0)
    # End saved data

    y2 = c2.compute_y(1)
    y1 = y2 - 20
    serif = lambda y: qc(y<y1,0,26*((y-y1)/(y2-y1))**4)
    c2.nib = lambda c,x,y,t,theta: (lambda k: (6,0,k,k))(18 + serif(y))
    phi = c1.compute_theta(1)
    psi = c0.compute_theta(0)
    c0.nib = c1.nib = lambda c,x,y,t,theta: (lambda k: 4+k)(20*cos(pi/2*(theta-phi)/(psi-phi))**2)

    gamma = 1/tan(c2.compute_theta(0.5))
    shear = lambda theta: (lambda dx,dy: atan2(-dy,dx+gamma*dy))(cos(theta),-sin(theta))
    cont.default_nib = lambda c,x,y,t,theta: 12-9*sin(shear(theta))

    cont.by = dynamicm.by
    cont.lx = 510.4 + (-23.26 - -38.26) * cont.scale / 3600.0
    cont.rx = 690.615 - (-51.72 - -28.72) * cont.scale / 3600.0

    return cont
dynamicp = tmpfn()
def tmpfn(): # r
    cont = GlyphContext()

    # Saved data from gui.py
    c0 = CircleInvolute(cont, 551, 348, 0.635707, -0.77193, 585, 331, 1, 0)
    c1 = CircleInvolute(cont, 585, 331, 1, 0, 606, 360, -0.287348, 0.957826)
    c2 = StraightLine(cont, 606, 360, 576, 460)
    c3 = CircleInvolute(cont, 617, 360, 0.287348, -0.957826, 687, 344, 0.707107, 0.707107)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    # End saved data

    cont.default_nib = 4
    c2.nib = (4,0,15,15)
    phi = c1.compute_theta(1)
    psi = c0.compute_theta(0)
    c0.nib = c1.nib = lambda c,x,y,t,theta: (lambda k: 4+k)(15*cos(pi/2*(theta-phi)/(psi-phi))**2)
    c3.nib = lambda c,x,y,t,theta: (lambda k: 8+k)(15*cos(pi/2*(theta-phi)/(psi-phi))**2)

    cont.by = dynamicm.by
    cont.lx = 557 + (-18.93 - 58.07) * cont.scale / 3600.0
    cont.rx = 670.187 - (-66.39 - -57.39) * cont.scale / 3600.0

    return cont
dynamicr = tmpfn()
def tmpfn(): # s

    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 635, 341, -0.845489, -0.533993, 564, 361, 0, 1)
    c1 = CircleInvolute(cont, 564, 361, 0, 1, 592, 398, 0.885832, 0.464007)
    c2 = CircleInvolute(cont, 592, 398, 0.885832, 0.464007, 619, 437, -0.196116, 0.980581)
    c3 = CircleInvolute(cont, 619, 437, -0.196116, 0.980581, 541, 452, -0.776114, -0.630593)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    # End saved data

    phi = c1.compute_theta(1)
    cont.default_nib = lambda c,x,y,t,theta: 15+6*cos(theta-phi)
    blob(c0, 0, 'r', 12, 7)
    blob(c3, 1, 'r', 12, 7)

    cont.by = dynamicm.by
    cont.lx = 529 + (-0.36 - 52.64) * cont.scale / 3600.0
    cont.rx = 628.788 - (-36.35 - -51.35) * cont.scale / 3600.0

    return cont
dynamics = tmpfn()
def tmpfn(): # z

    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 568, 338, 678, 338)
    c1 = StraightLine(cont, 678, 338, 539, 453)
    c2 = CircleInvolute(cont, 539, 453, 0.707107, -0.707107, 602, 441, 0.784883, 0.619644)
    c3 = CircleInvolute(cont, 602, 441, 0.784883, 0.619644, 654, 427, 0.33035, -0.943858)
    c4 = CircleInvolute(cont, 654, 427, 0.33035, -0.943858, 654, 411, -0.341743, -0.939793)
    c0.weld_to(1, c1, 0, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0)
    # End saved data

    x2 = c0.compute_x(0)
    x1 = x2 + 30
    x0 = c0.compute_x(1)
    serif = lambda x: qc(x>x1,0,13*((x-x1)/(x2-x1))**4)
    serifangle = 1.15 # radians of the slant at the end of the z's top stroke
    c0.nib = lambda c,x,y,t,theta: (lambda k: (6,1.15,0,k))(min(26 + serif(x), x0-x))
    c1.nib = 6

    xr = c3.compute_x(1)
    xl = c2.compute_x(0)
    m = 0.5
    # Construct a cubic which is 0 at both 0 and 1, and 1 with
    # derivative 0 at m. Second derivative at 0 is non-negative iff
    # m <= 2/3, so we require 1/3 <= m <= 2/3 for the values on
    # [0,1] to be contained within [0,1].
    a = (1-2*m)/(m**4-2*m**3+m**2)
    b = (3*m**2-1)/(m**4-2*m**3+m**2)
    c = -a-b
    #sys.stderr.write("set xrange [0:1]\nplot x*(%g+x*(%g+x*%g))\n" % (c,b,a))
    cubic = lambda x: x*(c+x*(b+x*a))
    slantangle = c1.compute_theta(1)
    c2.nib = c3.nib = lambda c,x,y,t,theta: ((lambda k: (6, slantangle, k, k))(16*cubic((x-xl)/(xr-xl))))

    c4.nib = 6
    blob(c4, 1, 'l', 12, 8)

    cont.by = dynamicm.by
    cont.lx = 533 + (-0.2 - 22.8) * cont.scale / 3600.0
    cont.rx = 650.1 - (-65.44 - -42.44) * cont.scale / 3600.0

    return cont
dynamicz = tmpfn()
for x in dynamicf, dynamicm, dynamicp, dynamicr, dynamics, dynamicz:
    x.origin = (x.by * 3600. / x.scale, x.lx * 3600. / x.scale)
    x.width = x.rx - x.lx

# ----------------------------------------------------------------------
# Accent mark.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 421, 415, 633, 472)
    c1 = StraightLine(cont, 633, 472, 421, 529)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    cont.default_nib = 10

    return cont
accent = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = accent, "800 0 translate -1 1 scale", accent

    return cont
espressivo = tmpfn()

# ----------------------------------------------------------------------
# Miscellaneous articulation marks.

def tmpfn(): # stopping
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 527, 316, 527, 466)
    c1 = StraightLine(cont, 453, 391, 601, 391)
    # End saved data

    cont.default_nib = 8

    return cont
stopping = tmpfn()

def tmpfn(): # legato
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 454, 461, 600, 461)
    # End saved data

    cont.default_nib = 8
    cont.ly = c0.compute_y(0.5)

    return cont
legato = tmpfn()

def tmpfn(): # staccato
    cont = GlyphContext()

    cont.extra = "newpath 527 446 26 0 360 arc fill "

    return cont
staccato = tmpfn()

def tmpfn(): # 'portato' - a staccato stacked on a legato
    cont = GlyphContext()

    cont.extra = legato, "0 -54 translate", staccato

    cont.ly = legato.ly

    return cont
portatoup = tmpfn()    

def tmpfn(): # portato, the other way up
    cont = GlyphContext()

    cont.extra = "0 1000 translate 1 -1 scale", portatoup

    cont.ly = 1000 - portatoup.ly

    return cont
portatodn = tmpfn()    

def tmpfn(): # staccatissimo
    cont = GlyphContext()

    cont.extra = "newpath 498 381 moveto 526 478 lineto 554 381 lineto closepath fill "

    return cont
staccatissdn = tmpfn()

def tmpfn(): # staccatissimo pointing the other way
    cont = GlyphContext()

    cont.extra = "newpath 498 478 moveto 526 381 lineto 554 478 lineto closepath fill "

    return cont
staccatissup = tmpfn()

def tmpfn(): # snap-pizzicato
    cont = GlyphContext()

    cont.extra = "newpath 500 500 50 0 360 arc 500 500 moveto 500 400 lineto 16 setlinewidth 1 setlinejoin 1 setlinecap stroke"

    return cont
snappizz = tmpfn()

# ----------------------------------------------------------------------
# The 'segno' sign (for 'D.S. al Fine' sort of stuff).

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 504, 162, -0.284088, -0.958798, 420, 152, -0.393919, 0.919145)
    c1 = CircleInvolute(cont, 420, 152, -0.393919, 0.919145, 514, 295, 0.923077, 0.384615)
    c2 = CircleInvolute(cont, 514, 295, 0.923077, 0.384615, 608, 438, -0.393919, 0.919145)
    c3 = CircleInvolute(cont, 608, 438, -0.393919, 0.919145, 524, 428, -0.284088, -0.958798)
    c4 = StraightLine(cont, 624, 128, 404, 462)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    # End saved data

    c4.nib = 10

    cont.default_nib = lambda c,x,y,t,theta: 8+16*cos(theta-c.nibdir(t))**2

    phi0 = c0.compute_theta(0)
    phi1 = c1.compute_theta(0) + 3*pi/2
    phi2 = c1.compute_theta(1) + pi
    c0.nibdir = lambda t: phi0 + (phi1-phi0)*t
    c1.nibdir = lambda t: phi1 + (phi2-phi1)*t
    c2.nibdir = lambda t: phi2 + (phi1-phi2)*t
    c3.nibdir = lambda t: phi1 + (phi0-phi1)*t

    # Draw the two dots.
    cont.extra = \
    "newpath 618 251 24 0 360 arc fill " + \
    "newpath 410 339 24 0 360 arc fill "

    return cont
segno = tmpfn()

# ----------------------------------------------------------------------
# The coda sign.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 528, 198, 528, 475)
    c1 = StraightLine(cont, 418, 337, 639, 337)
    c2 = CircleInvolute(cont, 528, 230, 1, 0, 596, 337, 0, 1)
    c3 = CircleInvolute(cont, 596, 337, 0, 1, 528, 444, -1, 0)
    c4 = CircleInvolute(cont, 528, 444, -1, 0, 460, 337, 0, -1)
    c5 = CircleInvolute(cont, 460, 337, 0, -1, 528, 230, 1, 0)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c2, 0)
    # End saved data

    c0.nib = c1.nib = 10
    cont.default_nib = lambda c,x,y,t,theta: 8+12*abs(sin(theta))**2.5

    return cont
coda = tmpfn()

def tmpfn(): # variant square form used by Lilypond
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 528, 198, 528, 475)
    c1 = StraightLine(cont, 418, 337, 639, 337)
    c2 = CircleInvolute(cont, 469, 241, 0.970143, -0.242536, 587, 241, 0.970143, 0.242536)
    c3 = CircleInvolute(cont, 587, 241, 0.110432, 0.993884, 587, 433, -0.110432, 0.993884)
    c4 = CircleInvolute(cont, 587, 433, -0.970143, 0.242536, 469, 433, -0.970143, -0.242536)
    c5 = CircleInvolute(cont, 469, 433, -0.110432, -0.993884, 469, 241, 0.110432, -0.993884)
    c2.weld_to(1, c3, 0, 1)
    c3.weld_to(1, c4, 0, 1)
    c4.weld_to(1, c5, 0, 1)
    c5.weld_to(1, c2, 0, 1)
    # End saved data

    c0.nib = c1.nib = 10
    c3.nib = c5.nib = 8, 0, 12, 12
    xmid = c0.compute_x(0)
    xend = c2.compute_x(0)
    xdiff = xend - xmid
    c2.nib = c4.nib = lambda c,x,y,t,theta: (lambda k: (8, 0, k, k))(12.0*(x-xmid)/xdiff)

    return cont
varcoda = tmpfn()

# ----------------------------------------------------------------------
# The turn sign.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 443, 448, -0.860927, 0.508729, 370, 401, 0, -1)
    c1 = CircleInvolute(cont, 370, 401, 0, -1, 423, 347, 1, 0)
    c2 = CircleInvolute(cont, 423, 347, 1, 0, 525, 402, 0.707107, 0.707107)
    c3 = CircleInvolute(cont, 525, 402, 0.707107, 0.707107, 627, 457, 1, 0)
    c4 = CircleInvolute(cont, 627, 457, 1, 0, 681, 395, 0, -1)
    c5 = CircleInvolute(cont, 681, 395, 0, -1, 607, 356, -0.860927, 0.508729)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    c3.weld_to(1, c4, 0)
    c4.weld_to(1, c5, 0)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: 8+16*cos(theta-c.nibdir(theta))**2

    shift = lambda theta: (theta+pi/2) % (2*pi) - pi/2

    theta0 = shift(c0.compute_theta(0))
    phi0 = theta0
    theta2 = shift(c2.compute_theta(1))
    phi2 = theta2 + pi
    c0.nibdir = c1.nibdir = c2.nibdir = c3.nibdir = c4.nibdir = c5.nibdir = \
    lambda theta: phi0 + (phi2-phi0)*(shift(theta)-theta0)/(theta2-theta0)

    return cont
turn = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 525, 304, 525, 500)
    # End saved data

    cont.default_nib = 8

    cont.extra = turn

    return cont
invturn = tmpfn()

# ----------------------------------------------------------------------
# Mordent and its relatives.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 397.935, 402, 426, 368)
    c1 = StraightLine(cont, 426, 368, 498, 439)
    c2 = StraightLine(cont, 498, 439, 556, 368)
    c3 = StraightLine(cont, 556, 368, 628, 439)
    c4 = StraightLine(cont, 628, 439, 656.065, 405)
    c0.weld_to(1, c1, 0, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    c3.weld_to(1, c4, 0, 1)
    # End saved data

    alpha = c2.compute_theta(.5)
    cont.default_nib = (8, alpha, 30, 30)

    cont.cy = c2.compute_y(.5)

    return cont
mordentupper = tmpfn()
def tmpfn(): # and the same with a vertical line through it
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 526, 264, 526, 466)
    # End saved data

    cont.default_nib = 8

    # These things are stacked above the note, so they each have a
    # baseline and a height rather than being vertically centred.
    # Hence we must translate the other mordent sign upwards.
    cont.extra = "gsave 0 -43 translate", mordentupper, "grestore"

    cont.cy = mordentupper.cy - 43

    return cont
mordentlower = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 397.935, 402, 426, 368)
    c1 = StraightLine(cont, 426, 368, 498, 439)
    c2 = StraightLine(cont, 498, 439, 556, 368)
    c3 = StraightLine(cont, 556, 368, 628, 439)
    c4 = StraightLine(cont, 628, 439, 686, 368)
    c5 = StraightLine(cont, 686, 368, 758, 439)
    c6 = StraightLine(cont, 758, 439, 786.065, 405)
    c0.weld_to(1, c1, 0, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    c3.weld_to(1, c4, 0, 1)
    c4.weld_to(1, c5, 0, 1)
    c5.weld_to(1, c6, 0, 1)
    # End saved data

    alpha = c2.compute_theta(.5)
    cont.default_nib = (8, alpha, 30, 30)

    cont.cy = mordentupper.cy

    return cont
mordentupperlong = tmpfn()
def tmpfn(): # and the same with a vertical line through it
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 656, 264, 656, 466)
    # End saved data

    cont.default_nib = 8

    # These things are stacked above the note, so they each have a
    # baseline and a height rather than being vertically centred.
    # Hence we must translate the other mordent sign upwards.
    cont.extra = "gsave 0 -43 translate", mordentupperlong, "grestore"

    cont.cy = mordentupper.cy - 43

    return cont
mordentupperlower = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 397.935, 402, 426, 368)
    c1 = StraightLine(cont, 426, 368, 498, 439)
    c2 = StraightLine(cont, 498, 439, 556, 368)
    c3 = StraightLine(cont, 556, 368, 628, 439)
    c4 = StraightLine(cont, 628, 439, 686, 368)
    c5 = StraightLine(cont, 686, 368, 758, 439)
    c6 = StraightLine(cont, 758, 439, 786.065, 405)
    c7 = CircleInvolute(cont, 370, 524, -0.354654, -0.934998, 397.935, 402, 0.636585, -0.771206)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c7, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    c3.weld_to(1, c4, 0, 1)
    c4.weld_to(1, c5, 0, 1)
    c5.weld_to(1, c6, 0, 1)
    # End saved data

    alpha = c2.compute_theta(.5)
    cont.default_nib = (8, alpha, 30, 30)
    c0.nib = c7.nib = 8

    cont.cy = mordentupper.cy

    return cont
upmordentupperlong = tmpfn()
def tmpfn(): # and the same with a vertical line through it
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 656, 264, 656, 466)
    # End saved data

    cont.default_nib = 8

    # These things are stacked above the note, so they each have a
    # baseline and a height rather than being vertically centred.
    # Hence we must translate the other mordent sign upwards.
    cont.extra = "gsave 0 -43 translate", upmordentupperlong, "grestore"

    cont.cy = mordentupper.cy - 43

    return cont
upmordentupperlower = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 378.602, 425.667, 426, 368)
    c1 = StraightLine(cont, 426, 368, 498, 439)
    c2 = StraightLine(cont, 498, 439, 556, 368)
    c3 = StraightLine(cont, 556, 368, 628, 439)
    c4 = StraightLine(cont, 628, 439, 686, 368)
    c5 = StraightLine(cont, 686, 368, 758, 439)
    c6 = StraightLine(cont, 758, 439, 786.065, 405)
    c7 = CircleInvolute(cont, 378, 287, -0.481919, 0.876216, 378.602, 425.667, 0.636585, 0.771206)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c7, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    c3.weld_to(1, c4, 0, 1)
    c4.weld_to(1, c5, 0, 1)
    c5.weld_to(1, c6, 0, 1)
    # End saved data

    alpha = c2.compute_theta(.5)
    cont.default_nib = (8, alpha, 30, 30)
    c0.nib = c7.nib = 8

    cont.cy = mordentupper.cy

    return cont
downmordentupperlong = tmpfn()
def tmpfn(): # and the same with a vertical line through it
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 656, 264, 656, 466)
    # End saved data

    cont.default_nib = 8

    # These things are stacked above the note, so they each have a
    # baseline and a height rather than being vertically centred.
    # Hence we must translate the other mordent sign upwards.
    cont.extra = "gsave 0 -43 translate", downmordentupperlong, "grestore"

    cont.cy = mordentupper.cy - 43

    return cont
downmordentupperlower = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 378.602, 425.667, 426, 368)
    c1 = StraightLine(cont, 426, 368, 498, 439)
    c2 = StraightLine(cont, 498, 439, 556, 368)
    c3 = StraightLine(cont, 556, 368, 628, 439)
    c4 = StraightLine(cont, 628, 439, 686, 368)
    c5 = StraightLine(cont, 686, 368, 758, 439)
    c6 = StraightLine(cont, 758, 439, 786.065, 405)
    c7 = StraightLine(cont, 378.602, 277, 378.602, 425.667)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c7, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    c3.weld_to(1, c4, 0, 1)
    c4.weld_to(1, c5, 0, 1)
    c5.weld_to(1, c6, 0, 1)
    # End saved data

    alpha = c2.compute_theta(.5)
    cont.default_nib = (8, alpha, 30, 30)
    c0.nib = c7.nib = 8

    cont.cy = mordentupper.cy

    return cont
straightmordentupperlong = tmpfn()

def tmpfn():
    # Lilypond renders this glyph as a reflection of
    # upmordentupperlong, but it seems obviously preferable to me to
    # render it as a rotation of downmordentupperlong, so as to get
    # the mordent zigzag itself the same way round.
    cont = GlyphContext()
    cont.extra = "gsave 1000 1000 translate -1 -1 scale", downmordentupperlong
    cont.cy = 1000 - mordentupper.cy
    return cont
mordentupperlongdown = tmpfn()
def tmpfn():
    # Likewise, Lilypond uses a reflection of downmordentupperlong,
    # whereas I rotate upmordentupperlong.
    cont = GlyphContext()
    cont.extra = "gsave 1000 1000 translate -1 -1 scale", upmordentupperlong
    cont.cy = 1000 - mordentupper.cy
    return cont
mordentupperlongup = tmpfn()

# ----------------------------------------------------------------------
# Fermata signs.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 364, 465, 0, -1, 527, 313, 1, 0)
    c1 = CircleInvolute(cont, 527, 313, 1, 0, 690, 465, 0, 1)
    c0.weld_to(1, c1, 0)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: 8+18*cos(theta)**2

    # Draw the dot.
    cont.extra = "newpath 527 446 24 0 360 arc fill "

    return cont
fermata = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 384, 465, 527, 234)
    c1 = StraightLine(cont, 527, 233, 670, 465)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    c0.nib = 8
    c1.nib = lambda c,x,y,t,theta: (8, pi, min(24, t*250), 0)

    # Draw the dot.
    cont.extra = "newpath 527 446 24 0 360 arc fill "

    return cont
fermata0 = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 384, 441, 384, 313)
    c1 = StraightLine(cont, 384, 313, 670, 313)
    c2 = StraightLine(cont, 670, 313, 670, 441)
    c0.weld_to(1, c1, 0, 1)
    c1.weld_to(1, c2, 0, 1)
    # End saved data

    cont.default_nib = 8, pi/2, 24, 24

    # Draw the dot.
    cont.extra = "newpath 527 446 24 0 360 arc fill "

    return cont
fermata2 = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 424, 447, 424, 370)
    c1 = StraightLine(cont, 424, 370, 630, 370)
    c2 = StraightLine(cont, 630, 370, 630, 447)
    c3 = StraightLine(cont, 384, 441, 384, 286)
    c4 = StraightLine(cont, 384, 286, 670, 286)
    c5 = StraightLine(cont, 670, 286, 670, 441)
    c0.weld_to(1, c1, 0, 1)
    c1.weld_to(1, c2, 0, 1)
    c3.weld_to(1, c4, 0, 1)
    c4.weld_to(1, c5, 0, 1)
    # End saved data

    c0.nib = c1.nib = c2.nib = 8, pi/2, 18, 18
    c3.nib = c4.nib = c5.nib = 8, pi/2, 24, 24

    # Draw the dot.
    cont.extra = "newpath 527 446 24 0 360 arc fill "

    return cont
fermata3 = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = '0 1000 translate 1 -1 scale', fermata
    return cont
fermataup = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = '0 1000 translate 1 -1 scale', fermata0
    return cont
fermata0up = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = '0 1000 translate 1 -1 scale', fermata2
    return cont
fermata2up = tmpfn()
def tmpfn():
    cont = GlyphContext()
    cont.extra = '0 1000 translate 1 -1 scale', fermata3
    return cont
fermata3up = tmpfn()

# ----------------------------------------------------------------------
# Parentheses to go round accidentals.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 367, 334, -0.478852, 0.877896, 367, 604, 0.478852, 0.877896)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: 6+8*sin(pi*t)

    cont.rx = c0.compute_x(0) + c0.compute_nib(0) + 10

    return cont
acclparen = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = "gsave 1000 0 translate -1 1 scale", acclparen, "grestore"

    cont.lx = 1000 - acclparen.rx

    return cont
accrparen = tmpfn()

# ----------------------------------------------------------------------
# Braces between staves.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 442, 109, -0.490261, 0.871576, 401, 692, 0.33035, 0.943858)
    c1 = CircleInvolute(cont, 401, 692, 0.33035, 0.943858, 313, 994, -0.810679, 0.585491)
    c0.weld_to(1, c1, 0)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: 2+30*sin(pi/2*t)**2
    c1.nib = lambda c,x,y,t,theta: 2+30*cos(pi/2*t)**2

    cont.scale = 1600
    cont.origin = 1000, 10

    return cont
braceupper = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 442, 919, -0.490261, -0.871576, 401, 336, 0.33035, -0.943858)
    c1 = CircleInvolute(cont, 401, 336, 0.33035, -0.943858, 313, 34, -0.810679, -0.585491)
    c0.weld_to(1, c1, 0)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: 2+30*sin(pi/2*t)**2
    c1.nib = lambda c,x,y,t,theta: 2+30*cos(pi/2*t)**2

    cont.scale = 1600
    cont.origin = 1000, 2170

    return cont
bracelower = tmpfn()

def tmpfn(span): # arbitrarily sized brace
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 87, 20, -0.490261, 0.871576, 64, 313, 0.33035, 0.943858)
    c1 = CircleInvolute(cont, 64, 313, 0.33035, 0.943858, 20, 464, -0.810679, 0.585491)
    c2 = CircleInvolute(cont, 20, 464, 0.810679, 0.585491, 64, 615, -0.33035, 0.943858)
    c3 = CircleInvolute(cont, 64, 615, -0.33035, 0.943858, 87, 907, 0.490261, 0.871576)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0)
    # End saved data

    # We want the absolute distance between the _outer_ edges of the
    # tips - i.e. the logical tip positions incremented by the
    # thinnest nib width - to be equal to 'span'. The minimum nib
    # width is fixed at that which would have equalled 4 under the
    # scale of 1600, i.e. 4*3600/1600 = 9 in output coordinates.
    # Hence we want the logical distance between the tip centres to
    # be span-18.
    xtop = c0.compute_y(0)
    xbot = c3.compute_y(1)
    cont.scale = 3600 * (xbot-xtop) / float(span-18)

    # Now the maximum nib width is fixed relative to the brace
    # shape, and hence is (nearly) always 16. The minimum is
    # calculated from the above scale.
    nibmin = 4 * cont.scale / 1600
    nibmax = (8 + (32-8)*sqrt((span-525)/(4000.-525))) * cont.scale / 1600
    nibdiff = nibmax - nibmin

    c0.nib = lambda c,x,y,t,theta: nibmin+nibdiff*sin(pi/2*t)**2
    c1.nib = lambda c,x,y,t,theta: nibmin+nibdiff*cos(pi/2*t)**2
    c2.nib = lambda c,x,y,t,theta: nibmin+nibdiff*sin(pi/2*t)**2
    c3.nib = lambda c,x,y,t,theta: nibmin+nibdiff*cos(pi/2*t)**2

    cont.canvas_size = 105, 930

    cont.trace_res = max(8, int(ceil(8*sqrt(1600.0/cont.scale))))
    cont.curve_res = max(1001, int(span))

    return cont
scaledbrace = tmpfn # note this is a function, not an actual GlyphContext

# Should be equivalent to 'braceupper'+'bracelower'
fixedbrace = scaledbrace(3982)

# ----------------------------------------------------------------------
# End pieces for an arbitrary-sized bracket between two staves.

def tmpfn(vwid):
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 616, 615, -0.808736, -0.588172, 407, 541, -1, 0)
    c1 = StraightLine(cont, 407, 541, 407, 441)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    if vwid < 0:
        c1.nib = 0
    else:
        c1.nib = (4,0,vwid,0)
    y0 = c0.compute_y(0)
    y1 = c0.compute_y(1)
    c0.nib = lambda c,x,y,t,theta: (4,pi/2,45*(y-y0)/(y1-y0),0)

    cont.hy = c1.compute_y(0)

    return cont
bracketlower = tmpfn(75)
bracketlowerlily = tmpfn(-1) # omit the vertical
def tmpfn(x):
    cont = GlyphContext()

    cont.extra = "0 946 translate 1 -1 scale", x

    cont.hy = 946 - x.hy

    return cont
bracketupper = tmpfn(bracketlower)
bracketupperlily = tmpfn(bracketlowerlily)

# ----------------------------------------------------------------------
# Note head indicating an artificial harmonic above another base
# note.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 526, 402, 0.526355, 0.850265, 609, 476, 0.884918, 0.465746)
    c1 = CircleInvolute(cont, 609, 476, -0.850265, 0.526355, 528, 541, -0.613941, 0.789352)
    c2 = CircleInvolute(cont, 528, 541, -0.526355, -0.850265, 445, 467, -0.884918, -0.465746)
    c3 = CircleInvolute(cont, 445, 467, 0.850265, -0.526355, 526, 402, 0.613941, -0.789352)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c3, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    # End saved data

    c0.nib = c2.nib = lambda c,x,y,t,theta: (2,theta-pi/2,min(24,t*200,(1-t)*200),0)
    c1.nib = c3.nib = lambda c,x,y,t,theta: (2,theta-pi/2,min(6,t*50,(1-t)*50),0)

    cont.ay = c1.compute_y(0)

    return cont
harmart = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 526, 402, 0.526355, 0.850265, 609, 476, 0.884918, 0.465746)
    c1 = CircleInvolute(cont, 609, 476, -0.850265, 0.526355, 528, 541, -0.613941, 0.789352)
    c2 = CircleInvolute(cont, 528, 541, -0.526355, -0.850265, 445, 467, -0.884918, -0.465746)
    c3 = CircleInvolute(cont, 445, 467, 0.850265, -0.526355, 526, 402, 0.613941, -0.789352)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c3, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: ptp_nib(c,x,y,t,theta,527,472,2)

    cont.ay = c1.compute_y(0)

    return cont
harmartfilled = tmpfn()

# ----------------------------------------------------------------------
# Natural harmonic mark and a couple of other miscellaneous note flags.

def tmpfn():
    cont = GlyphContext()

    cont.extra = "newpath 527 439 40 0 360 arc 6 setlinewidth stroke "

    return cont
harmnat = tmpfn()

def tmpfn(thumb):
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 500, 450, 1, 0, 537, 500, 0, 1)
    c1 = CircleInvolute(cont, 537, 500, 0, 1, 500, 550, -1, 0)
    c2 = CircleInvolute(cont, 500, 550, -1, 0, 463, 500, 0, -1)
    c3 = CircleInvolute(cont, 463, 500, 0, -1, 500, 450, 1, 0)
    c4 = StraightLine(cont, 500, 580, 500, 554)
    c0.weld_to(1, c1, 0)
    c0.weld_to(0, c3, 1)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: 6 + 4*sin(theta)**2
    if thumb:
        c4.nib = 10
    else:
        c4.nib = 0

    cont.cy = c0.compute_y(1)

    return cont
flagopen = tmpfn(0)
flagthumb = tmpfn(1)

# ----------------------------------------------------------------------
# Ditto (same as previous bar) mark.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 425, 604, 630, 339)
    # End saved data

    c0.nib = (4,0,40,40)

    cont.extra = \
    "newpath 423 397 35 0 360 arc fill " + \
    "newpath 632 546 35 0 360 arc fill "

    return cont
ditto = tmpfn()

# ----------------------------------------------------------------------
# Breath mark and related stuff.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 577, 341, 0.843661, 0.536875, 548, 466, -0.894427, 0.447214)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: 4+30*cos(pi/2*t)**2

    blob(c0, 0, 'l', 5, 0)

    return cont
breath = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 547, 466, 587, 341)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: 4+14*t

    return cont
varbreath = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = "1000 1000 translate -1 -1 scale", breath
    return cont
revbreath = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = "1000 1000 translate -1 -1 scale", varbreath
    return cont
revvarbreath = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 400, 625, 550, 375)
    c1 = StraightLine(cont, 475, 625, 625, 375)
    # End saved data
    cont.default_nib = 8
    return cont
caesura = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 400, 625, 550-400, 375-625, 500, 375, 0, -1)
    c1 = CircleInvolute(cont, 475, 625, 625-475, 375-625, 575, 375, 0, -1)
    # End saved data
    cont.default_nib = lambda c,x,y,t,theta: 8+4.0*(x-c.compute_x(0))/(c.compute_x(1)-c.compute_x(0))
    return cont
caesuracurved = tmpfn()

# ----------------------------------------------------------------------
# Random functional stuff like arrowheads.

def tmpfn(rotate, is_open):
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 375, 450, 0.83205, 0.5547, 500, 500, 0.977802, 0.209529)
    c1 = CircleInvolute(cont, 500, 500, -0.977802, 0.209529, 375, 550, -0.83205, 0.5547)
    c2 = CircleInvolute(cont, 375, 550, 0.519947, -0.854199, 375, 450, -0.519947, -0.854199)
    c0.weld_to(1, c1, 0, 1)
    c0.weld_to(0, c2, 1, 1)
    c1.weld_to(1, c2, 0, 1)
    # End saved data

    if is_open:
        cont.default_nib = 10
        c2.nib = 0
    else:
        x0, y0 = c0.compute_x(0.5), c0.compute_y(1)
        cont.default_nib = lambda c,x,y,t,theta: ptp_nib(c,x,y,t,theta,x0,y0,10)

    if rotate:
        cont.before = "500 500 translate %g rotate -500 -500 translate" % rotate

    cont.cx = cont.cy = 500
    cont.extent = abs(c0.compute_y(0) - cont.cy) + 6

    return cont
openarrowright = tmpfn(0,1)
closearrowright = tmpfn(0,0)
openarrowleft = tmpfn(180,1)
closearrowleft = tmpfn(180,0)
openarrowup = tmpfn(270,1)
closearrowup = tmpfn(270,0)
openarrowdown = tmpfn(90,1)
closearrowdown = tmpfn(90,0)

# ----------------------------------------------------------------------
# Flat (and multiples of flat).

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 430, 236, 430, 548)
    c1 = Bezier(cont, 430, 548, 481, 499, 515.999, 458, 505, 424)
    c2 = CircleInvolute(cont, 505, 424, -0.307801, -0.951451, 430, 436, -0.462566, 0.886585)
    c0.weld_to(1, c1, 0, 1)
    c1.weld_to(1, c2, 0)
    # End saved data

    c0.nib = 8

    x0 = c1.compute_x(0)
    x1 = c1.compute_x(1)
    cont.default_nib = lambda c,x,y,t,theta: 8+12*((x-x0)/(x1-x0))**2

    cont.ox = c0.compute_x(0.5)
    cont.hy = 469 # no sensible way to specify this except manually

    return cont
flat = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 430, 236, 430, 548)
    c1 = Bezier(cont, 430, 548, 481, 499, 515.999, 458, 505, 424)
    c2 = CircleInvolute(cont, 505, 424, -0.307801, -0.951451, 430, 436, -0.462566, 0.886585)
    c0.weld_to(1, c1, 0, 1)
    c1.weld_to(1, c2, 0)
    # End saved data

    c0.nib = 8

    x0 = c1.compute_x(0)
    x1 = c1.compute_x(1)
    cont.default_nib = lambda c,x,y,t,theta: 8+12*((x-x0)/(x1-x0))**2

    cont.ox = c0.compute_x(0.5)
    cont.hy = 469 # no sensible way to specify this except manually

    cont.extra = "gsave 430 236 16 add translate 0.7 dup scale -500 dup 150 sub translate", closearrowup, "grestore"

    return cont
flatup = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 430, 236, 430, 568)
    c1 = Bezier(cont, 430, 548, 481, 499, 515.999, 458, 505, 424)
    c2 = CircleInvolute(cont, 505, 424, -0.307801, -0.951451, 430, 436, -0.462566, 0.886585)
    c1.weld_to(1, c2, 0)
    # End saved data

    c0.nib = 8

    x0 = c1.compute_x(0)
    x1 = c1.compute_x(1)
    cont.default_nib = lambda c,x,y,t,theta: 8+12*((x-x0)/(x1-x0))**2

    cont.ox = c0.compute_x(0.5)
    cont.hy = 469 # no sensible way to specify this except manually

    cont.extra = "gsave 430 568 16 sub translate 0.7 dup scale -500 dup 150 add translate", closearrowdown, "grestore"

    return cont
flatdn = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 430, 236, 430, 568)
    c1 = Bezier(cont, 430, 548, 481, 499, 515.999, 458, 505, 424)
    c2 = CircleInvolute(cont, 505, 424, -0.307801, -0.951451, 430, 436, -0.462566, 0.886585)
    c1.weld_to(1, c2, 0)
    # End saved data

    c0.nib = 8

    x0 = c1.compute_x(0)
    x1 = c1.compute_x(1)
    cont.default_nib = lambda c,x,y,t,theta: 8+12*((x-x0)/(x1-x0))**2

    cont.ox = c0.compute_x(0.5)
    cont.hy = 469 # no sensible way to specify this except manually

    cont.extra = flatup.extra + flatdn.extra

    return cont
flatupdn = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = flat, "gsave -90 0 translate", flat, "grestore"
    cont.ox = flat.ox - 90
    cont.hy = flat.hy
    return cont
doubleflat = tmpfn()

def tmpfn():
    cont = GlyphContext()
    reflectpt = flat.ox - 20
    cont.extra = "gsave %g 0 translate -1 1 scale" % (2*reflectpt), \
    flat, "grestore"
    cont.hy = flat.hy
    return cont
semiflat = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = flat, semiflat
    cont.hy = flat.hy
    return cont
sesquiflat = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 580 380 translate 0.5 dup scale -580 -380 translate", flat, "grestore"
    return cont
smallflat = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 370, 363, 490, 303)
    # End saved data

    c0.nib = 8

    cont.ox = flat.ox
    cont.hy = flat.hy

    cont.extra = flat

    return cont
flatslash = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 372, 373, 490, 333)
    c1 = StraightLine(cont, 372, 313, 490, 273)
    # End saved data

    c0.nib = c1.nib = 8

    cont.ox = flat.ox
    cont.hy = flat.hy

    cont.extra = flat

    return cont
flatslash2 = tmpfn()

def tmpfn():
    cont = GlyphContext()
    reflectpt = flat.ox - 20
    cont.extra = "gsave %g 0 translate -1 1 scale" % (2*reflectpt), \
    flatslash, "grestore"
    cont.hy = flatslash.hy
    return cont
semiflatslash = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 282, 361, 490, 281)
    # End saved data

    c0.nib = 8

    cont.ox = doubleflat.ox
    cont.hy = doubleflat.hy

    cont.extra = doubleflat

    return cont
doubleflatslash = tmpfn()

# ----------------------------------------------------------------------
# Natural.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 519, 622, 519, 399)
    c1 = StraightLine(cont, 519, 399, 442, 418)
    c2 = StraightLine(cont, 442, 318, 442, 539)
    c3 = StraightLine(cont, 442, 539, 519, 520)
    c0.weld_to(1, c1, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.cy = (c0.compute_y(0) + c2.compute_y(0)) / 2.0

    return cont
natural = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 519, 622, 519, 399)
    c1 = StraightLine(cont, 519, 399, 442, 418)
    c2 = StraightLine(cont, 442, 318, 442, 539)
    c3 = StraightLine(cont, 442, 539, 519, 520)
    c0.weld_to(1, c1, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.extra = "gsave 442 318 translate 0.7 dup scale -500 dup 150 sub translate", closearrowup, "grestore"

    cont.cy = natural.cy

    return cont
naturalup = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 519, 622, 519, 399)
    c1 = StraightLine(cont, 519, 399, 442, 418)
    c2 = StraightLine(cont, 442, 318, 442, 539)
    c3 = StraightLine(cont, 442, 539, 519, 520)
    c0.weld_to(1, c1, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.extra = "gsave 519 622 translate 0.7 dup scale -500 dup 150 add translate", closearrowdown, "grestore"

    cont.cy = natural.cy

    return cont
naturaldn = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 519, 622, 519, 399)
    c1 = StraightLine(cont, 519, 399, 442, 418)
    c2 = StraightLine(cont, 442, 318, 442, 539)
    c3 = StraightLine(cont, 442, 539, 519, 520)
    c0.weld_to(1, c1, 0, 1)
    c2.weld_to(1, c3, 0, 1)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.extra = naturalup.extra + naturaldn.extra

    cont.cy = natural.cy

    return cont
naturalupdn = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 580 280 translate 0.5 dup scale -580 -280 translate", natural, "grestore"
    return cont
smallnatural = tmpfn()

# ----------------------------------------------------------------------
# Sharp.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 442, 306, 442, 652)
    c1 = StraightLine(cont, 493, 291, 493, 637)
    c2 = StraightLine(cont, 413, 419, 523, 392)
    c3 = StraightLine(cont, 413, 551, 523, 524)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.cy = (c2.compute_y(0) + c3.compute_y(1))/2.0

    return cont
sharp = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 442, 306, 442, 652)
    c1 = StraightLine(cont, 493, 271, 493, 637)
    c2 = StraightLine(cont, 413, 419, 523, 392)
    c3 = StraightLine(cont, 413, 551, 523, 524)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.extra = "gsave 493 271 translate 0.7 dup scale -500 dup 150 sub translate", closearrowup, "grestore"

    cont.cy = sharp.cy

    return cont
sharpup = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 442, 306, 442, 672)
    c1 = StraightLine(cont, 493, 291, 493, 637)
    c2 = StraightLine(cont, 413, 419, 523, 392)
    c3 = StraightLine(cont, 413, 551, 523, 524)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.extra = "gsave 442 672 translate 0.7 dup scale -500 dup 150 add translate", closearrowdown, "grestore"

    cont.cy = sharp.cy

    return cont
sharpdn = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 442, 306, 442, 672)
    c1 = StraightLine(cont, 493, 271, 493, 637)
    c2 = StraightLine(cont, 413, 419, 523, 392)
    c3 = StraightLine(cont, 413, 551, 523, 524)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.extra = sharpup.extra + sharpdn.extra

    cont.cy = sharp.cy

    return cont
sharpupdn = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = "gsave 580 280 translate 0.5 dup scale -580 -280 translate", sharp, "grestore"
    return cont
smallsharp = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 442, 306, 442, 652)
    c1 = StraightLine(cont, 413, 421, 472, 401.518)
    c2 = StraightLine(cont, 413, 555, 472, 533.981)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    return cont
semisharp = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 442, 300.351, 442, 646.351)
    c1 = StraightLine(cont, 493, 291, 493, 637)
    c2 = StraightLine(cont, 544, 281.649, 544, 627.649)
    c3 = StraightLine(cont, 413, 414, 574, 384.481)
    c4 = StraightLine(cont, 413, 547, 574, 517.481)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    return cont
sesquisharp = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 442, 306, 442, 652)
    c1 = StraightLine(cont, 493, 291, 493, 637)
    c2 = StraightLine(cont, 413, 397, 523, 370)
    c3 = StraightLine(cont, 413, 573, 523, 546)
    c4 = StraightLine(cont, 401, 487.945, 535, 455.055)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.cy = (c2.compute_y(0) + c3.compute_y(1))/2.0

    return cont
sharp3 = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 442, 306, 442, 652)
    c1 = StraightLine(cont, 413, 399, 472, 379.518)
    c2 = StraightLine(cont, 413, 577, 472, 555.981)
    c3 = StraightLine(cont, 400.5, 492.703, 483.5, 465.297)
    # End saved data

    cont.default_nib = (8, pi/2, 16, 16)

    cont.cy = (c2.compute_y(0) + c3.compute_y(1))/2.0

    return cont
semisharp3 = tmpfn()

# ----------------------------------------------------------------------
# Double sharp.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 409, 426, 504, 521)
    c1 = StraightLine(cont, 409, 521, 504, 426)
    # End saved data

    cont.default_nib = 8

    # Blobs at the ends of the lines.
    cont.extra = \
    "/square { gsave 3 1 roll translate newpath dup dup moveto dup neg dup neg lineto dup neg dup lineto dup neg lineto closepath fill grestore } def " + \
    "newpath 409 426 24 square " + \
    "newpath 409 521 24 square " + \
    "newpath 504 426 24 square " + \
    "newpath 504 521 24 square "

    return cont
doublesharp = tmpfn()

# ----------------------------------------------------------------------
# Arpeggio mark and friends.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = Bezier(cont, 491, 334, 516, 359, 516, 378, 491, 403)
    c1 = Bezier(cont, 491, 403, 466, 428, 466, 447, 491, 472)
    c2 = Bezier(cont, 491, 472, 516, 497, 516, 516, 491, 541)
    c3 = Bezier(cont, 491, 541, 466, 566, 466, 585, 491, 610)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: 4+14*abs(cos(theta + 3*pi/4))**1.5

    return cont
arpeggio = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = Bezier(cont, 491, 334, 516, 359, 516, 378, 491, 403)
    c1 = Bezier(cont, 491, 403, 466, 428, 466, 447, 491, 472)
    c0.weld_to(1, c1, 0)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: 4+14*abs(cos(theta + 3*pi/4))**1.5

    cont.ty = c0.compute_y(0)
    cont.oy = c1.compute_y(1)
    cont.lx = c0.compute_x(0) - closearrowdown.extent
    cont.rx = c0.compute_x(0) + closearrowdown.extent

    return cont
arpeggioshort = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = Bezier(cont, 491, 334, 516, 359, 491, 370, 491, 403)
    # End saved data

    cont.default_nib = lambda c,x,y,t,theta: 4+16*t*(1-t)

    cont.extra = "-9 0 translate", closearrowdown

    cont.lx = arpeggioshort.lx
    cont.rx = arpeggioshort.rx
    cont.ey = c0.compute_y(0)

    return cont
arpeggioarrowdown = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = "1000 1000 translate -1 -1 scale", arpeggioarrowdown

    cont.ey = 1000 - arpeggioarrowdown.ey
    cont.lx = 1000 - arpeggioshort.rx
    cont.rx = 1000 - arpeggioshort.lx

    return cont
arpeggioarrowup = tmpfn()

def tmpfn():
    # Rotate the arpeggio mark by 90 degrees and use it as the wavy
    # line after 'tr' to indicate an extended trill.
    cont = GlyphContext()

    cont.extra = "500 500 translate -90 rotate -500 -500 translate", \
    arpeggioshort

    cont.lx = arpeggioshort.ty
    cont.rx = arpeggioshort.oy

    return cont
trillwiggle = tmpfn()

# ----------------------------------------------------------------------
# Downbow and upbow marks.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 447, 430, 447, 330)
    c1 = StraightLine(cont, 447, 330, 608, 330)
    c2 = StraightLine(cont, 608, 330, 608, 430)
    c0.weld_to(1, c1, 0, 1)
    c1.weld_to(1, c2, 0, 1)
    # End saved data

    cont.default_nib = 8, pi/2, 35, 35

    return cont
bowdown = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 475, 256, 535, 460)
    c1 = StraightLine(cont, 535, 460, 595, 256)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: (6, 0, min(25, (1-t)*100), 0)
    c1.nib = 6

    return cont
bowup = tmpfn()

# ----------------------------------------------------------------------
# Sforzando / marcato is an inverted upbow mark.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = StraightLine(cont, 475, 460, 535, 256)
    c1 = StraightLine(cont, 535, 256, 595, 460)
    c0.weld_to(1, c1, 0, 1)
    # End saved data

    c0.nib = 6
    c1.nib = lambda c,x,y,t,theta: (6, pi, min(25, t*100), 0)

    return cont
sforzando = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = "1000 1000 translate -1 -1 scale", sforzando

    return cont
sforzandodn = tmpfn()

# ----------------------------------------------------------------------
# Repeat mark (just a pair of dots).

def tmpfn():
    cont = GlyphContext()

    cont.extra = \
    "newpath 561 401 32 0 360 arc fill " + \
    "newpath 561 542 32 0 360 arc fill "

    return cont
repeatmarks = tmpfn()

# ----------------------------------------------------------------------
# Grace notes.

def tmpfn():
    cont = GlyphContext()

    cont.extra = [
    "gsave 495 472 translate 0.45 dup scale -527 -472 translate",
    "gsave 602.346 452.748 -450 add translate -535 -465 translate",
    tailquaverup,
    "grestore",
    headcrotchet,
    "newpath 602.346 452.748 moveto 0 -450 rlineto 16 setlinewidth stroke",
    "grestore",
    ]

    return cont
appoggiatura = tmpfn()

def tmpfn():
    cont = GlyphContext()

    # Saved data from gui.py
    c0 = StraightLine(cont, 502, 394, 601, 327)
    # End saved data

    c0.nib = 6

    cont.ox = 532
    cont.oy = 261

    return cont
accslashup = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = appoggiatura, accslashup

    return cont
acciaccatura = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = "-500 0 translate 1 .45 div dup scale", accslashup

    cont.ox = -500 + accslashup.ox / .45
    cont.oy = accslashup.oy / .45

    return cont
accslashbigup = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = '0 1000 translate 1 -1 scale', accslashbigup

    cont.ox = accslashbigup.ox
    cont.oy = 1000 - accslashbigup.oy

    return cont
accslashbigdn = tmpfn()

# ----------------------------------------------------------------------
# Piano pedal marks.

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 340, 451, 0.039968, 0.999201, 293, 487, -0.664364, -0.747409)
    c1 = CircleInvolute(cont, 293, 487, -0.664364, -0.747409, 399, 373, 1, 0)
    c2 = CircleInvolute(cont, 399, 373, 1, 0, 472, 451, -0.485643, 0.874157)
    c3 = CircleInvolute(cont, 472, 451, -0.485643, 0.874157, 421, 441, -0.164399, -0.986394)
    c4 = Bezier(cont, 395, 376, 374.611, 410.556, 351.98, 449.02, 388.876, 485.371)
    c5 = Bezier(cont, 388.876, 485.371, 428.041, 523.958, 366, 586, 331.736, 624.799)
    c6 = CircleInvolute(cont, 331.736, 624.799, 0.225579, -0.974225, 440, 613.5, 0.464007, 0.885832)
    c7 = StraightLine(cont, 440, 613.5, 482, 580)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    c4.weld_to(1, c5, 0)
    c5.weld_to(1, c6, 0, 1)
    c6.weld_to(1, c7, 0, 1)
    # End saved data

    cont.default_nib = 6

    # Construct a quintic which is 0 with derivative 0 at both 0 and
    # 1, and 1 with derivative 0 at m. Second derivative at 0 is
    # non-negative iff m <= 0.6, so we require 0.4 <= m <= 0.6 for
    # the values on [0,1] to be contained within [0,1].
    def quintic(m,x):
        denom = m*m*m*(-1+m*(3+m*(-3+m)))
        a = (2-4*m)/denom
        b = (-4+m*(5+m*5))/denom
        c = (2+m*(2+m*-10))/denom
        d = (m*(-3+m*5))/denom
        return x*x*(d+x*(c+x*(b+x*a)))
    def shift(theta, phi):
        return (theta-(phi+pi)) % (2*pi) + (phi+pi)
    shift01 = 3*pi/4
    end0 = shift(c0.compute_theta(0),shift01)
    end1 = shift(c1.compute_theta(1),shift01)
    c0.nib = c1.nib = lambda c,x,y,t,theta: 6+10*quintic(0.4, (shift(theta, shift01)-end0)/(end1-end0))
    shift23 = -3*pi/4
    end2 = shift(c2.compute_theta(0),shift23)
    end3 = shift(c3.compute_theta(1),shift23)
    c2.nib = c3.nib = lambda c,x,y,t,theta: 6+10*quintic(0.6, (shift(theta, shift23)-end2)/(end3-end2))

    theta45 = (c4.compute_theta(0) + c5.compute_theta(1))/2
    c4.nib = c5.nib = lambda c,x,y,t,theta: 6 + 15*sin(theta-theta45)**2

    theta7 = c7.compute_theta(0)
    c6.nib = lambda c,x,y,t,theta: (6, theta7, 18*t**2, 18*t**2)

    cont.by = c5.compute_y(1) + c5.compute_nib(1)

    return cont
pedP = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 482, 580, 0.786318, -0.617822, 533, 541, 0.804176, -0.594391)
    c1 = CircleInvolute(cont, 533, 541, 0.804176, -0.594391, 520, 496, -1, 0)
    c2 = CircleInvolute(cont, 520, 496, -1, 0, 495, 604, 0.485643, 0.874157)
    c3 = CircleInvolute(cont, 495, 604, 0.485643, 0.874157, 571, 591, 0.581238, -0.813733)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    # End saved data

    theta0 = c0.compute_theta(0)
    theta1 = c3.compute_theta(1)
    c0.nib = 6, theta0, 7, 0 # avoid running over left edge of e
    c1.nib = 6, theta0, 7, 7 # avoid running over left edge of e
    c2.nib = lambda c,x,y,t,theta: (6, theta0, 7+3*t, 7+3*t)
    c3.nib = lambda c,x,y,t,theta: (6, (theta0+t*(theta1-theta0)), 10, 10)

    cont.by = pedP.by

    return cont
pede = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 638, 484, -0.91707, 0.398726, 580, 567, 0, 1)
    c1 = CircleInvolute(cont, 580, 567, 0, 1, 623, 625, 1, 0)
    c2 = CircleInvolute(cont, 623, 625, 1, -0, 664, 527, -0.304776, -0.952424)
    c3 = CircleInvolute(cont, 664, 527, -0.304776, -0.952424, 514, 410, -0.980581, -0.196116)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    c2.weld_to(1, c3, 0)
    # End saved data

    theta0 = -pi
    theta1 = 0
    theta2 = +pi
    c0.nib = c1.nib = lambda c,x,y,t,theta: 6+8*sin(pi*(theta-theta0)/(theta1-theta0))**2
    c2.nib = c3.nib = lambda c,x,y,t,theta: 6+12*sin(pi*(theta-theta1)/(theta2-theta1))**2

    cont.by = pedP.by

    return cont
pedd = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = "newpath 708 611 20 0 360 arc fill "

    cont.by = pedP.by

    return cont
peddot = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = pedP, pede, pedd

    cont.by = pedP.by

    return cont
pedPed = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cont.extra = pedP, pede, pedd, peddot

    cont.by = pedP.by

    return cont
pedPeddot = tmpfn()

# The pedal-up asterisk is drawn by drawing a single curved edge and
# repeating it around the circle eight times.
def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = CircleInvolute(cont, 411, 448, 0.92388, -0.382683, 425, 425, 0, -1)
    c1 = CircleInvolute(cont, 425, 425, 0, -1, 413, 405, -0.747409, -0.664364)
    c2 = CircleInvolute(cont, 413, 405, -0.747409, -0.664364, 425, 373, 1, 0)
    c0.weld_to(1, c1, 0)
    c1.weld_to(1, c2, 0)
    # End saved data

    x0 = c0.compute_x(1)
    cont.default_nib = lambda c,x,y,t,theta: (6, 0, 2*(x0-x), 0)

    cont.cx = x0
    cont.cy = c0.compute_y(0) + (x0 - c0.compute_x(0)) / tan(pi/8)
    cont.r = sqrt((c0.compute_x(0) - cont.cx)**2 + (c0.compute_y(0) - cont.cy)**2)

    return cont
pedstarcomponent = tmpfn()

def tmpfn():
    cont = GlyphContext()

    cx, cy, r = pedstarcomponent.cx, pedstarcomponent.cy, pedstarcomponent.r

    cont.extra = "8 {", pedstarcomponent, \
    "%g %g translate 45 rotate %g %g translate } repeat" % (cx,cy, -cx,-cy) + \
    " newpath %g %g %g 0 360 arc closepath 12 setlinewidth stroke" % (cx,cy, r-5)

    cont.by = pedP.by

    return cont
pedstar = tmpfn()

def tmpfn():
    cont = GlyphContext()
    # Saved data from gui.py
    c0 = Bezier(cont, 463, 538, 493, 518, 540, 544, 570, 524)
    # End saved data

    c0.nib = lambda c,x,y,t,theta: (4, pi/3, 18, 18)

    cont.by = pedP.by

    return cont
peddash = tmpfn()

# ----------------------------------------------------------------------
# Some note flags I don't really understand, but which Lilypond's
# font supports so I must too.

def tmpfn():
    cont = GlyphContext()
    cont.extra = \
    "newpath 450 420 moveto 500 500 50 180 0 arcn 550 420 lineto " + \
    "16 setlinewidth 1 setlinecap stroke"
    cont.cy = 500
    return cont
upedalheel = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = \
    "newpath 450 580 moveto 500 500 50 180 0 arc 550 580 lineto " + \
    "16 setlinewidth 1 setlinecap stroke"
    cont.cy = 500
    return cont
dpedalheel = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = \
    "newpath 450 420 moveto 500 550 lineto 550 420 lineto " + \
    "16 setlinewidth 1 setlinecap 1 setlinejoin stroke"
    cont.cy = 500
    return cont
upedaltoe = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.extra = \
    "newpath 450 580 moveto 500 450 lineto 550 580 lineto " + \
    "16 setlinewidth 1 setlinecap 1 setlinejoin stroke"
    cont.cy = 500
    return cont
dpedaltoe = tmpfn()

# ----------------------------------------------------------------------
# Accordion-specific markings.

def tmpfn(n):
    cont = GlyphContext()
    cont.scale = 1440 # make life easier: one stave space is now 100px
    r = 50*n
    cont.extra = "newpath 500 500 %g 0 360 arc " % r
    for i in range(1,n):
        y = 100*i - r
        x = sqrt(r*r - y*y)
        cont.extra = cont.extra + "%g %g moveto %g %g lineto " % (500-x, 500+y, 500+x, 500+y)
    cont.extra = cont.extra + "8 setlinewidth stroke"
    return cont
acc2 = tmpfn(2)
acc3 = tmpfn(3)
acc4 = tmpfn(4)

def tmpfn(w,h):
    cont = GlyphContext()
    cont.scale = 1440 # make life easier: one stave space is now 100px
    ww = 50*w
    hh = 50*h
    cont.extra = ("newpath %g %g moveto %g %g lineto " + \
    "%g %g lineto %g %g lineto closepath ") % \
    (500-ww,500-hh,500+ww,500-hh,500+ww,500+hh,500-ww,500+hh)
    for i in range(1,h):
        y = 100*i - hh
        cont.extra = cont.extra + "%g %g moveto %g %g lineto " % (500-ww, 500+y, 500+ww, 500+y)
    cont.extra = cont.extra + "8 setlinewidth stroke"
    return cont
accr = tmpfn(2,3)

def tmpfn():
    cont = GlyphContext()
    cont.scale = 1440 # make life easier: one stave space is now 100px
    cont.extra = "newpath 500 500 25 0 360 arc fill "
    return cont
accdot = tmpfn()

def tmpfn():
    cont = GlyphContext()
    cont.scale = 1440 # make life easier: one stave space is now 100px
    cont.extra = "500 500 translate " + \
    "newpath 0 0 100 0 360 arc 8 setlinewidth stroke " + \
    "8 { " + \
    "  newpath 0 65 20 0 360 arc fill " + \
    "  newpath -9 65 moveto 9 65 lineto 4 0 lineto -4 0 lineto fill" + \
    "  " + \
    "  45 rotate" + \
    "} repeat"
    return cont
accstar = tmpfn()

# ----------------------------------------------------------------------
# A blank glyph!

def tmpfn():
    cont = GlyphContext()
    cont.lx = 500
    cont.rx = 600
    cont.by = 500
    cont.ty = 600
    return cont
blank = tmpfn()

# ----------------------------------------------------------------------
# End of actual glyph definitions. Now for the output layer.

verstring = "version unavailable"

lilyglyphlist = [
("accent",       "scripts.sforzato",       0, 0.5,0.5, 1,0.5),
("espressivo",   "scripts.espr",           0, 0.5,0.5, 1,0.5),
("accslashbigup", "flags.ugrace",          0, 'ox','oy', 1,'oy'),
("accslashbigdn", "flags.dgrace",          0, 'ox','oy', 1,'oy'),
("acclparen",    "accidentals.leftparen",  0, 1,0.5, 1,0.5, {"x1":"rx"}),
("accrparen",    "accidentals.rightparen", 0, 0,0.5, 1,0.5, {"x0":"lx"}),
("arpeggioshort", "scripts.arpeggio",      0, 0,'oy', 1,'oy', {"x0":"lx","x1":"rx","y0":"oy","y1":"ty"}),
("arpeggioarrowdown", "scripts.arpeggio.arrow.M1", 0, 0,0, 1,0, {"x0":"lx","x1":"rx","y1":"ey"}),
("arpeggioarrowup", "scripts.arpeggio.arrow.1", 0, 0,0, 1,0, {"x0":"lx","x1":"rx","y0":"ey"}),
("trillwiggle",  "scripts.trill_element",  0, 'lx',0, 1,0, {"x0":"lx", "x1":"rx"}),
# Irritatingly, we have to put the digits' baselines at the
# glitch (see below) rather than at the real baseline.
("big0",         "zero",                   0x0030, 0,'gy', 1,'gy'),
("big1",         "one",                    0x0031, 0,'gy', 1,'gy'),
("big2",         "two",                    0x0032, 0,'gy', 1,'gy'),
("big3",         "three",                  0x0033, 0,'gy', 1,'gy'),
("big4",         "four",                   0x0034, 0,'gy', 1,'gy'),
("big5",         "five",                   0x0035, 0,'gy', 1,'gy'),
("big6",         "six",                    0x0036, 0,'gy', 1,'gy'),
("big7",         "seven",                  0x0037, 0,'gy', 1,'gy'),
("big8",         "eight",                  0x0038, 0,'gy', 1,'gy'),
("big9",         "nine",                   0x0039, 0,'gy', 1,'gy'),
("asciiperiod",  "period",                 0x002e, 0,'gy', 1,'gy'),
("asciicomma",   "comma",                  0x002c, 0,'gy', 1,'gy'),
("asciiplus",    "plus",                   0x002b, 0,'gy', 1,'gy'),
("asciiminus",   "hyphen",                 0x002d, 0,'gy', 1,'gy'),
("bowdown",      "scripts.downbow",        0, 0.5,0, 1,0),
("bowup",        "scripts.upbow",          0, 0.5,0, 1,0),
("bracketlowerlily", "brackettips.down",   0, 0,'hy', 1,'hy'),
("bracketupperlily", "brackettips.up",     0, 0,'hy', 1,'hy'),
("breath",       "scripts.rcomma",         0, 0,0.5, 1,0.5),
("revbreath",    "scripts.lcomma",         0, 0,0.5, 1,0.5),
("varbreath",    "scripts.rvarcomma",      0, 0.5,0.5, 1,0.5),
("revvarbreath", "scripts.lvarcomma",      0, 0.5,0.5, 1,0.5),
("caesura",      "scripts.caesura",        0, 0,0.4, 1,0.4),
("caesura",      "scripts.caesura.straight", 0, 0,0.4, 1,0.4),
("caesuracurved", "scripts.caesura.curved", 0, 0,0.4, 1,0.4),
("breve",        "noteheads.sM1",          0, 0,0.5, 1,0.5),
("clefC",        "clefs.C",                0, 0,0.5, 1,0.5),
("clefF",        "clefs.F",                0, 0,'hy', 1,'hy'),
("clefG",        "clefs.G",                0, 0,'hy', 1,'hy'),
("clefTAB",      "clefs.tab",              0, 0,'hy', 1,'hy'),
("clefperc",     "clefs.percussion",       0, 0,0.5, 1,0.5),
("clefCsmall",   "clefs.C_change",         0, 0,0.5, 1,0.5),
("clefFsmall",   "clefs.F_change",         0, 0,'hy', 1,'hy'),
("clefGsmall",   "clefs.G_change",         0, 0,'hy', 1,'hy'),
("clefTABsmall", "clefs.tab_change",       0, 0,'hy', 1,'hy'),
("clefpercsmall", "clefs.percussion_change", 0, 0,0.5, 1,0.5),
("coda",         "scripts.coda",           0, 0.5,0.5, 1,0.5),
("varcoda",      "scripts.varcoda",        0, 0.5,0.5, 1,0.5),
("dynamicf",     "f",                      0x0066, 'lx','by', 'rx','by', {"x0":"lx", "x1":"rx", "xw":"rx"}),
("dynamicm",     "m",                      0x006d, 'lx','by', 'rx','by', {"x0":"lx", "x1":"rx", "xw":"rx"}),
("dynamicp",     "p",                      0x0070, 'lx','by', 'rx','by', {"x0":"lx", "x1":"rx", "xw":"rx"}),
("dynamicr",     "r",                      0x0072, 'lx','by', 'rx','by', {"x0":"lx", "x1":"rx", "xw":"rx"}),
("dynamics",     "s",                      0x0073, 'lx','by', 'rx','by', {"x0":"lx", "x1":"rx", "xw":"rx"}),
("dynamicz",     "z",                      0x007a, 'lx','by', 'rx','by', {"x0":"lx", "x1":"rx", "xw":"rx"}),
("blank",        "space",                  0x0020, 'lx','by', 'rx','by', {"x0":"lx", "x1":"rx", "y0":"by", "y1":"ty", "xw":"rx"}),
("fermata",      "scripts.ufermata",       0, 0.5,0, 1,0),
("fermata0",     "scripts.ushortfermata",  0, 0.5,0, 1,0),
("fermata2",     "scripts.ulongfermata",   0, 0.5,0, 1,0),
("fermata3",     "scripts.uverylongfermata", 0, 0.5,0, 1,0),
("fermataup",    "scripts.dfermata",       0, 0.5,1, 1,1),
("fermata0up",   "scripts.dshortfermata",  0, 0.5,1, 1,1),
("fermata2up",   "scripts.dlongfermata",   0, 0.5,1, 1,1),
("fermata3up",   "scripts.dverylongfermata", 0, 0.5,1, 1,1),
("semiflat",     "accidentals.M1",         0, 0,'hy', 1,'hy'),
("semiflat",     "accidentals.mirroredflat", 0, 0,'hy', 1,'hy'),
("semiflatslash", "accidentals.mirroredflat.backslash", 0, 0,'hy', 1,'hy'),
("flat",         "accidentals.M2",         0, 'ox','hy', 1,'hy'),
("flat",         "accidentals.flat",       0, 'ox','hy', 1,'hy'),
("flatup",       "accidentals.flat.arrowup", 0, 'ox','hy', 1,'hy'),
("flatdn",       "accidentals.flat.arrowdown", 0, 'ox','hy', 1,'hy'),
("flatupdn",     "accidentals.flat.arrowboth", 0, 'ox','hy', 1,'hy'),
("flatslash",    "accidentals.flat.slash", 0, 'ox','hy', 1,'hy'),
("flatslash2",   "accidentals.flat.slashslash", 0, 'ox','hy', 1,'hy'),
("sesquiflat",   "accidentals.M3",         0, 0,'hy', 1,'hy'),
("sesquiflat",   "accidentals.mirroredflat.flat", 0, 0,'hy', 1,'hy'),
("doubleflat",   "accidentals.M4",         0, 'ox','hy', 1,'hy'),
("doubleflat",   "accidentals.flatflat",   0, 'ox','hy', 1,'hy'),
("doubleflatslash",   "accidentals.flatflat.slash", 0, 'ox','hy', 1,'hy'),
("harmart",      "noteheads.s0harmonic",   0, 0,0.5, 1,'ay'),
("harmartfilled", "noteheads.s2harmonic",  0, 0,0.5, 1,'ay'),
("harmnat",      "scripts.flageolet",      0, 0.5,0.5, 1,0.5),
("flagopen",     "scripts.open",           0, 0.5,'cy', 1,'cy'),
("flagthumb",    "scripts.thumb",          0, 0.5,'cy', 1,'cy'),
("headcrotchet", "noteheads.s2",           0, 0,0.5, 1,'ay'),
("headminim",    "noteheads.s1",           0, 0,0.5, 1,'ay'),
("legato",       "scripts.tenuto",         0, 0.5,0.5, 1,0.5),
("portatoup",    "scripts.uportato",       0, 0.5,'ly', 1,'ly'),
("portatodn",    "scripts.dportato",       0, 0.5,'ly', 1,'ly'),
("mordentlower", "scripts.mordent",        0, 0.5,'cy', 1,'cy'),
("mordentupper", "scripts.prall",          0, 0.5,'cy', 1,'cy'),
("mordentupperlong", "scripts.prallprall", 0, 0.5,'cy', 1,'cy'),
("mordentupperlower", "scripts.prallmordent", 0, 0.5,'cy', 1,'cy'),
("upmordentupperlong", "scripts.upprall",  0, 0.5,'cy', 1,'cy'),
("upmordentupperlower", "scripts.upmordent", 0, 0.5,'cy', 1,'cy'),
("mordentupperlongdown", "scripts.pralldown", 0, 0.5,'cy', 1,'cy'),
("downmordentupperlong", "scripts.downprall", 0, 0.5,'cy', 1,'cy'),
("downmordentupperlower", "scripts.downmordent", 0, 0.5,'cy', 1,'cy'),
("mordentupperlongup", "scripts.prallup",  0, 0.5,'cy', 1,'cy'),
("straightmordentupperlong", "scripts.lineprall", 0, 0.5,'cy', 1,'cy'),
("natural",      "accidentals.0",          0, 0,'cy', 1,'cy'),
("natural",      "accidentals.natural",    0, 0,'cy', 1,'cy'),
("naturalup",    "accidentals.natural.arrowup", 0, 0,'cy', 1,'cy'),
("naturaldn",    "accidentals.natural.arrowdown", 0, 0,'cy', 1,'cy'),
("naturalupdn",  "accidentals.natural.arrowboth", 0, 0,'cy', 1,'cy'),
("peddot",       "pedal..",                0, 0,'by', 1,'by'),
("pedP",         "pedal.P",                0, 0,'by', 1,'by'),
("pedd",         "pedal.d",                0, 0,'by', 1,'by'),
("pede",         "pedal.e",                0, 0,'by', 1,'by'),
("pedPed",       "pedal.Ped",              0, 0,'by', 1,'by'),
("pedstar",      "pedal.*",                0, 0,'by', 1,'by'),
("peddash",      "pedal.M",                0, 0,'by', 1,'by'),
("restdbllonga", "rests.M3",               0, 0,0.5, 1,0.5),
("restlonga",    "rests.M2",               0, 0,0.5, 1,0.5),
("restbreve",    "rests.M1",               0, 0,0, 1,0),
("restcrotchet", "rests.2",                0, 0,0.5, 1,0.5),
("restcrotchetx", "rests.2classical",      0, 0,0.5, 1,0.5),
("restdemi",     "rests.5",                0, 0,'cy', 1,'cy'),
("resthemi",     "rests.6",                0, 0,'cy', 1,'cy'),
("restquasi",    "rests.7",                0, 0,'cy', 1,'cy'),
("restminim",    "rests.1",                0, 0,0, 1,0),
("restminimo",   "rests.1o",               0, 0,'oy', 1,'oy'),
("restquaver",   "rests.3",                0, 0,'cy', 1,'cy'),
("restsemi",     "rests.4",                0, 0,'cy', 1,'cy'),
("restminim",    "rests.0",                0, 0,1, 1,1), # reuse restminim as semibreve rest
("restsemibreveo", "rests.0o",             0, 0,'oy', 1,'oy'),
("segno",        "scripts.segno",          0, 0.5,0.5, 1,0.5),
("semibreve",    "noteheads.s0",           0, 0,0.5, 1,0.5),
("sforzando",    "scripts.umarcato",       0, 0.5,0, 1,0),
("sforzandodn",  "scripts.dmarcato",       0, 0.5,1, 1,1),
("semisharp",    "accidentals.1",          0, 0,0.5, 1,0.5),
("semisharp",    "accidentals.sharp.slashslash.stem", 0, 0,0.5, 1,0.5),
("semisharp3",   "accidentals.sharp.slashslashslash.stem", 0, 0,0.5, 1,0.5),
("sharp",        "accidentals.2",          0, 0,'cy', 1,'cy'),
("sharp",        "accidentals.sharp",      0, 0,'cy', 1,'cy'),
("sharp3",       "accidentals.sharp.slashslashslash.stemstem", 0, 0,'cy', 1,'cy'),
("sharpup",      "accidentals.sharp.arrowup", 0, 0,'cy', 1,'cy'),
("sharpdn",      "accidentals.sharp.arrowdown", 0, 0,'cy', 1,'cy'),
("sharpupdn",    "accidentals.sharp.arrowboth", 0, 0,'cy', 1,'cy'),
("sesquisharp",  "accidentals.3",          0, 0,0.5, 1,0.5),
("sesquisharp",  "accidentals.sharp.slashslash.stemstemstem", 0, 0,0.5, 1,0.5),
("doublesharp",  "accidentals.4",          0, 0,0.5, 1,0.5),
("doublesharp",  "accidentals.doublesharp", 0, 0,0.5, 1,0.5),
("staccatissup", "scripts.dstaccatissimo", 0, 0.5,1, 1,1),
("staccatissdn", "scripts.ustaccatissimo", 0, 0.5,0, 1,0),
("staccato",     "scripts.staccato",       0, 0.5,0.5, 1,0.5),
("staccato",     "dots.dot",               0, 0,0.5, 1,0.5),
("snappizz",     "scripts.snappizzicato",  0, 0.5,0.5, 1,0.5),
("stopping",     "scripts.stopped",        0, 0.5,0.5, 1,0.5),
("tailquaverdn", "flags.d3",               0, 'ox','oy', 1,'oy'),
("tailquaverup", "flags.u3",               0, 'ox','oy', 1,'oy'),
("tailsemidn",   "flags.d4",               0, 'ox','oy', 1,'oy'),
("tailsemiup",   "flags.u4",               0, 'ox','oy', 1,'oy'),
("taildemidn",   "flags.d5",               0, 'ox','oy', 1,'oy'),
("taildemiup",   "flags.u5",               0, 'ox','oy', 1,'oy'),
("tailhemidn",   "flags.d6",               0, 'ox','oy', 1,'oy'),
("tailhemiup",   "flags.u6",               0, 'ox','oy', 1,'oy'),
("tailquasidn",  "flags.d7",               0, 'ox','oy', 1,'oy'),
("tailquasiup",  "flags.u7",               0, 'ox','oy', 1,'oy'),
("timeCbar",     "timesig.C22",            0, 0,0.5, 1,0.5),
("timeC",        "timesig.C44",            0, 0,0.5, 1,0.5),
("trill",        "scripts.trill",          0, 0.5,0, 1,0),
("turn",         "scripts.turn",           0, 0.5,0.5, 1,0.5),
("invturn",      "scripts.reverseturn",    0, 0.5,0.5, 1,0.5),
("openarrowup",  "arrowheads.open.11",     0, 'cx','cy', 1,0.5),
("openarrowdown", "arrowheads.open.1M1",   0, 'cx','cy', 1,0.5),
("openarrowleft", "arrowheads.open.0M1",   0, 'cx','cy', 1,'cy'),
("openarrowright", "arrowheads.open.01",   0, 'cx','cy', 1,'cy'),
("closearrowup",  "arrowheads.close.11",   0, 'cx','cy', 1,0.5),
("closearrowdown", "arrowheads.close.1M1", 0, 'cx','cy', 1,0.5),
("closearrowleft", "arrowheads.close.0M1", 0, 'cx','cy', 1,'cy'),
("closearrowright", "arrowheads.close.01", 0, 'cx','cy', 1,'cy'),
("upedalheel",   "scripts.upedalheel",     0, 0.5,'cy', 1,'cy'),
("dpedalheel",   "scripts.dpedalheel",     0, 0.5,'cy', 1,'cy'),
("upedaltoe",    "scripts.upedaltoe",      0, 0.5,0, 1,0),
("dpedaltoe",    "scripts.dpedaltoe",      0, 0.5,1, 1,1),
("acc2",         "accordion.accFreebase",  0, 0.5,0, 1,0),
("acc3",         "accordion.accDiscant",   0, 0.5,0, 1,0),
("acc4",         "accordion.accStdbase",   0, 0.5,0, 1,0),
("accr",         "accordion.accBayanbase", 0, 0.5,0, 1,0),
("accdot",       "accordion.accDot",       0, 0.5,0.5, 1,0.5),
("accstar",      "accordion.accOldEE",     0, 0.5,0, 1,0),
("diamondsemi",  "noteheads.s0diamond",    0, 0,0.5, 1,0.5),
("diamondminim", "noteheads.s1diamond",    0, 0,0.5, 1,0.5),
("diamondcrotchet", "noteheads.s2diamond", 0, 0,0.5, 1,0.5),
("trianglesemi", "noteheads.s0triangle",   0, 0,0.5, 1,0.5),
("triangleminim", "noteheads.d1triangle",  0, 0,0.5, 1,'iy'),
("triangleminim", "noteheads.u1triangle",  0, 0,0.5, 1,'ay'),
("trianglecrotchet", "noteheads.d2triangle", 0, 0,0.5, 1,'iy'),
("trianglecrotchet", "noteheads.u2triangle", 0, 0,0.5, 1,'ay'),
("crosssemi",    "noteheads.s0cross",      0, 0,0.5, 1,0.5),
("crossminim",   "noteheads.s1cross",      0, 0,0.5, 1,'ay'),
("crosscrotchet", "noteheads.s2cross",     0, 0,0.5, 1,'ay'),
("crosscircle",  "noteheads.s2xcircle",    0, 0,0.5, 1,0.5),
("slashsemi",    "noteheads.s0slash",      0, 0,0.5, 1,0.5),
("slashminim",   "noteheads.s1slash",      0, 0,0.5, 1,'ay'),
("slashcrotchet", "noteheads.s2slash",     0, 0,0.5, 1,'ay'),
]

def writesfd(filepfx, fontname, encodingname, encodingsize, outlines, glyphlist):
    fname = filepfx + ".sfd"
    f = open(fname, "w")
    f.write("SplineFontDB: 3.0\n")
    f.write("FontName: %s\n" % fontname)
    f.write("FullName: %s\n" % fontname)
    f.write("FamilyName: %s\n" % fontname)
    f.write("Copyright: No copyright is claimed on this font file.\n")
    f.write("Version: %s\n" % verstring)
    f.write("ItalicAngle: 0\n")
    f.write("UnderlinePosition: -100\n")
    f.write("UnderlineWidth: 50\n")
    f.write("Ascent: 800\n")
    f.write("Descent: 200\n")
    f.write("LayerCount: 2\n")
    f.write("Layer: 0 0 \"Back\" 1\n")
    f.write("Layer: 1 0 \"Fore\" 0\n")
    f.write("UseXUID: 0\n")
    f.write("OS2Version: 0\n")
    f.write("OS2_WeightWidthSlopeOnly: 0\n")
    f.write("OS2_UseTypoMetrics: 1\n")
    f.write("CreationTime: 1252826347\n") # when I first wrote this prologue-writing code
    f.write("ModificationTime: %d\n" % time.time())
    f.write("OS2TypoAscent: 0\n")
    f.write("OS2TypoAOffset: 1\n")
    f.write("OS2TypoDescent: 0\n")
    f.write("OS2TypoDOffset: 1\n")
    f.write("OS2TypoLinegap: 0\n")
    f.write("OS2WinAscent: 0\n")
    f.write("OS2WinAOffset: 1\n")
    f.write("OS2WinDescent: 0\n")
    f.write("OS2WinDOffset: 1\n")
    f.write("HheadAscent: 0\n")
    f.write("HheadAOffset: 1\n")
    f.write("HheadDescent: 0\n")
    f.write("HheadDOffset: 1\n")
    f.write("OS2Vendor: 'PfEd'\n")
    f.write("DEI: 0\n")
    f.write("Encoding: %s\n" % encodingname)
    f.write("UnicodeInterp: none\n")
    f.write("NameList: Adobe Glyph List\n")
    f.write("DisplaySize: -96\n")
    f.write("AntiAlias: 1\n")
    f.write("FitToEm: 1\n")
    f.write("WinInfo: 64 8 2\n")
    f.write("BeginChars: %d %d\n" % (encodingsize, len(glyphlist)))

    i = 0
    for glyph in glyphlist:
        ourname, theirname, encoding, ox, oy = glyph[:5]
        bbox, path = outlines[ourname]
        char = eval(ourname)
        xrt = lambda x: x * (3600.0 / (40*char.scale)) # potrace's factor of ten, ours of four
        yrt = lambda y: y * (3600.0 / (40*char.scale))
        xat = lambda x: xrt(x) - char.origin[0]
        yat = lambda y: yrt(y) - char.origin[1]
        xt = lambda x: xat(x) - xat(ox)
        yt = lambda y: yat(y) - yat(oy)
        if len(glyph) > 9 and glyph[9].has_key("xw"):
            width = xt(glyph[9]["xw"]) # explicitly specified width
        else:
            width = xt(bbox[2]) # mostly default to RHS of bounding box
        f.write("\nStartChar: %s\n" % theirname)
        f.write("Encoding: %d %d %d\n" % (encoding, encoding, i))
        f.write("Width: %g\n" % width)
        f.write("Flags: W\n")
        f.write("LayerCount: 2\n")
        f.write("Fore\n")
        f.write("SplineSet\n")
        for c in path:
            if c[0] == 'm':
                f.write("%g %g m 1\n" % (xt(c[1]), yt(c[2])))
            elif c[0] == 'l':
                f.write(" %g %g l 1\n" % (xt(c[3]), yt(c[4])))
            elif c[0] == 'c':
                f.write(" %g %g %g %g %g %g c 0\n" % (xt(c[3]), yt(c[4]), xt(c[5]), yt(c[6]), xt(c[7]), yt(c[8])))
            # closepath is not given explicitly
        f.write("EndSplineSet\n")
        f.write("EndChar\n")
        i = i + 1

    f.write("\nEndChars\n")

    f.write("EndSplineFont\n")
    f.close()

args = sys.argv[1:]
if len(args) >= 1 and args[0][:6] == "--ver=":
    verstring = args[0][6:]
    args = args[1:]
if len(args) == 2 and args[0] == "-test":
    # example usage:
    # ./glyphs.py -test braceupper | gs -sDEVICE=pngmono -sOutputFile=out.png -r72 -g1000x1000 -dBATCH -dNOPAUSE -q -
    # and then to view that in gui for correction:
    # convert -recolor '.25 0 0 0 0 .25 0 0 0 0 .25 0 .75 .75 .75 1' out.png zout.gif && ./gui.py zout.gif
    glyph = eval(args[1])
    glyph.testdraw()
elif len(args) == 2 and (args[0] == "-testps" or args[0] == "-testpsunscaled"):
    char = eval(args[1])
    bbox, path = get_ps_path(char)
    if args[0] == "-testps":
        xrt = lambda x: x * (3600.0 / (40*char.scale)) # potrace's factor of ten, ours of four
        yrt = lambda y: y * (3600.0 / (40*char.scale))
        xat = lambda x: xrt(x) - char.origin[0]
        yat = lambda y: yrt(y) - char.origin[1]
    else:
        xat = yat = lambda x: x
    print "%% bbox: %g %g %g %g" % (xat(bbox[0]), yat(bbox[1]), xat(bbox[2]), yat(bbox[3]))
    for c in path:
        if c[0] == 'm':
            print "%g %g moveto" % (xat(c[1]), yat(c[2]))
        elif c[0] == 'l':
            print "  %g %g lineto" % (xat(c[3]), yat(c[4]))
        elif c[0] == 'c':
            print "  %g %g %g %g %g %g curveto" % (xat(c[3]), yat(c[4]), xat(c[5]), yat(c[6]), xat(c[7]), yat(c[8]))
        elif c[0] == 'cp':
            print "closepath"

elif len(args) == 1 and args[0] == "-mus":
    # Generate a Postscript prologue suitable for use with 'mus' in
    glyphlist = [
    "accent",
    "acciaccatura",
    "appoggiatura",
    "arpeggio",
    "big0",
    "big1",
    "big2",
    "big3",
    "big4",
    "big5",
    "big6",
    "big7",
    "big8",
    "big9",
    "bowdown",
    "bowup",
    "bracelower",
    "braceupper",
    "bracketlower",
    "bracketupper",
    "breath",
    "breve",
    "clefC",
    "clefF",
    "clefG",
    "coda",
    "ditto",
    "doubleflat",
    "doublesharp",
    "dynamicf",
    "dynamicm",
    "dynamicp",
    "dynamics",
    "dynamicz",
    "fermata",
    "flat",
    "harmart",
    "harmnat",
    "headcrotchet",
    "headminim",
    "legato",
    "mordentlower",
    "mordentupper",
    "natural",
    "repeatmarks",
    "restbreve",
    "restcrotchet",
    "restdemi",
    "resthemi",
    "restminim",
    "restquaver",
    "restsemi",
    "segno",
    "semibreve",
    "sforzando",
    "sharp",
    "small0",
    "small1",
    "small2",
    "small3",
    "small4",
    "small5",
    "small6",
    "small7",
    "small8",
    "small9",
    "smallflat",
    "smallnatural",
    "smallsharp",
    "staccatissdn",
    "staccatissup",
    "staccato",
    "stopping",
    "taildemidn",
    "taildemiup",
    "tailhemidn",
    "tailhemiup",
    "tailquaverdn",
    "tailquaverup",
    "tailsemidn",
    "tailsemiup",
    "timeCbar",
    "timeC",
    "trill",
    "turn",
    ]
    encoding = [(i+33, glyphlist[i]) for i in range(len(glyphlist))]
    # the parent directory.
    f = open("prologue.ps", "w")
    g = open("abspaths.txt", "w")
    f.write("save /m /rmoveto load def /l /rlineto load def\n")
    f.write("/hm {0 m} def /vm {0 exch m} def /hl {0 l} def /vl {0 exch l} def\n")
    f.write("/mm /moveto load def\n")
    f.write("/c {4 -1 roll 5 index add 4 -1 roll 4 index add 4 2 roll\n")
    f.write("    exch 3 index add exch 2 index add rcurveto} def\n")
    f.write("/vhc {0 5 1 roll 0 c} def /hvc {0 4 1 roll 0 exch c} def\n")
    f.write("/f /fill load def\n")
    f.write("/cp {currentpoint closepath moveto} def\n")
    f.write("/ip {0.02 dup scale 2 setlinecap 0 setlinejoin 0 setgray} def\n")
    f.write("/beam {newpath 50 sub moveto\n")
    f.write("  0 100 rlineto 50 add lineto 0 -100 rlineto closepath fill} def\n")
    f.write("/line {newpath moveto lineto setlinewidth stroke} def\n")
    f.write("/tdict 5 dict def\n")
    f.write("/tie {tdict begin\n")
    f.write("  /x2 exch def /yp exch def /x1 exch def /y exch def newpath\n")
    f.write("  x1 yp moveto\n")
    f.write("  x1 y abs add yp y add\n")
    f.write("  x2 y abs sub yp y add\n")
    f.write("  x2 yp curveto\n")
    f.write("  30 setlinewidth stroke\n")
    f.write("end} def\n")
    f.write("10 dict dup begin\n")
    f.write("/FontType 3 def /FontMatrix [1 0 0 1 0 0] def\n")
    f.write("/Encoding 256 array def 0 1 255 {Encoding exch /.notdef put} for\n")
    for code, name in encoding:
        f.write("Encoding %d /.%s put\n" % (code, name))
    f.write("/BBox %d dict def\n" % len(encoding))
    f.write("/CharacterDefs %d dict def\n" % len(encoding))
    fontbbox = (None,)*4
    for code, name in encoding:
        char = eval(name)
        xrt = lambda x: x * (3600.0 / (40*char.scale)) # potrace's factor of ten, ours of four
        yrt = lambda y: y * (3600.0 / (40*char.scale))
        xat = lambda x: round(xrt(x) - char.origin[0])
        yat = lambda y: round(yrt(y) - char.origin[1])
        bbox, path = get_ps_path(char)
        f.write("CharacterDefs /.%s {\n" % name)
        g.write("# %s\n" % name)
        output = "newpath"
        currentpoint = (None, None)
        for c in path:
            if c[0] == 'm':
                x1, y1 = xat(c[1]), yat(c[2])
                x0, y0 = currentpoint
                if x0 == None:
                    output = output + " %g %g mm" % (x1,y1)
                elif x0 == x1:
                    output = output + " %g vm" % (y1-y0)
                elif y0 == y1:
                    output = output + " %g hm" % (x1-x0)
                else:
                    output = output + " %g %g m" % (x1-x0, y1-y0)
                g.write("  %g %g moveto\n" % (x1,y1))
                currentpoint = x1,y1
            elif c[0] == 'l':
                x0, y0 = xat(c[1]), yat(c[2])
                x1, y1 = xat(c[3]), yat(c[4])
                if x0 == x1:
                    output = output + " %g vl" % (y1-y0)
                elif y0 == y1:
                    output = output + " %g hl" % (x1-x0)
                else:
                    output = output + " %g %g l" % (x1-x0, y1-y0)
                g.write("  %g %g lineto\n" % (x1,y1))
                currentpoint = x1,y1
            elif c[0] == 'c':
                x0, y0 = xat(c[1]), yat(c[2])
                x1, y1 = xat(c[3]), yat(c[4])
                x2, y2 = xat(c[5]), yat(c[6])
                x3, y3 = xat(c[7]), yat(c[8])
                if x0 == x1 and y2 == y3:
                    output = output + " %g %g %g %g vhc" % (y1-y0, x2-x1, y2-y1, x3-x2)
                elif y0 == y1 and x2 == x3:
                    output = output + " %g %g %g %g hvc" % (x1-x0, x2-x1, y2-y1, y3-y2)
                else:
                    output = output + " %g %g %g %g %g %g c" % (x1-x0, y1-y0, x2-x1, y2-y1, x3-x2, y3-y2)
                g.write("  %g %g %g %g %g %g curveto\n" % (x1,y1,x2,y2,x3,y3))
                currentpoint = x3,y3
            elif c[0] == 'cp':
                output = output + " cp"
                g.write("  closepath\n")
                currentpoint = None, None
        f.write("  " + output + " f\n")
        x0, y0 = xat(bbox[0]), yat(bbox[1])
        x1, y1 = xat(bbox[2]), yat(bbox[3])
        f.write("} put BBox /.%s [%g %g %g %g] put\n" % ((name, x0, y0, x1, y1)))
        g.write("  # bbox: %g %g %g %g\n" % (x0, y0, x1, y1))
        g.write("  # w,h: %g %g\n" % (x1-x0, y1-y0))
        fontbbox = update_bbox(fontbbox, x0,y0)
        fontbbox = update_bbox(fontbbox, x1,y1)
    x0,y0,x1,y1 = fontbbox
    f.write("/FontBBox [%g %g %g %g] def\n" % (x0, y0, x1, y1))
    f.write("/BuildChar {0 begin /char exch def /fontdict exch def\n")
    f.write("  /charname fontdict /Encoding get char get def\n")
    f.write("  0 0 fontdict /BBox get charname get aload pop setcachedevice\n")
    f.write("  fontdict /CharacterDefs get charname get exec\n")
    f.write("end} def\n")
    f.write("/BuildChar load 0 3 dict put\n")
    f.write("/UniqueID 1 def\n")
    f.write("end /MusicGfx exch definefont /MGfx exch def\n")
    f.write("/ss 1 string def\n")
    for code, name in encoding:
        f.write("/.%s {moveto MGfx setfont ss 0 %d put ss show} def\n" % (name, code))
    f.write("/.tdot {gsave\n")
    f.write("  currentpoint translate 0.5 dup scale\n")
    f.write("  51 150 .staccato\n")
    f.write("  grestore 67 hm} def\n")
    f.write("/.tbreve {gsave\n")
    f.write("  currentpoint translate 0.5 dup scale\n")
    f.write("  333 150 .breve\n")
    f.write("  grestore 351 hm} def\n")
    f.write("/.tsemibreve {gsave\n")
    f.write("  currentpoint translate 0.5 dup scale\n")
    f.write("  207 150 .semibreve\n")
    f.write("  grestore 247 hm} def\n")
    f.write("/.tminim {gsave\n")
    f.write("  currentpoint translate 0.5 dup scale\n")
    f.write("  160 150 .headminim\n")
    f.write("  24 setlinewidth newpath 304 186 moveto 850 vl stroke\n")
    f.write("  grestore 178 hm} def\n")
    f.write("/.tcrotchet {gsave\n")
    f.write("  currentpoint translate 0.5 dup scale\n")
    f.write("  160 150 .headcrotchet\n")
    f.write("  24 setlinewidth newpath 304 186 moveto 850 vl stroke\n")
    f.write("  grestore 178 hm} def\n")
    f.write("/.tquaver {gsave\n")
    f.write("  currentpoint translate 0.5 dup scale\n")
    f.write("  160 150 .headcrotchet\n")
    f.write("  24 setlinewidth newpath 304 186 moveto 850 vl stroke\n")
    f.write("  304 1050 .tailquaverup\n")
    f.write("  grestore 293 hm} def\n")
    f.write("/.tsemiquaver {gsave\n")
    f.write("  currentpoint translate 0.5 dup scale\n")
    f.write("  160 150 .headcrotchet\n")
    f.write("  24 setlinewidth newpath 304 186 moveto 850 vl stroke\n")
    f.write("  304 1050 .tailquaverup\n")
    f.write("  304 900 .tailquaverup\n")
    f.write("  grestore 293 hm} def\n")
    f.write("/.tdemisemiquaver {gsave\n")
    f.write("  currentpoint translate 0.5 dup scale\n")
    f.write("  160 150 .headcrotchet\n")
    f.write("  24 setlinewidth newpath 304 186 moveto 850 vl stroke\n")
    f.write("  304 1050 .tailquaverup\n")
    f.write("  304 900 .tailquaverup\n")
    f.write("  304 750 .tailquaverup\n")
    f.write("  grestore 293 hm} def\n")
    f.write("/.themidemisemiquaver {gsave\n")
    f.write("  currentpoint translate 0.5 dup scale\n")
    f.write("  160 150 .headcrotchet\n")
    f.write("  24 setlinewidth newpath 304 186 moveto 850 vl stroke\n")
    f.write("  304 1050 .tailquaverup\n")
    f.write("  304 900 .tailquaverup\n")
    f.write("  304 750 .tailquaverup\n")
    f.write("  304 600 .tailquaverup\n")
    f.write("  grestore 293 hm} def\n")
    f.write("/.df {\n")
    f.write("  currentfont currentpoint currentpoint .dynamicf moveto 216 hm setfont\n")
    f.write("} def\n")
    f.write("/.dm {\n")
    f.write("  currentfont currentpoint currentpoint .dynamicm moveto 460 hm setfont\n")
    f.write("} def\n")
    f.write("/.dp {\n")
    f.write("  currentfont currentpoint currentpoint .dynamicp moveto 365 hm setfont\n")
    f.write("} def\n")
    f.write("/.ds {\n")
    f.write("  currentfont currentpoint currentpoint .dynamics moveto 225 hm setfont\n")
    f.write("} def\n")
    f.write("/.dz {\n")
    f.write("  currentfont currentpoint currentpoint .dynamicz moveto 299 hm setfont\n")
    f.write("} def\n")
    f.close()
    g.close()

    # Now generate prologue.c.
    f = open("prologue.ps", "r")
    g = open("../prologue.c", "w")
    g.write("/* This file is automatically generated from the Mus glyph\n")
    g.write(" * descriptions. Do not expect changes made directly to this\n")
    g.write(" * file to be permanent. */\n")
    g.write("\n")
    g.write("#include <stdio.h>\n")
    g.write("\n")
    g.write("static char *prologue[] = {\n")
    wrapbuf = ""
    while 1:
        s = f.readline()
        if s == "": break
        ws = s.split()
        for w in ws:
            if len(wrapbuf) + 1 + len(w) <= 69:
                wrapbuf = wrapbuf + " " + w
            else:
                g.write("    \"%s\\n\",\n" % wrapbuf)
                wrapbuf = w
    g.write("    \"%s\\n\",\n" % wrapbuf)
    g.write("    NULL\n")
    g.write("};\n")
    g.write("\n")
    g.write("void write_prologue(FILE *fp) {\n")
    g.write("    char **p;\n")
    g.write("\n")
    g.write("    for (p=prologue; *p; p++)\n")
    g.write("        fputs(*p, fp);\n")
    g.write("}\n")
elif len(args) == 1 and args[0][:5] == "-lily":
    # Generate .sfd files and supporting metadata which we then
    # process with FontForge into a replacement system font set for
    # GNU LilyPond.
    def writetables(filepfx, size, subids, subnames, outlines, glyphlist, bracesonly=0):
        fname = filepfx + ".LILF"
        f = open(fname, "w")
        f.write(" ".join(subnames))
        f.close()
        fname = filepfx + ".LILY"
        f = open(fname, "w")
        if not bracesonly:
            f.write("(staffsize . %.6f)\n" % size)
            f.write("(stafflinethickness . %.6f)\n" % (size/40.))
            f.write("(staff_space . %.6f)\n" % (size/4.))
            f.write("(linethickness . %.6f)\n" % (size/40.))
            bbbox = outlines["headcrotchet"][0]
            bwidth = bbbox[2] - bbbox[0]
            f.write("(black_notehead_width . %.6f)\n" % (bwidth * 3600.0 / (40*headcrotchet.scale) * (size/1000.)))
            f.write("(ledgerlinethickness . %.6f)\n" % (size/40.))
        f.write("(design_size . %.6f)\n" % size)
        if not bracesonly:
            f.write("(blot_diameter . 0.4)\n")
        f.close()
        fname = filepfx + ".LILC"
        f = open(fname, "w")
        for glyph in glyphlist:
            ourname, theirname, encoding, ox, oy, ax, ay, subid, subcode = glyph[:9]
            char = eval(ourname)
            bbox, path = outlines[ourname]
            xrt = lambda x: x * (3600.0 / (40*char.scale)) # potrace's factor of ten, ours of four
            yrt = lambda y: y * (3600.0 / (40*char.scale))
            xat = lambda x: xrt(x) - char.origin[0]
            yat = lambda y: yrt(y) - char.origin[1]
            xt = lambda x: (xat(x) - xat(ox)) * (size/1000.)
            yt = lambda y: (yat(y) - yat(oy)) * (size/1000.)
            f.write("(%s .\n" % theirname)
            f.write("((bbox . (%.6f %.6f %.6f %.6f))\n" % (xt(bbox[0]), yt(bbox[1]), xt(bbox[2]), yt(bbox[3])))
            f.write("(subfont . \"%s\")\n" % subnames[subid])
            f.write("(subfont-index . %d)\n" % subcode)
            f.write("(attachment . (%.6f . %.6f))))\n" % (xt(ax), yt(ay)))
        f.close()

    if args[0] != "-lilybrace":
        # Allocate sequential Unicode code points in the private use
        # area for all the glyphs that don't already have a specific
        # ASCII code point where they need to live.
        code = 0xe100
        for i in range(len(lilyglyphlist)):
            g = lilyglyphlist[i]
            if g[2] == 0:
                lilyglyphlist[i] = g[:2] + (code,) + g[3:]
                code = code + 1

        # Construct the PS outlines via potrace, once for each glyph
        # we're actually using.
        outlines = {}
        for g in lilyglyphlist:
            gid = g[0]
            char = eval(gid)
            if not outlines.has_key(gid):
                outlines[gid] = get_ps_path(char)

        # PAINFUL HACK! Add invisible droppings above and below the
        # digits. This is because LP draws time signatures by
        # mushing the digits up against the centre line of the
        # stave, in the assumption that they'll be big enough to
        # overlap the top and bottom lines too. Personally I like
        # time signatures to _not quite_ collide with the stave
        # lines (except the 2nd and 4th, of course, which they can't
        # avoid), and that means I need LP to consider the digits'
        # bounding boxes to be just a bit wider.
        #
        # The pathlets appended here are of zero thickness, so they
        # shouldn't ever actually show up.
        digits = ["big%d" % i for i in range(10)]
        ymid = (outlines["big4"][0][1] + outlines["big4"][0][3]) / 2.0
        for d in digits:
            char = eval(d)
            d250 = 250.0 * (40*char.scale) / 3600.0
            u250 = 236.0 * (40*char.scale) / 3600.0 # empirically chosen
            one = 1.0 * (40*char.scale) / 3600.0
            yone = 0 # set to one to make the droppings visible for debugging
            bbox, path = outlines[d]
            xmid = (bbox[0] + bbox[2]) / 2.0
            path.append(('m', xmid, ymid-d250+yone))
            path.append(('l', xmid, ymid-d250+yone, xmid-one, ymid-d250))
            path.append(('l', xmid-one, ymid-d250, xmid+one, ymid-d250))
            path.append(('l', xmid+one, ymid-d250, xmid, ymid-d250+yone))
            path.append(('m', xmid, ymid+u250-yone))
            path.append(('l', xmid, ymid+u250-yone, xmid-one, ymid+u250))
            path.append(('l', xmid-one, ymid+u250, xmid+one, ymid+u250))
            path.append(('l', xmid+one, ymid+u250, xmid, ymid+u250-yone))
            bbox = (bbox[0], min(bbox[1], ymid-d250), \
                    bbox[2], max(bbox[3], ymid+u250))
            outlines[d] = bbox, path

        # Go through the main glyph list and transform the
        # origin/attachment/width specifications into coordinates in
        # the potrace coordinate system.
        for i in range(len(lilyglyphlist)):
            g = list(lilyglyphlist[i])
            gid = g[0]
            if len(g) > 7:
                dict = g[7]
                for k, v in dict.items():
                    if k[0] == "x":
                        v = eval(gid+"."+v) * 40
                    elif k[0] == "y":
                        v = (1000 - eval(gid+"."+v)) * 40
                    else:
                        raise "Error!"
                    dict[k] = v
            else:
                dict = {}
            x0, y0, x1, y1 = outlines[gid][0]
            # Allow manual overriding of the glyph's logical
            # bounding box as written into the LILC table (used to
            # make arpeggio and trill elements line up right, and
            # also - for some reason - used for dynamics glyph
            # kerning in place of the perfectly good system in the
            # font format proper). If this happens, the attachment
            # points are given in terms of the overridden bounding
            # box.
            x0 = dict.get("x0", x0)
            x1 = dict.get("x1", x1)
            y0 = dict.get("y0", y0)
            y1 = dict.get("y1", y1)
            outlines[gid] = ((x0,y0,x1,y1),outlines[gid][1])
            xo = g[3]
            if type(xo) == types.StringType:
                xo = eval(gid+"."+xo) * 40
            else:
                xo = x0 + (x1-x0) * xo
            g[3] = xo
            yo = g[4]
            if type(yo) == types.StringType:
                yo = (1000 - eval(gid+"."+yo)) * 40
            else:
                yo = y0 + (y1-y0) * yo
            g[4] = yo
            xa = g[5]
            if type(xa) == types.StringType:
                xa = eval(gid+"."+xa) * 40
            else:
                xa = x0 + (x1-x0) * xa
            g[5] = xa
            ya = g[6]
            if type(ya) == types.StringType:
                ya = (1000 - eval(gid+"."+ya)) * 40
            else:
                ya = y0 + (y1-y0) * ya
            g[6] = ya
            lilyglyphlist[i] = tuple(g)

        # Split up the glyph list into appropriately sized chunks
        # for the custom-encoded .pfas.
        subid = 0
        subcode = 256
        subglyphlists = [[]]
        for i in range(len(lilyglyphlist)):
            if lilyglyphlist[i][2] < 256:
                thissubid = 0
                thissubcode = lilyglyphlist[i][2]
            else:
                if subcode >= 256:
                    subid = subid + 1
                    subcode = 33
                    subglyphlists.append([])
                thissubid = subid
                thissubcode = subcode
                subcode = subcode + 1
            subglyphlists[thissubid].append(lilyglyphlist[i][:2] + (thissubcode,) + lilyglyphlist[i][3:])
            lilyglyphlist[i] = lilyglyphlist[i][:7] + (thissubid, thissubcode) + lilyglyphlist[i][7:]
        subids = subid + 1

        sizes = 11, 13, 14, 16, 18, 20, 23, 26
        for size in sizes:
            writesfd("gonville-%d" % size, "Gonville-%d" % size, "UnicodeBmp", 65537, outlines, lilyglyphlist)
            subnames = ["gonvillealpha%d" % size] + ["gonvillepart%d" % subid for subid in range(1,subids)]
            writetables("gonville-%d" % size, size, subids, subnames, outlines, lilyglyphlist)
            writesfd("gonvillealpha%d" % size, subnames[0], "Custom", 256, outlines, subglyphlists[0])
        for subid in range(1,subids):
            writesfd("gonvillepart%d" % subid, "Gonville-Part%d" % subid, "Custom", 256, outlines, subglyphlists[subid])

        for dir in "lilyfonts", "lilyfonts/type1", "lilyfonts/otf", "lilyfonts/svg":
            try:
                os.mkdir(dir)
            except OSError, e:
                pass # probably already existed, which we don't mind

        for size in sizes:
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "LoadTableFromFile(\"LILC\", \"gonville-%d.LILC\"); " + \
            "LoadTableFromFile(\"LILF\", \"gonville-%d.LILF\"); " + \
            "LoadTableFromFile(\"LILY\", \"gonville-%d.LILY\"); " + \
            "Generate($2)' gonville-%d.sfd lilyfonts/otf/gonville-%d.otf") % ((size,)*5))
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "LoadTableFromFile(\"LILC\", \"gonville-%d.LILC\"); " + \
            "LoadTableFromFile(\"LILF\", \"gonville-%d.LILF\"); " + \
            "LoadTableFromFile(\"LILY\", \"gonville-%d.LILY\"); " + \
            "SetFontNames(\"Emmentaler-%d\",\"Emmentaler-%d\",\"Emmentaler-%d\"); " + \
            "Generate($2)' gonville-%d.sfd lilyfonts/otf/emmentaler-%d.otf") % ((size,)*8))
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "SetFontNames(\"Emmentaler-%d\",\"Emmentaler-%d\",\"Emmentaler-%d\"); " + \
            "Generate($2)' gonville-%d.sfd lilyfonts/svg/emmentaler-%d.svg") % ((size,)*5))
        for size in sizes:
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "SetFontNames(\"feta-alphabet%d\",\"feta-alphabet%d\",\"feta-alphabet%d\"); " + \
            "Generate($2)' gonvillealpha%d.sfd lilyfonts/type1/gonvillealpha%d.pfa") % ((size,)*5))
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "SetFontNames(\"feta-alphabet%d\",\"feta-alphabet%d\",\"feta-alphabet%d\"); " + \
            "Generate($2)' gonvillealpha%d.sfd lilyfonts/type1/gonvillealpha%d.pfb") % ((size,)*5))
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "SetFontNames(\"feta-alphabet%d\",\"feta-alphabet%d\",\"feta-alphabet%d\"); " + \
            "Generate($2)' gonvillealpha%d.sfd lilyfonts/svg/gonvillealpha%d.svg") % ((size,)*5))
            try:
                os.symlink("gonvillealpha%d.pfa" % size, "lilyfonts/type1/feta-alphabet%d.pfa" % size)
            except OSError, e:
                pass # probably already existed, which we don't mind
            try:
                os.symlink("gonvillealpha%d.pfb" % size, "lilyfonts/type1/feta-alphabet%d.pfb" % size)
            except OSError, e:
                pass # probably already existed, which we don't mind
            try:
                os.symlink("gonvillealpha%d.svg" % size, "lilyfonts/svg/feta-alphabet%d.svg" % size)
            except OSError, e:
                pass # probably already existed, which we don't mind
        for subid in range(1,subids):
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "Generate($2)' gonvillepart%d.sfd lilyfonts/type1/gonvillepart%d.pfa") % ((subid,)*2))
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "Generate($2)' gonvillepart%d.sfd lilyfonts/svg/gonvillepart%d.svg") % ((subid,)*2))

    # Now do most of that all over again for the specialist brace
    # font, if we're doing that. (The "-lilymain" option doesn't
    # regenerate the braces, because they're large and slow and it's
    # nice to be able to debug just the interesting bits.) Construct
    # the PS outlines via potrace, once for each glyph we're
    # actually using.
    if args[0] != "-lilymain":
        outlines = {}
        bracelist = []
        for i in range(576):
            char = scaledbrace(525 * (151./150)**i)
            gid = "brace%d" % i
            exec "%s = char" % gid
            outlines[gid] = get_ps_path(char)
            x0, y0, x1, y1 = outlines[gid][0]
            yh = (y0+y1)/2.0
            bracelist.append((gid, gid, 0xe100+i, x1, yh, x1, yh))

        # Split up the glyph list into appropriately sized chunks
        # for the custom-encoded .pfas.
        subid = -1
        subcode = 256
        subbracelists = [[]]
        for i in range(len(bracelist)):
            if subcode >= 256:
                subid = subid + 1
                subcode = 33
                subbracelists.append([])
            thissubid = subid
            thissubcode = subcode
            subcode = subcode + 1
            subbracelists[thissubid].append(bracelist[i][:2] + (thissubcode,) + bracelist[i][3:])
            bracelist[i] = bracelist[i] + (thissubid, thissubcode)
        subids = subid + 1

        writesfd("gonville-brace", "Gonville-Brace", "UnicodeBmp", 65537, outlines, bracelist)
        subnames = ["gonville-bracepart%d" % subid for subid in range(subids)]
        writetables("gonville-brace", 20, subids, subnames, outlines, bracelist, 1)
        for subid in range(subids):
            writesfd("gonville-bracepart%d" % subid, "Gonville-Brace-Part%d" % subid, "Custom", 256, outlines, subbracelists[subid])

        system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
        "LoadTableFromFile(\"LILC\", \"gonville-brace.LILC\"); " + \
        "LoadTableFromFile(\"LILF\", \"gonville-brace.LILF\"); " + \
        "LoadTableFromFile(\"LILY\", \"gonville-brace.LILY\"); " + \
        "Generate($2)' gonville-brace.sfd lilyfonts/otf/gonville-brace.otf"))
        system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
        "Generate($2)' gonville-brace.sfd lilyfonts/svg/gonville-brace.svg"))
        try:
            os.symlink("gonville-brace.otf", "lilyfonts/otf/aybabtu.otf")
            os.symlink("gonville-brace.svg", "lilyfonts/svg/aybabtu.svg")
            os.symlink("gonville-brace.otf", "lilyfonts/otf/emmentaler-brace.otf")
            os.symlink("gonville-brace.svg", "lilyfonts/svg/emmentaler-brace.svg")
        except OSError, e:
            pass # probably already existed, which we don't mind
        for subid in range(subids):
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "Generate($2)' gonville-bracepart%d.sfd lilyfonts/type1/gonville-bracepart%d.pfa") % ((subid,)*2))
            system(("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
            "Generate($2)' gonville-bracepart%d.sfd lilyfonts/svg/gonville-bracepart%d.svg") % ((subid,)*2))
elif len(args) == 1 and args[0] == "-simple":
    # Generate an .sfd file which can be compiled into a really
    # simple binary font in which all the glyphs are in the bottom
    # 256 code points.
    #
    # Future glyphs should be added to the end of this list, so that
    # the existing code point values stay the same.
    glyphlist = [
    ("big0", 0x30),
    ("big1", 0x31),
    ("big2", 0x32),
    ("big3", 0x33),
    ("big4", 0x34),
    ("big5", 0x35),
    ("big6", 0x36),
    ("big7", 0x37),
    ("big8", 0x38),
    ("big9", 0x39),
    ("dynamicf", 0x66),
    ("dynamicm", 0x6d),
    ("dynamicp", 0x70),
    ("dynamicr", 0x72),
    ("dynamics", 0x73),
    ("dynamicz", 0x7a),
    ("asciiplus", 0x2b),
    ("asciicomma", 0x2c),
    ("asciiminus", 0x2d),
    ("asciiperiod", 0x2e),
    ("accent", 0x3e),
    ("acclparen", 0x28),
    ("accrparen", 0x29),
    ("fixedbrace", 0x7b),
    "espressivo",
    "accslashbigup",
    "accslashbigdn",
    "acciaccatura",
    "appoggiatura",
    "arpeggioshort",
    "arpeggioarrowdown",
    "arpeggioarrowup",
    "trillwiggle",
    "bowdown",
    "bowup",
    "bracketlowerlily",
    "bracketupperlily",
    "breath",
    "revbreath",
    "varbreath",
    "revvarbreath",
    "caesura",
    "caesuracurved",
    "breve",
    "clefC",
    "clefF",
    "clefG",
    "clefTAB",
    "clefperc",
    "clefCsmall",
    "clefFsmall",
    "clefGsmall",
    "clefTABsmall",
    "clefpercsmall",
    "coda",
    "varcoda",
    "ditto",
    "fermata",
    "fermata0",
    "fermata2",
    "fermata3",
    "fermataup",
    "fermata0up",
    "fermata2up",
    "fermata3up",
    "semiflat",
    "semiflatslash",
    "flat",
    "flatup",
    "flatdn",
    "flatupdn",
    "flatslash",
    "flatslash2",
    "sesquiflat",
    "doubleflat",
    "doubleflatslash",
    "harmart",
    "harmartfilled",
    "harmnat",
    "flagopen",
    "flagthumb",
    "headcrotchet",
    "headminim",
    "legato",
    "portatoup",
    "portatodn",
    "mordentlower",
    "mordentupper",
    "mordentupperlong",
    "mordentupperlower",
    "upmordentupperlong",
    "upmordentupperlower",
    "mordentupperlongdown",
    "downmordentupperlong",
    "downmordentupperlower",
    "mordentupperlongup",
    "straightmordentupperlong",
    "natural",
    "naturalup",
    "naturaldn",
    "naturalupdn",
    "peddot",
    "pedP",
    "pedd",
    "pede",
    "pedPed",
    "pedPeddot",
    "pedstar",
    "peddash",
    "repeatmarks",
    "restdbllonga",
    "restlonga",
    "restbreve",
    "restcrotchet",
    "restcrotchetx",
    "restdemi",
    "resthemi",
    "restquasi",
    "restminimo",
    "restquaver",
    "restsemi",
    "restsemibreveo",
    "segno",
    "semibreve",
    "sforzando",
    "sforzandodn",
    "semisharp",
    "semisharp3",
    "sharp",
    "sharp3",
    "sharpup",
    "sharpdn",
    "sharpupdn",
    "sesquisharp",
    "doublesharp",
    "staccatissup",
    "staccatissdn",
    "staccato",
    "snappizz",
    "stopping",
    "tailquaverdn",
    "tailquaverup",
    "tailsemidn",
    "tailsemiup",
    "taildemidn",
    "taildemiup",
    "tailhemidn",
    "tailhemiup",
    "tailquasidn",
    "tailquasiup",
    "timeCbar",
    "timeC",
    "trill",
    "turn",
    "invturn",
    "openarrowup",
    "openarrowdown",
    "openarrowleft",
    "openarrowright",
    "closearrowup",
    "closearrowdown",
    "closearrowleft",
    "closearrowright",
    "upedalheel",
    "dpedalheel",
    "upedaltoe",
    "dpedaltoe",
    "acc2",
    "acc3",
    "acc4",
    "accr",
    "accdot",
    "accstar",
    "diamondsemi",
    "diamondminim",
    "diamondcrotchet",
    "trianglesemi",
    "triangleminim",
    "trianglecrotchet",
    "crosssemi",
    "crossminim",
    "crosscrotchet",
    "crosscircle",
    "slashsemi",
    "slashminim",
    "slashcrotchet",
    ]

    code = 0x21 # use sequential code points for anything not explicitly given

    codes = {}
    for i in range(0x7f, 0xa1):
        codes[i] = None # avoid these code points

    outlines = {}
    for i in range(len(glyphlist)):
        gid = glyphlist[i]

        if type(gid) == types.TupleType:
            # Allocate a specific code.
            gid, thiscode = gid
        else:
            while codes.has_key(code):
                code = code + 1
            assert code < 0x100
            thiscode = code
        codes[thiscode] = gid

        char = eval(gid)

        if not outlines.has_key(gid):
            outlines[gid] = get_ps_path(char)

        xo, yo = char.origin
        if (xo,yo) == (1000,1000):
            # Hack: that particular origin is taken to indicate that
            # the origin was not set to anything more sensible by
            # GlyphContext.__init__, and so we instead use the
            # centre of the glyph's bounding box.
            x0, y0, x1, y1 = outlines[gid][0]
            xo = (x0+x1)/2
            yo = (y0+y1)/2
        else:
            xo = xo * char.scale / 3600. * 40
            yo = yo * char.scale / 3600. * 40
        if char.__dict__.has_key("hy"):
            yo = (1000 - char.hy) * 40
        if char.__dict__.has_key("hx"):
            xo = char.hx * 40

        dict = {}
        if char.__dict__.has_key("width"):
            dict["xw"] = char.width * 40 + xo

        glyphlist[i] = (gid, gid, thiscode, xo, yo, None, None, None, None, dict)

    writesfd("gonville-simple", "Gonville-Simple", "UnicodeBmp", 65537, outlines, glyphlist)
    system("fontforge -lang=ff -c 'Open($1); CorrectDirection(); " + \
    "Generate($2)' gonville-simple.sfd gonville-simple.otf")

elif len(args) == 2 and args[0] == "-lilycheck":
    # Run over the list of glyph names in another font file and list
    # the ones not known to this file. Expects one additional
    # argument which is the name of a font file.
    known = {}
    for g in lilyglyphlist:
        known[g[1]] = 1

    # Regexps 
    import re
    ignored = [
    ".notdef",
    # I wasn't able to get LP to generate this glyph name at all; my
    # guess is that it's a legacy version of trill_element used in
    # older versions.
    "scripts.trilelement",
    # Longa notes are not supported.
    re.compile(r'noteheads\.[ud]M2'),
    # Solfa note heads are not supported.
    re.compile(r'noteheads\..*(do|re|mi|fa|so|la|ti)'),
    # Ancient music is not supported.
    re.compile(r'.*vaticana.*'),
    re.compile(r'.*mensural.*'),
    re.compile(r'.*petrucci.*'),
    re.compile(r'.*medicaea.*'),
    re.compile(r'.*solesmes.*'),
    re.compile(r'.*hufnagel.*'),
    "scripts.ictus",
    "scripts.uaccentus",
    "scripts.daccentus",
    "scripts.usemicirculus",
    "scripts.dsemicirculus",
    "scripts.circulus",
    "scripts.augmentum",
    "scripts.usignumcongruentiae",
    "scripts.dsignumcongruentiae",
    ]

    s = string.replace(args[1], "'", "'\\''")
    system("fontforge -lang=ff -c 'Open($1); Save($2)' '%s' temp.sfd >&/dev/null" % s)
    f = open("temp.sfd", "r")
    while 1:
        s = f.readline()
        if s == "": break
        ss = s.split()
        if len(ss) >= 2 and ss[0] == "StartChar:":
            name = ss[1]
            ok = known.get(name, 0)
            if not ok:
                for r in ignored:
                    if type(r) == types.StringType:
                        match = (r == name)
                    else:
                        match = r.match(name)
                    if match:
                        ok = 1
                        break
            if not ok:
                print name
    f.close()
