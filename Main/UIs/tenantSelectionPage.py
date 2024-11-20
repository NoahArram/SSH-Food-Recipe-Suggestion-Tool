import tkinter as tk
from tkinter import messagebox

# Function to display the selected tenants
def submitSelection():
    selected_tenants = [tenant.get() for tenant in tenant_vars]
    selected_names = [tenant_names[i] for i in range(len(selected_tenants)) if selected_tenants[i]]
    messagebox.showinfo("Selection", f"Selected Tenants: {', '.join(selected_names) if selected_names else 'None'}")

# Initialise the main window
root = tk.Tk()
root.title("Select Tenants")
root.geometry("400x400")
root.configure(bg="navy")

# Top rectangle (with 'Select Tenants')
top_frame = tk.Frame(root, bg="lightblue", bd=2, relief="flat")
top_frame.pack(fill="x", side="top", pady=0)  # Using pack to make sure the top frame stays on top

# Title label
title_label = tk.Label(top_frame, text="Select Tenants", font=("Arial", 16), bg="lightblue", fg="black")
title_label.pack(expand=True)

# Frame for tenant selection (this frame has a black background for the entire group of tenants)
tenant_container_frame = tk.Frame(root, bg="black")
tenant_container_frame.pack(fill="both", expand=True, padx=10, pady=90)  # Expand and fill window space

tenant_names = ["Tenant 1", "Tenant 2", "Tenant 3", "Tenant 4"]
tenant_vars = []

# Create tenant frames inside the container frame
for i, name in enumerate(tenant_names):
    # Create a frame for each tenant inside the container frame
    tenant_frame = tk.Frame(tenant_container_frame, bg="#1C1C1C", width=80, height=40)  # Initial height set to 40px
    tenant_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")  # Use sticky to make them stretch in both directions
    
    # Add the image placeholder (circle icon)
    icon_label = tk.Label(tenant_frame, text="👤", font=("Arial", 30), bg="#1C1C1C", fg="lightblue")
    icon_label.pack(expand=True, fill="both", pady=2)  # Use fill and expand to make the icon resize
    
    # Tenant name label
    name_label = tk.Label(tenant_frame, text=name, bg="#1C1C1C", fg="white", font=("Arial", 10))
    name_label.pack(expand=True, fill="both", pady=2)  # Fill the frame with this label
    
    # Checkbox
    var = tk.BooleanVar()
    tenant_vars.append(var)
    checkbox = tk.Checkbutton(tenant_frame, variable=var, bg="#1C1C1C", activebackground="#1C1C1C", fg="lightblue", highlightthickness=0)
    checkbox.pack(expand=True, fill="both", pady=2)  # Expand the checkbox to resize

# Configure grid layout for tenant container frame to allow resizing
tenant_container_frame.grid_rowconfigure(0, weight=1)  # Allow the row to expand vertically
for i in range(len(tenant_names)):
    tenant_container_frame.grid_columnconfigure(i, weight=1)  # Allow each column to expand horizontally

# Bottom rectangle (with buttons)
bottom_frame = tk.Frame(root, bg="lightblue", bd=2, relief="flat")
bottom_frame.pack(fill="x", side="bottom", pady=0)  # Using pack to make sure the bottom frame stays at the bottom

# Buttons for Cancel and OK
cancel_button = tk.Button(bottom_frame, text="Cancel", command=root.quit, bg="#B0C4DE", width=10)
cancel_button.pack(side="left", padx=10, pady=10)

ok_button = tk.Button(bottom_frame, text="OK", command=submitSelection, bg="#B0C4DE", width=10)
ok_button.pack(side="right", padx=10, pady=10)

# Start the GUI loop
root.mainloop()
