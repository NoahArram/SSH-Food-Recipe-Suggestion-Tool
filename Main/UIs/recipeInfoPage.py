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
            return QPixmap("default_image.png")  # Use a placeholder image if URL is empty
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception for HTTP errors
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
    def __init__(self, recipe):
        super().__init__()
        self.setWindowTitle("Recipe Instructions")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Title
        title_label = QLabel(recipe[4])  # Assuming recipe[4] is the title
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: white; background-color: #4355ff; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Scrollable area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Scrollable content
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)

        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        # Recipe metadata (image, time, and servings)
        metadata_frame = QFrame()
        metadata_frame.setStyleSheet("background-color: #333333; border: 1px solid #444;")
        metadata_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        metadata_layout = QHBoxLayout(metadata_frame)
        metadata_layout.setContentsMargins(10, 10, 10, 10)
        metadata_layout.setSpacing(10)

        # Load the image
        pixmap = load_image_from_url(recipe[5])  # Assuming recipe[5] is the image URL
        if pixmap and not pixmap.isNull():
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        else:
            image_label = QLabel("No Image")
            image_label.setStyleSheet("color: white; font-weight: bold;")
            image_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        metadata_layout.addWidget(image_label)

        # Time and Servings
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)
        info_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        time_label = QLabel(f"Cooking Time: {recipe[2]} minutes")  # Assuming recipe[2] is time in minutes
        time_label.setStyleSheet("color: white; font-size: 12pt;")
        time_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        info_layout.addWidget(time_label)

        servings_label = QLabel(f"Servings: {recipe[3]}")  # Assuming recipe[3] is servings
        servings_label.setStyleSheet("color: white; font-size: 12pt;")
        servings_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        info_layout.addWidget(servings_label)

        metadata_layout.addLayout(info_layout)
        scroll_layout.addWidget(metadata_frame)

        # Ingredients
        ingredients_frame = QFrame()
        ingredients_frame.setStyleSheet("background-color: #1C1C1C; border: 1px solid #444;")
        ingredients_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        ingredients_layout = QVBoxLayout(ingredients_frame)
        ingredients_layout.setContentsMargins(10, 10, 10, 10)
        ingredients_layout.setSpacing(5)

        ingredients_title = QLabel("Ingredients")
        ingredients_title.setStyleSheet("font-size: 14pt; font-weight: bold; color: white;")
        ingredients_title.setAlignment(Qt.AlignLeft)
        ingredients_layout.addWidget(ingredients_title)

        for ingredient in recipe[0]:  # Assuming recipe[0] is a list of ingredients
            ingredient_label = QLabel(ingredient)
            ingredient_label.setStyleSheet("color: white; font-size: 10pt;")
            ingredient_label.setWordWrap(True)
            ingredient_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            ingredients_layout.addWidget(ingredient_label)

        scroll_layout.addWidget(ingredients_frame)

        # Instructions
        instructions_frame = QFrame()
        instructions_frame.setStyleSheet("background-color: #1C1C1C; border: 1px solid #444;")
        instructions_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        instructions_layout = QVBoxLayout(instructions_frame)
        instructions_layout.setContentsMargins(10, 10, 10, 10)
        instructions_layout.setSpacing(5)

        instructions_title = QLabel("Instructions")
        instructions_title.setStyleSheet("font-size: 14pt; font-weight: bold; color: white;")
        instructions_title.setAlignment(Qt.AlignLeft)
        instructions_layout.addWidget(instructions_title)

        for i, step in enumerate(recipe[1], start=1):  # Assuming recipe[1] is a list of steps
            step_label = QLabel(f"{i}. {step}")
            step_label.setStyleSheet("color: white; font-size: 10pt;")
            step_label.setWordWrap(True)
            step_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            instructions_layout.addWidget(step_label)

        scroll_layout.addWidget(instructions_frame)

        # Back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #4355ff; color: white; font-size: 12pt; font-weight: bold; padding: 10px;")
        back_button.clicked.connect(self.close)
        main_layout.addWidget(back_button, alignment=Qt.AlignCenter)


# Test the application with dummy data if running directly
if __name__ == "__main__":
    app = QApplication(sys.argv)


    

    window = RecipeInstructionsPage(getRecipeInfo.get_recipe_info(875447))
    window.show()
    sys.exit(app.exec_())
