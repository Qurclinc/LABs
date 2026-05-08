import tkinter as tk
from tkinter import messagebox

def proccess():
    age = int(entry.get())
    messagebox.showinfo("Возраст", f"Через год вам будет: {age + 1}")

root = tk.Tk()

entry = tk.Entry()
entry.pack()

btn = tk.Button(root, text="OK", command=proccess)
btn.pack()

root.mainloop()
