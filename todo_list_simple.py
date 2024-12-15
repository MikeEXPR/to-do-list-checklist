import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# File to save tasks
FILE_NAME = "todo_list.txt"

# Load tasks from file
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return [line.strip().split(",") for line in file]

# Save tasks to file
def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for task, status in tasks:
            file.write(f"{task},{status}\n")

# Add a new task
def add_task():
    task = simpledialog.askstring("Add Task", "Enter the task:")
    if task:
        tasks.append([task, "pending"])
        save_tasks()
        update_task_list()

# Mark a task as complete
def mark_complete():
    selected_index = task_listbox.curselection()
    if selected_index:
        tasks[selected_index[0]][1] = "done"
        save_tasks()
        update_task_list()
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as complete.")

# Delete a task
def delete_task():
    selected_index = task_listbox.curselection()
    if selected_index:
        tasks.pop(selected_index[0])
        save_tasks()
        update_task_list()
    else:
        messagebox.showwarning("Warning", "Please select a task to delete.")

# Move task up
def move_up():
    selected_index = task_listbox.curselection()
    if selected_index and selected_index[0] > 0:
        tasks[selected_index[0]], tasks[selected_index[0] - 1] = tasks[selected_index[0] - 1], tasks[selected_index[0]]
        save_tasks()
        update_task_list()
        task_listbox.select_set(selected_index[0] - 1)
    else:
        messagebox.showwarning("Warning", "Cannot move the task up.")

# Move task down
def move_down():
    selected_index = task_listbox.curselection()
    if selected_index and selected_index[0] < len(tasks) - 1:
        tasks[selected_index[0]], tasks[selected_index[0] + 1] = tasks[selected_index[0] + 1], tasks[selected_index[0]]
        save_tasks()
        update_task_list()
        task_listbox.select_set(selected_index[0] + 1)
    else:
        messagebox.showwarning("Warning", "Cannot move the task down.")

# Update the task listbox
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task, status in tasks:
        checkmark = "✔" if status == "done" else "✘"
        display_text = f"{task} [{checkmark}]"
        task_listbox.insert(tk.END, display_text)

# GUI Setup
root = tk.Tk()
root.title("To-Do List with Checklist and Task Reordering")
root.geometry("500x500")

# Load tasks into memory
tasks = load_tasks()

# Widgets
frame = ttk.Frame(root, padding="10")
frame.pack(pady=10)

# Listbox with scrollbar
task_listbox = tk.Listbox(frame, width=70, height=15, selectmode=tk.SINGLE, font=("Arial", 12))
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=task_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
task_listbox.config(yscrollcommand=scrollbar.set)

# Buttons
btn_add = ttk.Button(root, text="Add Task", command=add_task)
btn_add.pack(pady=5)

btn_complete = ttk.Button(root, text="Mark as Complete", command=mark_complete)
btn_complete.pack(pady=5)

btn_delete = ttk.Button(root, text="Delete Task", command=delete_task)
btn_delete.pack(pady=5)

btn_move_up = ttk.Button(root, text="Move Task Up", command=move_up)
btn_move_up.pack(pady=5)

btn_move_down = ttk.Button(root, text="Move Task Down", command=move_down)
btn_move_down.pack(pady=5)

# Populate the task list
update_task_list()

# Run the application
root.mainloop()