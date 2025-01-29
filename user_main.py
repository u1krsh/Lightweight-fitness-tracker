import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from hashlib import sha256
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt

# database connect
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dhruvsingh',
    'database': 'workout_tracker1'
}

# muscles
muscle_groups = {
    'Chest': 'E:/HACKATHON/images/chest.png',
    'Back': 'E:/HACKATHON/images/back.png',
    'Shoulder': 'E:/HACKATHON/images/shoulder.png',
    'Biceps': 'E:/HACKATHON/images/bicep.png',
    'Triceps': 'E:/HACKATHON/images/tricep.png',
    'Quads': 'E:/HACKATHON/images/quads.png',
    'Hamstring': 'E:/HACKATHON/images/hamstring.png',
    'Calves': 'E:/HACKATHON/images/calves.png',
    'Glutes': 'E:/HACKATHON/images/glutes.png',
    'Core': 'E:/HACKATHON/images/core.png'
}

# main application window
root = tk.Tk()
root.title("LightWeight")
root.geometry("1200x800")  # Set window size
root.attributes('-fullscreen', True)  # Set the window to fullscreen

root.iconbitmap('bg.ico')

# Dark mode colors
bg_color = "#181819"  # Dark background
fg_color = "#FFFFFF"  # White foreground
button_bg_color = "#3E3E3E"  # Button background
button_fg_color = "#FFFFFF"  # Button text color

# Ctop title bar
title_bar = tk.Frame(root, bg="#2A2A2A", relief="raised", bd=2)
title_bar.pack(side=tk.TOP, fill=tk.X)

app_name_label = tk.Label(title_bar, text="LightWeight", bg="#2A2A2A", fg=fg_color, font=("BOOTLE", 14, "bold"))
app_name_label.pack(side=tk.LEFT, padx=10)
# Close button 
def close_app():
    root.quit()

# Minimize button 
def minimize_app():
    root.iconify()  # Minimize 

# Create a rounded button 
def create_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command, bg=button_bg_color, fg=button_fg_color, relief='flat', padx=10, pady=5)
    button.pack(side=tk.RIGHT, padx=5)

# Create the close and minimize 
create_button(title_bar, "Minimize", minimize_app)
create_button(title_bar, "Close", close_app)

#user authentication
auth_frame = tk.Frame(root, bg=bg_color)
auth_frame.pack(fill=tk.BOTH, expand=True)

#create a connection to the database
def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Database Connection Error", f"Error: {e}")
        return None

#hash the password
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# register new user
def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    if username and password:
        hashed_password = hash_password(password)
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                connection.commit()
                messagebox.showinfo("Registration Successful", "User registered successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Registration Error", f"Error: {err}")
            finally:
                cursor.close()
                connection.close()
    else:
        messagebox.showerror("Input Error", "Please fill in all fields.")

#log in a user
def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()
    hashed_password = hash_password(password)

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            messagebox.showinfo("Login Successful", "Welcome to the Workout Tracker!")
            auth_frame.pack_forget()  # Hide auth frame
            setup_workout_tracker()  # Show workout tracker UI
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

#registration and login UI
def create_auth_ui():
    # Load logo image
    logo_path = "E:/HACKATHON/images/bg.png"  # Replace with the path to your logo
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((150, 150), Image.ANTIALIAS)  # Resize logo if needed
    logo_tk = ImageTk.PhotoImage(logo_image)
    # Add logo to authentication frame
    logo_label = tk.Label(auth_frame, image=logo_tk, bg=bg_color)
    logo_label.image = logo_tk  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)

    # Registration
    reg_label = tk.Label(auth_frame, text="Register", bg=bg_color, fg=fg_color, font=("Fake Receipt", 19))
    reg_label.pack(pady=10)

    tk.Label(auth_frame, text="Username:", bg=bg_color, fg=fg_color , font=("Fake Receipt", 10)).pack()
    global reg_username_entry  # Make it global to access in register_user
    reg_username_entry = tk.Entry(auth_frame, font = ("SF Pro", 10))
    reg_username_entry.pack(pady=5)

    tk.Label(auth_frame, text="Password:", bg=bg_color, fg=fg_color, font=("Fake Receipt", 10)).pack()
    global reg_password_entry  # Make it global to access in register_user
    reg_password_entry = tk.Entry(auth_frame ,font = ("SF Pro", 10), show="*")
    reg_password_entry.pack(pady=5)

    tk.Button(auth_frame, text="Register", command=register_user, bg=button_bg_color, fg=button_fg_color, font=("Fake Receipt", 10)).pack(pady=10)

    # Login
    login_label = tk.Label(auth_frame, text="Login", bg=bg_color, fg=fg_color, font=("Fake Receipt", 19))
    login_label.pack(pady=10)

    tk.Label(auth_frame, text="Username:", bg=bg_color, fg=fg_color, font=("Fake Receipt", 10)).pack()
    global login_username_entry  # Make it global to access in login_user
    login_username_entry = tk.Entry(auth_frame,font = ("SF Pro", 10))
    login_username_entry.pack(pady=5)

    tk.Label(auth_frame, text="Password:", bg=bg_color, fg=fg_color, font=("Fake Receipt", 10)).pack()
    global login_password_entry  # Make it global to access in login_user
    login_password_entry = tk.Entry(auth_frame, font = ("SF Pro", 10),show="*")
    login_password_entry.pack(pady=5)

    tk.Button(auth_frame, text="Login", command=login_user, bg=button_bg_color, fg=button_fg_color, font=("Fake Receipt", 10)).pack(pady=10)

