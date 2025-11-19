#!/bin/bash

/bin/bash -c ./proc1.sh & /bin/bash -c ./proc2.sh &

PID=$( ps aux | grep "[p]roc1.sh" | awk '{print $2}' )
cpulimit -p $PID -l 20
