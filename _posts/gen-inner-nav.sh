#! /usr/bin/bash
# Generate inner-nav for all headings of each md file with front matter

shopt -s globstar
for target in **/*.md
do
    echo "Working on ${target}"
    cp "${target}" "${target}.tmp"
    python3 md_h_to_liq.py < "${target}" > "${target}.out"
done
shopt -u globstar