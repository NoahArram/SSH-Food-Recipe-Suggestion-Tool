# tenantSelectionPage.py
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from UIs.recipeListPage import RecipeApp
from UIs.favRecipePage import FavoritesPage

class TenantSelectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Tenants")
        self.setGeometry(100, 100, 1000, 600)  
        self.selected_tenants = []  

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.add_top_container()

        self.add_tenant_container()

        self.add_bottom_container()

    def add_top_container(self):
        """Create and add the top container with the title."""
        self.top_container = QWidget(self.central_widget)
        self.top_container.setStyleSheet("background-color: #4355ff;")
        self.top_container.setFixedHeight(50)  
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

        tenant_images = [
            "UIs/images/pexels-anastasiya-gepp-654466-1462630.jpg",
            "UIs/images/pexels-hai-nguyen-825252-1699419.jpg",
            "UIs/images/pexels-tamhoang139-1007066.jpg",
            "UIs/images/pexels-timothypictures-2826131.jpg",
        ]
        tenant_names = ["Megan", "Xiang", "Zhong", "Bradley"]

        for img_path, name in zip(tenant_images, tenant_names):
            tenant_card = self.create_tenant_card(img_path, name)
            tenant_layout.addWidget(tenant_card)

    def create_tenant_card(self, image_path, name):
        """Create an individual tenant card with larger elements and fixed button styling."""
        card = QWidget()
        card.setStyleSheet("background-color: #eeeff4; border-radius: 15px;")  
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)

        try:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
            image_label = QLabel()
            image_label.setPixmap(pixmap)
        except Exception:
            image_label = QLabel("No Image")
            image_label.setStyleSheet("color: black; font-size: 12px;")

        image_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(image_label)

        name_label = QLabel(name)
        name_label.setStyleSheet("color: black; font-size: 20px; font-weight: bold;")  
        name_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(name_label)

        select_button = QPushButton("Select")
        select_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4355ff; 
                color: white; 
                font-size: 16px; 
                font-weight: bold; 
                padding: 10px 20px; 
                border-radius: 12px; 
            }
            QPushButton:pressed {
                background-color: green; 
                border-radius: 12px; 
            }
            QPushButton:checked {
                background-color: green;
            }
            QPushButton:hover {
                background-color: #6677ff;  
            }
            """
        )
        select_button.clicked.connect(lambda: self.toggle_selection(name, select_button))
        card_layout.addWidget(select_button)

        fav_button = QPushButton("Favorites")
        fav_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff4444; 
                color: white; 
                font-size: 16px; 
                font-weight: bold; 
                padding: 10px 20px; 
                border-radius: 12px; 
            }
            QPushButton:pressed {
                background-color: #ff6666;  
                border-radius: 12px; 
            }
            QPushButton:hover {
                background-color: #ff7777;  
            }
            """
        )
        fav_button.clicked.connect(lambda: self.open_favorites_page(name))
        card_layout.addWidget(fav_button)

        return card

    def open_favorites_page(self, name):
        self.favoritesWindow = FavoritesPage(name)
        self.favoritesWindow.show()

    def add_bottom_container(self):
        self.bottom_container = QWidget(self.central_widget)
        self.bottom_container.setStyleSheet("background-color: #eeeff4;")
        self.bottom_container.setFixedHeight(80)  
        self.main_layout.addWidget(self.bottom_container)

        bottom_layout = QHBoxLayout(self.bottom_container)
        cancel_button = QPushButton("Cancel", self.bottom_container)
        cancel_button.setStyleSheet(
                """
                    QPushButton {
                        background-color: #4355ff; 
                        color: white; 
                        font-size: 16px; 
                        padding: 15px 2px; 
                        font-weight: bold; 
                        border-radius: 12px;
                    }
                    QPushButton:hover {
                        background-color: #5a6aff;
                    }
                """
            )
        cancel_button.clicked.connect(self.close)
        bottom_layout.addWidget(cancel_button)

        ok_button = QPushButton("OK", self.bottom_container)
        ok_button.setStyleSheet(
            """
                QPushButton {
                    background-color: #4355ff; 
                    color: white; 
                    font-size: 16px; 
                    padding: 15px 2px; 
                    font-weight: bold; 
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background-color: #5a6aff;
                }
                """
        )

        ok_button.clicked.connect(self.submit_selection)
        bottom_layout.addWidget(ok_button)

    def toggle_selection(self, name, button):
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
                    border-radius: 12px; 
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
                    border-radius: 12px;
                }
                
                """
            )

    def submit_selection(self):
        selected_tenants = self.selected_tenants
        if not selected_tenants:
            print("No tenants selected.")
            return

        ingredients = self.get_ingredients_for_tenants(selected_tenants)
        from API import getRecipes
        recipes = getRecipes.get_recipes_by_ingredients(ingredients)

        self.recipeListWindow = RecipeApp(recipes, parent=self)
        self.recipeListWindow.show()
        self.hide()

    def get_ingredients_for_tenants(self, tenants):
        """Retrieve ingredients for the selected tenants."""
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(current_dir, '../Data/ingredient.json')

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