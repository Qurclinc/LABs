#!/bin/bash

echo "$( ps aux | tail -1 | awk '{print "The last PID is " $2 " and it got run at " $9}' )"
