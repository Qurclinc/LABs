#!/bin/bash

LOCATION="$PWD/../task1/task1.sh"
COMMAND="/bin/bash -c $LOCATION"
result=$(crontab -l | grep "$COMMAND")

if [[ -z $result ]]; then
    ( crontab -l; echo "* * * * * /bin/bash -c $LOCATION") | crontab -
fi
