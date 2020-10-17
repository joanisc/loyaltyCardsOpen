# Here we imported the 'setup' module which allows us to install Python scripts to the local system beside performing some other tasks, you can find the documentation here: https://docs.python.org/2/distutils/apiref.html 
from distutils.core import setup 

setup(name = "loyaltycardsopen", # Name of the program. 
      version = "1.0", # Version of the program. 
      description = "Linux App to save and view all your loyalty cards and any kind of card. Ready to use with a Linux Phone.",  
      author = "Joan Singla Casamitjana", 
      author_email = "joan@singlacasamitjana.eu",
      url = "https://github.com/joanisc/loyaltyCardsOpen",
      license='GPLv3', # The license of the program. 
      scripts=['loyaltyCards.py'], 

# Here you can choose where do you want to install your files on the local system, the "loyaltycardsopen" file will be automatically installed in its correct place later, so you have only to choose where do you want to install the optional files that you shape with the Python script 
      data_files = [ ("lib/loyaltycardsopen", ["gladeWindowDesign.glade"]), # This is going to install the "gladeWindowDesign.glade" file under the /usr/lib/loyaltycardsopen path. 
                     ("share/applications", ["loyaltycardsopen.desktop"]), # And this is going to install the .desktop file under the /usr/share/applications folder, all the folder are automatically installed under the /usr folder in your root partition, you don't need to add "/usr/ to the path. 
                     ("/usr/share/pixmaps", ["loyaltycardsopen.svg"]),
                     ("~/.local/share/loyaltycardsopen", ["loyaltyCardsDb.db"]) ] ) 

