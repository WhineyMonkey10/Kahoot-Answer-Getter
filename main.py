import requests
import colorama
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk



colorama.init()

# Create the Tkinter window
window = ctk.CTk()

# Set window title
window.title("Kahoot Answer Getter")

# Function to retrieve the game ID
def get_quiz_id():
    global quiz_id
    quiz_id = quiz_id_entry.get()
    quiz_id_entry.delete(0, tk.END)
    quiz_id_entry.focus()

    global data
    data = requests.get("https://play.kahoot.it/rest/kahoots/" + quiz_id)
    
    if "The Emoji Quiz 😀😜😬" in data.text:
        messagebox.showerror("Error", "This game is not supported.")
        exit()

    if data.status_code == 200:
        messagebox.showinfo("Success", "Game found!")
        title_label.configure(text="Title: " + data.json()["title"])
        description_label.configure(text="Description: " + data.json()["description"])
        # Check if the quiz id is in history.txt, if not, write it to history.txt
        with open("history.txt", "r") as f:
            lines = f.read().splitlines()
        if quiz_id in lines:
            pass
        else:
            with open("history.txt", "a") as f:
                f.write(quiz_id + "\n")

        
    else:
        if data.json()["error"] == "INVALID_DATA" or data.json()["error"] == "NOT_FOUND":
            messagebox.showerror("Error", "Game not found.")
        elif data.json()["errorCode"] == 49:
            messagebox.showerror("Error", "Game is private.")
        else:
            messagebox.showerror("Error", "Unknown error.")
            if messagebox.askyesno("Error", "Do you want to see the error?"):
                messagebox.showinfo("Error", str(data.json()))
                
def refresh_quiz_info(session_id):
    # Perform the necessary actions to refresh the quiz information
    # For example, you can call the get_quiz_id() function again or update the labels with the latest data
    # Update the title and description labels with the refreshed data
    
    # Re-fetch the data from the API to get the latest data and update the labels and variables
    try:
        if session_id == None:
            newData = requests.get("https://play.kahoot.it/rest/kahoots/" + quiz_id)
            
            title_label.configure(text="Title: " + newData.json()["title"])
            description_label.configure(text="Description: " + newData.json()["description"])
            
            # Update the data variable with the new data
            print("Updating data variable...")
            global data
            data = newData
            
            messagebox.showinfo("Success", "Quiz information refreshed!")
        else:
            newData = requests.get("https://play.kahoot.it/rest/kahoots/" + session_id)
            
            title_label.configure(text="Title: " + newData.json()["title"])
            description_label.configure(text="Description: " + newData.json()["description"])
            
            
            data = newData
            
            messagebox.showinfo("Success", "Quiz information refreshed!")
    except:
        messagebox.showerror("Error", "An error occurred while refreshing the quiz information.")
    

# Function to retrieve the question name and get the answer
def get_answer():
    question_name = question_entry.get()
    question_entry.delete(0, tk.END)
    question_entry.focus()

    answer = get_question_answer(question_name)
    
    if answer == None:
        messagebox.showerror("Error", "The question contains unrecognizable characters.")
        return
    
    if answer == "MULTIPLE_ANSWERS":
        pass
    else:
        try:
            messagebox.showinfo("Answer", f"Answer: {answer}")
        except:
            messagebox.showerror("Error", "Either the question doesn't exist or it is not a multiple-choice question.")

# Function to retrieve the answer for a given question
def get_question_answer(question_name):
    try:
        print("INITIATING REQUEST...")
        for question in data.json()["questions"]:
            print(question)
            if question["question"] == question_name:
                print("QUESTION FOUND!")
                answer = [answer["answer"] for answer in question["choices"] if answer["correct"] == True]
                print("ANSWER FOUND!", answer)
                if len(answer) > 1:
                    print("MULTIPLE ANSWERS FOUND!")
                    if messagebox.askyesno("Multiple Answers", "Multiple answers found. Do you want to see all of them?"):
                        answer = ", ".join(answer)
                        answer = answer.replace("[", "")
                        answer = answer.replace("]", "")
                        answer = answer.replace("'", "")
                        messagebox.showinfo("Answers", "Answers: " + answer)
                        return "MULTIPLE_ANSWERS"
                    else:
                        print("GIVING YOU THE FIRST ANSWER!")
                        messagebox.showinfo("Answer", "Giving you the first answer.")
                        return answer[0]
                else:
                    answer = ", ".join(answer)
                    answer = answer.replace("[", "")
                    answer = answer.replace("]", "")
                    answer = answer.replace("'", "")
                    return answer
    except:
        messagebox.showerror("Error", "Either the question doesn't exist or it is not a multiple-choice question.")
        return "Error"
    
