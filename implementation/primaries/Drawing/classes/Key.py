majors = {-6: "Gflat", -5: "Dflat", -4: "Aflat", -3: "Eflat", -2: "Bflat", -1: "F", 0: "C", 1: "G", 2: "D", 3: "A",
          4: "E", 5: "B"}
minors = {-6: "Aflat", -5: "Bflat", -4: "F", -3: "C", -2: "G", -1: "D", 0: "A", 1: "E", 2: "B", 3: "Fsharp",
          4: "Csharp", 5: "Gsharp"}


class Key(object):
    def __init__(self, **kwargs):
        if "fifths" in kwargs:
            self.fifths = kwargs["fifths"]
        if "mode" in kwargs:
            self.mode = kwargs["mode"]

    def __str__(self):
        if hasattr(self, "fifths"):
            if hasattr(self, "mode"):
                if self.mode == "major":
                    return majors[self.fifths] + " major"
                if self.mode == "minor":
                    return minors[self.fifths] + " minor"
