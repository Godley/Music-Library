from implementation.primaries.GUI.helper import get_base_dir
def parseStyle(stylesheet):
    results = []
    for line in stylesheet:
        if "themes/" in line:
            result = line.split("themes")
            result_string = result[0] + get_base_dir(True)+"/themes"+result[1]
            results.append(result_string)
        else:
            results.append(line)
    return "\n".join(results)

