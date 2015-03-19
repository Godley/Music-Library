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
        for i in range(len(list_of_input)):
            item = list_of_input[i]
            nxt = None
            if i != len(list_of_input)-1:
                nxt = list_of_input[i+1]
            if item.endswith(".xml"):
                if "filename" not in result:
                    result["filename"] = []
                result["filename"].append(item)

            if ":" in item:
                pairing = item.split(":")
                options = ["instrument","tempo","time","meter","key","clef","title",
                           "composer","lyricist","lyrics","playlist","filename","transposition"]
                if pairing[0] in options:
                    if pairing[0] not in result and pairing[0] != "meter" and pairing[0] != "key" and pairing[0] != "clef":
                        result[pairing[0]] = []
                    elif pairing[0] == "meter" and "time" not in result:
                        result["time"] = []
                    elif (pairing[0] == "key" or pairing[0] == "clef") and pairing[0] not in result:
                        result[pairing[0]] = {"other":[]}
                    if pairing[0] == "key":
                        if "other" not in result[pairing[0]]:
                            result[pairing[0]]["other"] = []
                        if nxt == "major" or nxt == "minor":
                            result[pairing[0]]["other"].append(pairing[1]+" "+nxt)
                        else:
                            result[pairing[0]]["other"].append(pairing[1]+" major")
                    if pairing[0] == "clef":
                        if "other" not in result[pairing[0]]:
                            result[pairing[0]]["other"] = []
                        result[pairing[0]]["other"].append(pairing[1])
                    if pairing[0] == "filename" and not pairing[1].endswith(".xml"):
                        result[pairing[0]].append(pairing[1]+".xml")
                    if pairing[0] == "meter":
                        result["time"].append(pairing[1])
                    elif pairing[0] != "key" and pairing[0] != "clef" and pairing[0] != "filename" and pairing[0] != "meter":
                        result[pairing[0]].append(pairing[1])
                else:
                    if pairing[0] == "with":
                        instrument = ""
                        length = len(pairing)
                        updated_pairing = []
                        for index in range(length):
                            text = pairing[index]
                            if ";" in text:
                                split_text = text.split(";")
                                updated_pairing.append(split_text[0])
                                updated_pairing.append(split_text[1])
                            else:
                                updated_pairing.append(text)
                        pairing = updated_pairing

                        if "instrument" in result and len(result["instrument"]) > 0:
                            instrument = result["instrument"][-1]
                        if instrument != "":
                            index = 1
                            while index < len(pairing):
                                if pairing[index] == "key":
                                    if "key" not in result:
                                        result["key"] = {}
                                    elif "key" in result and result["key"] == []:
                                        data = result["key"]
                                        result["key"] = {"other":data}

                                    if nxt == "major" or nxt == "minor":
                                        if instrument not in result["key"]:
                                            result["key"][instrument] = []
                                        result["key"][instrument].append(pairing[index+1]+" "+nxt)
                                    else:
                                        if instrument not in result["key"]:
                                            result["key"][instrument] = []
                                        result["key"][instrument].append(pairing[index+1]+" major")

                                if pairing[index] == "clef":
                                    if "clef" not in result:
                                        result["clef"] = {}
                                    elif "clef" in result and result["clef"] == []:
                                        data = result["clef"]
                                        if data is None:
                                            data = []
                                        result["clef"] = {"other":data}
                                    if instrument not in result["clef"]:
                                        result["clef"][instrument] = []
                                    result["clef"][instrument].append(pairing[index+1])
                                index += 2



                continue
            elif not item.endswith(".xml") and ":" not in item:
                if "/" in item:
                    if "time_signature" not in result:
                        result["time"] = []
                    result["time"].append(item)
                    continue

                if "=" in item:
                    if "tempo" not in result:
                        result["tempo"] = []
                    result["tempo"].append(item)
                    continue

                if len(item) == 1 or "sharp" in item or "flat" in item or "#" in item:
                    if "key" not in result:
                        result["key"] = []
                    if nxt == "major" or nxt == "minor":
                        result["key"].append(item+" "+nxt)
                    else:
                        result["key"].append(item+" major")
                    continue

                elif item != "major" and item != "minor":
                    if "text" not in result:
                        result["text"] = []
                    result["text"].append(item)
        return result

