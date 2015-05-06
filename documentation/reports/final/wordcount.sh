#!/bin/bash
VALUE="$(detex "Final Report.tex" | wc -w)"
APPEND="$(detex appendices.tex | wc -w)"
SUMMARY="$(detex summarytable.tex | wc -w)"
TOTAL=`expr $VALUE - $APPEND - $SUMMARY`
echo "${TOTAL}";
