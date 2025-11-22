# -*- coding: utf-8 -*-
"""
Coordinate Transformer Dialog - Giao diện và xử lý logic chuyển đổi tọa độ
"""

import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (QDialog, QFileDialog, QMessageBox, 
                                  QVBoxLayout, QHBoxLayout, QLabel, 
                                  QComboBox, QPushButton, QLineEdit,
                                  QGroupBox, QProgressBar)
from qgis.PyQt.QtCore import Qt
from qgis.core import (QgsProject, QgsVectorLayer, QgsVectorFileWriter,
                       QgsCoordinateReferenceSystem, QgsCoordinateTransform,
                       QgsWkbTypes)


class CoordinateTransformerDialog(QDialog):
    """Dialog for Coordinate Transformer plugin."""

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(CoordinateTransformerDialog, self).__init__(parent)
        self.iface = iface
        self.setup_ui()
        self.setup_connections()
        
        # Danh sách các hệ tọa độ phổ biến tại Việt Nam
        self.crs_list = [
            ("EPSG:4326", "WGS 84 (Địa lý)"),
            ("EPSG:32648", "WGS 84 / UTM zone 48N"),
            ("EPSG:32649", "WGS 84 / UTM zone 49N"),
            ("EPSG:4756", "VN-2000"),
            ("EPSG:3405", "VN-2000 / UTM zone 48N"),
            ("EPSG:3406", "VN-2000 / UTM zone 49N"),
            ("EPSG:5896", "VN-2000 / TM-3 zone 481"),
            ("EPSG:5897", "VN-2000 / TM-3 zone 482"),
            ("EPSG:5898", "VN-2000 / TM-3 zone 491"),
            ("EPSG:9210", "VN-2000 / TM-3 105-00"),
            ("EPSG:9211", "VN-2000 / TM-3 105-30"),
            ("EPSG:9212", "VN-2000 / TM-3 106-00"),
            ("EPSG:9213", "VN-2000 / TM-3 106-30"),
            ("EPSG:9214", "VN-2000 / TM-3 107-00"),
            ("EPSG:9215", "VN-2000 / TM-3 107-30"),
        ]

    def setup_ui(self):
        """Thiết lập giao diện người dùng."""
        self.setWindowTitle("Chuyển đổi Hệ tọa độ Shapefile")
        self.setMinimumWidth(550)
        self.setMinimumHeight(400)
        
        main_layout = QVBoxLayout()
        
        # === Group 1: Chọn lớp dữ liệu nguồn ===
        source_group = QGroupBox("1. Lớp dữ liệu nguồn")
        source_layout = QVBoxLayout()
        
        # Combobox chọn layer từ project
        layer_layout = QHBoxLayout()
        layer_layout.addWidget(QLabel("Chọn lớp từ Project:"))
        self.cbo_layers = QComboBox()
        self.cbo_layers.setMinimumWidth(300)
        layer_layout.addWidget(self.cbo_layers)
        source_layout.addLayout(layer_layout)
        
        # Hoặc browse shapefile
        browse_layout = QHBoxLayout()
        browse_layout.addWidget(QLabel("Hoặc chọn Shapefile:"))
        self.txt_input_path = QLineEdit()
        self.txt_input_path.setReadOnly(True)
        browse_layout.addWidget(self.txt_input_path)
        self.btn_browse_input = QPushButton("Duyệt...")
        browse_layout.addWidget(self.btn_browse_input)
        source_layout.addLayout(browse_layout)
        
        # Hiển thị hệ tọa độ hiện tại
        current_crs_layout = QHBoxLayout()
        current_crs_layout.addWidget(QLabel("Hệ tọa độ hiện tại:"))
        self.lbl_current_crs = QLabel("<chưa chọn lớp dữ liệu>")
        self.lbl_current_crs.setStyleSheet("font-weight: bold; color: #0066cc;")
        current_crs_layout.addWidget(self.lbl_current_crs)
        current_crs_layout.addStretch()
        source_layout.addLayout(current_crs_layout)
        
        source_group.setLayout(source_layout)
        main_layout.addWidget(source_group)
        
        # === Group 2: Chọn hệ tọa độ đích ===
        target_group = QGroupBox("2. Hệ tọa độ đích")
        target_layout = QVBoxLayout()
        
        target_crs_layout = QHBoxLayout()
        target_crs_layout.addWidget(QLabel("Chọn hệ tọa độ mới:"))
        self.cbo_target_crs = QComboBox()
        self.cbo_target_crs.setMinimumWidth(300)
        target_crs_layout.addWidget(self.cbo_target_crs)
        target_layout.addLayout(target_crs_layout)
        
        # Nút chọn CRS khác từ QGIS
        other_crs_layout = QHBoxLayout()
        other_crs_layout.addWidget(QLabel("Hoặc chọn CRS khác:"))
        self.btn_select_crs = QPushButton("Chọn từ danh sách QGIS...")
        other_crs_layout.addWidget(self.btn_select_crs)
        other_crs_layout.addStretch()
        target_layout.addLayout(other_crs_layout)
        
        # Hiển thị CRS đã chọn
        selected_crs_layout = QHBoxLayout()
        selected_crs_layout.addWidget(QLabel("CRS đã chọn:"))
        self.lbl_selected_crs = QLabel("<chưa chọn>")
        self.lbl_selected_crs.setStyleSheet("font-weight: bold; color: #009933;")
        selected_crs_layout.addWidget(self.lbl_selected_crs)
        selected_crs_layout.addStretch()
        target_layout.addLayout(selected_crs_layout)
        
        target_group.setLayout(target_layout)
        main_layout.addWidget(target_group)
        
        # === Group 3: Lưu kết quả ===
        output_group = QGroupBox("3. Lưu kết quả")
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Đường dẫn lưu:"))
        self.txt_output_path = QLineEdit()
        output_layout.addWidget(self.txt_output_path)
        self.btn_browse_output = QPushButton("Duyệt...")
        output_layout.addWidget(self.btn_browse_output)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # === Progress bar ===
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # === Buttons ===
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.btn_transform = QPushButton("Chuyển đổi")
        self.btn_transform.setMinimumWidth(120)
        self.btn_transform.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        button_layout.addWidget(self.btn_transform)
        self.btn_close = QPushButton("Đóng")
        self.btn_close.setMinimumWidth(80)
        button_layout.addWidget(self.btn_close)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def setup_connections(self):
        """Thiết lập các kết nối tín hiệu."""
        self.cbo_layers.currentIndexChanged.connect(self.on_layer_changed)
        self.btn_browse_input.clicked.connect(self.browse_input_shapefile)
        self.btn_browse_output.clicked.connect(self.browse_output_path)
        self.btn_select_crs.clicked.connect(self.select_crs_from_dialog)
        self.cbo_target_crs.currentIndexChanged.connect(self.on_target_crs_changed)
        self.btn_transform.clicked.connect(self.transform_coordinates)
        self.btn_close.clicked.connect(self.close)

    def populate_layers(self):
        """Đổ danh sách các lớp vector từ project hiện tại."""
        self.cbo_layers.clear()
        self.cbo_layers.addItem("-- Chọn lớp dữ liệu --", None)
        
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if isinstance(layer, QgsVectorLayer):
                self.cbo_layers.addItem(layer.name(), layer.id())
        
        # Đổ danh sách CRS
        self.cbo_target_crs.clear()
        self.cbo_target_crs.addItem("-- Chọn hệ tọa độ --", None)
        for epsg, name in self.crs_list:
            self.cbo_target_crs.addItem(f"{name} ({epsg})", epsg)

    def on_layer_changed(self, index):
        """Xử lý khi người dùng chọn layer khác."""
        layer_id = self.cbo_layers.currentData()
        if layer_id:
            layer = QgsProject.instance().mapLayer(layer_id)
            if layer:
                crs = layer.crs()
                self.lbl_current_crs.setText(f"{crs.authid()} - {crs.description()}")
                self.txt_input_path.clear()
        else:
            self.lbl_current_crs.setText("<chưa chọn lớp dữ liệu>")

    def browse_input_shapefile(self):
        """Mở dialog chọn file shapefile nguồn."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn Shapefile nguồn", "", 
            "Shapefile (*.shp);;All Files (*)"
        )
        if file_path:
            self.txt_input_path.setText(file_path)
            self.cbo_layers.setCurrentIndex(0)
            
            # Load và hiển thị CRS
            temp_layer = QgsVectorLayer(file_path, "temp", "ogr")
            if temp_layer.isValid():
                crs = temp_layer.crs()
                self.lbl_current_crs.setText(f"{crs.authid()} - {crs.description()}")
            else:
                self.lbl_current_crs.setText("<Không đọc được file>")

    def browse_output_path(self):
        """Mở dialog chọn đường dẫn lưu file kết quả."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu Shapefile kết quả", "", 
            "Shapefile (*.shp);;All Files (*)"
        )
        if file_path:
            if not file_path.lower().endswith('.shp'):
                file_path += '.shp'
            self.txt_output_path.setText(file_path)

    def select_crs_from_dialog(self):
        """Mở dialog chọn CRS từ QGIS."""
        from qgis.gui import QgsProjectionSelectionDialog
        
        dialog = QgsProjectionSelectionDialog(self)
        dialog.setWindowTitle("Chọn Hệ tọa độ")
        
        if dialog.exec_():
            crs = dialog.crs()
            self.selected_custom_crs = crs
            self.lbl_selected_crs.setText(f"{crs.authid()} - {crs.description()}")
            self.cbo_target_crs.setCurrentIndex(0)

    def on_target_crs_changed(self, index):
        """Xử lý khi người dùng chọn CRS từ combobox."""
        epsg = self.cbo_target_crs.currentData()
        if epsg:
            crs = QgsCoordinateReferenceSystem(epsg)
            self.lbl_selected_crs.setText(f"{crs.authid()} - {crs.description()}")
            self.selected_custom_crs = None

    def get_source_layer(self):
        """Lấy layer nguồn từ project hoặc từ file."""
        layer_id = self.cbo_layers.currentData()
        if layer_id:
            return QgsProject.instance().mapLayer(layer_id)
        elif self.txt_input_path.text():
            return QgsVectorLayer(self.txt_input_path.text(), "source", "ogr")
        return None

    def get_target_crs(self):
        """Lấy CRS đích."""
        if hasattr(self, 'selected_custom_crs') and self.selected_custom_crs:
            return self.selected_custom_crs
        epsg = self.cbo_target_crs.currentData()
        if epsg:
            return QgsCoordinateReferenceSystem(epsg)
        return None

    def transform_coordinates(self):
        """Thực hiện chuyển đổi tọa độ."""
        # Kiểm tra đầu vào
        source_layer = self.get_source_layer()
        if not source_layer or not source_layer.isValid():
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn lớp dữ liệu nguồn hợp lệ!")
            return
        
        target_crs = self.get_target_crs()
        if not target_crs or not target_crs.isValid():
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn hệ tọa độ đích!")
            return
        
        output_path = self.txt_output_path.text()
        if not output_path:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đường dẫn lưu file!")
            return
        
        # Kiểm tra nếu CRS nguồn và đích giống nhau
        if source_layer.crs() == target_crs:
            QMessageBox.warning(self, "Cảnh báo", 
                "Hệ tọa độ nguồn và đích giống nhau!\nKhông cần chuyển đổi.")
            return
        
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(10)
            
            # Thực hiện chuyển đổi sử dụng QgsVectorFileWriter
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = "ESRI Shapefile"
            options.fileEncoding = "UTF-8"
            
            # Thiết lập transform context
            transform_context = QgsProject.instance().transformContext()
            
            self.progress_bar.setValue(30)
            
            # Ghi file với CRS mới
            error = QgsVectorFileWriter.writeAsVectorFormatV3(
                source_layer,
                output_path,
                transform_context,
                options
            )
            
            self.progress_bar.setValue(50)
            
            # Tạo layer với CRS mới từ file tạm, rồi reproject
            # Phương pháp tốt hơn: sử dụng native:reprojectlayer
            import processing
            
            result = processing.run("native:reprojectlayer", {
                'INPUT': source_layer,
                'TARGET_CRS': target_crs,
                'OUTPUT': output_path
            })
            
            self.progress_bar.setValue(80)
            
            # Load layer kết quả vào project
            layer_name = os.path.splitext(os.path.basename(output_path))[0]
            new_layer = QgsVectorLayer(output_path, f"{layer_name}_transformed", "ogr")
            
            if new_layer.isValid():
                QgsProject.instance().addMapLayer(new_layer)
                
                # Zoom để hiển thị cả 2 layer
                self.iface.mapCanvas().setExtent(new_layer.extent())
                self.iface.mapCanvas().refresh()
                
                self.progress_bar.setValue(100)
                
                QMessageBox.information(self, "Thành công", 
                    f"Đã chuyển đổi thành công!\n\n"
                    f"Từ: {source_layer.crs().authid()}\n"
                    f"Sang: {target_crs.authid()}\n\n"
                    f"File đã lưu tại:\n{output_path}\n\n"
                    f"Layer mới đã được thêm vào Project.")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể tạo layer kết quả!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chuyển đổi:\n{str(e)}")
        finally:
            self.progress_bar.setVisible(False)
            self.progress_bar.setValue(0)