import tkinter as tk
from tkinter import ttk

def on_button_click():
    label.config(text="Hello, Tkinter!")

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter App")

# Create a label
label = ttk.Label(root, text="Click the button.")
label.pack(pady=20)

# Create a button
button = ttk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=10)

# Start the event loop
root.mainloop()
