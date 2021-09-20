#!/usr/bin/bash

echo -n "
This will remove loyatyCardsOpen from your system. Do you want to continue (y/N)? "
read -n 1 ans
echo ""

case $ans in
	[Yy])	path="${HOME}/.local/share"
		rm -rf "$path/loyaltyCardsOpen"

		rm -f "$path/applications/loyaltyCards.desktop"
		echo ""
		echo "Completely removed loyaltyCardsOpen."
		echo ""
		echo "To reinstall loyaltyCardsOpen download the source from https://github.com/joanisc/loyaltyCardsOpen/ and run install.sh"
		echo ""
	;;

	*)	echo "Aborted"
		echo ""
		exit
	;;
esac

