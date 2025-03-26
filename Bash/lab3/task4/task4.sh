#!/bin/bash

SAVEFILE=PID_subtractions_log
ls /proc | grep -E "^[0-9]*$" | sort -n | while read -r PID; do
    subtraction=$( cat "/proc/$PID/statm" 2>/dev/null | awk '{print $2-$3}' )
    if [[ -n $subtraction ]]; then
        echo "$PID:$subtraction"
    fi
done | sort -t: -k2,2nr -k1,1n > $SAVEFILE 
