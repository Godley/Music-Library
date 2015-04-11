import math


def myRowCalculator(columnCount, total, position):
    rowFl = position/columnCount
    row = math.floor(rowFl)

    if position % columnCount == 0 and position > 0 and row > 0:
        row -= 1

    if position > columnCount-1:
        column = position-(row*columnCount)
    else:
        column = position

    return row, column

def reverseCalculation(columnCount, row, column):

    position = (row*columnCount)+column

    return position