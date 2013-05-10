# Copyright (c) 2011-2013, ImageCat Inc.
#
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU Affero General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License 
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Draw vertical header used by mapping scheme widget
"""
from PyQt4.QtGui import QPushButton, QPainter, QPen 
from PyQt4 import QtCore

class VerticalQLabel(QPushButton):
    """
    Vertical clickable label
    """
    def __init__(self, parent):        
        super(VerticalQLabel,self).__init__(parent)
    
    def paintEvent(self, event):
        """ custom paint event to draw vertical text """
        painter = QPainter(self)        
        
        # draw box around
        arc_size, line_width=10, 1
        pen = QPen(QtCore.Qt.gray)
        pen.setWidth(line_width)
        painter.setPen(pen)
        painter.drawLine(arc_size,0, self.width(), 0)
        painter.drawLine(0, arc_size,0, self.height()-arc_size)
        painter.drawLine(arc_size-5,self.height()-1,self.width(), self.height()-1)
        painter.drawArc(0,0, arc_size*2, arc_size*2, 180*16, -90*16)
        painter.drawArc(0,self.height()-arc_size*2, arc_size*2, arc_size*2, 180*16, 90*16)
        # draw box around
        if (self.isEnabled()):  
            painter.setPen(QtCore.Qt.black)
        else:
            painter.setPen(QtCore.Qt.gray)
        painter.translate(self.width(), self.height())
        painter.rotate(270)
        painter.drawText(QtCore.QPointF(10,- self.width()/3), self.text())
        # destroy
        del painter
        