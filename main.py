import tkinter as tk
import mysql.connector as sql
from mysql.connector import Error
from PIL import Image, ImageTk
import os



bg_color = "#181819"
fg_color = "#4D4D4D"
#databse host and pass
databse_con = {
    "host": "localhost",
    "user": "root",
    "password": "dhruvsingh",
    "database": "workout_tracker"
}
muscle_grp = {
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
root = tk.Tk()
root.title("Main")
root.geometry("1200x800")

#left side bar
input_fr = tk.Frame(root,width=600, bg=bg_color)
input_fr.pack(side=tk.LEFT,fill=tk.Y)

#background
image_fr = tk.Frame(root, bg = fg_color)
image_fr.pack(side=tk.RIGHT,fill=tk.BOTH , expand=True)
#seperator for bars
sep = tk.Frame(root, width=2, bg="black")
sep.pack(side=tk.LEFT, fill=tk.Y)

# Global session variable
current_session = {'exercises': [], 'muscles': {muscle: 0 for muscle in muscle_grp.keys()}}
#sql conncetion and error messages
def sqlcon():
    try: 
        conn = sql.connect(**databse_con)
        if conn.is_connected(): 
            print("Connected to MySQL")
            return conn
            
    except Error as e: 
        #add message box later
        print("Not connected to MySQL" , f"{e}")
        return None

#addind excersises and nserting to database
def add_excer_datab():
    exercise_name = excer_enter.get()
    try:
        intensity_values = [int(entry.get()) for entry in intensity_ent]
        if exercise_name and any(intensity_values):
            connection = sqlcon()
            if connection:
                cursor = connection.cursor()
                #values getting enterd
                cursor.execute("""INSERT INTO excersize(name,chest, back, shoulder, 
                               biceps,triceps, quads,hamstring,calves,glutes,core) 
                               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                               [exercise_name]+ [intensity_val])
                connection.commit()
                cursor.close()
                connection.close()
                #replace with text promt
                print("Data inserted successfully")
        else:
            #replace with text promt
            print("Input Error")
    except ValueError:
            #replace with text promt
            print("Input Error")
    
    excer_enter.delete(0, tk.END)
    for entry in intensity_ent:
        entry.delete(0, tk.END)

#load from database
def load_excer():
    excersize_listbox.delete(0, tk.END)
    conn = sqlcon()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM excersize")
        excercises = cursor.fetchall()
        exercise_names = [excercise[0] for excercise in excercises]
        cursor.close()
        for exercise_name in exercise_names:
            excersize_listbox.insert(tk.END, exercise_name)
            
            
#select exercise
def select_exercise():
    selected_exercise = exercise_listbox.get(tk.ACTIVE)
    if not selected_exercise:
        messafebox.showeror("Selection Eroor", "Please select an exercise from list")
        return
    conn = sqlcon()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM excersize WHERE name=%s", (selected_exercise))
        exercise_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if exercise_data:
            _, name, *intensities = exercise_data
            current_session['exercises'].append(name)
            for i, muscle in enumerate(muscle_grp.keys()):
                current_session['muscles'][muscle] += intensities[i]
            messagebox.showinfo("Exercise Selected", f"Selected '{name}' and added to the current session.")

#show muscle images    
def muscle_img():
    for widget in image_frame.winfo_children():
        widget.destroy()
    # display images 
    for muscle,intensity in current_session['muscles'].items():
        image_path = muscle_grp[muscle]
        
        if os.path.exists(image_path):
            muscle_img = Image.open(image_path).convert('RGBA')
            alpha = int((intensity/10)*255)
            
            alpha_channel = Image.new('L', muscle_image.size, alpha)
            muscle_image.putalpha(alpha_channel)

            # Resize image to fit the window (increased size)
            muscle_image = muscle_image.resize((400, 400), Image.ANTIALIAS)  # Increased size to 400x400

            # Convert to ImageTk format
            tk_image = ImageTk.PhotoImage(muscle_image)

            # Create a label to display the image
            image_label = tk.Label(image_frame, image=tk_image, bg="black")
            image_label.image = tk_image  # Keep a reference to avoid garbage collection
            image_label.pack(side=tk.TOP, padx=10, pady=10)
            
            
    
        
        
excer_label = tk.Label(input_fr, text = "Enter Exersize Name:", bg = "#181819", fg="white")
excer_label.pack(pady=5)
excer_enter = tk.Entry(input_fr)
excer_enter.pack(pady=5)
#intensity list
intensity_lab = []
intensity_ent = []

for muscle in muscle_grp.keys():
    lab = tk.Label(input_fr,text = f"{muscle} Intensity:(0-10)", bg = "#181819", fg = "white")
    lab.pack(pady=2)
    entry = tk.Entry(input_fr)
    entry.pack(pady=2)
    intensity_lab.append(lab)
    intensity_ent.append(entry)
    
add_excer_datab()
    
# Button style
button_style = {
    'bg': "#3E3E3E",
    'fg': "#FFFFFF",
    'activebackground': "#5E5E5E",
    'activeforeground': "#FFFFFF",
    'padx': 10,  # Reduced padding
    'pady': 5,   # Reduced padding
    'font': ('Arial', 10)  # Smaller font size
}



#add excersize
add_exercise_button = tk.Button(input_fr, text="Add Exercise to Database", command=add_excer_datab, **button_style)
add_exercise_button.pack(pady=5)

#excersize listbox
exercise_list_label = tk.Label(input_fr, text="Select Exercise from Database:", bg=bg_color, fg="white")
exercise_list_label.pack(pady=5)
exercise_listbox = tk.Listbox(input_fr, width=40, height=8)  # Increased width for better visibility
exercise_listbox.pack(pady=5)

#close button
close_button = tk.Button(input_fr, text="Close", command=root.destroy, bg='red', fg='white')
close_button.pack(pady=5)

root.mainloop()

