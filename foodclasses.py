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

debug = True

class FoodObject:
    """ A FoodObject can be a food like cheese or a liquid like a juice """
    def __init__(self, foodname, amount, fat, carbon, protein, energy, liquid = False):
        self.data = {"name" : foodname, "amount" : amount, "fat" : fat, \
                "carbon" : carbon, "protein" : protein, "energy" : energy, \
                "liquid" : liquid }

        if not debug:
            return

        if liquid:
            print "New liquid: %s with %d KCal and %s fat" % (self.data["name"], self.data["energy"], self.data["fat"])
        else:
            print "New food: %s with %d KCal and %s fat" % (self.data["name"], self.data["energy"], self.data["fat"])
