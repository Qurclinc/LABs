#!/bin/bash

string=""
res=""

while true 
do
    read string
    if [[ "$string" == "q" ]]
        then break
    fi
    if [[ -n "$res" ]]; then
        res="$res $string"
    else 
        res="$string"
    fi
done

echo "$res"
