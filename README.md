#A Sheet Music Organisation System

<center>[![Build status](https://ci.appveyor.com/api/projects/status/l0rc9184c6tqe19d?svg=true)](https://ci.appveyor.com/project/Godley/music-library)
[![Build Status](https://magnum.travis-ci.com/Godley/Music-Library.svg?token=WYronetRoqG7kFrfqyBW)](https://magnum.travis-ci.com/Godley/Music-Library)</center>

  This project aims to create an application which manages a person's music collection - that is, sheet music, the visual
representation of a composed piece of music.
##Design
The system works by:
- taking a folder
- finding all the musicXML (.xml) files in that folder, and all the zipped musicXMl files in the folder (.mxl)
- unzipping all the mxl files
- running through each XML file and pulling out relevant metadata: this is defined in one of the closed issues under metadata milestone
- cataloging the data in a SQLite db in the folder
- loading stuff useful to the user:
  - a list of all pieces, which can be sorted by several methods
  - a list of all playlists made by the user
  - a list of all playlists generated by the system, organised by what category of metadata they came from
- a user can then click on any of the pieces or search for them. On click the system:
  - loads info about the piece and displays it
  - also checks for whether it's in any user created playlists and displays that
- if the user is connected to the internet, further stuff happens:
  - the system polls the MuseScore API for a list of files and compares them against the previous list it fetched from the API. 
  - If there's any new ones, it downloads them, unzips them, parses them for data, chucks that in the SQL DB and then deletes the XML and MXL files to save space.

##Documentation
Currently the system is documented using github issues and the reports stored in Documentation. Most of these were for submission to my degree, but they give a good overview for new users and are pitched at a compsci level so that people without knowledge of music can learn a bit and understand it without prior knowledge of sheet music.
Once I have a bit of time to do more writing there will be a proper documentation site with instructions on setting up

##Infrastructure
- Language: Python 3.4.
- GUI: PyQt4, with pdfs done by poppler on Linux and Mac, default pdf viewer on windows.
- Rendering: [Lilypond](http://lilypond.org) via [MuseParse](http://github.com/godley/MuseParse)
- Input format: MusicXML
- Output Format for rendering: PDF via lilypond
- APIs used: [MuseScore](http://musescore.com) - keys are individual except for the release build which will use my API key. Please contact the musescore developers for a key if you need to debug anything network related.

##Installation
You can find the latest installer scripts for each platform by clicking [releases](https://github.com/Godley/Music-Library/releases). You will also need to install [Lilypond](http://lilypond.org).
