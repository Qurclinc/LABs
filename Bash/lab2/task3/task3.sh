#!/bin/bash

destination="$PWD/emails.lst"
ROOT_DIR="/etc/"
PATTERN="<.*@\w*\.\w*>" 
ALL_EMAILS=()
grep -RiE "$PATTERN" "$ROOT_DIR" 2>/dev/null 1>tmp
while IFS= read -r line; do
    email=$( echo "$line" | grep -o -E "<[^>]+>")
    ALL_EMAILS+=("$email")
done < tmp
rm -f tmp
unique_emails=$(echo "${ALL_EMAILS[@]}" | tr ' ' '\n' | sort -u ) 

echo "$unique_emails" 1>/"$destination"
