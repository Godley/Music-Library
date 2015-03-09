\version "2.18.2"
\header {
  tagline = ""
}
\paper {
  #(set-paper-size "letter")
  top-margin = 0.7\cm
}
emptymusic = {
  \repeat unfold 1 % Change this for more lines.
  { s1\break }
}
\layout { 
  indent = 0.0\cm
  pagenumber = no
}
\new Score \with {
  \override TimeSignature #'transparent = ##t
  \override Clef #'transparent = ##t
  \remove Clef_engraver
} <<
  \context Staff \emptymusic
>>