class Node(object):
    def __init__(self, duration, value):
        self.duration = duration
        self.value = value
        self.next = None
        self.previous = None

    def SetNext(self, item):
        self.next = item

    def SetPrevious(self, item):
        self.previous = item

    def Next(self):
        return self.next

    def Previous(self):
        return self.previous

    def GetDuration(self):
        return self.duration

    def GetValue(self):
        return self.value

    def SetValue(self, item):
        self.value = item

    def SetDuration(self, dur):
        self.duration = dur

class LinkedList(object):
    def __init__(self):
        self.first = None
        self.last = None

    def Head(self):
        return self.first

    def Tail(self):
        return self.last

    def Add(self, item, offset=0):
        position = self.first
        if offset == 0:
            if position is None:
                self.first = item
                self.last = self.first.Next()
                if self.last is None:
                    self.last = item
            else:
                next = position.Next()
                if next is None:
                    self.first.SetNext(item)
                else:
                    while next is not None:
                        next = next.Next()
                        if next.Next() is not None:
                            next.SetNext(item)
        else:
            new_node = Node(offset, None)