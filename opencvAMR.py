import cv2
import numpy as np
import time
import serial

# Initialize serial communication
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace '/dev/ttyUSB0' with the correct port

def detect_object(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([64, 114, 30])
    upper = np.array([97, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Simpan area setiap kontur
    areas = [cv2.contourArea(c) for c in contours]

    # Ambil dua kontur dengan area terbesar
    sorted_areas = sorted(zip(areas, contours), key=lambda x: x[0], reverse=True)[:2]

    detected_boxes = 0  # Menghitung jumlah bounding box yang terdeteksi

    connected = False
    for area, contour in sorted_areas:
        x, y, w, h = cv2.boundingRect(contour)

        # Hitung titik tengah bounding box
        center_x = x + w // 2
        center_y = y + h // 2

        # Gambar bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Gambar titik tengah
        cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

        height, width, _ = frame.shape
        mid_x = width // 2
        # Gambar garis vertikal di tengah-tengah kamera
        cv2.line(frame, (mid_x, 0), (mid_x, height), (0, 0, 255), 2)

        if not connected:
            start_point = (center_x, center_y)
            connected = True
        else:
            end_point = (center_x, center_y)
            connected = False
            # Menghitung titik tengah pada garis penghubung
            mid_point = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)
            # Menggambar garis penghubung antara dua bounding box
            cv2.line(frame, start_point, end_point, (255, 255, 0), 2)
            # Menggambar titik tengah garis penghubung
            cv2.circle(frame, mid_point, 5, (0, 255, 255), -1)
            
            # Menggambar garis penghubung dari titik tengah garis penghubung ke garis vertikal
            cv2.line(frame, mid_point, (mid_x, mid_point[1]), (0, 255, 255), 2)

            # Menghitung nilai PWM berdasarkan posisi relatif terhadap garis vertikal tengah
            pwm_range = 500  # Rentang nilai PWM yang dapat diatur
            base_pwm = 1500  # Nilai PWM awal

            if mid_point[0] > mid_x:  # Jika di sebelah kanan garis vertikal
                distance = mid_point[0] - mid_x
                pwm = min(base_pwm + distance * (pwm_range / mid_x), base_pwm + pwm_range)  # Atur nilai PWM analog dari 1500 hingga 2000
            elif mid_point[0] < mid_x:  # Jika di sebelah kiri garis vertikal
                distance = mid_x - mid_point[0]
                pwm = max(base_pwm - distance * (pwm_range / mid_x), base_pwm - pwm_range)  # Atur nilai PWM analog dari 1500 hingga 1000
            else:
                pwm = base_pwm  # Jika berada tepat di tengah, gunakan nilai PWM default (1500)

            pwm = int(pwm)  # Ubah nilai PWM menjadi integer tanpa desimal

            print(pwm)  # Ini hanya untuk menampilkan nilai PWM di console

        detected_boxes += 1  # Menambah jumlah bounding box yang terdeteksi

    if detected_boxes == 0:  # Jika tidak ada objek yang terdeteksi
        height, width, _ = frame.shape
        mid_x = width // 2
        # Gambar garis vertikal di tengah-tengah kamera
        cv2.line(frame, (mid_x, 0), (mid_x, height), (0, 0, 255), 2)

    return frame

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 416)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 416)

start_time = time.time()
frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    detected_frame = detect_object(frame)

    # Menghitung FPS
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    # Menambahkan teks FPS ke frame
    cv2.putText(detected_frame, f'FPS: {round(fps, 2)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('Detected Object', detected_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
