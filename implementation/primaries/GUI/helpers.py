import os
import sys
import inspect


def get_base_dir(return_this_dir=False):
    if getattr(sys, "frozen", False):
        # If this is running in the context of a frozen (executable) file,
        # we return the path of the main application executable
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        # If we are running in script or debug mode, we need
        # to inspect the currently executing frame. This enable us to always
        # derive the directory of main.py no matter from where this function
        # is being called
        thisdir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        parent = os.path.abspath(os.path.join(thisdir, os.pardir))
        if return_this_dir:
            return thisdir
        else:
            return parent


def parseStyle(stylesheet, theme):
    results = []
    for line in stylesheet:
        if "themes/" in line:
            if sys.platform == 'win32':
                line.replace('/', '\\')
            else:
                line.replace('\\', '/')
            section1 = line
            postfix = ""
            while "themes" in section1:
                portion = os.path.split(section1)
                section1 = portion[0]
                postfix = os.path.join(portion[1],postfix)
            result_string = section1+os.path.join(get_base_dir(True), postfix)

            if "icons" in result_string:
                prefix = result_string
                postfix = ""
                while "icons" in prefix:
                    split_path = result_string.split('icons')
                    prefix = split_path[0]
                    postfix = "".join([postfix, split_path[1]])
                result_string = os.path.join(prefix, "icons", theme, postfix)
            print(result_string)
            results.append(result_string)

        else:
            results.append(line)
    return "\n".join(results)
