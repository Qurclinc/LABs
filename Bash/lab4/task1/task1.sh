#!/bin/bash

CWD=$PWD # Should be equal to $HOME
DATE=$(date +"%Y-%m-%d %H:%M:%S")
# RHOST=127.0.0.1
RHOST=10.10.11.58
RHOST="www.net_nikogo.ru"
# ERROR_MESSAGE="Error: Unable to ping host $RHOST"
mkdir "$CWD/test" && { echo "catalog test was created successfully" > "$CWD"/report && touch "$CWD/test/$DATE"; }; ping "$RHOST" -c 1 -t 1 2>>"$CWD/report"  # || echo "$ERROR_MESSAGE" >> "$CWD/report"

at
