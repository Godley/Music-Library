import unittest
from implementation.primaries.Drawing.classes import Piece
from implementation.primaries.Drawing.classes.tree_cls.Testclasses import PieceTree

class TestClass(unittest.TestCase):
    def setUp(self):
        self.tags = []
        self.attrs = {}
        self.chars = {}
        self.piece = PieceTree()

