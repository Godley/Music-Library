from implementation.primaries.Drawing.classes import Part, Piece, Meta
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testPiece(Lily):
    def setUp(self):
        self.item = Piece.Piece()
        self.lilystring = "<<>>"

class testPieceWithPart(Lily):
    def setUp(self):
        self.item = Piece.Piece()
        self.item.addPart(id="P2",part=Part.Part())
        self.lilystring = "<<>>"

class testPieceWithTitle(Lily):
    def setUp(self):
        self.item = Piece.Piece()
        self.item.meta = Meta.Meta(title="hello world")
        self.lilystring = "\n\header {\ntitle = \"hello world\"\n\n}<<>>"

