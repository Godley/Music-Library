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
\clef treble \key c \major \time 3/4 \tuplet 3/2 {b'4 b'4  b'4} r4  | 

 % measure 2
b'4( b'4 b'4)  | 

 % measure 3
b'4( b'4 b'4)  | 

 % measure 4
b'4\< b'4\! b'4  | 

 % measure 5
b'4\> b'4\! b'4  | 

 % measure 6
b'4\trill\startTrillSpan
 b'4 b'4\stopTrillSpan
  | 

 % measure 7
b'4\startTrillSpan
\stopTrillSpan
 r2  | 

 % measure 8

\ottava #1
 b''4 b''4 b''4
\ottava #0  | 

 % measure 9

\ottava #-2
 b,4 b,4 b,4
\ottava #0  | 

 % measure 10
\override TextSpanner.dash-fraction = 1.0 
b'4
\startTextSpan
 b'4 b'4 
\stopTextSpan
 | 

 % measure 11
\override TextSpanner.dash-fraction = 0.5 
b'4
\startTextSpan
 b'4 b'4 
\stopTextSpan
 | 

 % measure 12
\override TextSpanner.dash-fraction = 1.0 
b'4
\startTextSpan
 b'4 b'4 
\stopTextSpan
 | 

 % measure 13
\override TextSpanner.dash-fraction = 0.5 
b'4
\startTextSpan
 b'4 b'4 
\stopTextSpan
 | 

 % measure 14
\override TextSpanner.dash-fraction = 1.0 
b'4
\startTextSpan
 b'4 b'4 
\stopTextSpan
 | 

 % measure 15
b'4 b'4 b'4  | 

 % measure 16
\override Glissando.style = #'zigzag b'4\glissando f''4 r4  | 

 % measure 17
b'4\bendAfter #+6 c''4\bendAfter #0 r4  | 

 % measure 18
b'4\glissando c'4 r4  | 

 % measure 19
b'4 b'4 b'4  | 

 % measure 20
\repeat tremolo 4 b'16 \repeat tremolo 4 b'16 r4  | 

 % measure 21
b'4 b'4 r4  | 

 % measure 22
b'4 b'4 r4  | 

 % measure 23
b'4\sustainOn
 b'4\sustainOff\sustainOn
 b'4\sustainOff
  \bar "|."

 }

<<\ponestaffone>>