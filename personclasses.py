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

class Person:
    """ A person has the important properties like a weigth and a size """
    def __init__(self, name):
        self.name = name

        # in kilogramm
        self.weight = {}

        # in centimeter
        self.size = 100

        d = QDate( 1980, 24, 04 )

        # in years
        self.birthday = d

        # Male or Female
        self.gerder = "Male"

        self.loadData()

    def weightOfDate(self, date):
        try:
            d = self.weight[date]
            print "Found weight %d for %s" % (d, date.toString())
            return d
        except (KeyError), e:
            print "Date %s not found, ignoring input" % date.toString()

    def loadData(self):
        print "Loading data"

        error = None
        fh = None

        try:
            filename = "persons/"+ self.name + ".csv"
            print "trying to load the data of %s in this file: %s" % (self.name,filename)

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
                if line.startsWith( "Person" ):
                    content = line.split(",")
                    self.birthday = self.dateFromString( content[1] )
                else:
                    content = line.split(",")
                    date = self.dateFromString( content[0] )
                    weight = float(content[1])
                    self.weight[date] = float(weight)
            self.debugData()

        except (IOError, OSError, ValueError), e:
            error = "Failed to load: %s on line %d" % (e, lino)

    def debugData(self):
        """ a method just for testing: Spits out all data
        of the person. """
        for key, value in self.weight.iteritems():
            print "on %s, %s weigted %d kg" % (key.toString(), self.name, value )

    def dateFromString(self,date):
        """ return a QDate object from a string like 2008-05-04 """
        content = date.split( "-" )
        d = QDate( int(content[0]), int(content[1]), int(content[2]) )
        return d
