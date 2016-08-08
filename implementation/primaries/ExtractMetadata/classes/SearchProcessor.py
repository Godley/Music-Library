def split_input(query_input):
    with_split = query_input.split("with")
    split_input = [unit.split("\"") for unit in with_split]
    spaced_input = []
    for unit in split_input:
        data = []
        for value in unit:
            new_unit = value.split(" ")
            data.append(new_unit)
        spaced_input.append(data)
    return spaced_input

def handleColonsAndSemiColons(entry):
    pass

def process(query_input):
    """
    class which takes in a string input and figures out how to query the database for
    information, by using a variety of techniques. Using an object rather than a method to
    keep the system modular and organised.
    :param query_input: input from UI
    :return: dictionary of formatted queries to make on the DB
    """
    result = {}

    spaced_input = split_input(query_input)

    previous = None
    for i in range(len(spaced_input)):
        nxt = None
        for j in range(len(spaced_input[i])):
            if j + 1 != len(spaced_input[i]):
                nxt = spaced_input[i][j + 1]
            for k in range(len(spaced_input[i][j])):
                entry = spaced_input[i][j][k]
                if entry.endswith(".xml"):
                    if "filename" not in result:
                        result["filename"] = []
                    result["filename"].append(entry)

                if ":" in entry or ";" in entry:
                    if entry[0] == ":" or entry[0] == ";":

                        key_value_pair = entry.split(":")
                        semicolon_spacer = []
                        [semicolon_spacer.extend(
                            value.split(";")) for value in key_value_pair]
                        index = 0
                        instrument = ""
                        if "instrument" in result:
                            if len(result["instrument"]) > 0:
                                instrument = result["instrument"][-1]
                        while index < len(semicolon_spacer):
                            new_key = semicolon_spacer[index]
                            if new_key == "key":
                                if "key" not in result:
                                    result["key"] = {}
                                if instrument not in result["key"]:
                                    result["key"][instrument] = []
                                if nxt is not None:
                                    result["key"][instrument].append(
                                        " ".join(nxt))
                            if new_key == "clef":
                                if "clef" not in result:
                                    result["clef"] = {}
                                if instrument not in result["clef"]:
                                    result["clef"][instrument] = []
                                result["clef"][instrument].append(
                                    semicolon_spacer[
                                        index +
                                        1])
                            if new_key == "":
                                index += 1
                            else:
                                index += 2
                    else:
                        key_value_pair = entry.split(":")
                        options = [
                            "instrument",
                            "key",
                            "clef",
                            "with",
                            "time",
                            "meter",
                            "composer",
                            "title",
                            "lyricist",
                            "transposition"]
                        key = key_value_pair[0]
                        value = key_value_pair[1]
                        if len(value) == 0 and nxt is not None:
                            value = " ".join(nxt)
                        if key in options:
                            if key == "meter":
                                if "time" not in result:
                                    result["time"] = []
                                result["time"].append(value)

                            if key in ["key", "clef"]:
                                if key not in result:
                                    result[key] = {}
                                if "other" not in result[key]:
                                    result[key]["other"] = []
                                if key == "clef":
                                    result[key]["other"].append(value)
                                if key == "key":
                                    result[key]["other"].append(" ".join(nxt))
                            elif key != "meter" and key != "with" and key != "clef" and key != "key":
                                if key not in result:
                                    result[key] = []
                                result[key].append(value)
                                continue
                elif not entry.endswith(".xml"):
                    if ((len(entry) == 1 and entry in ["A", "B", "C", "D", "E", "F", "G"]) or
                        "sharp" in entry or "flat" in entry) and \
                            (previous is None or "key" not in previous[-1]):
                        if k != len(spaced_input[i][j]) - 1 and \
                                (spaced_input[i][j][k + 1] == "major" or spaced_input[i][j][k + 1] == "minor"):
                            if "key" not in result:
                                result["key"] = {}
                            if "other" not in result["key"]:
                                result["key"]["other"] = []
                            result["key"]["other"].append(
                                " ".join(
                                    spaced_input[i][j]))
                            continue

                    if "/" in entry and entry.split("/")[-1] != "":
                        if "time" not in result:
                            result["time"] = []
                        result["time"].append(entry)

                    if "=" in entry:
                        if "tempo" not in result:
                            result["tempo"] = []
                        result["tempo"].append(entry)

                    elif entry not in ["major", "minor"] and "=" not in entry and "/" not in entry and ((len(entry) > 1 or entry not in ["A", "B", "C", "D", "E", "F", "G"]) and k != len(spaced_input[i][j]))\
                            and (previous is None or len([item for item in previous if ":" in item]) == 0):
                        if len(entry) > 0:
                            if "text" not in result:
                                result["text"] = []
                            result["text"].append(entry)
            previous = spaced_input[i][j]
    return result
