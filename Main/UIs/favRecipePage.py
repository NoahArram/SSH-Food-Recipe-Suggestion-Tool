import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QWidget, QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class FavoritesPage(QMainWindow):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user  # Tenant name
        self.setWindowTitle(f"{self.user}'s Favorites")
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Header
        title_label = QLabel(f"{self.user}'s Favorites")
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: white; background-color: #4355ff; padding: 10px;"
        )
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Scrollable content for recipes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        # Fetch and display favorites
        from API import favorites_manager
        recipes = favorites_manager.get_favorites(self.user)
        for recipe in recipes:
            self.create_recipe_card(recipe, scroll_layout)

        # Back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet(
            "background-color: #4355ff; color: white; font-size: 14px; padding: 10px; border-radius: 5px;"
        )
        back_button.clicked.connect(self.go_back)
        main_layout.addWidget(back_button)

    def create_recipe_card(self, recipe, layout):
        """Create a card for each favorite recipe."""
        recipe_frame = QFrame()
        recipe_frame.setStyleSheet(
            "background-color: #444444; border: 1px solid #555; border-radius: 10px; padding: 10px;"
        )
        recipe_layout = QHBoxLayout(recipe_frame)

        # Recipe image
        from UIs.recipeApp import load_image_from_url
        pixmap = load_image_from_url(recipe[5])  # Image URL
        image_label = QLabel()
        if pixmap:
            image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        else:
            image_label.setText("No Image")
        recipe_layout.addWidget(image_label)

        # Recipe details
        details_layout = QVBoxLayout()
        title_label = QLabel(recipe[1])  # Recipe title
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        details_layout.addWidget(title_label)

        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet(
            "background-color: #ff4444; color: white; font-size: 12px; border-radius: 5px; padding: 5px;"
        )
        remove_button.clicked.connect(lambda: self.remove_recipe(recipe[0]))
        details_layout.addWidget(remove_button)

        recipe_layout.addLayout(details_layout)
        layout.addWidget(recipe_frame)

    def remove_recipe(self, recipe_id):
        """Remove a recipe from favorites."""
        from API import favorites_manager
        favorites_manager.remove_from_favorites(self.user, recipe_id)
        print(f"Recipe {recipe_id} removed from {self.user}'s favorites.")
        self.refresh_page()

    def refresh_page(self):
        """Refresh the favorites page."""
        self.close()
        self.__init__(self.user, parent=self.parent())
        self.show()

    def go_back(self):
        """Navigate back to the tenant selection page."""
        self.close()
        if self.parent() is not None:
            self.parent().show()
