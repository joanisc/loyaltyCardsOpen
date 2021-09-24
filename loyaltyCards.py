#!/usr/bin/python3
import os
import gi, sqlite3 as sqlite
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk
try:
    from barcode import Code128, EAN13, EAN14, EAN8
    from barcode.writer import ImageWriter
except ImportError:
    print("Error: The barcode dependency was not found. You can install it using 'pip3 install python-barcode'")

global sharedPath
global libPath

# If installation script **Comment**
libPath = ""
sharedPath = ""

# If installation script **Uncomment**
#libPath = "/usr/lib/loyaltycardsopen/"
#sharedPath = "/usr/share/loyaltycardsopen/"

con = sqlite.connect(sharedPath+"loyaltyCardsDb.db")

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

class Handler:
    global comeFromEdit 
    comeFromEdit = 0
    screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_file_selected(self, *args):
        print("File selected!")
        img = builder.get_object("img")
        frontImage = builder.get_object("frontImage")
        pathFront = frontImage.get_filename()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=pathFront, width=100, height=80, preserve_aspect_ratio=True)
        img.set_from_pixbuf(pixbuf)
        img.show_all()

    def on_file_selected_back(self, *args):
        print("Back File selected!")
        imgBack = builder.get_object("imgBack")
        backImage = builder.get_object("backImage")
        pathBack = backImage.get_filename()
        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=pathBack, width=100, height=80, preserve_aspect_ratio=True)
        imgBack.set_from_pixbuf(pixbuf1)
        imgBack.show_all()

    def entered_tab(self, cur, other):
        print ('Accessed SearchTab:')

        searchEntry = builder.get_object("searchEntry")
        listbox = builder.get_object("listbox")    
        searchParam = searchEntry.get_text()
        searchParam = "%"+searchParam+"%"
        print("searchParam:"+searchParam)
        #Clean listbox rows
        for row in listbox:
            listbox.remove(row)

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM CARD where CARD_NAME LIKE ? " , (searchParam,))
            rows = cur.fetchall()
            for row in rows:
                print (row[0], row[1])
                rowData = "       "+str(row[1])+"-"+str(row[2])+" "
                listbox.add(ListBoxRowWithData(rowData))
        listbox.show_all()
        
    def row_selected(self, cur , row):
        global stringId
        global cardName
        global codebar
        global photoPath
        global photoPathBack
        global barcodeImgFile
        image = builder.get_object("image")
        backImag = builder.get_object("backImag")
        barcodeImg = builder.get_object("barcodeImg")
        rowData = row.data
        rowData = rowData.strip()
        cardName, codebar = rowData.split("-")
        print("cardName:"+cardName)
        print("codebar:"+codebar)
    
        with con:
            cur = con.cursor()
            cur.execute("SELECT ID, BARCODE, IMAGE, IMAGEBACK FROM CARD where CARD_NAME = ? LIMIT 1" , (cardName,))
            row = cur.fetchone()
            id = row[0] 
            stringId = str(id)+""
            print("id0:"+stringId)
            
            codebar = row[1].strip()
            print("codebarYey:"+codebar)
            barcodeImgFile= sharedPath+"tmp/"+str(id)+"_barcode"
            try:
                if(len(codebar) == 13):
                    print("Predicted to have a EAN13 barcode")
                    codebarImg = EAN13(codebar, writer=ImageWriter())
                elif(len(codebar) == 8):
                    print("Predicted to have a EAN8 barcode")
                    codebarImg = EAN8(codebar, writer=ImageWriter())
                elif(len(codebar) == 14):
                    ("Predicted to have a EAN14 barcode")
                    codebarImg = EAN14(codebar, writer=ImageWriter())
                else:
                    ("Predicted to have a Code128 barcode")
                    codebarImg = Code128(codebar, writer=ImageWriter())

                codebarImg.save(barcodeImgFile)
                print("Barcode correctly Saved")
                pixbufCodeBar = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=barcodeImgFile+".png", width=400, height=100, preserve_aspect_ratio=True)
                barcodeImg.set_from_pixbuf(pixbufCodeBar)
                barcodeImg.show()
            except:
                print("Barcode no correctly generated because of the number of digits")
                barcodeImg.hide()
                
            photo = row[2]
            photoPath = sharedPath+"tmp/"+str(id)+".jpg"
            try:
                with open(photoPath, 'wb') as file:
                    file.write(photo)
                    print("Stored blob data into: ", photoPath, "\n")
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPath, width=80, height=60, preserve_aspect_ratio=True)
                image.set_from_pixbuf(pixbuf)
                image.show()
            except:
                print("No image where given")   
                image.hide() 

            try: 
                photoBack = row[3]
                photoPathBack = sharedPath+"tmp/"+str(id)+"_back.jpg"
                with open(photoPathBack, 'wb') as file:
                    file.write(photoBack)
                    print("Stored blob data into: ", photoPathBack, "\n")
                pixbufBack = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPathBack, width=80, height=60, preserve_aspect_ratio=True)
                backImag.set_from_pixbuf(pixbufBack)
                backImag.show()
            except:
                print("No image where given") 
                backImag.hide() 

        delete.show()
        edit.show()     

    def edit_clicked_cb(self, notebook):
        notebook = builder.get_object("notebook")
        notebook.next_page()
        global comeFromEdit
        comeFromEdit = 1
        print ("comeFromEdit:"+str(comeFromEdit))
        id = stringId
        print("id:"+id)
        entry = builder.get_object("cardNameEntry")
        img = builder.get_object("img")
        barcodeEntry = builder.get_object("barcodeEntry")
        frontImage = builder.get_object("frontImage")
        backImage = builder.get_object("backImage")
        imgBack = builder.get_object("imgBack")
        pathFront = frontImage.get_filename()
        pathBack = backImage.get_filename()
        entry.set_text(cardName)
        barcodeEntry.set_text(codebar)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPath, width=80, height=60, preserve_aspect_ratio=True)
        img.set_from_pixbuf(pixbuf)
        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPathBack, width=80, height=60, preserve_aspect_ratio=True)
        imgBack.set_from_pixbuf(pixbuf1)
        img.show_all()
        imgBack.show_all()

    def imgBig_clicked_cb(self, cur, button):
        print("Clicked image")
        image = builder.get_object("image")
        backImag = builder.get_object("backImag")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPath, width=150, height=150, preserve_aspect_ratio=True)
        image.set_from_pixbuf(pixbuf)
        image.show_all()
        pixbufBack = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPathBack, width=15, height=15, preserve_aspect_ratio=True)
        backImag.set_from_pixbuf(pixbufBack)
        backImag.show_all()
  
    def on_button_clicked(self, button):
        global comeFromEdit
        entry = builder.get_object("cardNameEntry")
        img = builder.get_object("img")
        imgBack = builder.get_object("imgBack")
        barcodeEntry = builder.get_object("barcodeEntry")
        frontImage = builder.get_object("frontImage")
        backImage = builder.get_object("backImage")
        savedImageInfo = builder.get_object("savedImageInfo")
       
        pathFront = frontImage.get_filename()
        pathBack = backImage.get_filename()
        try:
            with open(pathFront, 'rb') as input_file:
                pathFrontBlob = input_file.read()
        except:
            pathFrontBlob = 0
        try:
            with open(pathBack, 'rb') as input_file1:
                pathBackBlob = input_file1.read()
        except:
            pathBackBlob = 0
        
        cardName =str(entry.get_text())
        barcodeEntryStr =str(barcodeEntry.get_text())
        print('Card Name: %s' % cardName + ' '+ 'barcodeEntry: %s' % barcodeEntryStr)
        print("comeFromEditSave:"+str(comeFromEdit))
      
        with con:
            cur = con.cursor()
            if comeFromEdit == 0:
                print ("We will do an INSERT instead of update because it is not an edit")
                if (pathFrontBlob != 0 and pathBackBlob == 0):
                    print("FrontImage entered but not back")
                    cur.execute('INSERT INTO CARD(CARD_NAME, BARCODE, IMAGE) VALUES (?,?,?)', (cardName, barcodeEntryStr, sqlite.Binary(pathFrontBlob)))
                if (pathFrontBlob == 0 and pathBackBlob != 0):
                    print("BackImage entered but not front")
                    cur.execute('INSERT INTO CARD(CARD_NAME, BARCODE, IMAGEBACK) VALUES (?,?,?)', (cardName, barcodeEntryStr, sqlite.Binary(pathBackBlob)))
                if (pathFrontBlob == 0 and pathBackBlob == 0):
                    print("No Back or front image entered")
                    cur.execute('INSERT INTO CARD(CARD_NAME, BARCODE) VALUES (?,?)', (cardName, barcodeEntryStr))
                if (pathFrontBlob != 0 and pathBackBlob != 0):
                    cur.execute('INSERT INTO CARD(CARD_NAME, BARCODE, IMAGE, IMAGEBACK) VALUES (?,?,?,?)', (cardName, barcodeEntryStr, sqlite.Binary(pathFrontBlob), sqlite.Binary(pathBackBlob)))
                    print(cur)               
            else:
                print("Else => UPDATE")
                if (pathFrontBlob == 0 and pathBackBlob == 0):
                    sql =cur.execute("UPDATE CARD SET CARD_NAME = ?, BARCODE = ? WHERE ID = ?" , (cardName, barcodeEntryStr, stringId))
                if (pathFrontBlob != 0 and pathBackBlob == 0):
                    sql =cur.execute("UPDATE CARD SET CARD_NAME = ?, BARCODE = ?, IMAGE = ? WHERE ID = ?" , (cardName, barcodeEntryStr, sqlite.Binary(pathFrontBlob), stringId))
                if (pathFrontBlob == 0 and pathBackBlob != 0):
                    sql =cur.execute("UPDATE CARD SET CARD_NAME = ?, BARCODE = ?, IMAGEBACK = ? WHERE ID = ?" , (cardName, barcodeEntryStr, sqlite.Binary(pathBackBlob), stringId))
                if (pathFrontBlob != 0 and pathBackBlob != 0):
                    sql =cur.execute("UPDATE CARD SET CARD_NAME = ?, BARCODE = ?, IMAGE = ?, IMAGEBACK = ? WHERE ID = ?" , (cardName, barcodeEntryStr, sqlite.Binary(pathFrontBlob), sqlite.Binary(pathBackBlob), stringId))
                print(sql)
                comeFromEdit = 0
                
        cardName = entry.set_text('')
        barcodeEntry = barcodeEntry.set_text('')
        if (pathFrontBlob != 0 and pathBackBlob != 0):
            pathFront = frontImage.unselect_all()
            pathBack = backImage.unselect_all()
            img.hide()
            imgBack.hide()
            GLib.timeout_add_seconds(1, 3, self.show_saved_image_seconds())
            savedImageInfo.hide()
        
    def show_saved_image_seconds(self):
        print ('Accessed show_saved_image_seconds:')
        savedImageInfo.show()
    
    def del_clicked_cb(self, cur):
        popDelConfirm = builder.get_object("popDelConfirm")
        popDelConfirm.show_all()

    def del_yes_clicked_cb(self, cur):
        popDelConfirm = builder.get_object("popDelConfirm")
        id = stringId
        print("id:"+id)
        with con:
            cur = con.cursor()
            cur.execute('DELETE FROM CARD WHERE ID = ? ', (id,))
            print(cur)
        popDelConfirm.hide()
        self.entered_tab(stringId)
    
    def del_no_clicked_cb(self, cur):
        popDelConfirm = builder.get_object("popDelConfirm")
        popDelConfirm.hide()

    def newImageBig_clicked_cb(self, cur, button):
        imageBigNewWindow = builder.get_object("imageBigNewWindow")
        imageBigNewWindow.show_all()
        print("Front image Clicked")
        imageBigger = builder.get_object("imageBigger")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPath,width=300, height=300, preserve_aspect_ratio=True)
        imageBigger.set_from_pixbuf(pixbuf)
        imageBigger.show_all()
        imageBigNewWindow.show_all()
    
    def imgBigBack_clicked_cb(self, cur, button):
        imageBigNewWindow = builder.get_object("imageBigNewWindow")
        imageBigNewWindow.show_all()
        print("Back image Clicked")
        imageBigger = builder.get_object("imageBigger")
        pixbufBack = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPathBack,width=300, height=300, preserve_aspect_ratio=True)
        imageBigger.set_from_pixbuf(pixbufBack)
        imageBigger.show_all()
        imageBigNewWindow.show_all()

    def barcodeImgFile_clicked_cb(self, cur, button):
        imageBigNewWindow = builder.get_object("imageBigNewWindow")
        imageBigNewWindow.show_all()
        print("Barcode image Clicked")
        imageBigger = builder.get_object("imageBigger")
        pixbufBack = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=barcodeImgFile+".png",width=300, height=300, preserve_aspect_ratio=True)
        imageBigger.set_from_pixbuf(pixbufBack)
        imageBigger.show_all()
        imageBigNewWindow.show_all()

    def hide_clicked_cb(self, cur, button):
        print("Hide Clicked")
        imageBigNewWindow = builder.get_object("imageBigNewWindow")
        imageBigNewWindow.hide()

    def entered_settings(self):
        print("Entered settings")
     
    def on_theme_activated(self, cur, provider):
        path = sharedPath+"css/"
        if cur.get_active() == False:
            print("Theme on!")
            css_path = os.path.join(path, "main.css")
            self.provider.load_from_path(css_path)
            f=open('savedConf.conf','w+')
            f.write('main.css')
        else:
            print("Theme off!")
            css_path_plain = os.path.join(path, "plain.css")
            self.provider.load_from_path(css_path_plain)
            f=open('savedConf.conf','w+')
            f.write('plain.css')

    def destroy_clicked_cb(self):
        print("Asked to close window popup")  

    def quitButtonClicked(self, *args):
        print("Close and quit loyaltyCardsOpen... Good luck! See you soon!")  
        Gtk.main_quit()

    f=open(sharedPath+"savedConf.conf",'r')
    fContent=f.read()
    print("Loading default theme")
    path = sharedPath+"css/"
    css_path = os.path.join(path, fContent)
    provider.load_from_path(css_path)    
   
builder = Gtk.Builder()
builder.add_from_file(libPath+"gladeWindowDesign.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")  
   
delete = builder.get_object("del")
edit = builder.get_object("edit")
savedImageInfo = builder.get_object("savedImageInfo")

window.show_all()
delete.hide()
edit.hide()
savedImageInfo.hide()
imageBigNewWindow = builder.get_object("imageBigNewWindow")
imageBigNewWindow.hide()

Gtk.main()
