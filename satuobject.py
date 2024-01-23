import cv2
import numpy as np
import time

# Fungsi untuk menghitung nilai PWM berdasarkan posisi relatif
def calculate_pwm(center_x, target_x, max_pwm):
    # Menghitung selisih posisi relatif
    relative_position = center_x - target_x

    # Normalisasi nilai ke rentang -1 hingga 1
    normalized_position = relative_position / (target_x / 2)

    # Menghitung nilai PWM analog dari -max_pwm hingga max_pwm
    pwm_value = int(normalized_position * max_pwm)

    # Batasi nilai PWM dalam rentang yang diinginkan
    pwm_value = max(min(pwm_value, max_pwm), -max_pwm)

    return pwm_value

def detect_object(frame, target_x, max_pwm, width):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([35, 100, 100])
    upper = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Menghitung koordinat titik tengah
        center_x = x + w // 2
        center_y = y + h // 2

        # Menggambar titik tengah pada frame
        cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

        # Menggambar garis penyambung antara titik tengah dan garis vertikal
        cv2.line(frame, (center_x, center_y), (width // 2, center_y), (0, 255, 255), 2)

        # Menghitung nilai PWM berdasarkan posisi relatif
        pwm_value = calculate_pwm(center_x, target_x, max_pwm)

        # Menambahkan teks PWM ke frame
        cv2.putText(frame, f'PWM: {pwm_value}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Menambahkan garis vertikal di tengah kamera
    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2)

    return frame, pwm_value

# Set nilai maksimum PWM
max_pwm_value = 500

cap = cv2.VideoCapture(3)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 416)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 416)

start_time = time.time()
frame_count = 0

# Definisi width di sini untuk mengatasi NameError
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cap.read()

    if not ret:
        break

    detected_frame, pwm_value = detect_object(frame, width // 2, max_pwm_value, width)

    # Menghitung FPS
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    # Menambahkan teks FPS ke frame
    cv2.putText(detected_frame, f'FPS: {round(fps, 2)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('Detected Object', detected_frame)

    # Lakukan sesuatu dengan nilai PWM, misalnya mengirimkannya ke perangkat keras

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
