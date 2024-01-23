import cv2
import numpy as np

def nothing(x):
    pass

# Inisialisasi webcam
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Use 0, 1, 2, etc., depending on the camera index
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 416)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 416)

# Buat jendela GUI untuk kalibrasi
cv2.namedWindow('Calibration')
cv2.createTrackbar('Lower Hue', 'Calibration', 0, 179, nothing)
cv2.createTrackbar('Upper Hue', 'Calibration', 179, 179, nothing)
cv2.createTrackbar('Lower Saturation', 'Calibration', 0, 255, nothing)
cv2.createTrackbar('Upper Saturation', 'Calibration', 255, 255, nothing)
cv2.createTrackbar('Lower Value', 'Calibration', 0, 255, nothing)
cv2.createTrackbar('Upper Value', 'Calibration', 255, 255, nothing)

while True:
    # Ambil frame dari webcam
    ret, frame = cap.read()
    
    # Baca nilai trackbar
    lower_hue = cv2.getTrackbarPos('Lower Hue', 'Calibration')
    upper_hue = cv2.getTrackbarPos('Upper Hue', 'Calibration')
    lower_saturation = cv2.getTrackbarPos('Lower Saturation', 'Calibration')
    upper_saturation = cv2.getTrackbarPos('Upper Saturation', 'Calibration')
    lower_value = cv2.getTrackbarPos('Lower Value', 'Calibration')
    upper_value = cv2.getTrackbarPos('Upper Value', 'Calibration')
    
    # Mengubah gambar ke ruang warna HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Tentukan rentang warna sesuai dengan nilai dari trackbar
    lower_color = np.array([lower_hue, lower_saturation, lower_value])
    upper_color = np.array([upper_hue, upper_saturation, upper_value])
    
    # Membuat mask untuk warna yang ditentukan
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Menampilkan frame webcam dan mask
    cv2.imshow('Webcam Feed', frame)
    cv2.imshow('Mask', mask)
    
    # Keluar dari loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bebaskan sumber daya dan tutup jendela
cap.release()
cv2.destroyAllWindows()