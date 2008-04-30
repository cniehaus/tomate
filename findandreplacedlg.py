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

class FindAndReplaceDlg(QDialog,
        ui_findandreplacedlg.Ui_FindAndReplaceDlg):

    def __init__(self, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)
        self.setupUi(self)
        self.updateUi()

	self.connect(self.addButton, SIGNAL("clicked()"), self.addFood)
	self.connect(self.foodCombo, SIGNAL("activated(QString)"), self.foodSelected)

	f = FoodObject( "Tomate", 0.2, 0.4, 0.3, 10.0 )

    def addFood(self):
	print "adding food"
    
    def foodSelected(self, text):
	print "fillig combos", text

    def updateUi(self):
    	print "in updateUi"

class FoodObject:
    def __init__(self, foodname, fat, carbon, protein, energy):
	self.foodname = foodname
	self.fat = fat
	self.carbon = carbon
	self.protein = protein
	self.energy = energy
	print "New object: %s with %d KCal and %s fat" % (self.foodname, self.energy, self.fat)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = FindAndReplaceDlg()
    form.show()
    app.exec_()

