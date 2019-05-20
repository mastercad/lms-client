#!/bin/sh
IP=`ip route get 1 | awk '{print $NF;exit}'`
HOSTNAME="$1"

backupFile() {
    FILE="$1"

    if [ -f "$FILE" ] && [ ! -f "$FILE.bak" ]
    then
        sudo cp "$FILE" "$FILE.bak"
    fi
}

activateModule() {
    PARMATER="$1"
    FILE="$2"

    if grep -qn "#$PARMATER" "$FILE"
    then
        sudo sed -i "s/\#$PARMATER/$PARMATER/g" "$FILE"
    elif ! grep -qn "$PARMATER" "$FILE"
    then
        echo "$PARMATER" | sudo tee -a "$FILE"
    fi
}

sudo apt update -y && sudo apt install rpi-update && sudo rpi-update -y && sudo apt install -y squeezelite alsa-utils

# squeezelite autostart
backupFile "/etc/rc.local"

# echo "/usr/bin/squeezelize-armv6hf -o sysdefault:CARD=ALSA -s $IP -n $HOSTNAME &" | sudo tee -a /etc/rc.local >> /dev/null
activateModule "/usr/bin/squeezelize -o sysdefault:CARD=ALSA -s $IP -n $HOSTNAME &" "/etc/rc.local"

# fliegt mehrmals mit einem error raus:
# letzte zeilen sind in ungefähr:
#   File "/usr/share/python-wheels/urllib3-1.19.1-py2.py3-none-any.whl/urllib3/util/retry.py", line 315, in increment
#    total -= 1
# TypeError: unsupported operand type(s) for -=: 'Retry' and 'int'
# hier ist kein fehler klar. ich habe das mehrmals nacheinander ausgeführt und irgendwann ging es dann durch
# eventuell netzwerk probleme
python -m pip install pylms mfrc522 python-vlc simple_queue configparser --user

# module aktivieren
backupFile "/boot/config.txt"
activateModule "dtparam=spi=on" "/boot/config.txt"
activateModule "device_tree_param=spi=on" "/boot/config.txt"
activateModule "dtoverlay=hifiberry-dac" "/boot/config.txt"

backupFile "/etc/asound.conf"

echo "pcm.!default {
	type hw
	card 1
}

ctl.!default {
	type hw
	card 1
}
" | sudo tee /etc/asound.conf >> /dev/null
