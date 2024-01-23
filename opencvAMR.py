import cv2
import numpy as np
import time
import serial

# Open a serial connection to Arduino
#ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace '/dev/ttyUSB0' with the correct serial port and baud rate

# Initialize end_point
end_point = (0, 0)

def detect_object(frame):
    height, width, _ = frame.shape
    mid_x = width // 2  # Define mid_x at the beginning of the function

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define HSV ranges for green and red colors
    lower_green = np.array([64, 114, 30])
    upper_green = np.array([97, 255, 255])

    lower_red = np.array([0, 142, 88]) 
    upper_red = np.array([7, 231, 210])

    # Create masks for green and red colors
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # Apply morphological operations to the masks
    kernel = np.ones((5, 5), np.uint8)
    mask_green = cv2.erode(mask_green, kernel, iterations=1)
    mask_green = cv2.dilate(mask_green, kernel, iterations=1)

    mask_red = cv2.erode(mask_red, kernel, iterations=1)
    mask_red = cv2.dilate(mask_red, kernel, iterations=1)

    # Find contours in the masks
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Combine contours from both colors
    contours = contours_green + contours_red

    # Calculate areas of contours
    areas = [cv2.contourArea(c) for c in contours]

    # Sort contours based on area in descending order
    sorted_areas = sorted(zip(areas, contours), key=lambda x: x[0], reverse=True)[:2]

    detected_boxes = 0
    connected = False
    for area, contour in sorted_areas:
        x, y, w, h = cv2.boundingRect(contour)

        center_x = x + w // 2
        center_y = y + h // 2

        if area == sorted_areas[0][0]:  # Check if it's the first bounding box (green)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:  # It's the second bounding box, change the color to red
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if not connected:
            start_point = (center_x, center_y)
            connected = True
        else:
            end_point = (center_x, center_y)
            connected = False

            mid_point = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)
            cv2.line(frame, start_point, end_point, (255, 255, 0), 2)
            cv2.circle(frame, mid_point, 5, (0, 255, 255), -1)
            cv2.line(frame, mid_point, (mid_x, mid_point[1]), (0, 255, 255), 2)

            pwm_range = 500
            base_pwm = 1500

            if mid_point[0] > mid_x:
                distance = mid_point[0] - mid_x
                pwm = min(base_pwm + distance * (pwm_range / mid_x), base_pwm + pwm_range)
            elif mid_point[0] < mid_x:
                distance = mid_x - mid_point[0]
                pwm = max(base_pwm - distance * (pwm_range / mid_x), base_pwm - pwm_range)
            else:
                pwm = base_pwm

            pwm = int(pwm)

            print(pwm)
            
            # Send PWM value to Arduino
            #ser.write(str(pwm).encode('utf-8'))
            #ser.write(b'\n')  # Add a newline character to indicate the end of the message

        detected_boxes += 1

    if detected_boxes == 0:
        cv2.line(frame, (mid_x, 0), (mid_x, height), (0, 0, 255), 2)

    return frame


# OpenCV window creation
cv2.namedWindow('Detected Object', cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(2, cv2.CAP_V4L2)  # Use 0, 1, 2, etc., depending on the camera index
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 416)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 416)

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
        #ser.close()
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
