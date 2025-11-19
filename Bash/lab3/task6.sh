#!/bin/bash

get_data() {
    echo "$1" | awk -F: -v col=$2 '{print $col}' | awk -F= '{print $2}' | awk -F: '{print $1}'
}

FILEPATH="$PWD/task5/report.log"
sum=0
count=0
prev=""
while read -r line; do
    ppid=$( get_data "$line" 2 )
    timer=$( get_data "$line" 3 )
    
    if [[ -z "$prev" ]]; then
        prev=$ppid
        sum=$timer
        count=1

    elif [[ $ppid -eq $prev ]]; then
        (( sum+=timer ))
        (( count++ ))
    else
        avg=$(( sum/count ))
        echo "Average_Sleeping_Children_of_ParentID=$prev is $avg"
        prev=$ppid
        sum=$timer
        count=1
    fi
    echo "$line"
done < "$FILEPATH"

if [[ $count -gt 0 ]]; then
    avg=$((sum / count))
    echo "Average_Sleeping_Children_of_ParentID=$prev is $avg"
fi



