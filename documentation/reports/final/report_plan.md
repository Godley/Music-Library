# Introduction: 1500 words
- discuss sheet music
   - make sure to highlight SHEET aka, the written format, not audio
   - discuss the importance and usage of sheet music
   - discuss complexity of notation

- go on to discuss musicians and storage of music
   - music cabinets for personal use
   - orchestral problems: larger numbers of scores, larger number of instruments, harder to find matches
   - for both use the use cases which are in my pres
   - discuss problem of finding music which is of the appropriate difficulty, key, style from online and offline stores


- discuss current digital methods briefly
	 - some software uses bibliography and will automatically organise by this, with the option to manually add further info
	 - most will just let the user do it all manually
	 - link back to orchestral problems: big orchestras have big libraries of music, big online stores again have the same problem

explain proposed solution in brief and what the report will contain

# Aim and Objectives
copy aim from previous report

## Primary objectives
  - explain drawing objective: necessary to have some method of rendering so that it allows users to use the app effectively/in exclusion from others etc.
  - explain metadata objective: be clear on why auto extraction is important.
  - Also mention ability to search, that the system allows for both self created playlists and auto generated ones
  - explain importing online sources, and mention how copyright was/is an important thing to consider in this section

## Secondary objectives
- identify which have been included and why any that haven’t been included haven’t
- discuss MIDI/sound output and why it’s useful
- discuss difficulty rating on both a generic level (i.e lots of short rhythms/ink = hard) and an instrument level (e.g trumpet with music moving about by leaps = hard because of the instrument) and why it’s useful to include one or both
- musicOCR: easiest way to combine digitised collections with offline collections. Will be necessary for a lot of use cases because of the problem discussed with large collections of scores - as we need to know the meta data, not just have a flat file, for the system to work fully it will be necessary for users to either import using this method or recreate the files manually. 


# Background
## Problem context
  - discuss music notation in depth (staff notation, pitches, clefs, meters, tempos): maybe also discuss rhythms and accents to explain the difficulty rating portion of the secondary objectives - sort of depends if this gets implemented in time
  - discuss the area of Music Information Retrieval and the “Multifacetted” problem - i.e that music has a lot of different areas it can be categorised by. Also point out that while a lot of systems (use examples) have tried to do music categorisation, the easiest way to do it with integration to images is simple bibliography, but with this system it should be possible to extract and search by everything. Also explain that meta data models are not often discussed because different researchers need different models and none of them have been published (back this up with references).
  - Potentially also discuss the musicology aspects that could be implemented, but perhaps this could go in the appendix (i.e that music researchers sometimes want to search by a particular melody or chord progression, but that this is difficult to search with current methods because text input is harder to cover the same info) - maybe just briefly mention that area of music software but that the current implementation won’t cover it?

##Comparison of technologies
### programming language
    - c++
      - cross platform
      - low developer knowledge
      - memory management means a slower development time
      - harder for musicians to understand should any wish to contribute to the project once open sourced
    - C#
      - Microsoft implementation is currently not cross platform: being open sourced within the next few months, but announcement was made during the course of this project’s development
      - Mono implementation cross platform and fully featured (reference), but developer knowledge on using Mono is low
      - statically typed for the most part: means longer dev time as duck typing is not the standard
      - due to Microsoft implementation being not cross platform not highly used in open source

    - Python
      - cross platform
      - higher developer knowledge
      - dynamically typed: enables duck typing, but could also make the code harder to follow/some other pythonic features might make it less organised (access to class variables etc)
      - of the languages discussed, stats for open source projects are high
      - syntax is closest to english: means musicians are more likely to be able to read and contribute to project

  - Python 2.7 vs python 3
      - python 3 is the Foundation’s preferred and should therefore be adhered to if poss
      - a lot of projects haven’t updated to python 3 due to the lack of backward compatibility: this caused some problems (e.g installing certain graphics libraries, using some elements of lilypond book) and had the developer needed more libs might have caused regression to 2.7

