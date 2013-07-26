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
dialog for editing mapping scheme branches
"""
from PyQt4.QtGui import QDialog, QCloseEvent, QAbstractItemView
from PyQt4.QtCore import Qt, pyqtSlot, QSettings, QVariant, QString, QAbstractTableModel
from operator import itemgetter

from sidd.constants import logAPICall, SIDD_COMPANY, SIDD_APP_NAME, SIDD_VERSION, CNT_FIELD_NAME

from ui.constants import logUICall, UI_PADDING
from ui.qt.dlg_res_detail_ui import Ui_tablePreviewDialog

class DialogResult(Ui_tablePreviewDialog, QDialog):
    """
    dialog for visualize result details
    """
    
    # CONSTANTS
    #############################    
    UI_WINDOW_GEOM = 'dlg_result/geometry'
        
    # constructor
    ###############################     
    def __init__(self):
        super(DialogResult, self).__init__()
        self.ui = Ui_tablePreviewDialog()        
        self.ui.setupUi(self)
        
        self.ui.table_result.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.table_result.setSortingEnabled(True)
        
        # connect slots (ui event)
        self.ui.btn_ok.clicked.connect(self.accept)
    
        self.settings = QSettings(SIDD_COMPANY, '%s %s' %(SIDD_APP_NAME, SIDD_VERSION));
        self.restoreGeometry(self.settings.value(self.UI_WINDOW_GEOM).toByteArray());
    
    # window event handler overrides
    #############################
    def resizeEvent(self, event):
        """ handle window resize """        
        self.ui.table_result.resize(self.width()-2*UI_PADDING,
                                    self.height() - self.ui.table_result.y()-self.ui.btn_ok.height()-2*UI_PADDING)                        
        below_table = self.height() - self.ui.btn_ok.height() - UI_PADDING
        self.ui.lb_bldgcount.move(UI_PADDING, below_table)        
        self.ui.txt_bldgcount.move(self.ui.lb_bldgcount.width()+(2*UI_PADDING), below_table)
        self.ui.btn_ok.move(self.width()-UI_PADDING-self.ui.btn_ok.width(), below_table)

    @pyqtSlot(QCloseEvent)
    def closeEvent(self, event):
        self.settings.setValue(self.UI_WINDOW_GEOM, self.saveGeometry());
        super(DialogResult, self).closeEvent(event)
        
    # public method
    ###############################     
    
    @logUICall
    def showExposureData(self, header, selected):
        """
        display selected rows with header
        """
        fnames =[]      # retrieve field name as table headers
        cnt_sum = 0     # total number of buildings 
                
        # find index for building count field
        cnt_idx = -1
        for i, f in header.iteritems():
            fnames.append(f.name())
            if f.name() == CNT_FIELD_NAME:
                cnt_idx = i        
        if cnt_idx <> -1:   # building count index is found
            # increment building count
            for s in selected:
                cnt_sum  += s[cnt_idx].toDouble()[0]
                
        # display result 
        self.resultDetailModel = ResultDetailTableModel(header.values(), selected)        
        self.ui.table_result.setModel(self.resultDetailModel)
        self.ui.table_result.sortByColumn(3, Qt.AscendingOrder)        
        # display exposure specific ui elements         
        self.ui.txt_bldgcount.setVisible(True) 
        self.ui.lb_bldgcount.setVisible(True)
        self.ui.txt_bldgcount.setText('%d'% round(cnt_sum))
        self.ui.txt_bldgcount.setReadOnly(True)        

    @logUICall
    def showInfoData(self, header, selected):
        # sync UI 
        self.resultDetailModel = ResultDetailTableModel(header.values(), selected)        
        self.ui.table_result.setModel(self.resultDetailModel)                
        # hide exposure specific ui elements 
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
        # this format makes it easier to sort
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
        return Qt.ItemIsEnabled 
    