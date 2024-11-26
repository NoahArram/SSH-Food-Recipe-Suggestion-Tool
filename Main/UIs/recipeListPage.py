# recipeListPage.py
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from io import BytesIO

# Import RecipeInstructionsPage
from UIs.recipeInfoPage import RecipeInstructionsPage

from API import getRecipes

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Function to load an image from a URL
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
        self.setGeometry(100, 100, 800, 600)
        self.recipes = recipes
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Title
        title_label = QLabel("Recipe List")
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: white; background-color: #4355ff;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Scroll area for recipes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Scroll area content
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        # Populate the recipes
        for recipe in self.recipes.values():
            recipe_frame = QFrame()
            recipe_frame.setStyleSheet("background-color: #333333; border: 1px solid #444;")
            recipe_frame.setFrameShape(QFrame.StyledPanel)
            recipe_layout = QHBoxLayout(recipe_frame)

            # Image
            if recipe[7]:
                pixmap = load_image_from_url(recipe[7])
                if pixmap:
                    image_label = QLabel()
                    image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                    recipe_layout.addWidget(image_label)
                else:
                    image_label = QLabel("No Image")
                    image_label.setStyleSheet("color: white; font-weight: bold;")
                    recipe_layout.addWidget(image_label)

            # Recipe info
            info_layout = QVBoxLayout()
            recipe_info = f"{recipe[1]}\nTime: {recipe[5]} minutes - Serves: {recipe[6]}"
            info_label = QLabel(recipe_info)
            info_label.setStyleSheet("color: white; font-size: 10pt;")
            info_layout.addWidget(info_label)

            ingredients_info = "Ingredients Used:"+str(recipe[3])+"\nIngredients Needed:" +str(recipe[2])
            ingredients_label = QLabel(ingredients_info)
            ingredients_label.setStyleSheet("color: white; font-size: 10pt;")
            info_layout.addWidget(ingredients_label)

            # Add a button to view recipe details
            view_button = QPushButton("View Recipe")
            view_button.setStyleSheet("background-color: #4355ff; color: white;")
            view_button.clicked.connect(lambda checked, r_id=recipe[0]: self.open_recipe_info(r_id))
            info_layout.addWidget(view_button)

            recipe_layout.addLayout(info_layout)
            scroll_layout.addWidget(recipe_frame)

        # Add the back and close buttons
        button_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #4355ff; color: white; font-size: 10pt; font-weight: bold;")
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color: #4355ff; color: white; font-size: 10pt; font-weight: bold;")
        close_button.clicked.connect(self.close_application)
        button_layout.addWidget(close_button)
        
        main_layout.addLayout(button_layout)

    def go_back(self):
        """Return to the tenant selection page."""
        self.close()
        if self.parent() is not None:
            self.parent().show()

    def close_application(self):
        """Close the application."""
        self.close()
        QApplication.instance().quit()

    def open_recipe_info(self, recipe_id):
        """Open the recipe information page."""
        from API import getRecipeInfo
        recipe_info = getRecipeInfo.get_recipe_info(recipe_id)
        self.recipeInfoWindow = RecipeInstructionsPage(recipe_info, parent=self)
        self.recipeInfoWindow.show()
        self.hide()  # Hide the current window instead of closing it

# recipes = get_recipes_by_ingredients(ingredients)

'''
ingredients = ["apples", "bananas", "milk", "butter"]

# Call the function and print the results
recipes = getRecipes.get_recipes_by_ingredients(ingredients)
print("Ranked Recipes:")
for rank, recipe in recipes.items():
    print(f"Rank: {rank}")
    print(f"ID: {recipe[0]}")
    print(f"Title: {recipe[1]}")
    print(f"Missed Ingredients: {recipe[2]}")
    print(f"Used Ingredients: {recipe[3]}")
    print(f"Rank Score: {recipe[4]:.2f}")
    print(f"Preparation Time: {recipe[5]} minutes")
    print(f"Servings: {recipe[6]}")
    print(f"Image URL: {recipe[7]}")
    print()
'''