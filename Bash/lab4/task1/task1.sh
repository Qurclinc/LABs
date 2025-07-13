#!/bin/bash

CWD="$HOME/Desktop/LABs/Bash/lab4/task1" # Should be equal to your own work directory
DATE=$(date +"%Y-%m-%d %H:%M:%S")
RHOST="www.net_nikogo.ru"
mkdir "$CWD/test" && { echo "catalog test was created successfully" >> "$CWD"/report && touch "$CWD/test/$DATE"; }; ping "$RHOST" -c 1 -t 1 2>>"$CWD/report"  # || echo "$ERROR_MESSAGE" >> "$CWD/report"
