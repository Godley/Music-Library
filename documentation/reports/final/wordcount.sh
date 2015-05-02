#!/bin/bash
VALUE="$(detex "Final Report.tex" | wc -w)"
APPEND="$(detex appendices.tex | wc -w)"
TOTAL=`expr $VALUE - $APPEND`
echo "${TOTAL}";
