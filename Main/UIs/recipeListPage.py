import tkinter as tk
from tkinter import ttk

# Function to close the window
def close_window():
    root.destroy()

# Initialise the main window
root = tk.Tk()
root.title("Recipe List")
root.geometry("400x400")
root.configure(bg="#87CEFA")

# Title label
title_label = tk.Label(root, text="Recipe List", font=("Arial", 16), bg="#87CEFA", fg="black")
title_label.pack(pady=10)

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
MAX_FRAME_HEIGHT = 250  # Set the maximum height here

# Sample data to dynamically populate the GUI (replace with data from an external source)
recipes = [
    {
        "name": "Pizza",
        "time": "1h, 20mins",
        "serves": "2",
        "ingredients_used": "7",
        "ingredients_needed": "3",
        "favourite": True
    },
    {
        "name": "Fish & Chips",
        "time": "1h, 45mins",
        "serves": "2",
        "ingredients_used": "5",
        "ingredients_needed": "2",
        "favourite": False
    },
    {
        "name": "Veggie Stir Fry",
        "time": "30mins",
        "serves": "3",
        "ingredients_used": "5",
        "ingredients_needed": "4",
        "favourite": True
    },
    {
        "name": "Pasta Carbonara",
        "time": "40mins",
        "serves": "4",
        "ingredients_used": "6",
        "ingredients_needed": "4",
        "favourite": False
    },
    {
        "name": "Tacos",
        "time": "20mins",
        "serves": "2",
        "ingredients_used": "4",
        "ingredients_needed": "3",
        "favourite": True
    }
]

# Populate the frame with recipes
for recipe in recipes:
    # Create a frame for each recipe
    recipe_frame_item = tk.Frame(recipe_frame, bg="#333333", bd=1, relief="solid")
    recipe_frame_item.pack(fill="x", pady=5)

    # Add image placeholder
    image_label = tk.Label(recipe_frame_item, text="🍴", font=("Arial", 24), bg="#333333", fg="white")
    image_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

    # Add recipe name, time, and serves information
    recipe_info = f"{recipe['name']}\n{recipe['time']} - Serves: {recipe['serves']}"
    info_label = tk.Label(recipe_frame_item, text=recipe_info, bg="#333333", fg="white", font=("Arial", 10), anchor="w", justify="left")
    info_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)

    # Add ingredients used/needed information
    ingredients_info = f"Ingredients Used: {recipe['ingredients_used']}\nIngredients Needed: {recipe['ingredients_needed']}"
    ingredients_label = tk.Label(recipe_frame_item, text=ingredients_info, bg="#333333", fg="white", font=("Arial", 10), anchor="w", justify="left")
    ingredients_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    # Add favourite icon (heart)
    heart_color = "red" if recipe["favourite"] else "white"
    heart_label = tk.Label(recipe_frame_item, text="♥", font=("Arial", 18), bg="#333333", fg=heart_color)
    heart_label.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

# Function to adjust scroll region based on content height
def update_scrollregion(event=None):
    # Calculate the total height of the recipes and update the scroll region accordingly
    total_height = sum(child.winfo_height() for child in recipe_frame.winfo_children())

    # Ensure the recipe frame height doesn't exceed MAX_FRAME_HEIGHT
    frame_height = min(total_height, MAX_FRAME_HEIGHT)

    # Update the canvas scroll region with the new height of the frame
    canvas.config(scrollregion=(0, 0, 0, frame_height))

# Call the function to update scroll region on window resize
recipe_frame.bind("<Configure>", update_scrollregion)

# Bottom frame for close button
bottom_frame = tk.Frame(root, bg="#87CEFA")
bottom_frame.pack(side="bottom", fill="x", pady=10)

# Close button
close_button = tk.Button(bottom_frame, text="Close", command=close_window, bg="#B0C4DE", width=10)
close_button.pack()

# Start the GUI loop
root.mainloop()