#create authentication UI
create_auth_ui()    

# Global session variable
current_session = {'exercises': [], 'muscles': {muscle: 0 for muscle in muscle_groups.keys()}}

#add exercise and intensities to the database
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

#load exercises from the database
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

#select an exercise from the database
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
            except Exception as e:
                messagebox.showerror("Error", f"Could not update muscle intensities: {e}")
                return
            messagebox.showinfo("Exercise Selected", f"Selected '{name}' and added to the current session.")

def display_muscle_images():
    # Clear image frame
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

#refresh exercise list
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

#visualize weight history
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
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()
        else:
            messagebox.showinfo("No Data", "No weight records found.")
    else:
        messagebox.showerror("Database Error", "Could not connect to the database.")

# Rounded button function
def create_rounded_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command, bg=button_bg_color, fg=button_fg_color, relief='flat', padx=20, pady=10 , font = ("Fake Receipt", 10))
    button.pack(pady=10)
    button.bind("<Enter>", lambda e: button.config(bg="#5A5A5A"))  # Change color on hover
    button.bind("<Leave>", lambda e: button.config(bg=button_bg_color))  # Revert color

#set up workout tracker UI
def setup_workout_tracker():
    # Create a frame for input options with increased width
    input_frame = tk.Frame(root, width=600, bg=bg_color)  # Increased width to 600
    input_frame.pack(side=tk.LEFT, fill=tk.Y)

    #frame for muscle images
    global image_frame  # Make it global to access in display_muscle_images
    image_frame = tk.Frame(root, bg="black")
    image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # UI components for workout tracker
    exercise_label = tk.Label(input_frame, text="Exercise Name:", bg=bg_color, fg=fg_color, font = ("Fake Receipt", 10))
    exercise_label.pack(pady=10)
    global exercise_entry  # Make it global to access in add_exercise_to_db
    exercise_entry = tk.Entry(input_frame, bg=button_bg_color, fg=fg_color)
    exercise_entry.pack(pady=10)

    intensity_labels = ["Chest", "Back", "Shoulders", "Biceps", "Triceps", "Quads", "Hamstrings", "Calves", "Glutes", "Core"]
    global intensity_entries  # Make it global to access in add_exercise_to_db
    intensity_entries = []


    for label in intensity_labels:
        intensity_frame = tk.Frame(input_frame, bg=bg_color)
        intensity_frame.pack(pady=5)

        label_widget = tk.Label(intensity_frame, text=label + " Intensity (0-10):", bg=bg_color, fg=fg_color , font = ("Fake Receipt", 8))
        label_widget.pack(side=tk.LEFT, padx=5)

        entry_widget = tk.Entry(intensity_frame, bg=button_bg_color, fg=fg_color)
        entry_widget.pack(side=tk.RIGHT, padx=5)
        intensity_entries.append(entry_widget)
        
        
    create_rounded_button(input_frame, "Add Exercise", add_exercise_to_db)
    create_rounded_button(input_frame, "Load Exercises", load_exercises)
    # Exercise Listbox
    global exercise_listbox  # Make it global to access in other functions
    exercise_listbox = tk.Listbox(input_frame, bg=button_bg_color, fg=fg_color,height=5 , font = ("Fake Receipt", 8))
    exercise_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # Create buttons using the rounded button function
    create_rounded_button(input_frame, "Select Exercise", select_exercise)
    create_rounded_button(input_frame, "Visualize Muscle Intensity", display_muscle_images)
    create_rounded_button(input_frame, "Refresh List", refresh_exercise_list)

    # Weight tracking section
    weight_label = tk.Label(input_frame, text="Enter your Weight (kg):", bg=bg_color, fg=fg_color , font = ("Fake Receipt", 10))
    weight_label.pack(pady=10)
    global weight_entry  # Make it global to access in save_weight
    weight_entry = tk.Entry(input_frame, bg=button_bg_color, fg=fg_color, font = ("Fake Receipt", 10))
    weight_entry.pack(pady=10)
    create_rounded_button(input_frame, "Save Weight", save_weight)
    create_rounded_button(input_frame, "View Weight History", visualize_weight_history)



    # Load exercises initially
    load_exercises()


# Run the application
root.mainloop()