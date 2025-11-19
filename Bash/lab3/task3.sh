#!/bin/bash

#for line in $( ps aux | grep "/sbin" ); do
#    echo "$line"
#done

ps aux | grep "/sbin" | while read -r line; do
    if [[ -n $( echo "$line" | awk '{print $11}' | grep -E "^/sbin" ) ]]; then
        echo "$line" | awk '{print $2}'
    fi
done
