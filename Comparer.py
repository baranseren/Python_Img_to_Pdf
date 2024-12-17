import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
import os
import time
from datetime import datetime
import shutil
import subprocess

def select_images():
    file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
    if file_paths:
        progress_label.config(text="Processing Images...")
        root.update()  # Update the GUI to reflect the changes
        resized_paths = resize_images(file_paths)
        progress_label.config(text="Combining Images to PDF...")
        root.update()  # Update the GUI to reflect the changes
        combine_images_to_pdf(resized_paths)

def resize_images(image_paths):
    resized_dir = os.path.join(os.path.dirname(image_paths[0]), "kucukresimler")
    if not os.path.exists(resized_dir):
        os.makedirs(resized_dir)
    
    resized_paths = []
    for i, img_path in enumerate(image_paths):
        img = Image.open(img_path)
        if img.width > 1920:
            aspect_ratio = img.height / img.width
            new_width = 1920
            new_height = int(new_width * aspect_ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        resized_path = os.path.join(resized_dir, os.path.basename(img_path))
        img.save(resized_path)
        resized_paths.append(resized_path)
        
        progress = ((i + 1) / len(image_paths)) * 50  # Update progress to 50% after resizing
        progress_var.set(progress)
        progress_bar.update()
        root.update()  # Update the GUI to reflect progress
        time.sleep(0.1)  # This sleep simulates processing delay
    
    return resized_paths

def combine_images_to_pdf(image_paths):
    try:
        images = []
        for i, img_path in enumerate(image_paths):
            img = Image.open(img_path).convert('RGB')
            images.append(img)
            progress = 50 + ((i + 1) / len(image_paths)) * 50  # Update progress from 50% to 100% during combining
            progress_var.set(progress)
            progress_bar.update()
            root.update()  # Update the GUI to reflect progress
            time.sleep(0.1)  # This sleep simulates processing delay
        
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        save_path = os.path.join(os.path.dirname(image_paths[0]), f"{now}.pdf")
        images[0].save(save_path, save_all=True, append_images=images[1:])
        progress_label.config(text=f"PDF saved as: {save_path}")
        root.update()  # Update the GUI to reflect the final status
        subprocess.Popen([save_path], shell=True)  # Open the PDF after saving
    except Exception as e:
        progress_label.config(text=f"Error: {e}")
        root.update()  # Update the GUI to reflect the error

# Main Tkinter window
root = tk.Tk()
root.title("Image to PDF Converter")
root.geometry("400x200")

progress_var = tk.DoubleVar()

# Button to select images
select_button = tk.Button(root, text="Select Images", command=select_images)
select_button.pack(pady=20)

# Progress bar to indicate progress
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X, padx=20)

# Label to show progress or status
progress_label = tk.Label(root, text="")
progress_label.pack(pady=10)

root.mainloop()
