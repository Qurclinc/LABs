#!/bin/bash

REPORT_FILE="report.log"

ls /proc | grep -E "^[0-9]*$" | sort -n | while read -r PID; do
    Parent_PID=$( cat "/proc/$PID/status" 2>/dev/null | grep "PPid" | awk -F: '{print $2}' | xargs)
    if [[ -n $Parent_PID ]]; then
        avg_time=$( cat "/proc/$PID/sched" | grep "se.avg.util_avg" | awk -F: '{print $2}' | xargs)
        echo "$PID $Parent_PID $avg_time" 
    fi
done | sort -k2,2n | awk '{print "ProcessID="$1 ": Parent_ProcessID="$2 ": Average_Time="$3}' > "$REPORT_FILE"
