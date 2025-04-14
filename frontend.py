import tkinter as tk
from tkinter import filedialog
import os
import subprocess
from PIL import Image, ImageTk

# Create main window
root = tk.Tk()
root.title("Blood Cancer Detection")
root.geometry("1200x700")  # Adjusted window size

# Load background image
bg_image = Image.open("background.jpg")  # Ensure "background.jpg" exists
bg_image = bg_image.resize((1200, 700))
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to hold the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Fullscreen background

# Scrolling text function for the title
def scroll_title():
    global marquee_text
    marquee_text = marquee_text[1:] + marquee_text[0]  # Rotate text
    title_label.config(text=marquee_text)
    root.after(200, scroll_title)  # Repeat scrolling

# Title scrolling text
marquee_text = "   Blood Cancer Detection   "
title_label = tk.Label(root, text=marquee_text, font=("Arial", 20, "bold"), fg="red", bg="white")
title_label.pack(pady=5, fill=tk.X)

# Start scrolling effect
scroll_title()

# Frames for input image, processing text, and output image
frame = tk.Frame(root, bg="white")
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

input_frame = tk.Frame(frame, bg="white")
input_frame.pack(side=tk.LEFT, padx=10, pady=10)

process_frame = tk.Frame(frame, bg="white")
process_frame.pack(side=tk.LEFT, padx=10, pady=10)

output_frame = tk.Frame(frame, bg="white")
output_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Store selected image path
selected_image_path = None

# Function to select an image
def select_image():
    global selected_image_path, input_img_label

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")]
    )

    if file_path:
        selected_image_path = file_path  # Store full path
        image_label.config(text="Selected Image: " + os.path.basename(file_path))

        # Display selected input image (Left Side)
        img = Image.open(file_path)
        img = img.resize((400, 400))  # Resize for display
        input_img = ImageTk.PhotoImage(img)

        input_img_label.config(image=input_img)
        input_img_label.image = input_img  # Keep reference

        # Reset processing label and output image
        processing_label.config(text="")
        output_img_label.config(image="")

# Function to run detect.py
def run_detection():
    global selected_image_path

    if selected_image_path:
        processing_label.config(text="➡ Image Processing...", fg="blue")
        root.update()  # Force UI update

        subprocess.run(["python", "detect.py", os.path.basename(selected_image_path)])
        show_output_image(selected_image_path)  # Show detected image after processing

# Function to display the output image (Right Side)
def show_output_image(image_name):
    output_path = os.path.join("output", os.path.basename(image_name))  # Get processed image

    if os.path.exists(output_path):  # Check if the image exists
        img = Image.open(output_path)
        img = img.resize((400, 400))  # Resize for display
        output_img = ImageTk.PhotoImage(img)

        output_img_label.config(image=output_img)
        output_img_label.image = output_img  # Keep reference

        # Update processing text to "Output Image"
        processing_label.config(text="➡ Output Image", fg="green")
    else:
        processing_label.config(text="Output image not found!", fg="red")

# UI Elements
image_label = tk.Label(root, text="No image selected", font=("Arial", 12), bg="white")
image_label.pack(pady=10)

# Insert Image Button
insert_button = tk.Button(root, text="Insert Image", command=select_image, font=("Arial", 14), bg="lightblue")
insert_button.pack(pady=5)

# Input Image Display (Left Side)
input_img_label = tk.Label(input_frame, bg="white")
input_img_label.pack()

# Processing text with arrow (Middle)
processing_label = tk.Label(process_frame, text="", font=("Arial", 16, "bold"), fg="blue", bg="white")
processing_label.pack(pady=100)

# Output Image Display (Right Side)
output_img_label = tk.Label(output_frame, bg="white")
output_img_label.pack()

# Run Detection Button
run_button = tk.Button(root, text="Detect Cancer", command=run_detection, font=("Arial", 14), bg="lightgreen")
run_button.pack(pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12), bg="red", fg="white")
exit_button.pack(pady=10)

root.mainloop()
