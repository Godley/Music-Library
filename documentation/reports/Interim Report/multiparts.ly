\header {
tagline = ""
}
<<
  \new Staff \with {
    instrumentName = #"Flute"
  }
  { f2 g4 f }
  \new Staff \with {
    instrumentName = \markup {
      \center-column { "Clarinet"
        \line { "in B" \smaller \flat }
      }
    }
  }
  { c4 b c2 }
>>
\version "2.18.2"  % necessary for upgrading to future LilyPond versions.
