import unittest
from implementation.primaries.ImportOnlineDBs.calculator import myRowCalculator, getPositionsForWord

class testCalc(unittest.TestCase):

    def testZero(self):
        columnCount = 12
        position = 132
        total = 144
        self.assertEqual((0,0), myRowCalculator(columnCount, total, position))

    def testMax(self):
        columnCount = 12
        position = 11
        total = 144
        self.assertEqual((11,11), myRowCalculator(columnCount, total, position))

    def testTopVal(self):
        columnCount = 12
        position = 143
        total = 144
        self.assertEqual((0,11), myRowCalculator(columnCount, total, position))


    def testMidOfTopRow(self):
        columnCount = 12
        position = 7
        total = 144
        self.assertEqual((11,7), myRowCalculator(columnCount, total, position))


    def testMidOfSecondRow(self):
        columnCount = 12
        position = 14
        total = 144
        self.assertEqual((10,2), myRowCalculator(columnCount, total, position))

    def testGetNextPosFromZeroDirection6(self):
        position = 132
        total = 144
        columnCount = 12
        direction = 6
        length = 2
        self.assertEqual([132, (132-columnCount)], getPositionsForWord(position, total, columnCount, direction, length))

    def testGetNextPosFromZeroDirection6Length4(self):
        position = 132
        total = 144
        columnCount = 12
        direction = 6
        length = 4
        self.assertEqual([132, (132-columnCount), (132-(columnCount*2)), (132-(columnCount*3))], getPositionsForWord(position, total, columnCount, direction, length))

    def testGetNextPosFromZeroDirection5(self):
        position = 132
        total = 144
        columnCount = 12
        direction = 5
        length = 2
        self.assertEqual([132, (132-columnCount-1)], getPositionsForWord(position, total, columnCount, direction, length))

    def testGetNextPosFromZeroDirection5Length4(self):
        position = 132
        total = 144
        columnCount = 12
        direction = 5
        length = 4
        self.assertEqual([132, (132-columnCount-1), (132-(columnCount*2)-2), (132-(columnCount*3)-3)], getPositionsForWord(position, total, columnCount, direction, length))

    def testGetNextPosFromZeroDirection7(self):
        position = 132
        total = 144
        columnCount = 12
        direction = 7
        length = 2
        self.assertEqual([132, (132-columnCount+1)], getPositionsForWord(position, total, columnCount, direction, length))

    def testGetNextPosFromZeroDirection7Length4(self):
        position = 132
        total = 144
        columnCount = 12
        direction = 7
        length = 4
        self.assertEqual([132, (132-columnCount+1), (132-(columnCount*2)+2), (132-(columnCount*3)+3)], getPositionsForWord(position, total, columnCount, direction, length))