import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For profile pictures

# Function to display the selected tenants
def submitSelection():
    selected_tenants = [tenant.get() for tenant in tenant_vars]
    selected_names = [tenant_names[i] for i in range(len(selected_tenants)) if selected_tenants[i]]
    messagebox.showinfo("Selection", f"Selected Tenants: {', '.join(selected_names) if selected_names else 'None'}")

# Initialise the main window
root = tk.Tk()
root.title("Select Tenants")
root.geometry("800x600")
root.configure(bg="#f6f7fb")

# Top rectangle (with 'Select Tenants')
top_frame = tk.Frame(root, bg="#eeeff4", bd=2, relief="flat")
top_frame.pack(fill="x", side="top", pady=10)

# Title label
title_label = tk.Label(top_frame, text="Select Tenants", font=("Arial", 20, "bold"), bg="#eeeff4", fg="#4355ff")
title_label.pack(pady=10)

# Frame for tenant selection
tenant_container_frame = tk.Frame(root, bg="#f6f7fb")
tenant_container_frame.pack(fill="both", expand=True, padx=20, pady=20)

tenant_names = ["Tenant 1", "Tenant 2", "Tenant 3", "Tenant 4"]
tenant_images = [
    "Main/UIs/images/pexels-anastasiya-gepp-654466-1462630.jpg",  # Replace with actual image paths
    "Main/UIs/images/pexels-hai-nguyen-825252-1699419.jpg",
    "Main/UIs/images/pexels-tamhoang139-1007066.jpg",
    "Main/UIs/images/pexels-timothypictures-2826131.jpg",
]
tenant_vars = []

# Create tenant cards
for i, (name, image_path) in enumerate(zip(tenant_names, tenant_images)):
    # Frame for each tenant card
    tenant_frame = tk.Frame(tenant_container_frame, bg="#eeeff4", padx=10, pady=10)
    tenant_frame.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")
    
    # Add profile picture
    try:
        img = Image.open(image_path).resize((100, 100))  # Resize for uniformity
        photo = ImageTk.PhotoImage(img)
    except FileNotFoundError:
        photo = tk.Label(tenant_frame, text="No Image", bg="#eeeff4", fg="#4355ff", font=("Arial", 12))
        photo.pack(pady=10)
    else:
        img_label = tk.Label(tenant_frame, image=photo, bg="#eeeff4")
        img_label.image = photo
        img_label.pack(pady=10)

    # Tenant name label
    name_label = tk.Label(tenant_frame, text=name, bg="#eeeff4", fg="#4355ff", font=("Arial", 12))
    name_label.pack(pady=5)
    
    # Checkbox
    var = tk.BooleanVar()
    tenant_vars.append(var)
    checkbox = tk.Checkbutton(tenant_frame, variable=var, bg="#eeeff4", fg="#4355ff", activebackground="#eeeff4")
    checkbox.pack()

# Configure grid layout for responsiveness
tenant_container_frame.grid_columnconfigure(0, weight=1)
tenant_container_frame.grid_columnconfigure(1, weight=1)

# Bottom rectangle (with buttons)
bottom_frame = tk.Frame(root, bg="#eeeff4", bd=2, relief="flat")
bottom_frame.pack(fill="x", side="bottom", pady=10)

# Buttons for Cancel and OK
cancel_button = tk.Button(bottom_frame, text="Cancel", command=root.quit, bg="#4355ff", fg="white", font=("Arial", 12), relief="flat")
cancel_button.pack(side="left", padx=20, pady=10)

ok_button = tk.Button(bottom_frame, text="OK", command=submitSelection, bg="#4355ff", fg="white", font=("Arial", 12), relief="flat")
ok_button.pack(side="right", padx=20, pady=10)

# Start the GUI loop
root.mainloop()
