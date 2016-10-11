import traceback


class Tracer:

    def __init__(self, oldstream):
        self.oldstream = oldstream
        self.count = 0
        self.lastStack = None

    def write(self, s):
        newStack = traceback.format_stack()
        if newStack != self.lastStack:
            self.oldstream.write("".join(newStack))
            self.lastStack = newStack
        self.oldstream.write(s)
