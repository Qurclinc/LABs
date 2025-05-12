#!/bin/bash

HANDLER_NAME="handler.sh"

get_PID() {
    echo $( pgrep "$HANDLER_NAME" | awk 'NR==1' )
}


while true; do
    read -r LINE
    if [[ "$LINE" == "+" ]]; then
        kill -USR1 $( get_PID )
    elif [[ "$LINE" == "*" ]]; then
        kill -USR2 $( get_PID )
    elif [[ "$LINE" == "TERM" ]]; then
        kill -SIGTERM $( get_PID )
    fi
done
