import unittest
from implementation.primaries.Drawing.classes import Piece

class TestClass(unittest.TestCase):
    def setUp(self):
        self.tags = []
        self.attrs = {}
        self.chars = {}
        self.piece = Piece.Piece()

