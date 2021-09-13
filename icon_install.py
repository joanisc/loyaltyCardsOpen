#!/usr/bin/python3
import os
import subprocess as sp

username = sp.check_output('whoami', shell=True)
username = username.decode('utf-8').strip('\n')

if isinstance(username, list):
    username = username[0]
else:
    username = username

script_path = os.path.dirname(os.path.realpath(__file__))
path = f"{script_path}/loyaltyCards.py"
install_path = f"/home/{username}/.local/share/applications/loyalty_cards.desktop"
logo_path = f"{script_path}/loyaltycardsopen.svg"

icon_file = f"""
[Desktop Entry]
Name=Loyalty Cars Open
GenericName=Cards DDBB
X-GNOME-FullName=Loyalty Cars Open
Comment=A linux app to save your cards digitally and empty your pockets of cards.
Keywords=Loyalty Cars Open; store cards;
Exec={path}
Terminal=false
StartupNotify=true
Type=Application
Icon={logo_path}
Categories=GNOME;GTK;Utilities;
MimeType=application/python;
Name[en_US]=Loyalty Cards Open
X-Purism-FormFactor=Workstation;Mobile;
"""

with open(install_path, "w+") as f:
    f.write(icon_file)
