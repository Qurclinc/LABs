#!/bin/bash

DATA_FILE="data.txt"
touch "$DATA_FILE"

finish() {
    echo "Other proccess has just killed me with SIGTERM signal"
    killall tail
    exit
}


tail -n 0 -f "$DATA_FILE" | while true;
do
    trap finish SIGTERM
    read -r LINE
    echo "$LINE"
done 

#while true; do
#    sleep 1
#done
