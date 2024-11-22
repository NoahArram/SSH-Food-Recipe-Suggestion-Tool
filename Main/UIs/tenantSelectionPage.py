import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class TenantSelectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Tenants")
        self.setGeometry(100, 100, 1000, 600)  # Window size
        self.selected_tenants = []  # Track selected tenants

        # Initialize the UI
        self.initUI()

    def initUI(self):
        # Main layout setup
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Add the top container
        self.add_top_container()

        # Add the tenant container
        self.add_tenant_container()

        # Add the bottom container
        self.add_bottom_container()

    def add_top_container(self):
        """Create and add the top container with the title."""
        self.top_container = QWidget(self.central_widget)
        self.top_container.setStyleSheet("background-color: #4355ff;")
        self.top_container.setFixedHeight(50)  # Consistent top bar height
        self.main_layout.addWidget(self.top_container)

        top_layout = QHBoxLayout(self.top_container)
        title_label = QLabel("Select Tenants", self.top_container)
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(title_label)

    def add_tenant_container(self):
        """Create and add the tenant container."""
        self.tenant_container = QWidget(self.central_widget)
        self.tenant_container.setStyleSheet("background-color: #f6f7fb;")
        self.main_layout.addWidget(self.tenant_container, stretch=1)

        tenant_layout = QHBoxLayout(self.tenant_container)
        tenant_layout.setAlignment(Qt.AlignCenter)

        # Tenant data (images and names)
        tenant_images = [
            "Main/UIs/images/pexels-anastasiya-gepp-654466-1462630.jpg",
            "Main/UIs/images/pexels-hai-nguyen-825252-1699419.jpg",
            "Main/UIs/images/pexels-tamhoang139-1007066.jpg",
            "Main/UIs/images/pexels-timothypictures-2826131.jpg",
        ]
        tenant_names = ["Megan", "Xiang", "Zhong", "Bradley"]

        for img_path, name in zip(tenant_images, tenant_names):
            tenant_card = self.create_tenant_card(img_path, name)
            tenant_layout.addWidget(tenant_card)

    def create_tenant_card(self, image_path, name):
        """Create an individual tenant card with larger elements and fixed button styling."""
        card = QWidget()
        card.setStyleSheet("background-color: #eeeff4; border-radius: 15px;")  # Larger rounded card
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)

        # Load and display the tenant image with larger size
        try:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Increased image size
            image_label = QLabel()
            image_label.setPixmap(pixmap)
        except Exception:
            image_label = QLabel("No Image")
            image_label.setStyleSheet("color: black; font-size: 12px;")

        image_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(image_label)

        # Add the tenant name with larger font size
        name_label = QLabel(name)
        name_label.setStyleSheet("color: black; font-size: 20px; font-weight: bold;")  # Larger name font
        name_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(name_label)

        # Add the Select button with larger size and padding
        select_button = QPushButton("Select")
        select_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4355ff; 
                color: white; 
                font-size: 16px; 
                font-weight: bold; 
                padding: 10px 20px; 
                border-radius: 12px; /* Rounded corners */
            }
            QPushButton:pressed {
                background-color: green;  /* Change color when pressed */
                border-radius: 12px; /* Ensure rounded corners on press */
            }
            QPushButton:checked {
                background-color: green; /* When button is checked, color is green */
            }
            QPushButton:hover {
                background-color: #6677ff;  /* Hover color */
            }
            """
        )
        select_button.clicked.connect(lambda: self.toggle_selection(name, select_button))
        card_layout.addWidget(select_button)

        return card



    def add_bottom_container(self):
        """Create and add the bottom container with Cancel and OK buttons."""
        self.bottom_container = QWidget(self.central_widget)
        self.bottom_container.setStyleSheet("background-color: #eeeff4;")
        self.bottom_container.setFixedHeight(80)  # Consistent bottom bar height
        self.main_layout.addWidget(self.bottom_container)

        bottom_layout = QHBoxLayout(self.bottom_container)
        cancel_button = QPushButton("Cancel", self.bottom_container)
        cancel_button.setStyleSheet(
            "background-color: #4355ff; color: white; font-size: 16px; padding: 15px 2px; font-weight: bold; border-radius: 12px"
        )
        #cancel_button.setFixedWidth(300)
        cancel_button.clicked.connect(self.close)
        bottom_layout.addWidget(cancel_button)

        ok_button = QPushButton("OK", self.bottom_container)
        ok_button.setStyleSheet(
            "background-color: #4355ff; color: white; font-size: 16px; padding: 15px 2px; font-weight: bold; border-radius: 12px"
        )
        #ok_button.setFixedWidth(300)

        ok_button.clicked.connect(self.submit_selection)
        bottom_layout.addWidget(ok_button)

    def toggle_selection(self, name, button):
        """Toggle tenant selection."""
        if name in self.selected_tenants:
            self.selected_tenants.remove(name)
            button.setText("Select")
            button.setStyleSheet(
                    """
                QPushButton {
                    background-color: #4355ff; 
                    color: white; 
                    font-size: 16px; 
                    font-weight: bold; 
                    padding: 10px 20px; 
                    border-radius: 12px; /* Rounded corners */
                }
                
                """
            )
        else:
            self.selected_tenants.append(name)
            button.setText("Deselect")
            button.setStyleSheet(
                    """
                QPushButton {
                    background-color: green; 
                    color: white; 
                    font-size: 16px; 
                    font-weight: bold; 
                    padding: 10px 20px; 
                    border-radius: 12px; /* Rounded corners */
                }
                
                """
            )

    def submit_selection(self):
        """Display selected tenants."""
        selected = ", ".join(self.selected_tenants) if self.selected_tenants else "None"
        print(f"Selected Tenants: {selected}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TenantSelectionApp()
    window.show()
    sys.exit(app.exec_())




















































































# import tkinter as tk
# from tkinter import ttk
# from tkinter import messagebox
# from PIL import Image, ImageTk  # For handling non-native image formats

# # Tenant image paths and names
# tenant_images = [
#     "Main/UIs/images/pexels-anastasiya-gepp-654466-1462630.jpg",
#     "Main/UIs/images/pexels-hai-nguyen-825252-1699419.jpg",
#     "Main/UIs/images/pexels-tamhoang139-1007066.jpg",
#     "Main/UIs/images/pexels-timothypictures-2826131.jpg",
# ]
# tenant_names = ["Megan", "Xiang", "Zhong", "Bradley"]

# # Global list to track selected tenants
# selected_tenants = []

# # Function to toggle tenant selection
# def toggle_selection(name, button):
#     if name in selected_tenants:
#         selected_tenants.remove(name)
#         button.state(['!pressed'])
#     else:
#         selected_tenants.append(name)
#         button.state(['pressed'])

# # Function to display the selected tenants
# def submitSelection():
#     messagebox.showinfo("Selection", f"Selected Tenants: {', '.join(selected_tenants) if selected_tenants else 'None'}")

# # Initialise the main window
# root = tk.Tk()
# root.title("Select Tenants")
# root.geometry("800x400")
# root.configure(bg="#f6f7fb")

# # Create custom button style with rounded corners
# style = ttk.Style()
# style.theme_use('default')

# # Configure the style for select buttons
# style.configure('Select.TButton', 
#     background='#4355ff',
#     foreground='white',
#     font=('Helvetica', 10, 'bold'),
#     borderwidth=0,
#     relief='flat'
# )
# style.map('Select.TButton',
#     background=[('pressed', 'green'), ('active', '#6677ff')],
#     foreground=[('pressed', 'white'), ('active', 'white')]
# )

# # Top rectangle (with 'Select Tenants')
# top_frame = tk.Frame(root, bg="#4355ff", bd=2, relief="flat")
# top_frame.pack(fill="x", side="top", pady=0)

# # Title label with white text on blue background and sans-serif bold font
# title_label = tk.Label(top_frame, text="Select Tenants", font=("Helvetica", 16, "bold"), bg="#4355ff", fg="white")
# title_label.pack(expand=True)

# # Main container frame to center the content
# main_container = tk.Frame(root, bg="#f6f7fb")
# main_container.pack(expand=True, fill="both")

# # Create a frame for tenant cards
# tenant_container_frame = tk.Frame(main_container, bg="#f6f7fb")
# tenant_container_frame.pack(expand=True)

# # Create tenant frames inside the container frame
# for i, name in enumerate(tenant_names):
#     # Create a frame for each tenant inside the container frame
#     tenant_frame = tk.Frame(tenant_container_frame, bg="#f6f7fb", width=150, height=200)
#     tenant_frame.grid(row=0, column=i, padx=10, pady=10)

#     # Add the profile picture
#     try:
#         img = Image.open(tenant_images[i])  # Open the image
#         img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize to fit the card
#         profile_image = ImageTk.PhotoImage(img)
#         icon_label = tk.Label(tenant_frame, image=profile_image, bg="#f6f7fb")
#         icon_label.image = profile_image  # Prevent garbage collection
#     except Exception as e:
#         icon_label = tk.Label(tenant_frame, text="No Image", bg="#f6f7fb", fg="black", font=("Helvetica", 10, "bold"))

#     icon_label.pack(expand=True, fill="both", pady=5)

#     # Tenant name label with sans-serif bold font
#     name_label = tk.Label(tenant_frame, text=name, bg="#f6f7fb", fg="black", font=("Helvetica", 12, "bold"))
#     name_label.pack(expand=True, fill="both", pady=5)

#     # Select button with toggle functionality using ttk.Button
#     select_button = ttk.Button(
#         tenant_frame, 
#         text="Select", 
#         style='Select.TButton', 
#         command=lambda n=name, btn=None: toggle_selection(n, btn)
#     )
#     select_button.pack(expand=True, fill="both", pady=5)
    
#     # Store reference to button in the lambda to allow state change
#     select_button.configure(command=lambda n=name, btn=select_button: toggle_selection(n, btn))

# # Configure grid layout for centering tenants
# tenant_container_frame.grid_rowconfigure(0, weight=1)  # Allow vertical centering
# for i in range(len(tenant_names)):
#     tenant_container_frame.grid_columnconfigure(i, weight=1)  # Allow horizontal distribution

# # Bottom rectangle (with buttons)
# bottom_frame = tk.Frame(root, bg="#eeeff4", bd=2, relief="flat")
# bottom_frame.pack(fill="x", side="bottom", pady=0)

# # Buttons for Cancel and OK with sans-serif bold font
# cancel_button = ttk.Button(bottom_frame, text="Cancel", command=root.quit, style='Select.TButton')
# cancel_button.pack(side="left", padx=10, pady=10)

# ok_button = ttk.Button(bottom_frame, text="OK", command=submitSelection, style='Select.TButton')
# ok_button.pack(side="right", padx=10, pady=10)

# # Start the GUI loop
# root.mainloop()