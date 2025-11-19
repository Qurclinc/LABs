#!/bin/bash

max=0

if [[ "$1" -ge "$2" ]]
    then if [[ "$1" -ge "$3" ]]
        then max=$1
    else
        if [[ "$3" -ge "$2" ]]
            then max=$3
        fi
    fi
elif [[ "$2" -ge "$1" ]]
    then if [[ "$2" -ge "$3" ]]
        then max="$2"
    else
        if [[ "$3" -ge "$1" ]]
            then max=$3
        fi
    fi
fi

echo "$max"
