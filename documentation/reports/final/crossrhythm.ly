
\version "2.18.2"  % necessary for upgrading to future LilyPond versions.
\header{
tagline=""
}

upper = \relative c'' {

  a4 d4
}

lower = \relative c {
  \clef bass
  \tuplet 3/2 {a8 c d}
}

\score {
  \new PianoStaff <<
    \set PianoStaff.instrumentName = #"Piano  "
    \new Staff = "upper" \upper
    \new Staff = "lower" \lower
  >>
  \layout { }
  \midi { }
}
