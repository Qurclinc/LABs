#!/bin/bash

logfile="$PWD/errors.log"
ROOT_DIR="/var/log"

rm -f $"logfile"
# grep -Ri "acpi" "$ROOT_DIR" 2>/dev/null 1>"$logfile"
for filename in $( find /var/log -type f 2>/dev/null ); do
    cat $filename 2>/dev/null | grep ACPI | awk '! /^\/.*\/.*/' >> "$logfile"
    cat $filename 2>/dev/null | grep ACPI | awk '/^\/.*\/.*/'
done


