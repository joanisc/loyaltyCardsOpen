#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi, sqlite3 as sqlite
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio

con = sqlite.connect('loyaltyCardsDb.db')

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def entered_tab(self, button):

        searchEntry = builder.get_object("searchEntry")
        listbox = builder.get_object("listbox")
        listbox1 = builder.get_object("listbox1")
        button = builder.get_object("button")
        image = builder.get_object("image")
        thumb = builder.get_object("thumb")
        
        searchParam = searchEntry.get_text()
        searchParamDef = "%"+searchParam+"%"
        #Clean listbox rows
        for row in listbox:
            listbox.remove(row)
        for row in listbox1:
            listbox1.remove(row)

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM CARD where CARD_NAME LIKE ? " , (searchParamDef,))
            rows = cur.fetchall()
            for row in rows:
                print (row[0], row[1])
                photo = row[3]
                photoPathId = ""+str(row[0])+".jpg"
                object = "       "+str(row[1])+"      "+str(row[2])+" "
                listbox.add(ListBoxRowWithData(object))
                Gtk.Container.add(listbox, button)
                with open(photoPathId, 'wb') as file:
                    file.write(photo)
                image.set_from_file(photoPathId)
                thumb.set_from_file(photoPathId)
            
                listbox1.add(thumb)
                image.show_all()
                thumb.show_all()
  
        listbox.show_all()
        listbox1.show_all()

    def row_selected(cur, picture_id, row):
        image = builder.get_object("image")

        rowData = row.data.strip()
        rowData = " ".join(rowData.split())
        cardName, codebar = rowData.split()
        print("cardName:"+cardName)
        print("codebar:"+codebar)
               
        with con:
            cur = con.cursor()
            cur.execute("SELECT ID, IMAGE FROM CARD where CARD_NAME = ? " , (cardName))
            row = cur.fetchone()
            id = row[0]
            photo = row[1]
            photoPath = ""+str(id)+".jpg"
            with open(photoPath, 'wb') as file:
                file.write(photo)
                print("Stored blob data into: ", photoPath, "\n")
        image.set_from_file(""+str(id)+".jpg")
        image.show_all()
        
    def extract_picture(cur, picture_id):
        image = builder.get_object("image")
        with con:
            cur = con.cursor()
            cur.execute("SELECT ID, IMAGE FROM CARD where ID = 39")
            rows = cur.fetchall()
            for row in rows:
                id = row[0]
                photo = row[1]
                photoPath = ""+str(id)+".jpg"
                #write_file(photo, photoPath)
                with open(photoPath, 'wb') as file:
                    file.write(photo)
                    print("Stored blob data into: ", photoPath, "\n")
        image.set_from_file(""+str(id)+".jpg")
        image.add(image)
        image.show_all()

               
    def on_button_clicked(self, button):
        entry = builder.get_object("cardNameEntry")
        barcodeEntry = builder.get_object("barcodeEntry")
        frontImage = builder.get_object("frontImage")
            
        frontImage1 = frontImage.get_file()
        #print(frontImage1)
        x = bytes(frontImage1)

        cardName =str(entry.get_text())
        barcodeEntry =str(barcodeEntry.get_text())
        print ('Card Name: %s' % cardName + ' '+ 'barcodeEntry: %s' % barcodeEntry)
        
        with con:
            cur = con.cursor()
            cur.execute('INSERT INTO CARD(CARD_NAME, BARCODE, IMAGE) VALUES (?,?,?)', (cardName, barcodeEntry, x))


builder = Gtk.Builder()
builder.add_from_file("gladeWindowDesign.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()

Gtk.main()
