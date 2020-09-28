#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi, sqlite3 as sqlite
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio

con = sqlite.connect('ydb.db')

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

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
builder.add_from_file("TestGlade.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()

Gtk.main()
