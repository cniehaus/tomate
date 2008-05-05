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
import codecs
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import *
from bmiwidget import *
import ui_maindlg

from foodclasses import *

class MainDialog(QDialog,
        ui_maindlg.Ui_MainDlg):

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        self.bmi = BMIWid(self)

        # This dictionary saves all food for the day
        self.foodlist = {}

        self.food = []
        self.loadFood() # Now fill the list so that the data can be accessed

        self.dateEdit.setDate( QDate.currentDate() )

        self.connect(self.todayButton, SIGNAL("clicked()"), \
                self.setDateToToday)
        self.connect(self.saveButton, SIGNAL("clicked()"), \
                self.saveFoodList)
        self.connect(self.addButton, SIGNAL("clicked()"), \
                self.addFood)
        self.connect(self.foodstyle, SIGNAL("activated(int)"), \
                self.updateUi)
        self.connect(self.dateEdit, SIGNAL("dateChanged(QDate)"), \
                self.dateChanged)

        self.updateUi()
        #self.dateChanged( QDate.currentDate() )

    def dateChanged(self, date):
        #print date.toString()
        self.loadFoodFromDate(date)

    def setDateToToday(self):
        self.dateEdit.setDate( QDate.currentDate() ) 

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


        self.updateUi()

    def addFoodToDatabase(self, food, factor):
        """ adding the food 'food' with the factor of 'factor' to the database """
        if self.foodlist.has_key( food.data["name"]):
            self.foodlist[food.data["name"] ] += factor
        else:
            self.foodlist[food.data["name"] ] = factor	

    def findFood(self, name):
        """ return the food with the name 'name' """
        tempList = self.food
        for i in tempList:
            if i.data["name"] == name:
                #print "found ", i.data["name"]
                return i

        return None

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
        self.updateTreeWidget()

    def updateTreeWidget(self):
        """ This method iterates over all items in the foodlist 
        for the day and then adds one food after the other to the
        QTreeWidget
        """

        # Starting from zero
        self.treeWidget.clear()

        # Iterating over all fooditems in the list
        for key, value in self.foodlist.iteritems():
            food = self.findFood(key)
            topItem = QTreeWidgetItem(self.treeWidget)
            o = QTreeWidgetItem( topItem )
            topItem.setText( 0, food.data["name"] )
            o.setText( 0, "%s g" % unicode(food.data["fat"]))
            o.setText( 1, "%s g" % unicode(food.data["carbon"]))
            o.setText( 2, "%s mg" % unicode(food.data["protein"]))
            o.setText( 3, "%s kCal" %unicode(food.data["energy"]))
            o.setText( 4, unicode(value) )

            #the next line is there to auto-expand the items
            self.treeWidget.expandItem( topItem )

    def getDataOfTheDay(self):
        """ Return a list of the things that have been added for the day """
        
        data = []
        for key, value in self.foodlist.iteritems():
            food = self.findFood(key)

            set = { "name" : food.data["name"], "factor" : value }
            data.append(set)
        return data

    def saveFoodList(self):
        """ save the food of one day 
        
        The fileformat is very simple: Just the name of the product in
        first place, then the amount it was consumed that day. The are 
        seperated with a comma.
        """
        
        currentDate = self.dateEdit.date()
        savefilename = "days/" + str(currentDate.year()) + "-" \
                + str(currentDate.month()) + "-" + str(currentDate.day()) + ".csv"

        writer = csv.DictWriter(open(savefilename, "wb"), ["name", "factor"] )
        writer.writerows( self.getDataOfTheDay() )

    def loadFoodFromDate(self, date):
        """ Loading the data of the given date """

        filename = "days/" + str(date.year()) + "-" \
                + str(date.month()) + "-" + str(date.day()) + ".csv"

        print "Trying to load this file: ", filename
        error = None
        fh = None

        try:
            fh = QFile( filename )
            lino = 0
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")

            while not stream.atEnd():
                name = None
                line = stream.readLine()
                lino += 1
                content = line.split(",")
                name = content[0]
                factor = float(content[1])
                print "Trying to add '%s' '%f' times" % (name,factor)
                f = self.findFood( name )
                if f is not None:
                    self.addFoodToDatabase( f, factor )
                else:
                    print "Food not found..."

        except (IOError, OSError, ValueError), e:
            error = "Failed to load: %s on line %d" % (e, lino)

        self.updateUi()

    def loadFood(self):
        """ In this method the file food.csv is loaded and put
        into the internal datastructure """
        
        error = None
        fh = None

        try:
            filename = "food.csv"
            fh = QFile( filename )
            lino = 0
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")

            while not stream.atEnd():
                name = None
                line = stream.readLine()
                lino += 1
                content = line.split(",")
                name = content[0]
                amount = int(content[1])
                fat = float(content[2])
                carbon = float(content[3])
                protein = float(content[4])
                energy = float(content[5])
                liquid = bool(int(content[6]))
                self.food.append( FoodObject( name, amount, fat, carbon, \
                        protein, energy, liquid ) )

        except (IOError, OSError, ValueError), e:
            error = "Failed to load: %s on line %d" % (e, lino)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MainDialog()
    form.show()
    app.exec_()

