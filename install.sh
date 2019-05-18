#!/bin/sh
# sudo apt update -y && sudo apt install rpi-update && sudo rpi-update -y

# fliegt mehrmals mit einem error raus:
# letzte zeilen sind in ungefähr:
#   File "/usr/share/python-wheels/urllib3-1.19.1-py2.py3-none-any.whl/urllib3/util/retry.py", line 315, in increment
#    total -= 1
# TypeError: unsupported operand type(s) for -=: 'Retry' and 'int'
# hier ist kein fehler klar. ich habe das mehrmals nacheinander ausgeführt und irgendwann ging es dann durch
# eventuell netzwerk probleme
# python -m pip install pylms mfrc522 python-vlc simple_queue configparser --user

# $1 = parameter
# $2 = file
activateParam() {
    if grep -qn "#$1" "$2"
    then
        sed -i "s/\#$1/$1/g" "$2"
    elif ! grep -qn "$1" "$2"
    then
        echo "$1" >> "$2"
    fi
}

# spi aktivieren
activateParam "dtparam=spi=on" "/boot/config.txt"
activateParam "device_tree_param=spi=on" "/boot/config.txt"
activateParam "dtoverlay=hifiberry-dac" "/boot/config.txt"

echo "pcm.!default {
	type hw
	card 1
}

ctl.!default {
	type hw
	card 1
}
" > /etc/asound.conf
