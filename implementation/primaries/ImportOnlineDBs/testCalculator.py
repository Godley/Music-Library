import unittest
from implementation.primaries.ImportOnlineDBs.calculator import myRowCalculator, reverseCalculation

class testCalc(unittest.TestCase):

    def testZero(self):
        columnCount = 5
        position = 0
        total = 25
        self.assertEqual((4,0), myRowCalculator(columnCount, total, position))

    def testSmallerThanColCount(self):
        columnCount = 5
        position = 3
        total = 25
        self.assertEqual((4,3), myRowCalculator(columnCount, total, position))

    def testLargerThanColCount(self):
        columnCount = 5
        position = 6
        total = 25
        self.assertEqual((3,1), myRowCalculator(columnCount, total, position))

    def testColCount(self):
        columnCount = 5
        position = 4
        total = 25
        self.assertEqual((4,4), myRowCalculator(columnCount, total, position))

    def testDoubleColCount(self):
        columnCount = 5
        position = 8
        total = 25
        self.assertEqual((3,4), myRowCalculator(columnCount, total, position))

