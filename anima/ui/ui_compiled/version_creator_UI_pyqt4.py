# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_files/version_creator.ui'
#
# Created: Mon Feb  2 18:45:13 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(1753, 769)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalWidget = QtGui.QWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalWidget.setObjectName(_fromUtf8("verticalWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.logged_in_as_label = QtGui.QLabel(self.verticalWidget)
        self.logged_in_as_label.setTextFormat(QtCore.Qt.AutoText)
        self.logged_in_as_label.setObjectName(_fromUtf8("logged_in_as_label"))
        self.horizontalLayout_11.addWidget(self.logged_in_as_label)
        self.logged_in_user_label = QtGui.QLabel(self.verticalWidget)
        self.logged_in_user_label.setObjectName(_fromUtf8("logged_in_user_label"))
        self.horizontalLayout_11.addWidget(self.logged_in_user_label)
        self.logout_pushButton = QtGui.QPushButton(self.verticalWidget)
        self.logout_pushButton.setObjectName(_fromUtf8("logout_pushButton"))
        self.horizontalLayout_11.addWidget(self.logout_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.line_3 = QtGui.QFrame(self.verticalWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.tasks_groupBox = QtGui.QGroupBox(self.verticalWidget)
        self.tasks_groupBox.setObjectName(_fromUtf8("tasks_groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tasks_groupBox)
        self.verticalLayout_2.setContentsMargins(-1, 9, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.my_tasks_only_checkBox = QtGui.QCheckBox(self.tasks_groupBox)
        self.my_tasks_only_checkBox.setChecked(False)
        self.my_tasks_only_checkBox.setObjectName(_fromUtf8("my_tasks_only_checkBox"))
        self.verticalLayout_2.addWidget(self.my_tasks_only_checkBox)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.search_task_lineEdit = QtGui.QLineEdit(self.tasks_groupBox)
        self.search_task_lineEdit.setObjectName(_fromUtf8("search_task_lineEdit"))
        self.horizontalLayout_4.addWidget(self.search_task_lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.tasks_treeView = QtGui.QTreeView(self.tasks_groupBox)
        self.tasks_treeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tasks_treeView.setAlternatingRowColors(True)
        self.tasks_treeView.setUniformRowHeights(True)
        self.tasks_treeView.setObjectName(_fromUtf8("tasks_treeView"))
        self.tasks_treeView.header().setCascadingSectionResizes(True)
        self.verticalLayout_2.addWidget(self.tasks_treeView)
        self.recent_files_comboBox = QtGui.QComboBox(self.tasks_groupBox)
        self.recent_files_comboBox.setObjectName(_fromUtf8("recent_files_comboBox"))
        self.verticalLayout_2.addWidget(self.recent_files_comboBox)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.find_from_path_lineEdit = QtGui.QLineEdit(self.tasks_groupBox)
        self.find_from_path_lineEdit.setObjectName(_fromUtf8("find_from_path_lineEdit"))
        self.horizontalLayout_3.addWidget(self.find_from_path_lineEdit)
        self.find_from_path_pushButton = QtGui.QPushButton(self.tasks_groupBox)
        self.find_from_path_pushButton.setObjectName(_fromUtf8("find_from_path_pushButton"))
        self.horizontalLayout_3.addWidget(self.find_from_path_pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.thumbnail_graphicsView = QtGui.QGraphicsView(self.tasks_groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thumbnail_graphicsView.sizePolicy().hasHeightForWidth())
        self.thumbnail_graphicsView.setSizePolicy(sizePolicy)
        self.thumbnail_graphicsView.setMinimumSize(QtCore.QSize(320, 180))
        self.thumbnail_graphicsView.setMaximumSize(QtCore.QSize(320, 180))
        self.thumbnail_graphicsView.setAutoFillBackground(False)
        self.thumbnail_graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.thumbnail_graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.thumbnail_graphicsView.setBackgroundBrush(brush)
        self.thumbnail_graphicsView.setInteractive(False)
        self.thumbnail_graphicsView.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.thumbnail_graphicsView.setObjectName(_fromUtf8("thumbnail_graphicsView"))
        self.verticalLayout_2.addWidget(self.thumbnail_graphicsView)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem1)
        self.upload_thumbnail_pushButton = QtGui.QPushButton(self.tasks_groupBox)
        self.upload_thumbnail_pushButton.setObjectName(_fromUtf8("upload_thumbnail_pushButton"))
        self.horizontalLayout_16.addWidget(self.upload_thumbnail_pushButton)
        self.clear_thumbnail_pushButton = QtGui.QPushButton(self.tasks_groupBox)
        self.clear_thumbnail_pushButton.setObjectName(_fromUtf8("clear_thumbnail_pushButton"))
        self.horizontalLayout_16.addWidget(self.clear_thumbnail_pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_14.addWidget(self.tasks_groupBox)
        self.new_version_groupBox = QtGui.QGroupBox(self.verticalWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.new_version_groupBox.setFont(font)
        self.new_version_groupBox.setObjectName(_fromUtf8("new_version_groupBox"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.new_version_groupBox)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.takes_label = QtGui.QLabel(self.new_version_groupBox)
        self.takes_label.setMinimumSize(QtCore.QSize(35, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.takes_label.setFont(font)
        self.takes_label.setObjectName(_fromUtf8("takes_label"))
        self.gridLayout_3.addWidget(self.takes_label, 0, 0, 1, 1)
        self.description_label = QtGui.QLabel(self.new_version_groupBox)
        self.description_label.setMinimumSize(QtCore.QSize(35, 0))
        self.description_label.setObjectName(_fromUtf8("description_label"))
        self.gridLayout_3.addWidget(self.description_label, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.takes_listWidget = QtGui.QListWidget(self.new_version_groupBox)
        self.takes_listWidget.setObjectName(_fromUtf8("takes_listWidget"))
        self.horizontalLayout_6.addWidget(self.takes_listWidget)
        self.add_take_toolButton = QtGui.QToolButton(self.new_version_groupBox)
        self.add_take_toolButton.setObjectName(_fromUtf8("add_take_toolButton"))
        self.horizontalLayout_6.addWidget(self.add_take_toolButton)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 0, 1, 1, 1)
        self.description_textEdit = QtGui.QTextEdit(self.new_version_groupBox)
        self.description_textEdit.setEnabled(True)
        self.description_textEdit.setTabChangesFocus(True)
        self.description_textEdit.setObjectName(_fromUtf8("description_textEdit"))
        self.gridLayout_3.addWidget(self.description_textEdit, 2, 1, 1, 1)
        self.repr_as_separate_takes_checkBox = QtGui.QCheckBox(self.new_version_groupBox)
        self.repr_as_separate_takes_checkBox.setObjectName(_fromUtf8("repr_as_separate_takes_checkBox"))
        self.gridLayout_3.addWidget(self.repr_as_separate_takes_checkBox, 1, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_3)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.update_paths_checkBox = QtGui.QCheckBox(self.new_version_groupBox)
        self.update_paths_checkBox.setChecked(True)
        self.update_paths_checkBox.setObjectName(_fromUtf8("update_paths_checkBox"))
        self.horizontalLayout_7.addWidget(self.update_paths_checkBox)
        self.publish_checkBox = QtGui.QCheckBox(self.new_version_groupBox)
        self.publish_checkBox.setObjectName(_fromUtf8("publish_checkBox"))
        self.horizontalLayout_7.addWidget(self.publish_checkBox)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.environment_comboBox = QtGui.QComboBox(self.new_version_groupBox)
        self.environment_comboBox.setObjectName(_fromUtf8("environment_comboBox"))
        self.horizontalLayout_2.addWidget(self.environment_comboBox)
        self.export_as_pushButton = QtGui.QPushButton(self.new_version_groupBox)
        self.export_as_pushButton.setObjectName(_fromUtf8("export_as_pushButton"))
        self.horizontalLayout_2.addWidget(self.export_as_pushButton)
        self.save_as_pushButton = QtGui.QPushButton(self.new_version_groupBox)
        self.save_as_pushButton.setDefault(True)
        self.save_as_pushButton.setObjectName(_fromUtf8("save_as_pushButton"))
        self.horizontalLayout_2.addWidget(self.save_as_pushButton)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_14.addWidget(self.new_version_groupBox)
        self.previous_versions_groupBox = QtGui.QGroupBox(self.verticalWidget)
        self.previous_versions_groupBox.setObjectName(_fromUtf8("previous_versions_groupBox"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.previous_versions_groupBox)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.show_published_only_checkBox = QtGui.QCheckBox(self.previous_versions_groupBox)
        self.show_published_only_checkBox.setObjectName(_fromUtf8("show_published_only_checkBox"))
        self.horizontalLayout_10.addWidget(self.show_published_only_checkBox)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem4)
        self.show_only_label = QtGui.QLabel(self.previous_versions_groupBox)
        self.show_only_label.setObjectName(_fromUtf8("show_only_label"))
        self.horizontalLayout_10.addWidget(self.show_only_label)
        self.version_count_spinBox = QtGui.QSpinBox(self.previous_versions_groupBox)
        self.version_count_spinBox.setMaximum(999999)
        self.version_count_spinBox.setProperty("value", 25)
        self.version_count_spinBox.setObjectName(_fromUtf8("version_count_spinBox"))
        self.horizontalLayout_10.addWidget(self.version_count_spinBox)
        self.verticalLayout_7.addLayout(self.horizontalLayout_10)
        self.previous_versions_tableWidget = QtGui.QTableWidget(self.previous_versions_groupBox)
        self.previous_versions_tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.previous_versions_tableWidget.setAlternatingRowColors(True)
        self.previous_versions_tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.previous_versions_tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.previous_versions_tableWidget.setShowGrid(False)
        self.previous_versions_tableWidget.setColumnCount(5)
        self.previous_versions_tableWidget.setObjectName(_fromUtf8("previous_versions_tableWidget"))
        self.previous_versions_tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.previous_versions_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.previous_versions_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.previous_versions_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.previous_versions_tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.previous_versions_tableWidget.setHorizontalHeaderItem(4, item)
        self.previous_versions_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.previous_versions_tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_7.addWidget(self.previous_versions_tableWidget)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label = QtGui.QLabel(self.previous_versions_groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_5.addWidget(self.label)
        self.representations_comboBox = QtGui.QComboBox(self.previous_versions_groupBox)
        self.representations_comboBox.setObjectName(_fromUtf8("representations_comboBox"))
        self.horizontalLayout_5.addWidget(self.representations_comboBox)
        self.label_2 = QtGui.QLabel(self.previous_versions_groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.ref_depth_comboBox = QtGui.QComboBox(self.previous_versions_groupBox)
        self.ref_depth_comboBox.setObjectName(_fromUtf8("ref_depth_comboBox"))
        self.horizontalLayout_5.addWidget(self.ref_depth_comboBox)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.useNameSpace_checkBox = QtGui.QCheckBox(self.previous_versions_groupBox)
        self.useNameSpace_checkBox.setChecked(True)
        self.useNameSpace_checkBox.setObjectName(_fromUtf8("useNameSpace_checkBox"))
        self.horizontalLayout_5.addWidget(self.useNameSpace_checkBox)
        self.chose_pushButton = QtGui.QPushButton(self.previous_versions_groupBox)
        self.chose_pushButton.setObjectName(_fromUtf8("chose_pushButton"))
        self.horizontalLayout_5.addWidget(self.chose_pushButton)
        self.checkUpdates_checkBox = QtGui.QCheckBox(self.previous_versions_groupBox)
        self.checkUpdates_checkBox.setChecked(True)
        self.checkUpdates_checkBox.setObjectName(_fromUtf8("checkUpdates_checkBox"))
        self.horizontalLayout_5.addWidget(self.checkUpdates_checkBox)
        self.open_pushButton = QtGui.QPushButton(self.previous_versions_groupBox)
        self.open_pushButton.setObjectName(_fromUtf8("open_pushButton"))
        self.horizontalLayout_5.addWidget(self.open_pushButton)
        self.reference_pushButton = QtGui.QPushButton(self.previous_versions_groupBox)
        self.reference_pushButton.setObjectName(_fromUtf8("reference_pushButton"))
        self.horizontalLayout_5.addWidget(self.reference_pushButton)
        self.import_pushButton = QtGui.QPushButton(self.previous_versions_groupBox)
        self.import_pushButton.setObjectName(_fromUtf8("import_pushButton"))
        self.horizontalLayout_5.addWidget(self.import_pushButton)
        self.close_pushButton = QtGui.QPushButton(self.previous_versions_groupBox)
        self.close_pushButton.setStyleSheet(_fromUtf8(""))
        self.close_pushButton.setDefault(False)
        self.close_pushButton.setFlat(False)
        self.close_pushButton.setObjectName(_fromUtf8("close_pushButton"))
        self.horizontalLayout_5.addWidget(self.close_pushButton)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_14.addWidget(self.previous_versions_groupBox)
        self.horizontalLayout_14.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_14)
        self.horizontalLayout.addWidget(self.verticalWidget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.add_take_toolButton, self.description_textEdit)
        Dialog.setTabOrder(self.description_textEdit, self.export_as_pushButton)
        Dialog.setTabOrder(self.export_as_pushButton, self.save_as_pushButton)
        Dialog.setTabOrder(self.save_as_pushButton, self.previous_versions_tableWidget)
        Dialog.setTabOrder(self.previous_versions_tableWidget, self.open_pushButton)
        Dialog.setTabOrder(self.open_pushButton, self.reference_pushButton)
        Dialog.setTabOrder(self.reference_pushButton, self.import_pushButton)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Version Creator - Stalker", None))
        self.logged_in_as_label.setText(_translate("Dialog", "<b>Logged In As:</b>", None))
        self.logged_in_user_label.setText(_translate("Dialog", "TextLabel", None))
        self.logout_pushButton.setText(_translate("Dialog", "Logout", None))
        self.tasks_groupBox.setTitle(_translate("Dialog", "Tasks", None))
        self.my_tasks_only_checkBox.setText(_translate("Dialog", "Show my tasks only", None))
        self.tasks_treeView.setToolTip(_translate("Dialog", "<html><head/><body><p>Right Click:</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To go to the <span style=\" font-weight:600;\">Dependent Tasks</span></li><li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To go to the <span style=\" font-weight:600;\">Dependee Tasks</span></li></ul><p><br/></p></body></html>", None))
        self.recent_files_comboBox.setToolTip(_translate("Dialog", "Recent Files", None))
        self.find_from_path_lineEdit.setPlaceholderText(_translate("Dialog", "Find From Path", None))
        self.find_from_path_pushButton.setText(_translate("Dialog", "Find", None))
        self.upload_thumbnail_pushButton.setText(_translate("Dialog", "Upload", None))
        self.clear_thumbnail_pushButton.setText(_translate("Dialog", "Clear", None))
        self.new_version_groupBox.setTitle(_translate("Dialog", "New Version", None))
        self.takes_label.setText(_translate("Dialog", "Take", None))
        self.description_label.setText(_translate("Dialog", "Desc.", None))
        self.add_take_toolButton.setText(_translate("Dialog", "+", None))
        self.description_textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:9pt;\"><br /></p></body></html>", None))
        self.repr_as_separate_takes_checkBox.setToolTip(_translate("Dialog", "<html><head/><body><p>Check this to show <span style=\" font-weight:600;\">Representations</span> as separate takes if available</p></body></html>", None))
        self.repr_as_separate_takes_checkBox.setText(_translate("Dialog", "Representations as separate takes", None))
        self.update_paths_checkBox.setText(_translate("Dialog", "Update Paths", None))
        self.publish_checkBox.setText(_translate("Dialog", "Publish", None))
        self.export_as_pushButton.setText(_translate("Dialog", "Export Selection As", None))
        self.save_as_pushButton.setText(_translate("Dialog", "Save As", None))
        self.previous_versions_groupBox.setTitle(_translate("Dialog", "Previous Versions", None))
        self.show_published_only_checkBox.setText(_translate("Dialog", "Show Published Only", None))
        self.show_only_label.setText(_translate("Dialog", "Show Only", None))
        self.previous_versions_tableWidget.setToolTip(_translate("Dialog", "<html><head/><body><p>Right click to:</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li><span style=\" font-weight:600;\">Copy Path</span></li><li><span style=\" font-weight:600;\">Browse Path</span></li><li><span style=\" font-weight:600;\">Change Description</span></li></ul><p>Double click to:</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Open</span></li></ul></body></html>", None))
        item = self.previous_versions_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Version", None))
        item = self.previous_versions_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "User", None))
        item = self.previous_versions_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "File Size", None))
        item = self.previous_versions_tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Date", None))
        item = self.previous_versions_tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Description", None))
        self.label.setText(_translate("Dialog", "Repr", None))
        self.representations_comboBox.setToolTip(_translate("Dialog", "Choose Representation (if supported by the environment)", None))
        self.label_2.setText(_translate("Dialog", "Refs", None))
        self.ref_depth_comboBox.setToolTip(_translate("Dialog", "Choose reference depth (if supported by environment)", None))
        self.useNameSpace_checkBox.setToolTip(_translate("Dialog", "<html><head/><body><p>Uncheck it if you are going to use <span style=\" font-weight:600;\">Alembic Cache</span>.</p></body></html>", None))
        self.useNameSpace_checkBox.setText(_translate("Dialog", "Use Namespace", None))
        self.chose_pushButton.setText(_translate("Dialog", "Choose", None))
        self.checkUpdates_checkBox.setToolTip(_translate("Dialog", "Disable update check (faster)", None))
        self.checkUpdates_checkBox.setText(_translate("Dialog", "Check Updates", None))
        self.open_pushButton.setText(_translate("Dialog", "Open", None))
        self.reference_pushButton.setText(_translate("Dialog", "Reference", None))
        self.import_pushButton.setText(_translate("Dialog", "Import", None))
        self.close_pushButton.setText(_translate("Dialog", "Close", None))

