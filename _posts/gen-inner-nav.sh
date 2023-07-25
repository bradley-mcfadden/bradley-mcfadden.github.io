#! /usr/bin/bash
# Generate inner-nav for all headings of each md file with front matter

BACKUP_DIR="bak"
TARGETS=`find . -maxdepth 1 -name "*.md"`
if [ ! -d "${BACKUP_DIR}" ]; then
    mkdir "${BACKUP_DIR}"
fi
echo $TARGETS | while read -d " " target;
do
    cp "${target}" "${BACKUP_DIR}"
    python3 md_h_to_liq.py < "${target}" > "${target}"
done