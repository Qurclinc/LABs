#!/bin/bash

DATA_FILE="data.txt"
PROCCESS_NAME="handler.sh"

rm -f "$DATA_FILE"


while true;
do
    read -r LINE
    if [[ "$LINE" == "TERM" ]]; then
        PID=$( pgrep "$PROCCESS_NAME" | awk 'NR==2' )
        kill -SIGTERM "$PID"
    fi
    echo "$LINE" >> "$DATA_FILE"
done
