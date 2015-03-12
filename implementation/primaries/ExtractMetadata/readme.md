This portion of code contains any classes and methods which take a list of music XML files and take out the metadata.
This also includes searching and sorting through that data.

This is fundamentally organised into:
- the data layer in DataLayer.py: this is the baseline data layer which talks to an SQLite database created on a folder by folder basis.
- a layer on top which manipulates data coming from the parser + from the user
- a class/algorithm which takes a musicXML file and parses it for the data needed, then sends this to the data manipulator

Any unit tests created in the course of development are in the tests folder.
