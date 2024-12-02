import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QWidget, QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from io import BytesIO
from API import getRecipeInfo


def load_image_from_url(url):
    try:
        if not url:
            print("Image URL is empty")
            return QPixmap("default_image.png")  # still need to edit this part
        response = requests.get(url, timeout=5)
        response.raise_for_status()  
        img_data = BytesIO(response.content)
        pixmap = QPixmap()
        if not pixmap.loadFromData(img_data.getvalue()):
            print(f"Failed to load image from URL: {url}")
            return QPixmap("default_image.png")
        return pixmap
    except Exception as e:
        print(f"Error loading image from URL: {e}")
        return QPixmap("default_image.png")


class RecipeInstructionsPage(QMainWindow):
    def __init__(self, recipe, parent=None):
        super().__init__(parent)
        self.recipe = recipe
        self.parent_window = parent
        self.setGeometry(100, 100, 1000, 600)  
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        title_label = QLabel(self.recipe[4])  
        title_label.setStyleSheet(
            "font-size: 18pt; font-weight: bold; color: white; background-color: #4355ff; padding: 10px; margin: 0px;"
        )
        title_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #333333; border: none;")
        main_layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)

        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        metadata_frame = QFrame()
        metadata_frame.setStyleSheet("background-color: #444444; border: none; border-radius: 10px;")
        metadata_layout = QHBoxLayout(metadata_frame)
        metadata_layout.setContentsMargins(10, 10, 10, 10)
        metadata_layout.setSpacing(15)

        pixmap = load_image_from_url(self.recipe[5])  # Assuming recipe[5] is the image URL
        image_label = QLabel()
        if pixmap and not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            image_label.setText("No Image")
            image_label.setStyleSheet("color: white; font-weight: bold;")
        image_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        metadata_layout.addWidget(image_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        time_label = QLabel(f"<b>Cooking Time:</b> {self.recipe[2]} minutes")  
        time_label.setStyleSheet("color: white; font-size: 12pt;")
        info_layout.addWidget(time_label)

        servings_label = QLabel(f"<b>Servings:</b> {self.recipe[3]}")  
        servings_label.setStyleSheet("color: white; font-size: 12pt;")
        info_layout.addWidget(servings_label)

        metadata_layout.addLayout(info_layout)
        scroll_layout.addWidget(metadata_frame)

        ingredients_frame = QFrame()
        ingredients_frame.setStyleSheet("background-color: #1C1C1C; border: none; border-radius: 10px;")
        ingredients_layout = QVBoxLayout(ingredients_frame)
        ingredients_layout.setContentsMargins(10, 10, 10, 10)

        ingredients_title = QLabel("Ingredients")
        ingredients_title.setStyleSheet("font-size: 14pt; font-weight: bold; color: white; margin-bottom: 10px;")
        ingredients_title.setAlignment(Qt.AlignLeft)
        ingredients_layout.addWidget(ingredients_title)

        for ingredient in self.recipe[0]:  # Assuming recipe[0] is a list of ingredients
            ingredient_label = QLabel(ingredient)
            ingredient_label.setStyleSheet("color: white; font-size: 10pt;")
            ingredient_label.setWordWrap(True)
            ingredients_layout.addWidget(ingredient_label)

        scroll_layout.addWidget(ingredients_frame)

        # Instructions
        instructions_frame = QFrame()
        instructions_frame.setStyleSheet("background-color: #1C1C1C; border: none; border-radius: 10px;")
        instructions_layout = QVBoxLayout(instructions_frame)
        instructions_layout.setContentsMargins(10, 10, 10, 10)

        instructions_title = QLabel("Instructions")
        instructions_title.setStyleSheet("font-size: 14pt; font-weight: bold; color: white; margin-bottom: 10px;")
        instructions_title.setAlignment(Qt.AlignLeft)
        instructions_layout.addWidget(instructions_title)

        for i, step in enumerate(self.recipe[1], start=1):  # Assuming recipe[1] is a list of steps
            step_label = QLabel(f"{i}. {step}")
            step_label.setStyleSheet("color: white; font-size: 10pt;")
            step_label.setWordWrap(True)
            instructions_layout.addWidget(step_label)

        scroll_layout.addWidget(instructions_frame)

        # Back button
        back_button = QPushButton("Back")
        back_button.setFixedWidth(100)
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4355ff; 
                color: white; 
                font-size: 16px; 
                padding: 12px; 
                font-weight: bold; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6aff;
            }
        """

        )
        back_button.clicked.connect(self.go_back)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(back_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    def go_back(self):
        """Return to the recipe list."""
        self.close()
        if self.parent_window is not None:
            self.parent_window.show()


    def go_back(self):
        """Return to the recipe list."""
        self.close()
        if self.parent_window is not None:
            self.parent_window.show()

    def get_recipes(self):
        """Retrieve recipes again or pass them as needed."""
        # Implement a method to retrieve or pass the recipes
        # For this example, we can return an empty dictionary or re-fetch
        return {}
        back_button.setStyleSheet(
            "background-color: #4355ff; color: white; font-size: 12pt; font-weight: bold; padding: 10px;"
        )
        back_button.clicked.connect(self.go_back)

        # Center the button at the bottom
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(back_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    def go_back(self):
        """Return to the recipe list."""
        self.close()
        if self.parent_window is not None:
            self.parent_window.show()

    def get_recipes(self):
        """Retrieve recipes again or pass them as needed."""
        # Implement a method to retrieve or pass the recipes
        # For this example, we can return an empty dictionary or re-fetch
        return {}


# Test the application with dummy data if running directly
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecipeInstructionsPage(getRecipeInfo.get_recipe_info(875447))
    window.show()
    sys.exit(app.exec_())
