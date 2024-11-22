import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling non-native image formats

# Tenant image paths and names
tenant_images = [
    "Main/UIs/images/pexels-anastasiya-gepp-654466-1462630.jpg",
    "Main/UIs/images/pexels-hai-nguyen-825252-1699419.jpg",
    "Main/UIs/images/pexels-tamhoang139-1007066.jpg",
    "Main/UIs/images/pexels-timothypictures-2826131.jpg",
]
tenant_names = ["Megan", "Xiang", "Zhong", "Bradley"]

# Global list to track selected tenants
selected_tenants = []

# Function to toggle tenant selection
def toggle_selection(name, button):
    if name in selected_tenants:
        selected_tenants.remove(name)
        button.state(['!pressed'])
    else:
        selected_tenants.append(name)
        button.state(['pressed'])

# Function to display the selected tenants
def submitSelection():
    messagebox.showinfo("Selection", f"Selected Tenants: {', '.join(selected_tenants) if selected_tenants else 'None'}")

# Initialise the main window
root = tk.Tk()
root.title("Select Tenants")
root.geometry("800x400")
root.configure(bg="#f6f7fb")

# Create custom button style with rounded corners
style = ttk.Style()
style.theme_use('default')

# Configure the style for select buttons
style.configure('Select.TButton', 
    background='#4355ff',
    foreground='white',
    font=('Helvetica', 10, 'bold'),
    borderwidth=0,
    relief='flat'
)
style.map('Select.TButton',
    background=[('pressed', 'green'), ('active', '#6677ff')],
    foreground=[('pressed', 'white'), ('active', 'white')]
)

# Top rectangle (with 'Select Tenants')
top_frame = tk.Frame(root, bg="#4355ff", bd=2, relief="flat")
top_frame.pack(fill="x", side="top", pady=0)

# Title label with white text on blue background and sans-serif bold font
title_label = tk.Label(top_frame, text="Select Tenants", font=("Helvetica", 16, "bold"), bg="#4355ff", fg="white")
title_label.pack(expand=True)

# Main container frame to center the content
main_container = tk.Frame(root, bg="#f6f7fb")
main_container.pack(expand=True, fill="both")

# Create a frame for tenant cards
tenant_container_frame = tk.Frame(main_container, bg="#f6f7fb")
tenant_container_frame.pack(expand=True)

# Create tenant frames inside the container frame
for i, name in enumerate(tenant_names):
    # Create a frame for each tenant inside the container frame
    tenant_frame = tk.Frame(tenant_container_frame, bg="#f6f7fb", width=150, height=200)
    tenant_frame.grid(row=0, column=i, padx=10, pady=10)

    # Add the profile picture
    try:
        img = Image.open(tenant_images[i])  # Open the image
        img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize to fit the card
        profile_image = ImageTk.PhotoImage(img)
        icon_label = tk.Label(tenant_frame, image=profile_image, bg="#f6f7fb")
        icon_label.image = profile_image  # Prevent garbage collection
    except Exception as e:
        icon_label = tk.Label(tenant_frame, text="No Image", bg="#f6f7fb", fg="black", font=("Helvetica", 10, "bold"))

    icon_label.pack(expand=True, fill="both", pady=5)

    # Tenant name label with sans-serif bold font
    name_label = tk.Label(tenant_frame, text=name, bg="#f6f7fb", fg="black", font=("Helvetica", 12, "bold"))
    name_label.pack(expand=True, fill="both", pady=5)

    # Select button with toggle functionality using ttk.Button
    select_button = ttk.Button(
        tenant_frame, 
        text="Select", 
        style='Select.TButton', 
        command=lambda n=name, btn=None: toggle_selection(n, btn)
    )
    select_button.pack(expand=True, fill="both", pady=5)
    
    # Store reference to button in the lambda to allow state change
    select_button.configure(command=lambda n=name, btn=select_button: toggle_selection(n, btn))

# Configure grid layout for centering tenants
tenant_container_frame.grid_rowconfigure(0, weight=1)  # Allow vertical centering
for i in range(len(tenant_names)):
    tenant_container_frame.grid_columnconfigure(i, weight=1)  # Allow horizontal distribution

# Bottom rectangle (with buttons)
bottom_frame = tk.Frame(root, bg="#eeeff4", bd=2, relief="flat")
bottom_frame.pack(fill="x", side="bottom", pady=0)

# Buttons for Cancel and OK with sans-serif bold font
cancel_button = ttk.Button(bottom_frame, text="Cancel", command=root.quit, style='Select.TButton')
cancel_button.pack(side="left", padx=10, pady=10)

ok_button = ttk.Button(bottom_frame, text="OK", command=submitSelection, style='Select.TButton')
ok_button.pack(side="right", padx=10, pady=10)

# Start the GUI loop
root.mainloop()