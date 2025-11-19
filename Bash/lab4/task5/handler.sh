#!/bin/bash

DATA_FILE="data.txt"
touch "$DATA_FILE"
a=1
flag=true
operation="+"

tail -n 0 -f "$DATA_FILE" | while read -r LINE; do
    case $LINE in
        QUIT)
            echo "exit"
            killall tail
            exit
            ;;
        [0-9]*)
            if [[ "$operation" == "+" ]]; then
                (( a += $LINE ))
            elif [[ "$operation" == "*" ]]; then
                (( a *= $LINE ))
            fi
            echo "$a"
            ;;
        "+")
            operation="+"
            ;;
        "*")
            operation="*"
            ;;
        *)
            echo "Non-numeric text!"
            ;;
    esac
done
