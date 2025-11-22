# Hướng dẫn Cài đặt và Sử dụng Plugin Coordinate Transformer

## 1. Cấu trúc thư mục Plugin

```
coordinate_transformer/
├── __init__.py              # File khởi tạo plugin
├── metadata.txt             # Thông tin metadata
├── mainPlugin.py            # File chính của plugin
├── coordinate_transformer_dialog.py  # Giao diện và logic xử lý
├── resources.qrc            # File tài nguyên Qt
├── icon.jpg                 # Icon của plugin (32x32 pixels)
└── LICENSE                  # Giấy phép sử dụng
```

## 2. Cài đặt Plugin

### Cách 1: Cài đặt thủ công
1. Tìm thư mục plugins của QGIS:
   - **Windows**: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

2. Copy thư mục `coordinate_transformer` vào thư mục plugins

3. Khởi động lại QGIS

4. Vào menu **Plugins** → **Manage and Install Plugins** → Tab **Installed**

5. Tìm "Coordinate Transformer" và đánh dấu checkbox để kích hoạt

### Cách 2: Cài từ file ZIP
1. Nén thư mục `coordinate_transformer` thành file `.zip`
2. Trong QGIS: **Plugins** → **Manage and Install Plugins** → **Install from ZIP**
3. Chọn file ZIP và cài đặt

## 3. Sử dụng Plugin

### Bước 1: Mở Plugin
- Click vào icon trên toolbar, hoặc
- Vào menu **Vector** → **Coordinate Transformer** → **Chuyển đổi hệ tọa độ**

### Bước 2: Chọn lớp dữ liệu nguồn
- **Cách 1**: Chọn layer từ danh sách các layer đang mở trong Project
- **Cách 2**: Click "Duyệt..." để chọn file Shapefile từ máy tính

→ Hệ tọa độ hiện tại sẽ được hiển thị tự động

### Bước 3: Chọn hệ tọa độ đích
- Chọn từ danh sách các hệ tọa độ phổ biến (VN-2000, UTM, WGS84...)
- Hoặc click "Chọn từ danh sách QGIS..." để chọn hệ tọa độ khác

### Bước 4: Chọn nơi lưu file kết quả
- Click "Duyệt..." để chọn đường dẫn và tên file output

### Bước 5: Thực hiện chuyển đổi
- Click nút **"Chuyển đổi"**
- Đợi quá trình hoàn thành
- Layer mới sẽ tự động được thêm vào Project

## 4. Các hệ tọa độ được hỗ trợ sẵn

| EPSG Code | Tên hệ tọa độ |
|-----------|---------------|
| EPSG:4326 | WGS 84 (Địa lý) |
| EPSG:32648 | WGS 84 / UTM zone 48N |
| EPSG:32649 | WGS 84 / UTM zone 49N |
| EPSG:4756 | VN-2000 |
| EPSG:3405 | VN-2000 / UTM zone 48N |
| EPSG:3406 | VN-2000 / UTM zone 49N |
| EPSG:5896 | VN-2000 / TM-3 zone 481 |
| EPSG:5897 | VN-2000 / TM-3 zone 482 |
| EPSG:5898 | VN-2000 / TM-3 zone 491 |
| EPSG:9210 | VN-2000 / TM-3 105-00 |
| EPSG:9211 | VN-2000 / TM-3 105-30 |
| EPSG:9212 | VN-2000 / TM-3 106-00 |

## 5. Lưu ý quan trọng

⚠️ **Trước khi chuyển đổi:**
- Backup dữ liệu gốc
- Xác định đúng hệ tọa độ nguồn
- Chọn đúng hệ tọa độ đích phù hợp với vùng địa lý

⚠️ **Về VN-2000:**
- VN-2000 có nhiều múi chiếu khác nhau tùy theo tỉnh/thành phố
- Kiểm tra kỹ múi chiếu và kinh tuyến trục trước khi chuyển đổi

## 6. Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Cách khắc phục |
|-----|-------------|----------------|
| Plugin không hiển thị | Chưa kích hoạt | Vào Manage Plugins và enable |
| Không đọc được Shapefile | File lỗi hoặc thiếu file .shx, .dbf | Kiểm tra các file đi kèm |
| CRS không xác định | Layer chưa có CRS | Gán CRS cho layer trước |
| Lỗi khi chuyển đổi | Sai tham số CRS | Kiểm tra lại hệ tọa độ |

## 7. Liên hệ hỗ trợ

- Email: buidinhhuy900@gmail.com
- GitHub Issues: https://github.com/dinhhuy-project/ReprojectShapefile/issues