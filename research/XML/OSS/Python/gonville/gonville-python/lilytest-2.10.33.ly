% Test Lilypond file which attempts to exercise every glyph defined
% in Gonville.
%
% To obtain a list of glyphs tested, process the LilyPond PS output
% through
%
%   perl -ne '/%%EndProlog/ and $ok=1; $ok and /\s\/([^\/\s]+)( glyphshow)?\s*$/ and print "$1\n"' | sort | uniq
%
% and compare that against the output of running the .sfd through
%
%   perl -ne '/^StartChar: (\S+)$/ and print "$1\n"' | sort | uniq
%
% Putting it together, here's a pre-cooked command that lists the
% glyphs _not_ tested by this file:
%
%   comm -13 <(perl -ne '/%%EndProlog/ and $ok=1; $ok and /\s\/([^\/\s]+)( glyphshow)?\s*$/ and print "$1\n"' lilytest.ps | sort | uniq) <(perl -ne '/^StartChar: (\S+)$/ and print "$1\n"' gonville-20.sfd | sort | uniq)

\version "2.10.33"

\layout {
  ragged-right = ##t
}

discant = \markup { \musicglyph #"accordion.accDiscant" }
bayanbase = \markup { \musicglyph #"accordion.accBayanbase" }
freebase = \markup { \musicglyph #"accordion.accFreebase" }
oldee = \markup { \musicglyph #"accordion.accOldEE" }
stdbase = \markup { \musicglyph #"accordion.accStdbase" }
dot = \markup {
  \musicglyph #"accordion.accDot"
}
acca = \markup {
  \combine
  \discant
  \combine
  \raise #0.5 \dot
  \combine
  \raise #1.5 \dot
  \combine
  \translate #'(1 . 0) \raise #1.5 \dot
  \combine
  \translate #'(-1 . 0) \raise #1.5 \dot
  \raise #2.5 \dot
}
accb = \markup {
  \combine
  \freebase
  \combine
  \raise #0.5 \dot
  \raise #1.5 \dot
}
accc = \markup {
  \combine
  \stdbase
  \combine
  \translate #'(-0.5 . 0) \raise #0.5 \dot
  \combine
  \translate #'(+0.5 . 0) \raise #0.5 \dot
  \combine
  \translate #'(-1.5 . 0) \raise #1.5 \dot
  \combine
  \translate #'(-0.5 . 0) \raise #1.5 \dot
  \combine
  \translate #'(+0.5 . 0) \raise #1.5 \dot
  \combine
  \translate #'(+1.5 . 0) \raise #1.5 \dot
  \combine
  \translate #'(-1.5 . 0) \raise #2.5 \dot
  \combine
  \translate #'(-0.5 . 0) \raise #2.5 \dot
  \combine
  \translate #'(+0.5 . 0) \raise #2.5 \dot
  \combine
  \translate #'(+1.5 . 0) \raise #2.5 \dot
  \combine
  \translate #'(-0.5 . 0) \raise #3.5 \dot
  \translate #'(+0.5 . 0) \raise #3.5 \dot
}
accd = \markup {
  \combine
  \bayanbase
  \combine
  \translate #'(-0.5 . 0) \raise #0.5 \dot
  \combine
  \translate #'(+0.5 . 0) \raise #0.5 \dot
  \combine
  \translate #'(-0.5 . 0) \raise #1.5 \dot
  \combine
  \translate #'(+0.5 . 0) \raise #1.5 \dot
  \combine
  \translate #'(-0.5 . 0) \raise #2.5 \dot
  \translate #'(+0.5 . 0) \raise #2.5 \dot
}

arra = \markup {
  \combine
  \musicglyph #"arrowheads.close.01"
  \combine
  \musicglyph #"arrowheads.close.11"
  \combine
  \musicglyph #"arrowheads.open.0M1"
  \musicglyph #"arrowheads.open.1M1"
}

arrb = \markup {
  \combine
  \musicglyph #"arrowheads.close.01"
  \combine
  \musicglyph #"arrowheads.open.11"
  \combine
  \musicglyph #"arrowheads.open.0M1"
  \musicglyph #"arrowheads.close.1M1"
}

arrc = \markup {
  \combine
  \musicglyph #"arrowheads.open.01"
  \combine
  \musicglyph #"arrowheads.close.11"
  \combine
  \musicglyph #"arrowheads.close.0M1"
  \musicglyph #"arrowheads.open.1M1"
}

arrd = \markup {
  \combine
  \musicglyph #"arrowheads.open.01"
  \combine
  \musicglyph #"arrowheads.open.11"
  \combine
  \musicglyph #"arrowheads.close.0M1"
  \musicglyph #"arrowheads.close.1M1"
}

ouroboros = #(make-dynamic-script "ffmfpfrfsfzmmpmrmsmz zpprpspzrrsrzsszzf")

frag = {
  \key e \major
  e16 fis gis a b4
  \set TabStaff.minimumFret = #7
  e16 fis gis a b4
  \set TabStaff.minimumFret = #0
  e16 fis gis a b4
  \set TabStaff.minimumFret = #7
  e16 fis gis a b4
  \set TabStaff.minimumFret = #0
  e1
  r1*2
}

\book {
  \score {
    \new ChoirStaff <<
      \time 4/4
      \new Staff {
        \set Score.skipBars = ##t
        \clef alto
        r1
        \time 3/4
        fes2^\fermata
        f'?4^\trill
        \time 15/64
        g'8^\shortfermata \noBeam
        ais'16 \noBeam
        b'32^\verylongfermata \noBeam
        c''64\noBeam
        \time 1/128
        r128
        \time 9/1
        r\maxima r1^\longfermata
        \time 2/2
        \clef treble
        << { r1 } \\ { d'4 e' d' e' } >>
        << { r2 r2 } \\ { e''4 f'' e'' f'' } >>
        e''8^\espressivo e''8 e''8^\segno e''8
          e''8^\coda e''8 e''8^\varcoda e''8
        R1*70
        \arpeggioUp <g c' e' g' c'' e'' g'' c'''>4 \arpeggio
          <d' g'\harmonic>4 \startTrillSpan
          a'4 \stopTrillSpan
          r4
        \repeat volta 3 {
          \set Score.repeatCommands = #'((volta "-1,+1"))
          a'4 b' c'' d''
          \set Score.repeatCommands = #'()
        }
        \alternative { {e''2 a'} {g'2 e'} }
        a'4 \breathe a'
          \override BreathingSign #'text = #(make-musicglyph-markup "scripts.rvarcomma") \breathe
          a'
          \override BreathingSign #'text = #(make-musicglyph-markup "scripts.lcomma") \breathe
          a'
        a'4
          \override BreathingSign #'text = #(make-musicglyph-markup "scripts.lvarcomma") \breathe
          a'
          \override BreathingSign #'text = #(make-musicglyph-markup "scripts.caesura") \breathe
          a' a'
        \improvisationOn a'4 a' a' a' \improvisationOff
        f''8.\noBeam f''16.\noBeam f''32.\noBeam f''64.\noBeam r128 r64 r8 r2
      }
      \new GrandStaff <<
        \new Staff {
          \override MultiMeasureRest #'expand-limit = 20
          \clef treble
          c''1
          r2^\fermata\sustainDown
          d''4\sustainUp
          \set Staff.pedalSustainStrings = #'("Pe" "d." "-")
          r8\sustainDown
          r16\sustainUp\sustainDown
          r32\sustainUp
          r64
          r128
          r\longa r\breve r1_\ouroboros r2
            \once \override Staff.Rest #'style = #'classical
    	r4 r4 r1^\longfermata
          \clef bass
          a,8_\lheel a,_\ltoe a,_\staccato a,_\tenuto
            a,8_\portato a,_\marcato a,_\marcato aisis,_\staccatissimo
          e8^\prallmordent e e^\prallup e
            e^\upprall e e^\lineprall eisih
          e8^\accent e^\flageolet e^\open e^\reverseturn
            e^\stopped e^\thumb e^\trill eih^\turn
          R1*70
          \arpeggioDown <c, e, g, c e g c'>4 \arpeggio
          r4 r2
          \repeat volta 3 { a,4^\acca b,^\accb c^\accc d^\accd }
          \alternative { {e2 a,} {g2 e} }
          e4 e e \stemDown \acciaccatura d8 \stemNeutral e4
          e4 e^\arra e e^\arrb
          \improvisationOn a2 a \improvisationOff
          r1
        }
        \new Staff {
          \override MultiMeasureRest #'expand-limit = 20
          \clef bass
          c1
          c2_\fermata
          r4
          ges,8_\shortfermata \noBeam
          f,16 \noBeam
          e,32_\verylongfermata \noBeam
          g,64\noBeam
          r128
          d\breve e\breve f\breve. g1 r1_\longfermata
          \clef alto
          e'8^\rheel e'^\rtoe e'^\staccato e'^\tenuto
            e'8^\portato e'^\flageolet e'^\marcato eeses'^\staccatissimo
          e'8^\downbow e'^\upbow e'^\prall e'
            e'^\mordent e' e'^\prallprall eeseh'
          e'8^\pralldown e' e'^\downprall e'
            e'^\upmordent e' e'^\downmordent eeh'
          R1*70
          <c e g c' e' g' c''>4 \arpeggio
          r4 r2
          \repeat volta 3 { a4^\oldee b c' d' }
          \alternative { {e'2 a} {g2 e} }
          a4 a a \acciaccatura d8 a4
          a4 a^\arrc a a^\arrd
          \improvisationOn c'1 \improvisationOff
          f8.\noBeam f16.\noBeam f32.\noBeam f64.\noBeam r128 r64 r8 r2
        }
      >>
    >>
    \layout {}
  }
  \score {
    \new StaffGroup <<
      \new Staff { \clef "G_8" \frag }
      \new TabStaff { \frag }
      \new DrumStaff {
        \drummode {
          bd4 sn8 bd8 r8 bd8 sn16 bd8.
          \stemUp cyms8 cyms8 \stemNeutral cyms4 cyms2 cyms1
          \stemUp cb8 cb8 \stemNeutral cb4 cb2 cb1
          \stemUp hh8 hh8 \stemNeutral hh4 hh2 hh1
          \stemUp hhho8 hhho8 \stemNeutral hhho4 hhho2 hhho1
        }
      }
    >>
  }
}
