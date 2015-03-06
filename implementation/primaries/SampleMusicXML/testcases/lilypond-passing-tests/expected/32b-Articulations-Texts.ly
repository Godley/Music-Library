\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{\autoBeamOff % measure 1
\clef treble  \time 4/4 f'8 ^\markup { \medium "						Normal, Medium					"  } _\markup { \medium "						Bold, Medium					"  }  | 

 % measure 2
g'1 ^\markup { \large "						Normal, Large					"  } _\markup { \large "						Bold, Large					"  }  | 

 % measure 3
f'1 ^\markup { \small "						Normal, Small					"  } _\markup { \small "                                    Bold, Small"  } _\markup { \small "                                    Normal, Small, Colored, Below"  }  | 

 }

<<\ponestaffone>>