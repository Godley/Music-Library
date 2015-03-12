This folder consists of any and all code towards the algorithm to draw sheet music based on XML files. 

The main elements of this are:
- the MxmlParser file and class, which contains a lot of methods and a class which SAX parses XML files and puts them into classes
- the files contained in tree_cls of the classes folder, which describe the tree structure the piece will be loaded into. 
- all the other files in the classes folder are music object types. These are generally organised according to what class they will be attached to, i.e stuff in note.py 
  generally comes in the Note class, though some of the classes I moved around because the file was getting too big. 
- the toLily method which is implemented in basically every object. Each object and child object is standalone, so calling toLily on any of them will result in them calling themselves and their children in some order depending on what it is.
  
This algorithm has been tested against a very big set of testcases downloaded from lilypond.org (http://www.lilypond.org/doc/v2.18/input/regression/musicxml/collated-files.html) - thanks a lot for whoever made that public because it's been very useful.
These are stored in primaries/SampleMusicXML/testcases - around 57% of all the testcases pass, any that don't are in ignored but hopefully they should still generate pdf output. Most of the testcases in ignored are referenced in issues under the milestone
"testing of drawing/rendering algorithm" as I intend to get a lot more to pass, it's just at the FYP stage of this project I don't have the time, and I believe the set that I have made pass cover most usecases I was hoping for.
