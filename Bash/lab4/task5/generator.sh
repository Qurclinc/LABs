#!/bin/bash

DATA_FILE="data.txt"
rm -f $DATA_FILE

while true; do
    read -r LINE
    echo "$LINE" >> "$DATA_FILE"
done
