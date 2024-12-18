import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QWidget, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from io import BytesIO
import requests

from Data.favRecipe import favourites  

def load_image_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        pixmap = QPixmap()
        pixmap.loadFromData(img_data.getvalue())
        return pixmap
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

class FavoritesPage(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user  # Tenant name
        self.setWindowTitle(f"{self.user}'s Favorites")
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        title_label = QLabel(f"{self.user}'s Favorites")
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: white; background-color: #4355ff; padding: 10px;"
        )
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        recipes = favourites.get(self.user, [])
        for recipe in recipes:
            self.create_recipe_card(recipe, scroll_layout)

        
        back_button = QPushButton("Back")
        back_button.setStyleSheet(
            "background-color: #4355ff; color: white; font-size: 14px; padding: 10px; border-radius: 5px;"
        )
        back_button.clicked.connect(self.close)  
        main_layout.addWidget(back_button)

    def create_recipe_card(self, recipe, layout):
        """Create a card for each favorite recipe."""
        recipe_frame = QFrame()
        recipe_frame.setStyleSheet(
            "background-color: #444444; border: 1px solid #555; border-radius: 10px; padding: 10px;"
        )
        recipe_layout = QHBoxLayout(recipe_frame)

        pixmap = load_image_from_url(recipe[7])  # Image URL index is 7
        image_label = QLabel()
        if pixmap:
            image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        else:
            image_label.setText("No Image")
        recipe_layout.addWidget(image_label)

        details_layout = QVBoxLayout()
        title_label = QLabel(recipe[1])  # Recipe title index is 1
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        details_layout.addWidget(title_label)

        time_label = QLabel(f"Cooking Time: {recipe[5]} minutes")  # Cooking time index is 5
        time_label.setStyleSheet("color: white; font-size: 12px;")
        details_layout.addWidget(time_label)

        servings_label = QLabel(f"Servings: {recipe[6]}")  # Servings index is 6
        servings_label.setStyleSheet("color: white; font-size: 12px;")
        details_layout.addWidget(servings_label)

        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet(
            "background-color: #ff4444; color: white; font-size: 12px; border-radius: 5px; padding: 5px;"
        )
        remove_button.clicked.connect(lambda: self.remove_recipe(recipe[0]))  # Recipe ID index is 0
        details_layout.addWidget(remove_button)

        recipe_layout.addLayout(details_layout)
        layout.addWidget(recipe_frame)

    def remove_recipe(self, recipe_id):
        """Remove a recipe from favorites."""
        global favourites
        favourites[self.user] = [r for r in favourites[self.user] if r[0] != recipe_id]
        print(f"Recipe {recipe_id} removed from {self.user}'s favorites.")
        self.refresh_page()

    def refresh_page(self):
        """Refresh the favorites page."""
        self.close()
        self.__init__(self.user)
        self.show()

# Test the application with dummy data
if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = "Xiang"
    window = FavoritesPage(user)
    window.show()
    sys.exit(app.exec_())