def SplitString(value):
    """simple method that puts in spaces every 10 characters"""
    string_length = len(value)
    chunks = int(string_length / 10)
    string_list = list(value)
    lstring = ""

    if chunks > 1:
        lstring = "\\markup { \n\r \column { "
        for i in range(int(chunks)):
            lstring += "\n\r\r \\line { \""
            index = i*10
            for i in range(index):
                lstring += string_list[i]
            lstring += "\" \r\r}"
        lstring += "\n\r } \n }"
    if lstring == "":
        indexes = [i for i in range(len(string_list)) if string_list[i] == "\r" or string_list[i] == "\n"]
        lstring = "\\markup { \n\r \column { "
        if len(indexes) == 0:
            lstring += "\n\r\r \\line { \"" + "".join(string_list) + "\" \n\r\r } \n\r } \n }"
        else:
            rows = []
            row_1 = string_list[:indexes[0]]
            rows.append(row_1)
            for i in range(len(indexes)):
                start = indexes[i]
                if i != len(indexes)-1:
                    end = indexes[i+1]
                else:
                    end = len(string_list)
                row = string_list[start:end]
                rows.append(row)

            for row in rows:
                lstring += "\n\r\r \\line { \""
                lstring += "".join(row)
                lstring += "\" \r\r}"
            lstring += "\n\r } \n }"
    return lstring
