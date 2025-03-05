#!/bin/bash

exec 2>/dev/null

k=0
FILEPATH="/var/log"
for file in $( find "$FILEPATH" -name *.log -type f 2>/dev/null ); do
    (( k+=$( wc -l "$file" 2>/dev/null | awk '{print $1}') ))
done

echo "$k"
