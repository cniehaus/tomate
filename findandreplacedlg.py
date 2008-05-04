#!/usr/bin/env python
# Copyright (c) 2008 Carsten Niehaus. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import csv
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_maindlg

from foodclasses import *

class MainDialog(QDialog,
        ui_maindlg.Ui_MainDlg):

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        # This dictionary saves all food for the day
        self.foodlist = {}

        self.food = []
        self.loadFood() # Now fill the list so that the data can be accessed

        self.connect(self.addButton, SIGNAL("clicked()"), self.addFood)
        self.connect(self.foodstyle, SIGNAL("activated(int)"), self.updateUi)

        self.updateUi()

    def updateCounter(self):
        """ This method updates all four LCD displays """
        cal_counter = 0.0
        fat_counter = 0.0
        protein_counter = 0.0
        carbon_counter = 0.0

        # Iterating over all fooditems in the list
        for key, value in self.foodlist.iteritems():
            food = self.findFood(key)
            cal_counter +=  food.data["energy"] * value
            carbon_counter +=  food.data["carbon"] * value
            fat_counter +=  food.data["fat"] * value
            protein_counter +=  food.data["protein"] * value

        #now updating the LCD counters
        self.kcallcd.display( cal_counter )
        self.carbonlcd.display( carbon_counter )
        self.fatlcd.display( fat_counter )
        self.proteinlcd.display( protein_counter )

    def addFood(self):
        f = self.findFood( self.foodCombo.currentText() )
        factor = self.doubleSpinBox.value()

        self.addFoodToDatabase( f, factor )

        self.treeWidget.clear()

        # Iterating over all fooditems in the list
        for key, value in self.foodlist.iteritems():
            food = self.findFood(key)
            topItem = QTreeWidgetItem(self.treeWidget)
            o = QTreeWidgetItem( topItem )
            topItem.setText( 0, food.data["name"] )
            o.setText( 0, str(food.data["fat"]) )
            o.setText( 1, str(food.data["carbon"]) )
            o.setText( 2, str(food.data["protein"]) )
            o.setText( 3, str(food.data["energy"]) )
            o.setText( 4, str(value) )
            #the next line is there to auto-expand the items
            self.treeWidget.expandItem( topItem )

        self.updateUi()

    def addFoodToDatabase(self, food, factor):
        if self.foodlist.has_key( food.data["name"]):
            self.foodlist[food.data["name"] ] += factor
        else:
            self.foodlist[food.data["name"] ] = factor	
            
        print "Food amount after : ", self.foodlist[food.data["name"] ]

    def findFood(self, name):
        """ return the food with the name 'name' """
        tempList = self.food
        for i in tempList:
            if i.data["name"] == name:
                print "found ", i.data["name"]
                return i

    def updateUi(self):
        """ Update all GUI-elements """
        self.foodCombo.clear()

        L = []

        for i in self.food:
            if self.foodstyle.currentIndex() == 0:
                if i.data["liquid"] == True:
                    L.append( i )
            else:
                if i.data["liquid"] == False:
                    L.append( i )

        for i in L:
            self.foodCombo.addItem( i.data["name"] )

        self.updateCounter()

    def loadFood(self):
        """ In this method the file food.csv is loaded and put
        into the internal datastructur """

        reader = csv.reader( open( "food.csv",  "rb"))
        for row in reader:
            name = row[0]
            amount = int(row[1])
            fat = float(row[2])
            carbon = float(row[3])
            protein = float(row[4])
            energy = float(row[5])
            liquid = bool(int(row[6]))
            self.food.append( FoodObject( name, amount, fat, carbon, protein, energy, liquid ) )

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MainDialog()
    form.show()
    app.exec_()

