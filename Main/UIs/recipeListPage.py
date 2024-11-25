import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from io import BytesIO


from API import getRecipeInfo
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
    def __init__(self, recipes):
        super().__init__()
        self.setWindowTitle("Recipe List")
        self.setGeometry(100, 100, 800, 600)

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
        for recipe in recipes.values():
            recipe_frame = QFrame()
            recipe_frame.setStyleSheet("background-color: #333333; border: 1px solid #444;")
            recipe_frame.setFrameShape(QFrame.StyledPanel)
            recipe_layout = QHBoxLayout(recipe_frame)

            # Image
            if recipe['image']:
                pixmap = load_image_from_url(recipe['image'])
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
            recipe_info = f"{recipe['name']}\n{recipe['time']} - Serves: {recipe['servings']}"
            info_label = QLabel(recipe_info)
            info_label.setStyleSheet("color: white; font-size: 10pt;")
            info_layout.addWidget(info_label)

            ingredients_info = f"Ingredients Used: {', '.join(recipe['ingredients_used'])}\nIngredients Needed: {', '.join(recipe['ingredients_needed'])}"
            ingredients_label = QLabel(ingredients_info)
            ingredients_label.setStyleSheet("color: white; font-size: 10pt;")
            info_layout.addWidget(ingredients_label)

            recipe_layout.addLayout(info_layout)
            scroll_layout.addWidget(recipe_frame)

        # Close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color: #4355ff; color: white; font-size: 10pt; font-weight: bold;")
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)

# recipes = get_recipes_by_ingredients(ingredients)
recipes = {
    1: {
        'name': 'Apple Pie',
        'time': '45 minutes',
        'servings': 4,
        'ingredients_used': ['apples', 'butter'],
        'ingredients_needed': ['sugar', 'flour'],
        'image': 'https://picsum.photos/200/300'
    },
    2: {
        'name': 'Banana Smoothie',
        'time': '10 minutes',
        'servings': 2,
        'ingredients_used': ['bananas', 'milk', 'yoghurt'],
        'ingredients_needed': [],
        'image': 'https://picsum.photos/200/300'
    },
    3: {
        'name': 'Chicken Curry',
        'time': '60 minutes',
        'servings': 6,
        'ingredients_used': ['chicken', 'carrots'],
        'ingredients_needed': ['spices', 'onions'],
        'image': 'https://picsum.photos/200/300'
    }
}

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

# Run the application
app = QApplication(sys.argv)
window = RecipeApp(recipes)
window.show()
sys.exit(app.exec_())
