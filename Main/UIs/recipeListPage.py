import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from io import BytesIO

from UIs.recipeInfoPage import RecipeInstructionsPage

from API import getRecipes
from Data import favRecipe

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def load_image_from_url(url):
    try:
        response = requests.get(url)
        img_data = BytesIO(response.content)
        pixmap = QPixmap()
        pixmap.loadFromData(img_data.getvalue())
        return pixmap
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

  

class RecipeApp(QMainWindow):
    def __init__(self, recipes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recipe List")
        self.setGeometry(100, 100, 1000, 600)
        self.recipes = recipes
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        title_label = QLabel("Recipe List")
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: white; background-color: #4355ff; padding: 10px; border-radius: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #f6f7fb;")
        main_layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        for recipe in self.recipes.values():
            recipe_frame = QFrame()
            recipe_frame.setStyleSheet("""
                background-color: #444444;
                border: 1px solid #555;
                border-radius: 10px;
                padding: 10px;
            """)
            recipe_frame.setFixedWidth(900)

            recipe_layout = QHBoxLayout(recipe_frame)
            recipe_layout.setContentsMargins(10, 10, 10, 10)
            recipe_layout.setSpacing(15)

            if recipe[7]:
                pixmap = load_image_from_url(recipe[7])
                if pixmap:
                    image_label = QLabel()
                    image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
                    image_label.setStyleSheet("border: none;")
                    recipe_layout.addWidget(image_label)
                else:
                    image_label = QLabel("No Image")
                    image_label.setStyleSheet("color: white; font-weight: bold;")
                    recipe_layout.addWidget(image_label)
            else:
                image_label = QLabel("No Image")
                image_label.setStyleSheet("color: white; font-weight: bold;")
                recipe_layout.addWidget(image_label)

            info_layout = QVBoxLayout()

            recipe_title = QLabel(recipe[1])
            recipe_title.setStyleSheet("color: white; font-size: 14pt; font-weight: bold;")
            info_layout.addWidget(recipe_title)

            recipe_details = f"Time: {recipe[5]} minutes - Serves: {recipe[6]}"
            details_label = QLabel(recipe_details)
            details_label.setStyleSheet("color: white; font-size: 12pt;")
            info_layout.addWidget(details_label)

            ingredients_info = "Ingredients Used:" + str(recipe[3]) + "\nIngredients Needed:" + str(recipe[2])
            ingredients_label = QLabel(ingredients_info)
            ingredients_label.setStyleSheet("color: white; font-size: 10pt;")
            info_layout.addWidget(ingredients_label)

            view_button = QPushButton("View Recipe")
            view_button.setProperty("clicked", False)
            view_button.setFixedWidth(300)
            view_button.setStyleSheet("""
                QPushButton {
                    background-color: #4355ff;
                    color: white;
                    font-size: 12pt;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #6475ff;  /* Lighter blue on hover */
                }
                
            """)

            favourite_button = QPushButton("❤")
            favourite_button.setProperty("clicked", False)
            favourite_button.setFixedSize(70, 40)
            favourite_button.setStyleSheet("""
                QPushButton {
                    background-color: #444444;
                    color: red;
                    font-size: 20pt;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #555555;  /* Slightly lighter grey on hover */
                }
               
            """)

            button_layout = QHBoxLayout()
            button_layout.addWidget(view_button)
            button_layout.addWidget(favourite_button)

            view_button.clicked.connect(lambda checked, r_id=recipe[0]: self.on_view_button_clicked(r_id, view_button))
            favourite_button.clicked.connect(lambda checked, r=recipe: self.on_favourite_button_clicked(r, favourite_button))

            info_layout.addLayout(button_layout)
            recipe_layout.addLayout(info_layout)

            card_container = QHBoxLayout()
            card_container.addWidget(recipe_frame)
            card_container.setAlignment(Qt.AlignCenter)
            scroll_layout.addLayout(card_container)

        button_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #4355ff;
                color: white;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #5a6aff;
            }
            QPushButton:clicked {
                background-color: green;
            }
        """)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4355ff;
                color: white;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
            background-color: #5a6aff;
            }
            QPushButton:clicked {
                background-color: green;
            }
        """)
        close_button.clicked.connect(self.close_application)
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout)

    def on_view_button_clicked(self, recipe_id, view_button):
        """Open the recipe information page and change the button state."""
        from API import getRecipeInfo
        recipe_info = getRecipeInfo.get_recipe_info(recipe_id)
        self.recipeInfoWindow = RecipeInstructionsPage(recipe_info, parent=self)
        self.recipeInfoWindow.show()
        self.hide()
        view_button.setProperty("clicked", True)
        view_button.setStyleSheet(view_button.styleSheet())

    def on_favourite_button_clicked(self, recipe, favourite_button):
        """Add the recipe to the user's favorites and change the button state."""
        user = self.parent().selected_tenants[0]  # Assuming a single user is selected
        favourites = favRecipe.favourites
        if user in favourites:
            favourites[user].append(recipe)
            print(f"Recipe {recipe[1]} added to {user}'s favorites.")
        else:
            print(f"User {user} not found in favorites.")
        favourite_button.setProperty("clicked", True)
        favourite_button.setStyleSheet(favourite_button.styleSheet())

    def go_back(self):
        """Return to the tenant selection page."""
        self.close()
        if self.parent() is not None:
            self.parent().show()

    def close_application(self):
        """Close the application."""
        self.close()
        QApplication.instance().quit()