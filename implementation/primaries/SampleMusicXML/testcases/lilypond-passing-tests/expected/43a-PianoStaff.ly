\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{\autoBeamOff % measure 1
\clef treble  \time 4/4 f'1  | 

 }

ponestafftwo = \new Staff{\autoBeamOff % measure 1
\clef bass \time 4/4 b,1  | 

 }

<<\new StaffGroup \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }<<\ponestaffone
\ponestafftwo>>>>