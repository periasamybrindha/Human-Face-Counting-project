import cv2 
import tkinter as tk 
from tkinter import filedialog 
from PIL import Image, ImageTk 
import numpy as np 
# Load the pre-trained face detection model (Haar Cascade) 
face_cascade = 'haarcascade_frontalface_default.xml') 
cv2.CascadeClassifier(cv2.data.haarcascades 
# Global variable to store the camera object 
cap = None 
# Function to detect faces in an image 
def detect_faces(image): 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5) 
return faces 
# Function to handle uploading an image 
def upload_image(): 
file_path = filedialog.askopenfilename() 
if file_path: 
image = cv2.imread(file_path) 
faces = detect_faces(image)  # Detect faces in the original image 
display_image(image, faces) 
# Function to capture image from camera after 5 seconds 
def capture_image(): 
global cap 
cap = cv2.VideoCapture(0)  # Open the camera 
if not cap.isOpened(): 
status_label.config(text="Error: Unable to access the camera.") 
return 
# Start displaying the camera feed in the window 
status_label.config(text="Capturing image in 5 seconds...") 
show_camera_feed() 

# Capture an image after 5 seconds (5000 milliseconds) 
root.after(5000, capture_frame_from_camera) 
# Function to show live camera feed in the Tkinter window 
def show_camera_feed(): 
global cap 
if cap is not None and cap.isOpened(): 
ret, frame = cap.read() 
if ret: 
# Resize the frame to fit the current window size 
frame = resize_frame_to_window(frame) 
# Convert the frame to RGB for Tkinter display 
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
img_pil = Image.fromarray(frame_rgb) 
img_tk = ImageTk.PhotoImage(image=img_pil) 
# Display the live camera feed 
img_label.config(image=img_tk) 
img_label.image = img_tk  # Keep a reference to avoid GC 
# Continue updating the camera feed every 10ms 
img_label.after(10, show_camera_feed) 
# Function to resize the captured frame to fit the window 
def resize_frame_to_window(frame): 
# Get the current size of the window 
window_width = root.winfo_width() 
window_height = root.winfo_height() 
# Resize the frame to fit the window size 
resized_frame = cv2.resize(frame, (window_width, window_height - 100))  # Leave space for labels 
return resized_frame 
# Function to capture the frame from the camera after 5 seconds 
def capture_frame_from_camera(): 
global cap 
if cap is not None and cap.isOpened(): 
ret, frame = cap.read() 
if ret: 
faces = detect_faces(frame)  # Detect faces in the current frame 
display_image(frame, faces)  # Display the captured frame with detected faces 
status_label.config(text="Image captured.") 
 
        else: 
            status_label.config(text="Error: Failed to capture image.") 
         
        # Release the camera after capturing the image 
        cap.release() 
        cap = None 
 
# Function to resize the image to half the size of the screen width 
def resize_image_half(image): 
    screen_width = root.winfo_screenwidth() 
     
    # Calculate new dimensions to be half the screen width 
    scale_factor = 0.5  # To resize to half of the screen 
    new_width = int(screen_width * scale_factor) 
     
    # Calculate the aspect ratio to maintain the image's original aspect ratio 
    h, w = image.shape[:2] 
    aspect_ratio = h / w 
    new_height = int(new_width * aspect_ratio) 
     
    # Resize the image 
    resized_image = cv2.resize(image, (new_width, new_height)) 
    return resized_image 
 
# Function to display image and detected faces in the Tkinter window 
def display_image(image, faces): 
    # Draw rectangles around faces (on the original image before resizing) 
    for (x, y, w, h) in faces: 
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2) 
     
    # Resize the image to fit within the window 
    resized_image = resize_image_half(image) 
     
    # Convert BGR image to RGB for displaying in Tkinter 
    image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB) 
    img_pil = Image.fromarray(image_rgb) 
    img_tk = ImageTk.PhotoImage(image=img_pil) 
     
    # Update the label with the image 
    img_label.config(image=img_tk) 
    img_label.image = img_tk  # Keep a reference to avoid GC 
 
    # Ensure the face count label updates correctly 
    if faces is not None: 
        face_count_label.config(text=f"Number of faces detected: {len(faces)}") 
else: 
face_count_label.config(text="Number of faces detected: 0") 
# Create the main window 
root = tk.Tk() 
root.title("Human Face Counting ") 
# Get the screen width and height 
screen_width = root.winfo_screenwidth() 
screen_height = root.winfo_screenheight() 
# Set the default window size to half the screen size 
window_width = int(screen_width / 2) 
window_height = int(screen_height / 2) 
root.geometry(f"{window_width}x{window_height}") 
# Create and place the buttons at the top 
camera_button = tk.Button(root, text="Capture from Camera", command=capture_image) 
camera_button.pack() 
upload_button = tk.Button(root, text="Upload photo", command=upload_image) 
upload_button.pack() 
# Frame to hold the image and the face count 
image_frame = tk.Frame(root) 
image_frame.pack() 
# Label to display the image 
img_label = tk.Label(image_frame) 
img_label.pack() 
# Label to display the number of faces detected (below the image) 
face_count_label = tk.Label(image_frame, text="Number of faces detected: 0") 
face_count_label.pack() 
# Label to show the status (like when the camera capture will happen) 
status_label = tk.Label(root, text="") 
status_label.pack() 
# Start the GUI event loop 
root.mainloop() 
