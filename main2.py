import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt

# Database connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dhruvsingh',
    'database': 'workout_tracker1'
}

# Define the muscle groups and associated images
muscle_groups = {
    'Chest': 'E:/HACKATHON/images/chest.png',
    'Back': 'E:/HACKATHON/images/back.png',
    'Shoulder': 'E:/HACKATHON/images/shoulder.png',
    'Biceps' : 'E:/HACKATHON/images/bicep.png',
    'Triceps' : 'E:/HACKATHON/images/tricep.png',
    'Quads' : 'E:/HACKATHON/images/quads.png',
    'Hamstring' : 'E:/HACKATHON/images/hamstring.png',
    'Calves' : 'E:/HACKATHON/images/calves.png',
    'Glutes' : 'E:/HACKATHON/images/glutes.png',
    'Core' : 'E:/HACKATHON/images/core.png'
}
# Create the main application window
root = tk.Tk()
root.title("Workout Tracker and Muscle Visualization")
root.geometry("1200x800")  # Set window size
root.attributes('-fullscreen', True)  # Set the window to fullscreen

# Dark mode colors
bg_color = "#181819"  # Dark background
fg_color = "#FFFFFF"  # White foreground
button_bg_color = "#3E3E3E"  # Button background
button_fg_color = "#FFFFFF"  # Button text color

# Create a frame for input options with increased width
input_frame = tk.Frame(root, width=600, bg=bg_color)  # Increased width to 600
input_frame.pack(side=tk.LEFT, fill=tk.Y)

# Create a frame for muscle images
image_frame = tk.Frame(root, bg="black")
image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Global session variable
current_session = {'exercises': [], 'muscles': {muscle: 0 for muscle in muscle_groups.keys()}}

# Connect to MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Database Connection Error", f"Error: {e}")
        return None

# Function to add exercise and intensities to the database
def add_exercise_to_db():
    exercise_name = exercise_entry.get()
    try:
        intensity_values = [int(entry.get()) for entry in intensity_entries]
        if exercise_name and any(intensity_values):
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO exercises (name, chest, back, shoulders, biceps, triceps,
                                           quadriceps, hamstrings, calves, glutes, core)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [exercise_name] + intensity_values
                )
                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Exercise Added", f"Exercise '{exercise_name}' added to the database.")
        else:
            messagebox.showerror("Input Error", "Please enter a valid exercise name and intensities.")
    except ValueError:
        messagebox.showerror("Input Error", "Intensity values must be numbers.")
    
    exercise_entry.delete(0, tk.END)
    for entry in intensity_entries:
        entry.delete(0, tk.END)

# Function to load exercises from the database
def load_exercises():
    exercise_listbox.delete(0, tk.END)  # Clear the listbox before loading
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM exercises")
        exercises = cursor.fetchall()
        exercise_names = [exercise[0] for exercise in exercises]
        cursor.close()
        connection.close()
        for exercise_name in exercise_names:
            exercise_listbox.insert(tk.END, exercise_name)

# Function to select an exercise from the database
def select_exercise():
    selected_exercise = exercise_listbox.get(tk.ACTIVE)
    if not selected_exercise:
        messagebox.showerror("Selection Error", "Please select an exercise from the list.")
        return

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM exercises WHERE name = %s", (selected_exercise,))
        exercise_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if exercise_data:
            _, name, *intensities = exercise_data
            current_session['exercises'].append(name)
            try:
                for i, muscle in enumerate(muscle_groups.keys()):
                    current_session['muscles'][muscle] += int(intensities[i])  # Convert intensity to int
            except (IndexError, ValueError) as e:
                messagebox.showerror("Data Error", f"Error processing intensities: {e}")
                return
            messagebox.showinfo("Exercise Selected", f"Selected '{name}' and added to the current session.")

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM exercises WHERE name = %s", (selected_exercise,))
        exercise_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if exercise_data:
            _, name, *intensities = exercise_data
            current_session['exercises'].append(name)
            for i, muscle in enumerate(muscle_groups.keys()):
                current_session['muscles'][muscle] += intensities[i]
            messagebox.showinfo("Exercise Selected", f"Selected '{name}' and added to the current session.")

def display_muscle_images():
    # Clear the image frame
    for widget in image_frame.winfo_children():
        widget.destroy()

    # Create a blank transparent image with a size suitable for the muscle images
    final_image = Image.new('RGBA', (810, 671), (0, 0, 0, 0))

    # Loop through each muscle group and its intensity
    for muscle, intensity in current_session['muscles'].items():
        image_path = muscle_groups.get(muscle)

        if image_path and os.path.exists(image_path):
            # Load the muscle group image and set transparency based on intensity
            muscle_image = Image.open(image_path).convert('RGBA')
            alpha = int(255 * (intensity / 10))  # Map intensity (0-10) to alpha (0-255)
            muscle_image.putalpha(alpha)

            # Resize the muscle image to match the final image dimensions
            muscle_image = muscle_image.resize((810, 671), Image.ANTIALIAS)

            # Combine muscle image with the final image
            final_image = Image.alpha_composite(final_image, muscle_image)

    # Convert to ImageTk format and display in the GUI
    tk_image = ImageTk.PhotoImage(final_image)
    image_label = tk.Label(image_frame, image=tk_image, bg="black")
    image_label.image = tk_image  # Keep a reference to avoid garbage collection
    image_label.pack(side=tk.TOP, padx=10, pady=10)

