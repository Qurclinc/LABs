#!/bin/bash

value=1
DELAY=1
CONST=2
OPERATION="+"

set_addition() {
    OPERATION="+"
}

set_multiplication() {
    OPERATION="*"
}

finish() {
    echo "Shutting down..."
    exit
}

trap set_addition USR1
trap set_multiplication USR2
trap finish SIGTERM

while true; do
    echo "$value"
    (( value = $value $OPERATION $CONST ))
    sleep "$DELAY"
done
