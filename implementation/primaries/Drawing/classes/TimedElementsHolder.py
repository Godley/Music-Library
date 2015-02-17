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

    def Add(self, item):
        if self.first is None:
            self.first = item
            if item.Next() is not None:
                self.last = item.Next()
            else:
                self.last = item
        else:
            next_val = self.Head().Next()
            if next_val is None:
                self.Head().SetNext(item)
            else:
                # need to do some checking of duration etc.
                pass