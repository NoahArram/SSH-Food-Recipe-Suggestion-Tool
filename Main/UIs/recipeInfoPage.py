import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from io import BytesIO


def load_image_from_url(url):
    try:
        if not url:
            print("Image URL is empty")
            return QPixmap("default_image.png")  # Use a placeholder image
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
        title_label = QLabel(recipe['name'])
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: white; background-color: #4355ff;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Scrollable area for instructions
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Scrollable content
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        # Recipe metadata (time and servings)
        metadata_frame = QFrame()
        metadata_frame.setStyleSheet("background-color: #333333; border: 1px solid #444;")
        metadata_layout = QVBoxLayout(metadata_frame)

        time_label = QLabel(f"Cooking Time: {recipe['time']}")
        time_label.setStyleSheet("color: white; font-size: 12pt;")
        metadata_layout.addWidget(time_label)

        servings_label = QLabel(f"Servings: {recipe['servings']}")
        servings_label.setStyleSheet("color: white; font-size: 12pt;")
        metadata_layout.addWidget(servings_label)

        scroll_layout.addWidget(metadata_frame)

        # Instructions
        instructions_frame = QFrame()
        instructions_frame.setStyleSheet("background-color: #1C1C1C; border: 1px solid #444; padding: 10px;")
        instructions_layout = QVBoxLayout(instructions_frame)

        instructions_title = QLabel("Instructions")
        instructions_title.setStyleSheet("font-size: 14pt; font-weight: bold; color: white;")
        instructions_title.setAlignment(Qt.AlignLeft)
        instructions_layout.addWidget(instructions_title)

        # Add each instruction step
        for i, step in enumerate(recipe['instructions'], start=1):
            step_label = QLabel(f"{i}. {step}")
            step_label.setStyleSheet("color: white; font-size: 10pt; margin-bottom: 5px;")
            step_label.setWordWrap(True)  # Allow text to wrap within the frame
            instructions_layout.addWidget(step_label)

        scroll_layout.addWidget(instructions_frame)

        # Back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #4355ff; color: white; font-size: 10pt; font-weight: bold;")
        back_button.clicked.connect(self.close)
        main_layout.addWidget(back_button)

# Dummy recipe data for testing
dummy_recipe = {
    'name': 'Apple Pie',
    'time': '45 minutes',
    'servings': 4,
    'image': 'https://picsum.photos/200/300',
    'instructions': [
        "Preheat the oven to 180°C (350°F).",
        "Peel, core, and slice the apples.",
        "Mix the apples with sugar, cinnamon, and lemon juice.",
        "Roll out the pie crust and place it in a pie dish.",
        "Fill the crust with the apple mixture and cover with the top crust.",
        "Bake for 45 minutes or until the crust is golden brown.",
        "Allow the pie to cool before serving."
    ]
}

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecipeInstructionsPage(dummy_recipe)
    window.show()
    sys.exit(app.exec_())
