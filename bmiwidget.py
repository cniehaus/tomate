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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_bmiwidget

class BMIWid(QWidget,
        ui_bmiwidget.Ui_BMIWidget):

    def __init__(self, parent=None):
        super(BMIWid, self).__init__(parent)
        self.setupUi(self)
        self.setDateToToday()
        
        self.connect(self.height_, SIGNAL("valueChanged(int)"), \
                self.updateUi)
        self.connect(self.age_, SIGNAL("valueChanged(int)"), \
                self.updateUi)
        self.connect(self.weight_, SIGNAL("valueChanged(double)"), \
                self.updateUi)

    def updateUi(self):
        """ Update the GUI """
        bmi = self.calculateBMI()
        self.bmi_label.setText( unicode( bmi ) )

    def calculateBMI(self):
        """ return the BMI for the given values.

        The SpinBox gets the value in centimeter. Therefore we need to
        divide by 1000.
        """
        w = float( self.weight_.value() )
        h = float( self.height_.value() )

        bmi = w / ( h**2 / 10000 )
        return bmi

    def setDateToToday(self):
        """ Set the DateEdit to todays day """
        self.dateEdit.setDate( QDate.currentDate() ) 
