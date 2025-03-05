#!/bin/bash

exec 2>/dev/null

# man bash | head -100 1>tmp

man bash 1>tmp

declare -A words

while IFS= read -r line; do
    for word in $( echo "$line" | awk '{for(i=1; i<=NF; i++) {gsub("[^a-zA-Zа-яА-ЯёЁ0-9]", "", $i); print $i }}' ); do
        if [[ ${#word} -gt 3 ]]; then
            (( words["$word"]++ ))
         fi 
        # echo "${words["$word"]}"
    done
done < tmp

rm tmp

count=3
for key in $(for k in "${!words[@]}"; do echo "${words[$k]} $k"; done | sort -rn | awk '{print $2}'); do
    if [[ "$count" -eq 0 ]]; then 
        break
    fi
    echo "$key ${words[$key]}"
    (( count-- ))
done



