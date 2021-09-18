#!/usr/bin/bash

path="${HOME}/.local/share"

mkdir -p "$path/loyaltyCardsOpen"

if [ $? -ne 0 ]; then 
	echo ""
	echo "Could not create folder '$path/loyaltyCardsOpen'"
	exit
fi

echo "" 
echo "Copying download folder to $path/loyaltyCardsOpen"
cp -ru ./* "$path/loyaltyCardsOpen"

if [ $? -ne 0 ]; then
	echo "" 
	echo "Could not copy download folder to $path/loyaltyCardsOpen'"
	exit
fi

echo "" 
echo "Create a new desktop file"
rm -f "$path/applications/loyaltyCards.desktop"

echo "[Desktop Entry]
Name=Loyalty Cards Open
GenericName=Cards DDBB
X-GNOME-FullName=Loyalty Cards Open
Comment=A linux app to save your cards digitally and empty your pockets of cards.
Keywords=Loyalty Cards Open; store cards;
Exec="$path/loyaltyCardsOpen/loyaltyCards.py"
Terminal=false
StartupNotify=true
Type=Application
Icon="$path/loyaltyCardsOpen/loyaltycardsopen.svg"
Categories=GNOME;GTK;Utility;
MimeType=application/python;
Name[en_US]=Loyalty Cards Open
X-Purism-FormFactor=Workstation;Mobile;" > "$path/applications/loyaltyCards.desktop"

if [ $? -ne 0 ]; then 
	echo "" 
	echo "Could not create desktop file in to $path/applications'"
	exit
fi

echo "" 
echo "Install complete - you may (optionally) remove the download folder"
