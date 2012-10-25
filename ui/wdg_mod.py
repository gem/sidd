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
# Version: $Id: wdg_mod.py 18 2012-10-24 20:21:41Z zh $

"""
Widget (Panel) for managing secondary modifier 
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from sidd.ms import *

from ui.exception import SIDDUIException
from ui.constants import logUICall, get_ui_string
from ui.qt.wdg_mod_ui import Ui_widgetSecondaryModifier
from ui.helper.ms_table import MSTableModel
from ui.dlg_mod_input import DialogModInput

class WidgetSecondaryModifier(Ui_widgetSecondaryModifier, QWidget):
    """
    Widget (Panel) for managing secondary modifier 
    """
    
    def __init__(self, app):
        """ constructor """
        super(WidgetSecondaryModifier, self).__init__()
        self.ui = Ui_widgetSecondaryModifier()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)

        self.dlgEditMod = DialogModInput(app)
        self.dlgEditMod.setModal(True)
        self.app = app
    
    @logUICall
    def addModifier(self):
        """ add a modifier to the tree (and the table view) """
        self.dlgEditMod.setNode(self.ms, None, addNew=True)
        ans = self.dlgEditMod.exec_()
        if ans == QDialog.Accepted:
            print self.dlgEditMod.node
            print self.dlgEditMod.values
            print self.dlgEditMod.weights
            self.dlgEditMod.node.update_modifier(self.dlgEditMod.values,
                                                 self.dlgEditMod.weights)
            self.app.visualizeMappingScheme(self.ms)
                    
    @logUICall
    def deleteModifier(self):
        """ delete selected modifier from the tree (and the table view) """
        mod = self.getSelectedModifier()
        if mod is None:
            QMessageBox.warning(self, 
                                get_ui_string("app.warning.title"),
                                get_ui_string("widget.ms.warning.node.required"))
            return
                        
        answer = QMessageBox.warning(self,
                                     get_ui_string("app.popup.delete.confirm"),
                                     get_ui_string("widget.mod.warning.delete"),
                                     QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            [zone_name, level1, level2, level3, startIdx, endIdx, modidx, modifier] = mod
            stats = self.ms.get_assignment_by_name(zone_name)
            node = stats.find_node([level1, level2, level3])
            print 'node found', node
            if node is not None:
                node.removeModifier(modidx)
            self.app.visualizeMappingScheme(self.ms)
        
    @logUICall
    def editModifier(self):
        """ edit selected modifier """
        mod = self.getSelectedModifier()
        if mod is None:
            QMessageBox.warning(self, 
                                get_ui_string("app.warning.title"),
                                get_ui_string("widget.ms.warning.node.required"))
            return
        
        self.dlgEditMod.setNode(self.ms, mod)
        ans = self.dlgEditMod.exec_()
        if ans == QDialog.Accepted:
            self.dlgEditMod.node.update_modifier(self.dlgEditMod.values,
                                                 self.dlgEditMod.weights,
                                                 self.dlgEditMod.modidx)
            self.app.visualizeMappingScheme(self.ms)
        
    @logUICall
    def applyMS(self):
        """ apply mapping scheme and modifiers """
        self.app.buildExposure()

    @logUICall
    def showMappingScheme(self, ms):
        self.ms = ms
        tableUI = self.ui.table_mod
        tableUI.setModel(MSTableModel(ms))        
        tableUI.resizeRowsToContents()
        tableUI.setSelectionMode(QAbstractItemView.SingleSelection)        

    # internal helper methods
    ###############################
    
    def getSelectedModifier(self):
        selected =self.ui.table_mod.selectedIndexes() 
        if (len(selected) > 0):
            return selected[0].internalPointer()
        else:
            return None

    def retranslateUi(self, ui):
        ui.lb_panel_title.setText(get_ui_string("widget.mod.title"))        
        ui.btn_build_exposure.setText(get_ui_string("widget.mod.build"))
        