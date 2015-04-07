\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Voice" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key a \major \time 2/2 cis'4 cis'4 cis'4 cis'4  | 

 }


\header {
title = "Compressed MusicXML file"
tagline = "Public Domain "
}<<\ponestaffone>>