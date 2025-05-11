#!/bin/bash

SOURCE_LOCATION='../task1'
SCRIPT_NAME="task1.sh"
# SCRIPT="$SOURCE_LOCATION/$SCRIPT_NAME"
REPORT="$SOURCE_LOCATION/report"
echo "cd $SOURCE_LOCATION && ./$SCRIPT_NAME" | at now + 2 minute

tail -n 0 -f $REPORT