### file format
    - mention lack of standardisation problems: whilst MusicXML will be selected and is used by most applications, handling for input and output has no set libraries or algorithms because every project has used their own methods (references). 
    Options:
    - discuss own format
      - upsides:
        - makes the files precisely relevant to this project
      - downsides:
        - this software doesn’t create music: would mean that the format would need to be well standardised/create importers from other formats to this format/get it integrated with current composition software
        - not great for integration into what’s currently available

    - discuss sib vs muscx
      - upside
        - either would make the software compatible with one of the most well used composition software packages
      - downsides
        - either would also couple the software with that package
        - muscx is OSS and probably easy to see how MuseScore uses it, but will be oriented toward what MuseScore wanted from the format
        - Sibelius is closed, and therefore sib format won’t be easy to apply. Might also cause copyright issues (need to research confirm that point
    - discuss MusicXML
      - upside
        - open format
        - integrated into both Sibelius and MuseScore, as well as Finale and a few other programs
        - aligning with an open format will make this project a better renderer of musicXML: give example that musescore uses its own format and allows importing and exporting to xml, but has issues (reference)
      - downside
        - not necessarily aligned directly with this project’s aims, meaining technical challenge to understand and implement with no ability to change the format.
        - designed by a third party (MakeMusic who made Finale) so probably a lot of different design goals oriented toward their software: it would be better if there were a file format which was created by an independent organisation or institute with the goals of all musicians in mind, but musicXML seems to be the closest alternate. (ref)

## comparison of algorithms for rendering
### XML to memory
      - discuss objects: why do we need them? conversion from input to output formats would be O(nsquared) - conversion from a loaded object would be O(n). also discuss coupling of 1 format to another format, which is a bad thing
      - also discuss XSL for rendering the xml file and why it can’t be used
      - discuss parsing options: SAX or DOM
        - DOM loads all the info: bad because we might not need all the info
        - SAX does it tag by tag: solves the problem
      - parsing options: Verifying or non-verifying
        - explain why this is an issue: verifying means that the user will always have to be online for the parser to work. 
        - non-verifying on the other hand means that the system might have a problem if the xml file provided isn’t valid XML.
        - verifying also makes it very slow: use non-verifying and cross fingers
### memory to output
    - mention music rendering by computers has existed for a long time, tho often using just images and that there’s various researchers (lilypond, abc, musitex) who’ve tried to make a good algorithm that covers all bases. With that in mind:
    - create own output algorithm using fonts
      - optimised for own means, rather than someone else’s
      - time consuming, not what this project is actually about
      - stupid because of the large body of research
      - zooming/panning problems
    - create own algorithm using image, then view the image in the GUI
      - above points, minus zooming/panning problems
      - create a formatted lilypond output
      - discuss lilypond as a project
      - not reinventing the wheel: has a lot of people working on it and is cross platform
      - used by several other projects (reference)
      - output/connections to lilypond would be easier to debug than if I were debugging my own algorithm: just output a string of lilypond output which is then processed by the eco system
      - adds complexity because needed to learn how to write lilypond output 


## Algorithms and structures for meta scanning
- diagram of system metadata view
### discuss meta model
  - collect data in a general sense - time sig, meter, clef, key, instruments, transposition, bibliography
    - upsides
      - provides data that’s useful to every type of musician reading
      - reasonable set of variation
      - allows for a wide range of searches, including allowing for subbing instrument name in for their transposition and matching pieces which won’t have a contrabass clarinet in, for example
    - downsides
      - no specifics: some musicians will want to know things like “does it contain arpeggios” in case their instruments make it more difficult to paly things that move around
      - some users like musicologists may want chord progressions so they can use it for analysis: this project focusses on being a library, not a musicology tool.
      - difficulty analysis would need to extend this to include note durations and patterns, as well as applying some semantics to the model (e.g if speed > 180 && lots of demi-semi quavers = hard)
  - collect data with specifics, and make the parser apply the instrument name as to whether to collect certain data
      - upsides
        - more precision of searching and more data collected that’s liable to be useful to the user
      - downsides
        - more technical challenge which may adversely affect the development time
        - some pieces spell different instrument names differently, like german pieces will say klarinette etc have to accomodate for that

### XML considerations
non-parsing, sax. discuss why but in 1 paragraph or so

### meta storage
  - data -> inmemory object <-> serialized file
    - upsides
      - scanner only runs once per file as memory is serialized
      - quick to develop, only uses 1 library to dump the file
    - downsides
      - sorting and searching algorithms and design of memory object are probably reinventing the wheel since this project is aiming to USE, not improve data storage
      - serialization of memory object couples the project and any extensions with python as they will need to use python to get the memory object back
  - data <-> database
    - upsides
      - database structures have been worked on by a lot of contributors (ref)
      - created to optimise searching and sorting for large amounts of data, use a B tree to store the data and are therefore probably faster than a memory object created by a singular developer (ref)
      - no coupling to python: most languages have built in libraries for the most popular databases (refs)
    - downsides
      - technical challenge learning DB libraries
      - longer design process making the table structure/management object

### Query Processing considerations
in some way will be necessary to take a string input and use it to query a database. this needs some form of structure, but also needs to be simple enough to be easy to learn for non-technical users.
  - option 1: create a new querying syntax and provide instructions
    - upsides
      - allows for a lot of complexity
      - doesn’t require as much processing
    - downsides
      - not very intuitive
      - slower user uptake if there’s a lot of commands
      - some searches don’t need the complexity this provides
  - option 2: allow users to use a querying syntax, but also do some language processing to “guess” what the user wants
    - upsides
      - simplicity: users can type in “blabla” and get back “blabla” composed this, is the title of this etc without needing to type more than the query itself.
      - ease of use because of the simplicity
      - can be extended and still allows for the complexity
    - downsides
      - more processing
      - guesswork might not always be right/might search the wrong field
      
  - querying using a GUI - i.e drawing on a staff

### Playlist considerations not sure there are any?


## Technologies for importing online sources
  - system should talk to at least one source, allow the user to browse that source in the same way as they browse their local files, and when they select a file which is online, download the file and add the meta info to the local DB.

### Sources
  - system should be extendable if new sources are found/want to be included. avoid coupling to 1 or more APIs using 	a manager class.
  - MuseScore Online: music created using MuseScore
    - not all music is public domain - created by other musicians who used the software. Each file on the DB does have this info tho, but it needed to be handled properly
    - all music provided in MXL, XML and PDF format: means the XML format doesn’t have to be rendered to be viewed, will speed up algorithm once downloaded
    - API provides a lot of bibliography info at JSON output level - means system doesn’t have to go to the XML file to extract the info, which again speeds up the connection

### algorithm for connecting
  - option 1: search only by bibliography and connect each time the user inputs data
    - upside
      - easy to implement
    - downside
      - repeated connection to internet
      - slow: internet
      - no advanced searching
  - option 2: download all files by a certain license, extract bibliography from api response, scan each file for metadata and delete the files after each scan
    - upside
      - data is the same quality and quantity as local files and can be searched in the same manner
      - connection to internet + to server only required on program open
    - downside
      - bigger overhead due to scanning all the files
      - might be a memory consideration if they’re all downloaded in 1 go and the user doesn’t have enough space

### Licensing
  - MuseScore has a variety of pieces which users have attributed different licenses.
  - option 1: only scan pieces by the most open license (creative commons/no license)
    - upside
      - no need to consider licensing whatsoever
    - downside
      - smaller input set
  - option 2: scan pieces for all licenses, but present a popup with the terms and considerations on download
    - upside
      - licensing covered
      - larger input set
    - downside
      - all rights reserved licensing? 

##Secondary objectives
###sound output					
  - The sound output algorithm must, for a given part or selection of parts, output the sheet music to a MIDI or MP3 file, which can then be played within the program.
					
  - It has been decided that each class in the solution will have a method to produce this output, in the same way as the algorithm described for rendering in section 3.3.4, which will be combined into an output file and played.
					
  - This creates an extendible architecture, as it would easily be possible to create output methods to other formats in the future. 

### image input
  - create own OCR algorithm
    - optimised to own needs
    - organised in way relating to project
    - not necessary: this project is not about OCR
  - use another program
    - other program dedicated to OCR may not have same design goals
    - however, OMR/OCR is a huge area and it would be impossible to create my own in a year (give scope using references)
    - use Audiveris instead
  - not implemented: why?

### Difficulty rating
  - useful to beginners/advanced players so they know how much time/energy will be needed to commit to learnign the piece
  - hard because can be specific to each instrument
  - mention feedback from other musicians
  - easy level: implement rating based on what all musicians consider hard
  - hard: implement rating based on instrument

## Alternative solutions
  - discuss each of the packages in interim report in more detail
  - perhaps do indepth analysis of the package closest to this project
  - mention that none are cross platform/provide all features for all platforms (depending on whether this project achieves full cross platform compatibility)


# Technical Development 
## UI design: 
	- discuss initial designs: influences
	- discuss changes based on user input

## Test design and system testing: 
	- discuss TDD implementation
	- discuss testcase creation (initial)
	- also discuss discovery of Lilypond-provided musicXML testcases 
	- decisions made over which to prioritise
	- decisions made over when to stop working on particular areas of notation
	- mention decision to ensure primary objectives work in small units and then as a whole, and also the intention to perfect the primary objectives before anything else is worked upon
	- include a sample testcase in appendix

## System design:
	- diagram for each objective’s system design (flow diagram)
	- diagram of how they fit together
	- class diagrams (tho some may need to be in appendix) particularly relating to each objective as a whole
	discussion of changes made through the course of development, e.g when particular features/problems found 	what changes had to be made to the design/how designs affected development
	- move this to designs: discuss problems that this project uses 2 formats (MXML and Lilypond) and both have 	their own idea of how to represent music: MXML is visual, Lilypond is like writing actual instructions which 		output to a visual. This means the object model had to be organised in a way which suits both ecosystems - 	whilst it’s not coupled to either, this made some elements of dev difficult, and without knowing either format 	well before the start of the project these elements weren’t known to the developer so caused some restructuring 		during development. May have been countered by more research, but not enough time. 
	- also discuss point that this system is designed around those files, whilst other packages don’t always 	handle it perfectly.
	- Also mention that some elements of music have been left out because this project is not about rendering, and it’s important to have a renderer which does the majority, but due to the time in which to complete the project getting absolutely every symbol in would have been unfeasible.

## System Implementation: 
	- discuss use of github issues and how development process changed over time - i.e no real process to TDD to 	- TDD with issues per feature being implemented
	- phrase it as realised scale of implementation and testing affected this, so needed to change process from 	dev and then testing to testing throughout
	- discuss meta data model and lack of standardisation: picked model based on personal preference with some 	input from other people + research, but no standard so had to create own
	- explain why that is - musicians aren’t always software devs
	- also highlight music is a big research area but there’s no standard for input->memory->output, so 	algorithm is sort of new and hopefully being open source will help new standards being created
	- mention difficulty rating has not been done in other apps in particular, so research had to be done into 	how people rank music

# Evaluation
## Project Achievements:
	- identify which objectives have been met and to what level

## Further work: 
	- mention issue reporting on improvements to rendering/issue reporting on notation which is completely 			- ignored: explain how decisions were made on to what limit to draw on notation
	- discuss problems with not knowing lilypond/musicXML enough to know a precise structure which would suit 	both
	- discuss any objectives which were not met

## Future developments
### porting to more platforms:
	- raspberry pi: input from PiPiano, output to SonicPi: both would serve as great educational tools for teaching kids to read music, teaching to code music and about MIDI input etc
	- linux/windows? depends on whether this has been achieved already

### musicology analysis
	- improve search to allow for searching by a passage of notes
	- optional symbols
	- ability to select how much notation is rendered, e.g ignore accidentals, accents, dynamics: would again 	suit educational purposes as a lot of notation can mean a lot more to take in when learning to read sheet music

# Reflection
	- personal reflection on project management/process etc

# Conclusion
	- discuss project in context of aims
	- discuss why aims are important in context of software in existance
	- discuss how project will/has improved standards/digitisation of music

Each appendix should have a title

References
Harris, M. B., 1974. Accelerating Dissertation Writing: Case Study. Psychological Reports, 34(3), pp. 984-986.
Holtom, D. & Fisher, E., 1999. Enjoy Writing Your Science Thesis or Dissertation. 1st ed. London: Imperial College Press.
Parker, D., 2013. Referencing with Word. [Online]
Available at: http://intra.net.dcs.hull.ac.uk/student/modules/08341/WebPages/ReferencingWithWord.html
[Accessed 18 September 2014].
University of Hull Skills Team, 2014. What is referencing and how do you do it?. [Online]
Available at: http://www2.hull.ac.uk/lli/skills-development/referencing/introduction_to_referencing.aspx
[Accessed 19 September 2014].