# Function to refresh exercise list
def refresh_exercise_list():
    load_exercises()

def save_weight():
    weight = weight_entry.get()
    try:
        weight_value = float(weight)
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO weights (weight_date, weight_value) VALUES (NOW(), %s)", (weight_value,))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Weight Tracker", "Weight recorded successfully.")
            weight_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Database Error", "Could not connect to the database.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid weight.")

# Function to visualize weight history
def visualize_weight_history():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT weight_date, weight_value FROM weights ORDER BY weight_date")
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        if records:
            dates = [record[0] for record in records]
            weights = [record[1] for record in records]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, weights, marker='o', color='cyan')
            plt.title("Weight Over Time", color='black')  # Changed title color to black
            plt.xlabel("Date", color='black')  # Changed x label color to black
            plt.ylabel("Weight (kg)", color='black')  # Changed y label color to black
            plt.xticks(rotation=45, color='black')  # Changed tick color to black
            plt.yticks(color='black')  # Changed tick color to black
            
            # Remove the dark mode background
            plt.gca().set_facecolor('white')  # Set the plot background color to white
            plt.grid(color='grey', linestyle='--', linewidth=0.5)  # Optional: Add grid for better readability
            
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("Weight History", "No weight records found.")

# Create a vertical separator
separator = tk.Frame(root, width=2, bg="black")
separator.pack(side=tk.LEFT, fill=tk.Y)

# Create labels and entry boxes for user input
exercise_label = tk.Label(input_frame, text="Exercise Name:", bg=bg_color, fg=fg_color)
exercise_label.pack(pady=5)
exercise_entry = tk.Entry(input_frame)
exercise_entry.pack(pady=5)

intensity_labels = []
intensity_entries = []

for muscle in muscle_groups.keys():
    label = tk.Label(input_frame, text=f"{muscle} Intensity (0-10):", bg=bg_color, fg=fg_color)
    label.pack(pady=2)
    entry = tk.Entry(input_frame)
    entry.pack(pady=2)
    intensity_labels.append(label)
    intensity_entries.append(entry)
# Button styles with smaller size
button_style = {
    'bg': button_bg_color,
    'fg': button_fg_color,
    'activebackground': "#5E5E5E",
    'activeforeground': button_fg_color,
    'padx': 10,  # Reduced padding
    'pady': 5,   # Reduced padding
    'font': ('Arial', 10)  # Smaller font size
}

# Button to add an exercise to the database
add_exercise_button = tk.Button(input_frame, text="Add Exercise to Database", command=add_exercise_to_db, **button_style)
add_exercise_button.pack(pady=5)

# Weight tracker input
weight_label = tk.Label(input_frame, text="Enter Weight (kg):", bg=bg_color, fg=fg_color)
weight_label.pack(pady=5)
weight_entry = tk.Entry(input_frame)
weight_entry.pack(pady=5)

# Button to save daily weight to the database
save_weight_button = tk.Button(input_frame, text="Save Weight", command=save_weight, **button_style)
save_weight_button.pack(pady=5)

# Button to visualize weight history
visualize_weight_button = tk.Button(input_frame, text="Visualize Weight History", command=visualize_weight_history, **button_style)
visualize_weight_button.pack(pady=5)

# Listbox for selecting exercises from the database
exercise_list_label = tk.Label(input_frame, text="Select Exercise from Database:", bg=bg_color, fg=fg_color)
exercise_list_label.pack(pady=5)
exercise_listbox = tk.Listbox(input_frame, width=40, height=8)  # Increased width for better visibility
exercise_listbox.pack(pady=5)

# Load exercises into the listbox
load_exercises()

select_exercise_button = tk.Button(input_frame, text="Select Exercise", command=select_exercise, **button_style)
select_exercise_button.pack(pady=5)

# Button to visualize muscle images
visualize_images_button = tk.Button(input_frame, text="Visualize Muscle Images", command=display_muscle_images, **button_style)
visualize_images_button.pack(pady=5)

# Refresh button
refresh_button = tk.Button(input_frame, text="Refresh Exercise List", command=refresh_exercise_list, **button_style)
refresh_button.pack(pady=5)

# Close and minimize buttons
close_button = tk.Button(input_frame, text="Close", command=root.destroy, bg='red', fg='white')
close_button.pack(pady=5)
minimize_button = tk.Button(input_frame, text="Minimize", command=root.iconify, **button_style)
minimize_button.pack(pady=5)

# Run the application
root.mainloop()
