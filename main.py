import requests
import colorama
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

colorama.init()

# Create the Tkinter window
window = ctk.CTk()

# Set window title
window.title("Kahoot Answer Getter")

# Function to retrieve the game ID
def get_quiz_id():
    quiz_id = quiz_id_entry.get()
    quiz_id_entry.delete(0, tk.END)
    quiz_id_entry.focus()

    global data  # Make the 'data' variable accessible globally
    data = requests.get("https://play.kahoot.it/rest/kahoots/" + quiz_id)

    if data.status_code == 200:
        messagebox.showinfo("Success", "Game found!")
        title_label.configure(text="Title: " + data.json()["title"])
        description_label.configure(text="Description: " + data.json()["description"])
    else:
        if data.json()["error"] == "INVALID_DATA" or data.json()["error"] == "NOT_FOUND":
            messagebox.showerror("Error", "Game not found.")
        elif data.json()["errorCode"] == 49:
            messagebox.showerror("Error", "Game is private.")
        else:
            messagebox.showerror("Error", "Unknown error.")
            if messagebox.askyesno("Error", "Do you want to see the error?"):
                messagebox.showinfo("Error", str(data.json()))

# Function to retrieve the question name and get the answer
def get_answer():
    question_name = question_entry.get()
    question_entry.delete(0, tk.END)
    question_entry.focus()

    answer = get_question_answer(question_name)
    if answer == "MULTIPLE_ANSWERS":
        pass
    else:
        try:
            messagebox.showinfo("Answer", "Answer: " + answer)
        except:
            messagebox.showerror("Error", "Either the question doesn't exist or it is not a multiple-choice question.")

# Function to retrieve the answer for a given question
def get_question_answer(question_name):
    try:
        for question in data.json()["questions"]:
            if question["question"] == question_name:
                answer = [answer["answer"] for answer in question["choices"] if answer["correct"] == True]
                if type(answer) == list:
                    if messagebox.askyesno("Multiple Answers", "Multiple answers found. Do you want to see all of them?"):
                        answer = ", ".join(answer)
                        answer = answer.replace("[", "")
                        messagebox.showinfo("Answers", "Answers: " + answer)
                        return "MULTIPLE_ANSWERS"
                    else:
                        messagebox.showinfo("Answer", "Giving you the first answer.")
                        return answer[0]
    except:
        messagebox.showerror("Error", "Either the question doesn't exist or it is not a multiple-choice question.")
        return "Error"

# Create the widgets
title_label = ctk.CTkLabel(window, text="Title: ")
description_label = ctk.CTkLabel(window, text="Description: ")
quiz_id_label = ctk.CTkLabel(window, text="Enter the game ID: ")
quiz_id_entry = ctk.CTkEntry(window)
get_quiz_id_button = ctk.CTkButton(window, text="Get Game Details", command=get_quiz_id)
question_label = ctk.CTkLabel(window, text="Question to search for: ")
question_entry = ctk.CTkEntry(window)
get_answer_button = ctk.CTkButton(window, text="Get Answer", command=get_answer)

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
