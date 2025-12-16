#!/bin/bash
# convert po file to mo file for i18n

while read poFile; do
    moFile=${poFile%.po}.mo
    echo "[+] convert $poFile to $moFile"
    msgfmt $poFile -o $moFile
done < <(find . -type f |grep po$)
