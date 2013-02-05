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
# Version: $Id: dlg_result.py 21 2012-10-26 01:48:25Z zh $

"""
dialog for editing mapping scheme branches
"""
from PyQt4.QtGui import QDialog, QAbstractItemView
from PyQt4.QtCore import QSize, Qt, QVariant, QString, QAbstractTableModel
from operator import itemgetter

from sidd.constants import logAPICall, CNT_FIELD_NAME

from ui.constants import logUICall, UI_PADDING
from ui.qt.dlg_res_detail_ui import Ui_tablePreviewDialog

class DialogResult(Ui_tablePreviewDialog, QDialog):
    """
    dialog for visualize result details
    """
    # constructor
    ###############################     
    def __init__(self):
        super(DialogResult, self).__init__()
        self.ui = Ui_tablePreviewDialog()
        self.ui.setupUi(self)
        self.ui.table_result.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.table_result.setSortingEnabled(True)
        self.resize(600, 425)
        
        # connect slots (ui event)
        self.ui.btn_ok.clicked.connect(self.accept)
    
    # window event handler overrides
    #############################
    def resizeEvent(self, event):
        """ handle window resize """
        self.ui.table_result.resize(
            QSize(self.width()-2*UI_PADDING, 
                  self.height() - self.ui.table_result.y()-self.ui.btn_ok.height()-2*UI_PADDING))
        
        below_table = self.height() - self.ui.btn_ok.height() - UI_PADDING
        self.ui.lb_bldgcount.move(UI_PADDING, below_table)        
        self.ui.txt_bldgcount.move(self.ui.lb_bldgcount.width()+(2*UI_PADDING), below_table)
        self.ui.btn_ok.move(self.width()-UI_PADDING-self.ui.btn_ok.width(), below_table)
        
    # public method
    ###############################     
    
    @logUICall
    def showExposureData(self, header, selected):
        """
        display selected rows with header
        """
        fnames =[]        
        cnt_idx = -1
        for i, f in header.iteritems():
            fnames.append(f.name())
            if f.name() == CNT_FIELD_NAME:
                cnt_idx = i        

        # TODO: error handling if cnt_idx == -1
        cnt_sum = 0
        for s in selected:
            cnt_sum  += s[cnt_idx].toInt()[0]

        # sync UI 
        self.resultDetailModel = ResultDetailTableModel(header.values(), selected)        
        self.ui.table_result.setModel(self.resultDetailModel)
        self.ui.table_result.sortByColumn(3, Qt.AscendingOrder)
        self.ui.txt_bldgcount.setText('%d'% cnt_sum) 
        self.ui.txt_bldgcount.setReadOnly(True)
        self.ui.txt_bldgcount.setVisible(True) 
        self.ui.lb_bldgcount.setVisible(True)

    @logUICall
    def showInfoData(self, header, selected):
        # sync UI 
        self.resultDetailModel = ResultDetailTableModel(header.values(), selected)        
        self.ui.table_result.setModel(self.resultDetailModel)
        self.ui.table_result.sortByColumn(3, Qt.AscendingOrder)
        self.ui.txt_bldgcount.setVisible(False) 
        self.ui.lb_bldgcount.setVisible(False)


class ResultDetailTableModel(QAbstractTableModel):
    """
    table model supporting visualization of result detail
    """
    # constructor
    ###############################         
    def __init__(self, fields, selected):
        """ constructor """
        QAbstractTableModel.__init__(self)
        # table header 
        self.headers = fields        
        # create copy of values to be shown and modified
        self.selected = []
        for row in selected:
            new_row = []
            for i, v in enumerate(row.values()):
                if self.headers[i].type() == QVariant.Int:
                    new_row.append(v.toInt()[0])
                elif self.headers[i].type() == QVariant.Double:
                    new_row.append(v.toDouble()[0])
                else:
                    new_row.append(str(v.toString()))
            self.selected.append(new_row)

    # override public method
    ###############################     
        
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
                return QString(self.headers[section].name())
            else:
                # no vertical header
                return QVariant()
        elif role == Qt.ToolTipRole:            
            return QString('tool tip for %s' % self.headers[section].name())
        else:            
            return QVariant()
    
    @logAPICall
    def data(self, index, role):
        """ return data to be displayed in a cell """
        if role == Qt.DisplayRole:
            logAPICall.log('row %s column %s ' %(index.row(), index.column()),
                             logAPICall.DEBUG_L2)
            return QString("%s" % self.selected[index.row()][index.column()])
        else:
            return QVariant()

    def sort(self, ncol, order):
        """ sort table """
        if ncol < 0 or ncol > len(self.headers):
            return
        self.layoutAboutToBeChanged.emit()
        
        self.selected.sort(key=itemgetter(ncol), reverse=(order==Qt.DescendingOrder))
                
        self.layoutChanged.emit()
    
    def flags(self, index):
        """ cell condition flag """
        # NOTE: 
        #   ItemIsEditable flag requires data() and setData() function
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    