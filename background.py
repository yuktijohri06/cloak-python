import cv2
from tkinter import *
from PIL import Image, ImageTk

def update_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Convert the image from OpenCV BGR format to PIL RGB format
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Update the label with the new image
        lbl.imgtk = imgtk
        lbl.configure(image=imgtk)
        
        # Call the function again after 10 milliseconds
        lbl.after(10, update_frame)

# Initialize the Tkinter window
root = Tk()
root.title("Webcam Stream")

# Initialize the video capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Create a label to hold the video frames
lbl = Label(root)
lbl.pack()

# Start updating the frames
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

