import cv2
import numpy as np
import time
from tkinter import *
from PIL import Image, ImageTk

# Start your default laptop camera with DirectShow backend
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Give time to open the camera
time.sleep(3)

# Capture the background image
for i in range(60):
    ret, background = cap.read()
    if not ret:
        print("Failed to capture background image")
        break
background = np.flip(background, axis=1)  # Flip the background image

# Initialize the Tkinter window
root = Tk()
root.title("Invisible Cloak")

# Create a label to hold the video frames
lbl = Label(root)
lbl.pack()

def update_frame():
    global background
    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    frame = np.flip(frame, axis=1)  # Flip the frame

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range for red color detection
    lower_red1 = np.array([0, 120, 50])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask1 = mask1 + mask2  # Combine both masks

    # Morphological operations to remove noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    # Create inverse mask
    mask2 = cv2.bitwise_not(mask1)

    # Segment out the red color part
    res1 = cv2.bitwise_and(frame, frame, mask=mask2)

    # Replace the red color part with background
    res2 = cv2.bitwise_and(background, background, mask=mask1)

    # Combine the two results
    final = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Convert the final image to RGB
    final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)

    # Convert to PIL image and then to ImageTk format
    img_tk = ImageTk.PhotoImage(image=Image.fromarray(final))

    # Update the label with the new image
    lbl.imgtk = img_tk
    lbl.configure(image=img_tk)

    # Schedule the next frame update
    lbl.after(10, update_frame)

# Start updating frames
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the video capture object
cap.release()
