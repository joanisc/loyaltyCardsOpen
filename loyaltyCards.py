#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi, sqlite3 as sqlite
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

con = sqlite.connect('loyaltyCardsDb.db')

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_file_selected(self, *args):
        print("File selected!")

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

    def row_selected(cur, image, row):
        image = builder.get_object("image")
        rowData = row.data
        rowData = rowData.strip()
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
        image.set_from_file(photoPath)
        

        # set size request, to limit image size
        image.set_size_request(width=10, height=10)
        image.show_all()
        
    def on_button_clicked(self, button):
        entry = builder.get_object("cardNameEntry")
        img = builder.get_object("img")
        barcodeEntry = builder.get_object("barcodeEntry")
        frontImage = builder.get_object("frontImage")
        backImage = builder.get_object("frontImage")
        pathFront = frontImage.get_filename()
        pathBack = backImage.get_filename()
        with open(pathFront, 'rb') as input_file:
            pathFrontBlob = input_file.read()
        with open(pathBack, 'rb') as input_file1:
            pathBackBlob = input_file1.read()
        img.set_from_file(pathFront)
        img.show_all()
        
        cardName =str(entry.get_text())
        barcodeEntry =str(barcodeEntry.get_text())
        print ('Card Name: %s' % cardName + ' '+ 'barcodeEntry: %s' % barcodeEntry)
        
        with con:
            cur = con.cursor()
            cur.execute('INSERT INTO CARD(CARD_NAME, BARCODE, IMAGE, IMAGEBACK) VALUES (?,?,?,?)', (cardName, barcodeEntry, sqlite.Binary(pathFrontBlob), sqlite.Binary(pathBackBlob)))


builder = Gtk.Builder()
builder.add_from_file("gladeWindowDesign.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()

Gtk.main()
