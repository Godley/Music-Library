#!/usr/bin/env python

import sys
import string

from Tkinter import *

from curves import *

tkroot = Tk()

class Container:
    pass

cont = Container()

cont.curves = {}
cont.curveid = 0
cont.canvas = Canvas(tkroot, width=1000, height=1000)

dragging = None

def click(event):
    global dragging
    for curve in cont.curves.values():
        if curve.tk_drag(event.x, event.y, 1):
            dragging = curve
            dragging.tk_refresh()
            break
def drag(event):
    global dragging
    if dragging != None:
        dragging.tk_drag(event.x, event.y, 2)
def release(event):
    global dragging
    if dragging != None:
        dragging.tk_drag(event.x, event.y, 3)
        dragging = None
def key(event):
    if event.char == 'i':
        curve = CircleInvolute(cont, event.x - 50, event.y, 1, -1, event.x + 50, event.y, 1, 1)
    elif event.char == 'l':
        curve = StraightLine(cont, event.x-50, event.y-20, event.x+50, event.y+20)
    elif event.char == 'b':
        curve = Bezier(cont, event.x - 50, event.y, event.x-25, event.y-25, event.x+25, event.y+25, event.x+50, event.y)
    elif event.char == 'e':
        curve = ExponentialInvolute(cont, event.x - 50, event.y, 2, -1, event.x + 50, event.y, 2, 1.2)
    elif event.char == 'w':
        ends = []
        for curve in cont.curves.values():
            end = curve.findend(event.x, event.y)
            if end != None:
                ends.append((curve, end))
        if len(ends) != 2:
            tkroot.bell()
        else:
            ends[0][0].weld_to(ends[0][1], ends[1][0], ends[1][1])
    elif event.char == 'u':
        for curve in cont.curves.values():
            end = curve.findend(event.x, event.y)
            if end != None:
                curve.unweld(end)
    elif event.char == 'S':
        # Indent to match the typical indent level in glyphs.py.
        print "    # Saved data from gui.py"
        for cid, curve in cont.curves.items():
            print "    c%d = %s" % (cid, curve.serialise())
        for cid1, curve1 in cont.curves.items():
            for cid2, curve2 in cont.curves.items():
                if cid2 < cid1:
                    continue # only output each weld one way round
                for end1 in (0, 1):
                    if curve1.welds[end1] != None and \
                    curve1.welds[end1][0] == curve2:
                        end2 = curve1.welds[end1][1]
                        if curve1.welds[end1][3] != None:
                            print "    c%d.weld_to(%d, c%d, %d, %d, %s)" % (cid1, end1, cid2, end2, curve1.welds[end1][2], repr(curve1.welds[end1][3]))
                        elif curve1.welds[end1][2] != 0:
                            print "    c%d.weld_to(%d, c%d, %d, %d)" % (cid1, end1, cid2, end2, curve1.welds[end1][2])
                        else:
                            print "    c%d.weld_to(%d, c%d, %d)" % (cid1, end1, cid2, end2)
        print "    # End saved data"
    elif event.char == 'L':
        for curve in cont.curves.values():
            curve.cleanup()
        cont.curves = {}
        cont.curveid = 0
        print "Paste saved curve data in, including the \"# End\" line:"
        while 1:
            x = sys.stdin.readline()
            if x == "":
                break
            while len(x) > 0 and x[:1] in string.whitespace:
                x = x[1:]
            if x[:5] == "# End":
                break
            exec x
    elif event.char == 'T' or event.char == '\x14':
        print "Enter a transformation matrix:"
        x = sys.stdin.readline()
        matrix = eval(x)
        for curve in cont.curves.values():
            curve.transform(matrix, event.char == '\x14')
            curve.tk_refresh()
    elif event.char == '\x11': # Ctrl-Q
        sys.exit(0)

cont.canvas.bind("<Button-1>", click)
cont.canvas.bind("<B1-Motion>", drag)
cont.canvas.bind("<ButtonRelease-1>", release)
tkroot.bind("<Key>", key)
cont.canvas.pack()

if len(sys.argv) > 1:
    img = PhotoImage(file=sys.argv[1])
    cont.canvas.create_image(500, 500, image=img)

mainloop()
