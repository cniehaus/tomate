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

import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_findandreplacedlg

debug = False

class FindAndReplaceDlg(QDialog,
        ui_findandreplacedlg.Ui_FindAndReplaceDlg):

    def __init__(self, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)
        self.setupUi(self)

	# This dictionary saves all food for the day
	self.foodlist = {}

	self.connect(self.addButton, SIGNAL("clicked()"), self.addFood)
	self.connect(self.foodCombo, SIGNAL("activated(QString)"), self.foodSelected)
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
		o.setText( 0, "Fett: %d" % (food.fat) )
		o.setText( 1, "Kohlenhydrate: %d" % (food.carbon) )
		o.setText( 2, "Protein: %d" % (food.protein) )
		o.setText( 3, "KCal: %d" % (food.energy) )
		o.setText( 4, "Faktor: %d" % (value) )
		
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
	tempList = self.initializeFood()
	#print "searching for ", name
	for i in tempList:
		if i.foodname == name:
			print "found ", i.foodname
			return i
    
    def foodSelected(self, text):
	print "fillig combos", text

    def updateUi(self):
	self.foodCombo.clear()
	
	L = []
	tempList = self.initializeFood()
	
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
		
    def initializeFood(self):
	l = []
	
	l.append( FoodObject( "Tomate", 1 , 2.2, 0.4, 0.3, 11.5, False ) )
	l.append( FoodObject( "Bier", 100, 0.2, 0.4, 0.3, 14.0, True ) )
	l.append( FoodObject( "Cola", 100, 0.9, 0.1, 3.3, 10.0, True ) )
	l.append( FoodObject( "Salate (50g)", 50, 0.2, 0.4, 0.3, 10.0, False ) )
	l.append( FoodObject( "Apfelsaft (100mL)", 100, 0.2, 0.4, 0.3, 10.0, True ) )

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

