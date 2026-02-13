# loyaltyCardsOpen

**The linux app to empty your pockets of cards.**

Linux App to save and view all your loyalty cards and any kind of card. Ready to use with a Linux Phone.

## Install on any distro with the installation script (Method 1)

1. Clone or download this repository
1. Open a terminal to the path where the repository folder is located
1. Install [dependencies](#Dependencies) according to your distribution
1. Make sure that the install.sh and uninstall.sh are executable. If necessary, do: ```chmod +x install.sh ``` and ```chmod +x uninstall.sh ```
1. Execute to install the app ``` ./install.sh ``` =>The script will install loyaltyCardsOpen to .local/share/loyaltyCards and create a .desktop file icon for the user.
1. To execute the app, find the new created icon on your apps

> Note: Alpine/PostmarketOS install will fail until 'sudo apk add coreutils' to make cp compatible with the install script

## Execute without installing (Method 2)

1. Clone or download this repository
1. Open a terminal to the path where the repository folder is located
1. Install dependencies according to your distribution if necessary
1. To execute the app:
> python3 loyaltyCards.py

## Dependencies: 

> python3

> sqlite

> python3-pip

> pip3 install python-barcode

> pip install pycairo PyGObject

### Detailed instructions on how to install dependencies in Alpine/PostmarketOS

sudo apk add python3
sudo apk add sqlite
sudo apk add py3-pip
python3 -m venv ~/venv-barcode
source ~/venv-barcode/bin/activate
pip install python-barcode
sudo apk add py3-gobject3 gobject-introspection-dev cairo-dev python3-dev gcc musl-dev pkgconf
sudo apk add coreutils


### Screenshots:

![Entry screen picture](/tmp/Entry.png?raw=true "Entry screen")

![Search screen picture](/tmp/Search.png?raw=true "Search screen")

![Entry screen in black](/tmp/SearchBlack.jpg?raw=true "Search screen")


~~ ## Install on Mobian/Debian/Ubuntu ~ Deprecated ~ 

Use the deb package from [here](https://github.com/joanisc/loyaltyCardsOpen/releases)*

Then to install it:

> sudo dpkg -i loyaltyCardsOpen.deb

After install, you can run it using the icon as any other app.

*Could not be updated. It is generated manually. For the latest version use the installation script (Method 1) ~~

### To do:

- [✔] Save images correctly in sqlite

- [✔] Show image and text correctly to the screen filtering by the search box

- [✔] Add screenshots to this file

- [✔] Fix problems deb file.

- [✔] Fix search on clean screen

- [✔] Make selected theme permanent

- [✔] Create a distro independent install script. Thanks @fdservices

- [✔] Put an scroll in order to manage unfiltered cards

- [] Create a flatpak package or create a project from scratch to have flatpak by default

- [] ¿Encrypt data in db?




