def process(query_input):
    spaced_input = split_input(query_input)
    data = {}
    for with_pair in spaced_input:
        if is_key(with_pair):
            entry = {"key":[" ".join(with_pair)]}
            data = combine_dictionaries(data, entry)
            continue
        for quote_pair in with_pair:
            if is_key(quote_pair):
                entry = {"key":[" ".join(quote_pair)]}
                data = combine_dictionaries(data, entry)
                continue

            entries = handle_meter_tempo_text_kv(quote_pair)
            data = combine_dictionaries(data, entries)
    return data

def handle_meter_tempo_text_kv(tokens):
    data = {}
    for token in tokens:
        if is_meter(token):
            entry = {"meter":[token]}
            combine_dictionaries(data, entry)

        elif is_tempo(token):
            entry = {"tempo": [token]}
            combine_dictionaries(data, entry)

        elif token.endswith(".xml"):
            entry = {"filename":[token]}
            combine_dictionaries(data, entry)

        elif ":" in token:
            result = handle_colons_and_semicolons(token)
            data = combine_dictionaries(result, data)

        else:
            entry = {"text": [token]}
            data = combine_dictionaries(entry, data)
    return data

def combine_dictionaries(dict1, dict2):
    new_dict = dict1
    for key in dict2:
        if key not in new_dict:
            new_dict[key] = dict2[key]
        elif type(new_dict[key]) is dict and type(dict2[key]) is dict:
            new_dict[key] = combine_dictionaries(new_dict[key], dict2[key])
        elif type(new_dict[key]) is dict:
            new_dict[key]["other"] = dict2[key]
        elif type(dict2[key]) is dict:
            cpy = new_dict[key]
            new_dict[key] = {"other":cpy}
            new_dict[key].update(dict2[key])
        else:
            new_dict[key].extend(dict2[key])
    return new_dict

def is_key(token_pair):
    if len(token_pair) == 2:
        if len(token_pair[0]) == 1 or "sharp" in token_pair[0] or "flat" in token_pair[0]:
            return has_mode(token_pair[1])
    return False

def has_mode(token):
    opt = ["major", "minor", "maj", "min"]
    if token.lower() in opt:
        return True
    return False

def is_meter(token):
    parts = token.split("/")
    verdict = True
    if len(parts) > 1:
        try:
            int(parts[0])
            int(parts[1])
        except:
            verdict = False
    else:
        verdict = False
    return verdict

def is_tempo(token):
    parts = token.split("=")
    if len(parts) > 1:
        try:
            int(parts[0])
            verdict = False
        except:
            verdict = True
    else:
        verdict = False
    return verdict


def split_input(query_input):
    quotes_input = []
    values = query_input.split("\"")
    quotes_input.extend([value for value in values if value != ''])

    spaced_input = []
    data = []
    for unit in quotes_input:
        new_unit = unit.split(" ")
        if type(new_unit) is list:
            new_unit = [u for u in new_unit if u != '']
            data.append(new_unit)
        elif new_unit != '':
            data.append(new_unit)
    spaced_input.append(data)
    return spaced_input

def handle_colons_and_semicolons(entry):
    tokens = entry.split(";")
    result = {}
    last_key = None
    first_value = None
    for token in tokens:
        kv = token.split(":")
        if len(kv) > 1:
            last_key = kv[0]
            if first_value == None:
                first_value = kv[1]
                dict_entry = {last_key: [kv[1]]}
                result = combine_dictionaries(result, dict_entry)
            else:
                dict_entry = {last_key: {first_value: [kv[1]]}}
                result = combine_dictionaries(result, dict_entry)
        else:
            if last_key is not None:
                dict_entry = {last_key: [kv[0]]}
                result = combine_dictionaries(result, dict_entry)

    return result
