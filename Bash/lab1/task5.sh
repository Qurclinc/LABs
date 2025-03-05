#!/bin/bash

print_menu() {
    echo "1) Run nano"
    echo "2) Run vi"
    echo "3) Run browser 'links'"
    echo "0) exit"
}

input=-1
while [[ "$input" -ne 0 ]]; do
    print_menu()
    if [[ "$input" -eq 1 ]]; then
        nano .
    fi
done
