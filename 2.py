def add_exercise_to_db():
    exercise_name = exercise_entry.get()
    try:
        intensity_values = [int(entry.get()) for entry in intensity_entries]
        if exercise_name and any(intensity_values):
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                #values getting enterd
                cursor.execute("""INSERT INTO excersize(name,chest, back, shoulder, 
                               biceps,triceps, quads,hamstring,calves,glutes,core) 
                               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                               [excer_nam]+ [intensity_val])
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
    
    exercise_entry.delete(0, tk.END)
    for entry in intensity_entries:
        entry.delete(0, tk.END)
