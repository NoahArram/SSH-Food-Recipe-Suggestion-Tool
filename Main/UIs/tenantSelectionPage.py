# tenantSelectionPage.py
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Import recipeListPage
from UIs.recipeListPage import RecipeApp

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
        """Process the selected tenants and show recipe list."""
        selected_tenants = self.selected_tenants
        if not selected_tenants:
            print("No tenants selected.")
            return

        ingredients = self.get_ingredients_for_tenants(selected_tenants)
        from API import getRecipes
        recipes = getRecipes.get_recipes_by_ingredients(ingredients)

        # Initialize RecipeApp with recipes and show it
        self.recipeListWindow = RecipeApp(recipes, parent=self)
        self.recipeListWindow.show()
        self.hide()

    def get_ingredients_for_tenants(self, tenants):
        """Retrieve ingredients for the selected tenants."""
        import os

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the data file relative to the script's directory
        data_file_path = os.path.join(current_dir, '../Data/ingredient.json')

        # Open the file using the constructed path
        with open(data_file_path, 'r') as f:
            data = json.load(f)

        ingredients = []
        for entry in data['main']:
            if entry['Owner'] in tenants:
                ingredients.extend(entry['ingredients'])
        return list(set(ingredients))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TenantSelectionApp()
    window.show()
    sys.exit(app.exec_())