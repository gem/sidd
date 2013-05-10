# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_edit_attributes.ui'
#
# Created: Thu Apr 25 17:06:39 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_editAttributesDialog(object):
    def setupUi(self, editAttributesDialog):
        editAttributesDialog.setObjectName(_fromUtf8("editAttributesDialog"))
        editAttributesDialog.resize(524, 301)
        self.buttonBox = QtGui.QDialogButtonBox(editAttributesDialog)
        self.buttonBox.setGeometry(QtCore.QRect(360, 270, 156, 23))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.lb_attribute_name = QtGui.QLabel(editAttributesDialog)
        self.lb_attribute_name.setGeometry(QtCore.QRect(10, 50, 100, 20))
        self.lb_attribute_name.setObjectName(_fromUtf8("lb_attribute_name"))
        self.txt_attribute_name = QtGui.QLineEdit(editAttributesDialog)
        self.txt_attribute_name.setGeometry(QtCore.QRect(100, 50, 251, 20))
        self.txt_attribute_name.setObjectName(_fromUtf8("txt_attribute_name"))
        self.lb_title = QtGui.QLabel(editAttributesDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.boxAttributes = QtGui.QGroupBox(editAttributesDialog)
        self.boxAttributes.setGeometry(QtCore.QRect(10, 140, 500, 131))
        self.boxAttributes.setObjectName(_fromUtf8("boxAttributes"))
        self.txt_modifier_value = QtGui.QLineEdit(editAttributesDialog)
        self.txt_modifier_value.setGeometry(QtCore.QRect(100, 100, 251, 20))
        self.txt_modifier_value.setObjectName(_fromUtf8("txt_modifier_value"))
        self.lb_modifier_value = QtGui.QLabel(editAttributesDialog)
        self.lb_modifier_value.setGeometry(QtCore.QRect(10, 100, 100, 20))
        self.lb_modifier_value.setObjectName(_fromUtf8("lb_modifier_value"))
        self.widget_mod_values_menu_r = QtGui.QWidget(editAttributesDialog)
        self.widget_mod_values_menu_r.setGeometry(QtCore.QRect(420, 120, 91, 23))
        self.widget_mod_values_menu_r.setObjectName(_fromUtf8("widget_mod_values_menu_r"))
        self.btn_add = QtGui.QPushButton(self.widget_mod_values_menu_r)
        self.btn_add.setGeometry(QtCore.QRect(0, 0, 31, 23))
        self.btn_add.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setObjectName(_fromUtf8("btn_add"))
        self.btn_delete = QtGui.QPushButton(self.widget_mod_values_menu_r)
        self.btn_delete.setGeometry(QtCore.QRect(30, 0, 31, 23))
        self.btn_delete.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(icon1)
        self.btn_delete.setObjectName(_fromUtf8("btn_delete"))
        self.txt_attribute = QtGui.QLineEdit(editAttributesDialog)
        self.txt_attribute.setGeometry(QtCore.QRect(100, 75, 251, 20))
        self.txt_attribute.setObjectName(_fromUtf8("txt_attribute"))
        self.lb_attribute = QtGui.QLabel(editAttributesDialog)
        self.lb_attribute.setGeometry(QtCore.QRect(10, 75, 100, 20))
        self.lb_attribute.setObjectName(_fromUtf8("lb_attribute"))

        self.retranslateUi(editAttributesDialog)
        QtCore.QMetaObject.connectSlotsByName(editAttributesDialog)

    def retranslateUi(self, editAttributesDialog):
        editAttributesDialog.setWindowTitle(QtGui.QApplication.translate("editAttributesDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_attribute_name.setText(QtGui.QApplication.translate("editAttributesDialog", "Attribute Name", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_title.setText(QtGui.QApplication.translate("editAttributesDialog", "Edit Modifier Value", None, QtGui.QApplication.UnicodeUTF8))
        self.boxAttributes.setTitle(QtGui.QApplication.translate("editAttributesDialog", "Values", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_modifier_value.setText(QtGui.QApplication.translate("editAttributesDialog", "Modifier Value", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_add.setToolTip(QtGui.QApplication.translate("editAttributesDialog", "Add value", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_delete.setToolTip(QtGui.QApplication.translate("editAttributesDialog", "Delete Last Value", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_attribute.setText(QtGui.QApplication.translate("editAttributesDialog", "Attribute", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
