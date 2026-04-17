import cv2
import matplotlib.pyplot as plt
import numpy as np

# 1. Tải ảnh (Thay link ảnh bên dưới bằng ảnh văn bản của bạn)
# !wget https://your-link-to-image.jpg -O sample.jpg
# Ở đây ta giả định đã có file 'sample.jpg'
image_path = 'example.png'
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 2. Chuyển sang ảnh xám
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 3. Nhị phân hóa (Binarization) - Đưa về đen trắng hoàn toàn
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Hiển thị kết quả so sánh
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1); plt.title("Ảnh gốc"); plt.imshow(img_rgb)
plt.subplot(1, 3, 2); plt.title("Ảnh xám"); plt.imshow(gray, cmap='gray')
plt.subplot(1, 3, 3); plt.title("Nhị phân hóa"); plt.imshow(thresh, cmap='gray')
plt.show()