#!/bin/bash

function grep_info() {
    echo "$1" | grep "$2" 
}

source="/var/log/Xorg.0.log"
destination="full.log"

header=$(head -12 "$source")
source_text=$(tail -n +13 "$source") # Skipping header (first 11 lines)
source_text=${source_text//"WW"/"Warning"}
source_text==${source_text//"II"/"Information"}
info_logs=$(grep_info "$source_text" "Information")
warning_logs=$(grep_info "$source_text", "Warning")
other_logs=$(echo "$source_text" | grep -v -E "Information|Warning")
echo "$header$info_logs$warning_logs$other_logs">"$destination"
