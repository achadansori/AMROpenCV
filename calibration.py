import cv2
import numpy as np

def calibrate_color(frame, color_name):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.namedWindow(f'Calibrate {color_name}')
    cv2.createTrackbar(f'Lower H {color_name}', f'Calibrate {color_name}', 0, 255, lambda x: None)
    cv2.createTrackbar(f'Upper H {color_name}', f'Calibrate {color_name}', 0, 255, lambda x: None)

    while True:
        # Get current trackbar positions
        lower_h = cv2.getTrackbarPos(f'Lower H {color_name}', f'Calibrate {color_name}')
        upper_h = cv2.getTrackbarPos(f'Upper H {color_name}', f'Calibrate {color_name}')

        # Define lower and upper bounds for the color range
        lower_bound = np.array([lower_h, 50, 50])
        upper_bound = np.array([upper_h, 255, 255])

        # Create a mask using the current color range
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

        # Apply the mask to the original frame
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Display the frame and the resulting mask
        cv2.imshow(f'Calibrate {color_name}', np.hstack([frame, result]))

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyWindow(f'Calibrate {color_name}')

    return lower_bound, upper_bound

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow('Original Frame', frame)

        key = cv2.waitKey(1)
        if key == ord('r'):
            lower_red, upper_red = calibrate_color(frame, 'Red')
            print(f'Red Calibration: {lower_red} - {upper_red}')
        elif key == ord('g'):
            lower_green, upper_green = calibrate_color(frame, 'Green')
            print(f'Green Calibration: {lower_green} - {upper_green}')
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
