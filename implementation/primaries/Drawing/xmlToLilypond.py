import sys, os
from implementation.primaries.Drawing.classes import MxmlParser, LilypondRender

def Run(fname):
    parser = MxmlParser.MxmlParser()
    try:
        pieceObj = parser.parse(fname)
    except BaseException as e:
        return [fname, str(e)]
    render = LilypondRender.LilypondRender(pieceObj, fname)
    try:
        render.run()
    except Exception as e:
        return [render.lyfile, str(e)]
    if not os.path.exists(render.pdf):
        return render.lyfile


if len(sys.argv) > 1:
    file = sys.argv[1]
    print(file)
    Run(file)

