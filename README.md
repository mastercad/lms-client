python -m pip install pylms
--> Could not install packages due to an EnvironmentError: [Errno 13] Keine Berechtigung: '/usr/local/lib/python2.7/dist-packages/pylms-1.0.dist-info' Consider using the `--user` option or check the permissions.

sudo apt install rpi-update
sudo rpi-update -y

sudo apt-get install squeezelite

python -m pip install pylms --user
python -m pip install mfrc522 --user
python -m pip install python-vlc --user
python -m pip install simple_queue --user

# installiert wird insgesamt:
pylms, spidev, RPi.GPIO, mfrc522, python-vlc, pytz, blinker, six, docutils, simple-mappers, jmespath, futures, python-dateutil, urllib3, botocore, s3transfer, boto3, simple-queue, configparser


# alternativ installiert man diese libs per, dann aber ohne --user
source bin/activate
<venv> python2 -m pip install...

sudo cp systemfiles/config.txt /boot/config.txt
sudo cp systemfiles/asound.conf /etc/asound.conf
rm ~/.asoundrc

# VIRTUAL ENV installieren, einrichten und aktivieren
cd lms-client
python -m pip install --user virtualenv
python2 -m virtualenv venv
source venv/bin/activate
pip install pylms
pip install mfrc522
pip install python-vlc
pip install simple_queue

# requirements anlegen
pip freeze > requirements.txt

# requirements installieren
pip install -r requirements.txt


# Mit virtualenv umgehen
installieren:
---
python -m pip install --user virtualenv

aktivieren:
---
source venv/Scripts/activate

# Probleme
ImportError: cannot import name main
---
pip install vlc-ctrl
Traceback (most recent call last):
  File "/usr/bin/pip", line 9, in <module>
    from pip import main
ImportError: cannot import name main

# Lösung:
python -m pip uninstall pip
apt remove python-pip
whereis pip

wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
sudo python /tmp/get-pip.py

# Optionale Schritte:
pip install --user pipenv
pip3 install --user pipenv
echo "PATH=$HOME/.local/bin:$PATH" >> ~/.profile
source ~/.profile
whereis pip

- Viele Probleme mit virtualenv rührten daher, das ich es unter Windows eingerichtet hatte und es unter linux dann auch verwenden wollte
das funktioniert so nicht, da das env mit Lib angelegt wird und mit Script statt bin, bzw. bin ganz fehlt, genau wie .local
 
- ich habe darauf hin das virtualenv neu eingerichtet unter linux per
$ python3 -m venv venv_name (venv)
$ source venv_name/bin/activate
(venv) $ pip install <packet name>

# In PyCharm hat es die im virtuelenv installierten pakete nicht vorgeschlagen
- das lag daran, das in den projekt einstellungen nicht der unter virtualenv installierte interpreter ausgewählt war

# Soundkarte brachte ständig Gerät oder Ressource belegt
- ich habe darauf hin in der /etc/asound.conf aus
card 0 card 1 gemacht, damit ging es dann

# soundkarte test
speaker-test -c2 -Dplughw:0,0 -twav

# liste der devices
aplay -l

# große liste der devices
aplay -L

# schreibrechte auf das device
ls -lisa /dev/snd/pcmC0D0p