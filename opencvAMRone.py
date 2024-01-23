import cv2
import numpy as np
import time
import serial

# Open a serial connection to Arduino
ser = serial.Serial('/dev/ttyACM1', 9600)  # Replace '/dev/ttyUSB0' with the correct serial port and baud rate

def detect_object(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([1, 107, 236])
    upper = np.array([179, 162, 255])

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        areas = [cv2.contourArea(c) for c in contours]
        sorted_areas = sorted(zip(areas, contours), key=lambda x: x[0], reverse=True)[:1]

        detected_boxes = 0

        for area, contour in sorted_areas:
            x, y, w, h = cv2.boundingRect(contour)

            center_x = x + w // 2
            center_y = y + h // 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

            height, width, _ = frame.shape
            mid_x = width // 2
            cv2.line(frame, (mid_x, 0), (mid_x, height), (0, 0, 255), 2)

            pwm_range = 500
            base_pwm = 1500

            distance = abs(center_x - mid_x)
            pwm = base_pwm + distance * (pwm_range / mid_x) if center_x > mid_x else base_pwm - distance * (pwm_range / mid_x)
            pwm = max(min(pwm, base_pwm + pwm_range), base_pwm - pwm_range)

            pwm = int(pwm)

            print(pwm)
            
            # Send PWM value to Arduino
            ser.write(str(pwm).encode('utf-8'))
            ser.write(b'\n')  # Add a newline character to indicate the end of the message

            detected_boxes += 1

        if detected_boxes == 0:
            height, width, _ = frame.shape
            mid_x = width // 2
            cv2.line(frame, (mid_x, 0), (mid_x, height), (0, 0, 255), 2)

    return frame

cap = cv2.VideoCapture(3)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

start_time = time.time()
frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    detected_frame = detect_object(frame)

    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    cv2.putText(detected_frame, f'FPS: {round(fps, 2)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('Detected Object', detected_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        ser.close()
        break

cap.release()
cv2.destroyAllWindows()
