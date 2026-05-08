import threading
import time
import tkinter as tk
from tkinter import messagebox

def proccess():
    def stub_task():
        time.sleep(5)
        root.after(0, show_result)
    def show_result():
        try:
            age = int(entry.get())
            messagebox.showinfo("Возраст", f"Через год вам будет: {age + 1}")
        except ValueError:
            messagebox.showerror("Возраст", "Должно быть целое число!")
    threading.Thread(target=stub_task, daemon=True).start()

root = tk.Tk()

entry = tk.Entry()
entry.pack()

btn = tk.Button(root, text="OK", command=proccess)
btn.pack()

root.mainloop()

