import math


def myRowCalculator(columnCount, total, position):
    # bottom left is 0,0. Top right is ColumnCount-1,rowCount-1
    row = 0
    column = 0
    rowCount = total / columnCount
    newPos = total - position - 1
    row = int(newPos / columnCount)
    column = position % columnCount
    return row, column


def getPositionsForWord(position, total, columnCount, direction, length):
    results = [position]
    if direction == 6:
        # north
        for i in range(1, length):
            newPosition = results[-1] - columnCount
            results.append(newPosition)

    if direction == 5:
        # north west
        for i in range(1, length):
            newPosition = results[-1] - columnCount - 1
            results.append(newPosition)

    if direction == 7:
        # north east
        for i in range(1, length):
            newPosition = results[-1] - columnCount + 1
            results.append(newPosition)
    return results
