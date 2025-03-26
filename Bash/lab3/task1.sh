#!/bin/bash

if [[ -z $1 ]]; then
    echo "You must defer user!"
    exit 1
fi

USER="$1"
ps aux | grep "$USER" | awk '{print $2 ":" $11}' | head -n-4
