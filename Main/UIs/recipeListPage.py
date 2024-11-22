import tkinter as tk
from tkinter import ttk
import functools
import sys
import os
from API.getRecipes import get_recipes_by_ingredients
from PIL import Image, ImageTk
import requests
from io import BytesIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Function to close the window
def close_window():
    root.destroy()

# Function to toggle favourite status
def toggle_favourite(event, heart_label, recipe):
    # Update the favourite status
    recipe["favourite"] = not recipe["favourite"]
    # Change the heart color based on the new status
    new_color = "red" if recipe["favourite"] else "white"
    heart_label.config(fg=new_color)

    print(f"Toggled {recipe['name']} favourite to {recipe['favourite']}")

# Function to adjust scroll region based on content height
def update_scrollregion(event=None):
    # Calculate the total height of the recipes and update the scroll region accordingly
    total_height = sum(child.winfo_height() for child in recipe_frame.winfo_children())

    # Ensure the recipe frame height doesn't exceed MAX_FRAME_HEIGHT
    frame_height = min(total_height, MAX_FRAME_HEIGHT)

    # Update the canvas scroll region with the new height of the frame
    canvas.config(scrollregion=(0, 0, 0, frame_height))

def load_image_from_url(url):
    response = requests.get(url)  # Get the image from the URL
    img_data = BytesIO(response.content)  # Convert to BytesIO for PIL
    img = Image.open(img_data)  # Open the image using PIL
    return img

# Initialise the main window
root = tk.Tk()
root.title("Recipe List")
root.geometry("800x400")
root.configure(bg="#f6f7fb")

style = ttk.Style()
style.theme_use('default')

# Configure the style for select buttons
style.configure('Select.TButton', 
    background='#4355ff',
    foreground='white',
    font=('Helvetica', 10, 'bold'),
    borderwidth=0,
    relief='flat'
)

top_frame = tk.Frame(root, bg="#4355ff", bd=2, relief="flat")
top_frame.pack(fill="x", side="top", pady=0)

title_label = tk.Label(top_frame, text="Recipe List", font=("Helvetica", 16, "bold"), bg="#4355ff", fg="white")
title_label.pack(expand=True)

# Create a canvas and a vertical scrollbar
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the recipe frames
recipe_frame = tk.Frame(canvas, bg="#1C1C1C")
canvas.create_window((0, 0), window=recipe_frame, anchor="nw")


# Define the maximum height for the recipe frame
MAX_FRAME_HEIGHT = 250

ingredients = ["apples","bananas","milk","butter","chicken","steak","carrots","yoghurt","ketchup"] #test data
recipes = get_recipes_by_ingredients(ingredients)

# Populate the frame with recipes
for recipe in recipes.values():
    #print(recipe)
    # Create a frame for each recipe
    recipe_frame_item = tk.Frame(recipe_frame, bg="#333333", bd=1, relief="solid")
    recipe_frame_item.pack(fill="x", pady=5)

    try:
        img = load_image_from_url(recipe[7])  # Open the image
        img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize to fit the card
        profile_image = ImageTk.PhotoImage(img)
        icon_label = tk.Label(recipe_frame_item, image=profile_image, bg="#f6f7fb")
        icon_label.image = profile_image  # Prevent garbage collection
    except Exception as e:
        print("Error")
        icon_label = tk.Label(recipe_frame_item, text="No Image", bg="#f6f7fb", fg="black", font=("Helvetica", 10, "bold"))

    icon_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)

    # Add recipe name, time, and serves information
    recipe_info = f"{recipe[1]}\n{recipe[5]} - Serves: {recipe[6]}"
    info_label = tk.Label(recipe_frame_item, text=recipe_info, bg="#333333", fg="white", font=("Arial", 10), anchor="w", justify="left")
    info_label.grid(row=0, column=1, padx=10, pady=5)

    # Add ingredients used/needed information
    ingredients_info = f"Ingredients Used: {recipe[3]}\nIngredients Needed: {recipe[2]}"
    ingredients_label = tk.Label(recipe_frame_item, text=ingredients_info, bg="#333333", fg="white", font=("Arial", 10), anchor="w", justify="left")
    ingredients_label.grid(row=1, column=1, padx=10, pady=5)

    '''
    # Add clickable heart icon
    heart_color = "red" if recipe["favourite"] else "white"
    heart_label = tk.Label(recipe_frame_item, text="♥", font=("Arial", 18), bg="#333333", fg=heart_color, cursor="hand2")
    heart_label.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

    # Use functools.partial to pass the current heart_label and recipe
    heart_label.bind(
        "<Button-1>",
        functools.partial(toggle_favourite, heart_label=heart_label, recipe=recipe)
    )
    '''

# Call the function to update scroll region on window resize
recipe_frame.bind("<Configure>", update_scrollregion)

# Bottom frame for close button
bottom_frame = tk.Frame(root, bg="#87CEFA")
bottom_frame.pack(side="bottom", fill="x", pady=10)

# Close button
close_button = ttk.Button(bottom_frame, text="Close", command=close_window, style="Select.TButton")
close_button.pack()

# Start the GUI loop
root.mainloop()
