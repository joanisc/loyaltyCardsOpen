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

# remove any existing backup files
rm "$path/loyaltyCardsOpen/*.bak"

# copy the updated files
cp -ruS .bak ./* "$path/loyaltyCardsOpen"

if [ $? -ne 0 ]; then
	echo "" 
	echo "Could not copy download folder to $path/loyaltyCardsOpen"
	exit
fi

# offer to copy back the database and config files
if [ -e "$path/loyaltyCardsOpen/loyaltyCardsDb.db.bak" ];then
	echo -n "Do you want to restore the loyaltyCards database? (Y/n)? "
	read -n 1 ans
	echo ""
	case $ans in
		[N|n]
		# do nothing
		;;
		*) cp -f "$path/loyaltyCardsOpen/loyaltyCardsDb.db.bak" "$path/loyaltyCardsOpen/loyaltyCardsDb.db"
		if [ $? -ne 0 ]; then 
		        echo ""
		        echo "Could not recover loyaltyCards database ($path/loyaltyCardsOpen/loyaltyCardsDb.db.bak)"
		        echo ""
		fi

		;;
	esac
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
Exec="$path/loyaltyCardsOpen/loyaltyCards.sh"
Terminal=false
StartupNotify=true
Type=Application
Icon=$path/loyaltyCardsOpen/loyaltycardsopen.svg
Categories=GNOME;GTK;Utility;
MimeType=application/python;
Name[en_US]=Loyalty Cards Open
X-Purism-FormFactor=Workstation;Mobile;" > "$path/applications/loyaltyCards.desktop"

if [ $? -ne 0 ]; then 
	echo "" 
	echo "Could not create desktop file in to $path/applications"
	exit
fi

rm -f "$path/loyaltyCards.sh"

echo "#!/usr/bin/bash

cd '$path/loyaltyCardsOpen'
python3 loyaltyCards.py" > "$path/loyaltyCardsOpen/loyaltyCards.sh"

chmod 0755 "$path/loyaltyCardsOpen/loyaltyCards.sh"

if [ $? -ne 0 ]; then 
	echo "" 
	echo "Could not create shell script in to $path/loyaltyCards"
	exit
fi

echo "" 
echo "Install complete - you may (optionally) remove the download folder"
