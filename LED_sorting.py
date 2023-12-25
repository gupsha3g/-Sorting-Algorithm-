"""An algorithm to sort count LED in real-time by counting no. of ON LED on the basis of its status"""
import cv2
import numpy as np

# Define HSV ranges for red, orange, and green colors
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

lower_orange = np.array([10, 100, 100])
upper_orange = np.array([25, 255, 255])

lower_green = np.array([35, 100, 100])
upper_green = np.array([85, 255, 255])

# Start capturing video from the default camera (usually camera index 0)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Display instructions on the frame
    cv2.putText(frame, "Press 's' to capture a frame.", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Real-time Camera", frame)

    # Break the loop when 's' key is pressed to capture a frame
    if cv2.waitKey(1) & 0xFF == ord('s'):
        captured_frame = frame.copy()  # Store the captured frame
        print("Frame captured!")
        break
# Convert the captured frame to HSV color space
hsv_frame = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2HSV)

# Create binary masks for red, orange, and green colors
red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
orange_mask = cv2.inRange(hsv_frame, lower_orange, upper_orange)
green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

# Find contours of red, orange, and green objects in the masks
red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize counters for each color
red_count = 0
orange_count = 0
green_count = 0

# Set a minimum contour area threshold
min_contour_area = 100  # Adjust this value based on your requirement


# Draw circles around detected pixels and count the circles for each color
for contour in red_contours:
    contour_area = cv2.contourArea(contour)
    if contour_area > min_contour_area:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(red_mask, center, radius, (0, 0, 255), 2)  # Draw red circles around red pixels
        red_count += 1

for contour in orange_contours:
    contour_area = cv2.contourArea(contour)
    if contour_area > min_contour_area:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(orange_mask, center, radius, (0, 165, 255), 2)  # Draw orange circles around orange pixels
        orange_count += 1
min_contours_green = 70
for contour in green_contours:
    contour_area = cv2.contourArea(contour)
    if contour_area > min_contours_green:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(green_count, center, radius, (0, 255, 0), 2)  # Draw green circles around green pixels
        green_count += 1

# Display the image with circles around detected pixels and the counts
cv2.putText(captured_frame, f"Red Circles: {red_count}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.putText(captured_frame, f"Orange Circles: {orange_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
cv2.putText(captured_frame, f"Green Circles: {green_count}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2.imshow("Image with Circles and Counts", captured_frame)
cv2.imshow("red Counts", red_mask)
cv2.imshow("orange Counts", orange_mask)
cv2.imshow("green Counts", green_mask)
print(f'RED_ON : {red_count}, GREEN_ON: {green_count}, ORANGE_ON{orange_count})
number = [red_count, green_count, orange_count]
Total = sum(number)
print(f"Toatl number of ON LED: {Total}")
# Wait for a key press and then close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
