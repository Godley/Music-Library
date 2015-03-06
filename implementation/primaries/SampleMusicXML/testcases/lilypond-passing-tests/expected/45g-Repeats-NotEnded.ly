\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{\autoBeamOff % measure 1
\clef treble \key c \major \time 4/4 c''1  | 

 % measure 2
 \bar ".|:"c''1  \bar "|."

 }

<<\ponestaffone>>