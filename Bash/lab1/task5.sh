#!/bin/bash

print_menu() {
    clear
    echo "1) Run nano"
    echo "2) Run vi"
    echo "3) Run browser 'links'"
    echo "0) exit"
}

input=-1
while true; do
    print_menu
    read input
    if [[ "$input" -eq 0  ]]; then 
        break
    elif [[ "$input" -eq 1 ]]; then
        nano 
    elif [[ "$input" -eq 2 ]]; then 
        vi
    elif [[ "$input" -eq 3 ]]; then
        links
    else
        echo "No such command!"
    fi
done

