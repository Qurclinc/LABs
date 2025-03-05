#!/bin/bash

declare -A dict
grep -RE '^#!' /bin 2>/dev/null 1>tmp
while IFS= read -r line; do
    key=$( echo "$line" | awk -F:#! '{split($2, arr, " "); print arr[1]'} )
    if [[ ! -v "${dict[$key]}" ]]; then
        (( dict[$key]++ ))
    fi
done < tmp
rm -f tmp

max_key=""
max_value=0
for key in "${!dict[@]}"; do
    if [[ "${dict[$key]}" -gt "$max_value" ]]; then
        max_key="$key"
        max_value="${dict[$key]}"
    fi    
done
echo "$max_key"
#echo "$( grep -R "$max_key" /bin 2>/dev/null | head -1 | awk -F: '{print $1}' )"
