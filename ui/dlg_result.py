# Copyright (c) 2011-2012, ImageCat Inc.
#
# SIDD is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with SIDD.  If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.
#
# Version: $Id: dlg_result.py 18 2012-10-24 20:21:41Z zh $

"""
dialog for editing mapping scheme brances
"""

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from sidd.constants import *
from sidd.ms import *

from ui.constants import logUICall
from ui.qt.dlg_res_detail_ui import Ui_tablePreviewDialog

class DialogResult(Ui_tablePreviewDialog, QDialog):
    """
    dialog for visualize results
    """    
    def __init__(self):
        super(DialogResult, self).__init__()
        self.ui = Ui_tablePreviewDialog()
        self.ui.setupUi(self)
        self.ui.table_result.setSelectionMode(QAbstractItemView.SingleSelection)
    
    @logUICall
    def showDetail(self, fields, selected):
        fnames =[]
        cnt_idx = -1
        for i, f in fields.iteritems():
            fnames.append(f.name())
            if f.name() == CNT_FIELD_NAME:
                cnt_idx = i
        cnt_sum = 0        
        for s in selected:
            cnt_sum  += s[cnt_idx].toInt()[0]
        #return
        self.resultDetailModel = ResultDetailTableModel(fnames, selected)        
        self.ui.table_result.setModel(self.resultDetailModel)
        self.ui.txt_bldgcount.setText('%d'% cnt_sum) 
        self.ui.txt_bldgcount.setReadOnly(True)
        self.resize(600, 425)
        self.ui.table_result.setGeometry(QRect(10, 40, 580, 271))

class ResultDetailTableModel(QAbstractTableModel):
    """
    table model supporting visualization of node in mapping scheme tree
    """
    
    def __init__(self, fields, selected):
        """ constructor """
        QAbstractTableModel.__init__(self)

        # table header 
        self.headers = fields #['Taxonomy', 'Count']
        
        # create copy of values to be shown and modified
        self.selected = selected
    
    @logAPICall
    def columnCount(self, parent):
        """ only two columns exist. always return 2 """
        return len(self.headers)

    @logAPICall
    def rowCount(self, parent):
        """ number of rows same as number of siblings """
        return len(self.selected)

    @logAPICall
    def headerData(self, section, orientation, role):
        """ return data to diaply for header row """        
        if role == Qt.DisplayRole:   
            if orientation == Qt.Horizontal:
                return QString(self.headers[section])
            else:
                # no vertical header
                return QVariant()
        elif role == Qt.ToolTipRole:            
            return QString('tool tip for %s' % self.headers[section])
        else:            
            return QVariant()
    
    @logAPICall
    def data(self, index, role):
        """ return data to be displayed in a cell """
        if role == Qt.DisplayRole:
            logAPICall.log('row %s column %s ' %(index.row(), index.column()),
                             logAPICall.DEBUG_L2)
            return QString(self.selected[index.row()][index.column()].toString())
        else:
            return QVariant()
    
    def flags(self, index):
        """ cell condition flag """
        # NOTE: 
        #   ItemIsEditable also required data() and setData() function
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
