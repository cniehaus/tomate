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
import ui_findandreplacedlg

debug = True

class FindAndReplaceDlg(QDialog,
        ui_findandreplacedlg.Ui_FindAndReplaceDlg):

    def __init__(self, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)
        self.setupUi(self)

        # This dictionary saves all food for the day
        self.foodlist = {}

        self.connect(self.addButton, SIGNAL("clicked()"), self.addFood)
        self.connect(self.foodstyle, SIGNAL("activated(int)"), self.updateUi)

        self.updateUi()
        self.loadFood()

    def updateCounter(self):
        """ This method updates all four LCD displays """
        cal_counter = 0.0
        fat_counter = 0.0
        protein_counter = 0.0
        carbon_counter = 0.0

        # Iterating over all fooditems in the list
        for key, value in self.foodlist.iteritems():
            food = self.findFood(key)
            cal_counter +=  food.energy * value
            carbon_counter +=  food.carbon * value
            fat_counter +=  food.fat * value
            protein_counter +=  food.protein * value

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
            topItem.setText( 0, food.foodname )
            o.setText( 0, str(food.fat) )
            o.setText( 1, str(food.carbon) )
            o.setText( 2, str(food.protein) )
            o.setText( 3, str(food.energy) )
            o.setText( 4, str(value ) )
            #the next line is there to auto-expand the items
            self.treeWidget.expandItem( topItem )

        self.updateUi()

    def addFoodToDatabase(self, food, factor):
        if self.foodlist.has_key( food.foodname):
            #print "Food amount, before: ", self.foodlist[food.foodname]
            #print "Adding %s to the databse" % (food.foodname)
            self.foodlist[food.foodname] += factor
        else:
            #print "%s not yet in the database!" % (food.foodname)
            self.foodlist[food.foodname] = factor	
            
        print "Food amount after : ", self.foodlist[food.foodname]	

    def findFood(self, name):
        tempList = self.loadFood()
        #print "searching for ", name
        for i in tempList:
            if i.foodname == name:
                print "found ", i.foodname
                return i

    def updateUi(self):
        """ Update all GUI-elements """
        self.foodCombo.clear()

        L = []
        tempList = self.loadFood()

        for i in tempList:
            if self.foodstyle.currentIndex() == 0:
                if i.liquid == True:
                    L.append( i )
            else:
                if i.liquid == False:
                    L.append( i )

        for i in L:
            self.foodCombo.addItem( i.foodname )

        self.updateCounter()

    def loadFood(self):
        """ In this method the file food.csv is loaded and put
        into the internal datastructur """
        l = []

        reader = csv.reader( open( "food.csv",  "rb"))
        for row in reader:
            name = row[0]
            amount = int(row[1])
            fat = float(row[2])
            carbon = float(row[3])
            protein = float(row[4])
            energy = float(row[5])
            liquid = row[6] != "1"
            l.append( FoodObject( name, amount, fat, carbon, protein, energy, liquid ) )

        return l

class FoodObject:
    def __init__(self, foodname, amount, fat, carbon, protein, energy, liquid = False):
        self.foodname = foodname
        self.amount = amount
        self.fat = fat
        self.carbon = carbon
        self.protein = protein
        self.energy = energy
        self.liquid = liquid

        if not debug:
            return

        if liquid:
            print "New liquid: %s with %d KCal and %s fat" % (self.foodname, self.energy, self.fat)
        else:
            print "New food: %s with %d KCal and %s fat" % (self.foodname, self.energy, self.fat)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = FindAndReplaceDlg()
    form.show()
    app.exec_()

