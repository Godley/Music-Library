import os, sys, inspect
def get_base_dir(return_this_dir=False):
   if getattr(sys,"frozen",False):
       # If this is running in the context of a frozen (executable) file,
       # we return the path of the main application executable
       return os.path.dirname(os.path.abspath(sys.executable))
   else:
       # If we are running in script or debug mode, we need
       # to inspect the currently executing frame. This enable us to always
       # derive the directory of main.py no matter from where this function
       # is being called
       thisdir = os.path.dirname(inspect.getfile(inspect.currentframe()))
       parent =  os.path.abspath(os.path.join(thisdir, os.pardir))
       if return_this_dir:
           return thisdir
       else:
           return parent

def parseStyle(stylesheet):
    results = []
    for line in stylesheet:
        if "themes/" in line:
            result = line.split("themes")
            result_string = result[0] + os.path.join(get_base_dir(True), "themes") +result[1]
            results.append(result_string)
        else:
            results.append(line)
    return "\n".join(results)


