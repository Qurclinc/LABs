#!/bin/bash

k=0

while true
do
    read number
    (( k++ ))
    if [[ $(( "$number" % 2 )) -eq 0 ]]; then
        break
    fi
done

echo "You've entered $k numbers."
