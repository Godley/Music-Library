\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 




 } 
shortInstrumentName = \markup { 




 } 
 }{\autoBeamOff % measure 1
c'1  | 

 % measure 2
\break c'1  | 

 }

ptwostaffone = \new Staff \with {
instrumentName = \markup { 




 } 
shortInstrumentName = \markup { 




 } 
 }{\autoBeamOff % measure 1
c'1  | 

 % measure 2
\break c'1  | 

 }

<<\ponestaffone\ptwostaffone>>