echo "passes:"
find lilypond-passing-tests -type f | wc -l
echo "to-pass:"
find lilypond-provided-testcases -type f | wc -l
echo "ignored:"
find ignored-lilypond-testcases -type f | wc -l