def get_session_history():
    with open("history.txt", "r") as f:
        history = f.readlines()

    session_ids = [session_id.strip() for session_id in history]
    session_titles = [get_session_title(session_id) for session_id in session_ids]

    session_dropdown = ttk.Combobox(window, values=session_titles)
    session_dropdown.grid(row=4, column=0, sticky=tk.W)

    def on_session_selected(event):
        selected_session_id = session_ids[session_dropdown.current()]
        update_session_info(selected_session_id)
        session_dropdown.grid_remove()  # Hide the dropdown after selection

    session_dropdown.bind("<<ComboboxSelected>>", on_session_selected)

def get_session_title(session_id):
    # You need to implement this function to retrieve the session title based on the session ID
    # Make necessary API requests or database queries to fetch the title
    # Return the session title
    return requests.get("https://play.kahoot.it/rest/kahoots/" + session_id).json()["title"]

def update_session_info(session_id):
    # You need to implement this function to update the title and description labels based on the selected session ID
    # Make necessary API requests or database queries to fetch the session details
    # Update the title and description labels with the retrieved information
    refresh_quiz_info(session_id)

    
    

# Create the widgets
title_label = ctk.CTkLabel(window, text="Title: ")
description_label = ctk.CTkLabel(window, text="Description: ")
quiz_id_label = ctk.CTkLabel(window, text="Enter the game ID: ")
quiz_id_entry = ctk.CTkEntry(window)
get_quiz_id_button = ctk.CTkButton(window, text="Get Game Details", command=get_quiz_id)
question_label = ctk.CTkLabel(window, text="Question to search for: ")
question_entry = ctk.CTkEntry(window)


get_answer_button = ctk.CTkButton(window, text="Get Answer", command=get_answer)

refresh_icon_image = Image.open("refresh_icon.png")  # Replace "refresh_icon.png" with the actual image path
refresh_icon_image = refresh_icon_image.resize((20, 20))  # Adjust the size as needed

refresh_icon = ImageTk.PhotoImage(refresh_icon_image)
refresh_icon_label = ctk.CTkLabel(window, image=refresh_icon)
# Remove the text from the refresh icon label
refresh_icon_label.configure(text="")
refresh_icon_label.grid(row=0, column=2, sticky=tk.NE)
refresh_icon_label.bind("<Button-1>", lambda e: refresh_quiz_info(None))


history_icon_image = Image.open("history_icon.png")  # Replace "refresh_icon.png" with the actual image path
history_icon_image = history_icon_image.resize((20, 20))  # Adjust the size as needed

history_icon = ImageTk.PhotoImage(history_icon_image)
history_icon_label = ctk.CTkLabel(window, image=history_icon)
# Remove the text from the refresh icon label
history_icon_label.configure(text="")
history_icon_label.grid(row=1, column=2, sticky=tk.NE)
history_icon_label.bind("<Button-1>", lambda e: get_session_history())


# Grid layout
title_label.grid(row=0, column=0, sticky=tk.W)
description_label.grid(row=1, column=0, sticky=tk.W)
quiz_id_label.grid(row=2, column=0, sticky=tk.W)
quiz_id_entry.grid(row=2, column=1)
get_quiz_id_button.grid(row=2, column=2)
question_label.grid(row=3, column=0, sticky=tk.W)
question_entry.grid(row=3, column=1)
get_answer_button.grid(row=3, column=2)

# Start the Tkinter event loop
window.mainloop()
