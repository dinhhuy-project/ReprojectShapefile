# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Coordinate Transformer
                                 A QGIS plugin
 Chuyển đổi hệ tọa độ cho các lớp dữ liệu Shapefile
                             -------------------
        begin                : 2024-01-01
        copyright            : (C) 2024 by Your Name
        email                : your.email@example.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


def classFactory(iface):
    """Load CoordinateTransformer class from file mainPlugin.
    
    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .mainPlugin import CoordinateTransformer
    return CoordinateTransformer(iface)