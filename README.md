# loyaltyCardsOpen

**The linux app to empty your pockets of cards.**

Linux App to save and view all your loyalty cards and any kind of card. Ready to use with a Linux Phone.

## Install on any distro with the installation script (Method 1)

1. Clone or download this repository
1. Open a terminal to the path where the repository folder is located
1. Install dependencies according to your distro if necessary
1. Make sure that the install.sh and uninstall.sh are executable. If necessary, do: ```chmod +x install.sh ``` and ```chmod +x uninstall.sh ```
1. Execute to install the app ``` ./install.sh ``` =>The script will install loyaltCardsOpen to .local/share/loyaltyCards and create a .desktop file icon for the user.
1. To execute the app, find the new created icon on your apps or from terminal:
> ~/.local/share/loyaltyCardsOpen/loyaltyCards.sh

## Execute without installing (Method 2)

1. Clone or download this repository
1. Open a terminal to the path where the repository folder is located
1. Install dependencies according to your distro if necessary
1. To execute the app:
> python3 loyaltyCards.py

## Dependencies: 

> python3

> sqlite

> python3-pip

> pip3 install python-barcode

## Install on Mobian/Debian/Ubuntu

Use the deb package from [here](https://github.com/joanisc/loyaltyCardsOpen/releases)*

Then to install it:

> sudo dpkg -i loyaltyCardsOpen.deb

After install, you can run it using the icon as any other app.

*Could not be updated. It is generated manually. For the latest version use the installation script (Method 1)

### Screenshots:

![Entry screen picture](/tmp/Entry.png?raw=true "Entry screen")

![Search screen picture](/tmp/Search.png?raw=true "Search screen")

![Entry screen in black](/tmp/SearchBlack.jpg?raw=true "Search screen")

### To do:

- [✔] Save images correctly in sqlite

- [✔] Show image and text correctly to the screen filtering by the search box

- [✔] Add screenshots to this file

- [✔] Fix problems deb file.

- [✔] Fix search on clean screen

- [✔] Make selected theme permanent

- [✔] Create a distro independent install script. Thanks @fdservices

- [✔] Put an scroll in order to manage unfiltered cards

- [] Create a flatpak package

- [] ¿Encrypt data in db?




