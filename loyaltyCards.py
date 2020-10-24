# -*- coding: utf-8 -*-
import gi, sqlite3 as sqlite, time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib

con = sqlite.connect('loyaltyCardsDb.db')

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

class Handler:
    global comeFromEdit 
    comeFromEdit = 0

    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_file_selected(self, *args):
        print("File selected!")
        img = builder.get_object("img")
        frontImage = builder.get_object("frontImage")
        pathFront = frontImage.get_filename()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=pathFront, width=80, height=60, preserve_aspect_ratio=True)
        img.set_from_pixbuf(pixbuf)
        img.show_all()

    def on_file_selected_back(self, *args):
        print("Back File selected!")
        imgBack = builder.get_object("imgBack")
        backImage = builder.get_object("backImage")
        pathBack = backImage.get_filename()
        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=pathBack, width=80, height=60, preserve_aspect_ratio=True)
        imgBack.set_from_pixbuf(pixbuf1)
        imgBack.show_all()

    def entered_tab(self, button):
        searchEntry = builder.get_object("searchEntry")
        listbox = builder.get_object("listbox")
        
        searchParam = searchEntry.get_text()
        searchParam = "%"+searchParam+"%"
        #Clean listbox rows
        for row in listbox:
            listbox.remove(row)

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM CARD where CARD_NAME LIKE ? " , (searchParam,))
            rows = cur.fetchall()
            for row in rows:
                print (row[0], row[1])
                rowData = "       "+str(row[1])+"      "+str(row[2])+" "
                listbox.add(ListBoxRowWithData(rowData))
        listbox.show_all()

    def row_selected(cur, self, row):
        global stringId
        global cardName
        global codebar
        global photoPath
        image = builder.get_object("image")
        rowData = row.data
        rowData = rowData.strip()
        rowData = " ".join(rowData.split())
        cardName, codebar = rowData.split()
        print("cardName:"+cardName)
        print("codebar:"+codebar)
               
        with con:
            cur = con.cursor()
            cur.execute("SELECT ID, IMAGE FROM CARD where CARD_NAME = ? LIMIT 1" , (cardName,))
            row = cur.fetchone()
            id = row[0] 
            stringId = ""+str(id)+""
            print("id0:"+stringId)
            photo = row[1]
            photoPath = ""+str(id)+".jpg"
            with open(photoPath, 'wb') as file:
                file.write(photo)
                print("Stored blob data into: ", photoPath, "\n")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPath, width=80, height=60, preserve_aspect_ratio=True)

        image.set_from_pixbuf(pixbuf)
        image.show_all()
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
        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=photoPath, width=80, height=60, preserve_aspect_ratio=True)
        imgBack.set_from_pixbuf(pixbuf1)
        img.show_all()
        imgBack.show_all()
        
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
        if pathFront is not None:
            with open(pathFront, 'rb') as input_file:
                pathFrontBlob = input_file.read()
        else:
            pathFrontBlob = ''
        if pathBack is not None:
            with open(pathBack, 'rb') as input_file1:
                pathBackBlob = input_file1.read()
        else:
            pathBackBlob = ''
        cardName =str(entry.get_text())
        barcodeEntryStr =str(barcodeEntry.get_text())
        print ('Card Name: %s' % cardName + ' '+ 'barcodeEntry: %s' % barcodeEntryStr)
        print ("comeFromEditSave:"+str(comeFromEdit))
        with con:
            cur = con.cursor()
            if comeFromEdit == 0:
                print ("If =>INSERT")
                cur.execute('INSERT INTO CARD(CARD_NAME, BARCODE, IMAGE, IMAGEBACK) VALUES (?,?,?,?)', (cardName, barcodeEntryStr, sqlite.Binary(pathFrontBlob), sqlite.Binary(pathBackBlob)))
                print(cur)
                
            else:
                print("Else => UPDATE")
                sql =cur.execute("UPDATE CARD SET CARD_NAME = ?, BARCODE = ?, IMAGE = IFNULL(?,''), IMAGEBACK = IFNULL(?,'') WHERE ID = ?" , (cardName, barcodeEntry, sqlite.Binary(pathFrontBlob), sqlite.Binary(pathBackBlob), stringId))
                print(sql)
                comeFromEdit = 0
                
        cardName = entry.set_text('')
        barcodeEntry = barcodeEntry.set_text('')
        pathFront = frontImage.unselect_all()
        pathBack = backImage.unselect_all()
        img.hide()
        imgBack.hide()
        GLib.timeout_add_seconds(1, 3, self.show_saved_image_seconds())
        savedImageInfo.hide()
        
     
    def entryCardsTab_activate_current_link_cb(self, cur, button):
        print ('Accessed entryCardsTab:')

    def show_saved_image_seconds(self):
        print ('Accessed show_saved_image_seconds:')
        savedImageInfo.show()
    
    def del_clicked_cb(self, cur):
        popDelConfirm = builder.get_object("popDelConfirm")
        popDelConfirm.show_all()
        popDelConfirm.popup()

    def del_yes_clicked_cb(self, cur):
        popDelConfirm = builder.get_object("popDelConfirm")
        id = stringId
        print("id:"+id)
        with con:
            cur = con.cursor()
            cur.execute('DELETE FROM CARD WHERE ID = ? ', (id,))
            print(cur)
        popDelConfirm.hide()
    
    def del_no_clicked_cb(self, cur):
        popDelConfirm = builder.get_object("popDelConfirm")
        popDelConfirm.hide()
         

builder = Gtk.Builder()
builder.add_from_file("gladeWindowDesign.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
delete = builder.get_object("del")
edit = builder.get_object("edit")
savedImageInfo = builder.get_object("savedImageInfo")

window.show_all()
delete.hide()
edit.hide()
savedImageInfo.hide()


Gtk.main()
