import math


def myRowCalculator(columnCount, total, position):
    # bottom left is 0,0. Top right is ColumnCount-1,rowCount-1
    rowCount = total / columnCount
    row = 0
    column = 0
    flooredVal = math.floor(position/columnCount)

    if position == 0:
        row = rowCount -1
        column = 0
    if position < columnCount-1:
        row = rowCount-1
        column = position
    if position % columnCount-1 == 0 or position == columnCount-1:
        normRow = flooredVal
        column = position-(columnCount*normRow)
        row = (rowCount-1)-flooredVal
    if position > columnCount-1:
        normRow = flooredVal
        column = position-(columnCount-1*normRow)
        row = (rowCount-1)-flooredVal

    return row, column

def reverseCalculation(columnCount, row, column):

    position = (row*columnCount)+column

    return position