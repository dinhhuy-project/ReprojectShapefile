# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Coordinate Transformer - Main Plugin
 Chuyển đổi hệ tọa độ cho các lớp dữ liệu Shapefile
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject
import os.path

from .coordinate_transformer_dialog import CoordinateTransformerDialog


class CoordinateTransformer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.
        
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = '&Coordinate Transformer'
        self.toolbar = self.iface.addToolBar('CoordinateTransformer')
        self.toolbar.setObjectName('CoordinateTransformer')
        self.dlg = None

    def add_action(self, icon_path, text, callback, enabled_flag=True,
                   add_to_menu=True, add_to_toolbar=True, status_tip=None,
                   whats_this=None, parent=None):
        """Add a toolbar icon to the toolbar."""
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.iface.addPluginToVectorMenu(self.menu, action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, 'icon.jpg')
        self.add_action(
            icon_path,
            text='Chuyển đổi hệ tọa độ',
            callback=self.run,
            parent=self.iface.mainWindow(),
            status_tip='Chuyển đổi hệ tọa độ Shapefile'
        )

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu('&Coordinate Transformer', action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        """Run method that performs all the real work."""
        if self.dlg is None:
            self.dlg = CoordinateTransformerDialog(self.iface)
        
        self.dlg.populate_layers()
        self.dlg.show()
        self.dlg.exec_()