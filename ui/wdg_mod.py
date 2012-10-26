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
# Version: $Id: wdg_mod.py 21 2012-10-26 01:48:25Z zh $

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
    # constructor / destructor
    ###############################        
    def __init__(self, app):
        """ constructor """
        super(WidgetSecondaryModifier, self).__init__()
        self.ui = Ui_widgetSecondaryModifier()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)

        self.dlgEditMod = DialogModInput(app)
        self.dlgEditMod.setModal(True)
        self.app = app

    # ui event handler
    ###############################
        
    @logUICall
    def addModifier(self):
        """ add a modifier to mapping scheme. update table view """
        
        # show edit dialogbox for new modifier
        self.dlgEditMod.setNode(self.ms, None, addNew=True)        
        ans = self.dlgEditMod.exec_()
        
        # accepted means apply change
        if ans == QDialog.Accepted:
            # NOTE: dlgEditMod already should have performed all the checks on 
            #       values/weights pair, we can safely assume that data is clean 
            #       to be used            
            self.dlgEditMod.node.update_modifier(self.dlgEditMod.values,
                                                 self.dlgEditMod.weights)
            self.app.visualizeMappingScheme(self.ms)
                    
    @logUICall
    def deleteModifier(self):
        """ delete selected modifier from mapping scheme. update table view """
        mod = self.getSelectedModifier()
        # make sure there is mod selected
        if mod is None:
            QMessageBox.warning(self, 
                                get_ui_string("app.warning.title"),
                                get_ui_string("widget.ms.warning.node.required"))
            return
        # confirm delete 
        answer = QMessageBox.warning(self,
                                     get_ui_string("app.popup.delete.confirm"),
                                     get_ui_string("widget.mod.warning.delete"),
                                     QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            # find node for selected modfiier
            [zone_name, level1, level2, level3, startIdx, endIdx, modidx, modifier] = mod
            stats = self.ms.get_assignment_by_name(zone_name)
            node = stats.find_node([level1, level2, level3])
            if node is not None:
                # remove modfiier
                node.removeModifier(modidx)            
            self.app.visualizeMappingScheme(self.ms)
        
    @logUICall
    def editModifier(self):
        """ edit selected modifier """
        mod = self.getSelectedModifier()
        # make sure there is mod selected
        if mod is None:
            QMessageBox.warning(self, 
                                get_ui_string("app.warning.title"),
                                get_ui_string("widget.ms.warning.node.required"))
            return
        
        # show edit dialogbox for selected modifier
        self.dlgEditMod.setNode(self.ms, mod)
        ans = self.dlgEditMod.exec_()
        
        # accepted means apply change
        if ans == QDialog.Accepted:
            # NOTE: dlgEditMod already should have performed all the checks on 
            #       values/weights pair, we can safely assume that data is clean 
            #       to be used            
            self.dlgEditMod.node.update_modifier(self.dlgEditMod.values,
                                                 self.dlgEditMod.weights,
                                                 self.dlgEditMod.modidx)
            self.app.visualizeMappingScheme(self.ms)
        
    @logUICall
    def applyMS(self):
        """ apply mapping scheme and modifiers """
        self.app.buildExposure()

    # public methods
    ###############################

    @logUICall
    def showMappingScheme(self, ms):
        self.ms = ms
        tableUI = self.ui.table_mod
        tableUI.setModel(MSTableModel(ms))        
        tableUI.resizeRowsToContents()
        tableUI.setSelectionMode(QAbstractItemView.SingleSelection)        
        self.ui.btn_add_mod.setEnabled(True)
        self.ui.btn_del_mod.setEnabled(True)
        self.ui.btn_edit_mod.setEnabled(True)
        self.ui.btn_build_exposure.setEnabled(True)
    
    def closeMappingScheme(self):
        """ clear current view """
        self.ui.table_mod.setModel(None)
        self.ui.btn_add_mod.setEnabled(False)
        self.ui.btn_del_mod.setEnabled(False)
        self.ui.btn_edit_mod.setEnabled(False)
        self.ui.btn_build_exposure.setEnabled(False)

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
        