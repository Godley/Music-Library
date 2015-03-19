class SearchProcessor(object):
    '''
    class which takes in a string input and figures out how to query the database for
    information, by using a variety of techniques. Using an object rather than a method to
    keep the system modular and organised.
    '''
    def __init__(self):
        pass

    def process(self, input):
        result = {}
        list_of_input = list(input.split(" "))
        for item in list_of_input:
            if item.endswith(".xml"):
                if "filename" not in result:
                    result["filename"] = []
                result["filename"].append(item)
            else:
                if "/" in item:
                    if "time_signature" not in result:
                        result["time_signature"] = []
                    result["time_signature"].append(item)
                if "=" in item:
                    if "tempo" not in result:
                        result["tempo"] = []
                    result["tempo"].append(item)

                if ":" in item:
                    pairing = item.split(":")
                    options = ["instrument","tempo","timesig","meter","key","clef","in","title",
                               "composer","lyricist","lyrics","playlist"]
                    if pairing[0] in options:
                        if pairing[0] not in result:
                            result[pairing[0]] = []
                        result[pairing[0]].append(pairing[1])
                elif "/" not in item and "=" not in item and ":" not in item:
                    if "text" not in result:
                        result["text"] = []
                    result["text"].append(item)
        return result

