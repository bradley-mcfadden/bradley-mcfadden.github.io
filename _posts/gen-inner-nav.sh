#! /usr/bin/bash
# Generate inner-nav for all headings of each md file with front matter

shopt -s globstar
for target in **/*.md
do
    echo "Working on ${target}"
    cp "${target}" "_bak/${target}"
    python3 md_h_to_liq.py < "_bak/${target}" > "${target}"
done
shopt -u globstar