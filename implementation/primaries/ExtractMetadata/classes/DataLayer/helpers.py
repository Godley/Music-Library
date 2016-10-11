def get_if_exists(dict, key, default=0):
    if dict is not None:
        if key in dict:
            return dict[key]
    return default


def filter_dict(entry, method=lambda k: k is not None and len(k) > 0):
    return {key: entry[key] for key in entry if method(entry[key])}


def filter_list(entry, method=lambda k: len(k) > 0 and k is not None):
    return [key for key in entry if method(key)]
