import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def congratulate():
    name = entry_name.get().strip()
    age_str = entry_age.get().strip()
    
    if not name:
        messagebox.showerror("❌ Ошибка", "Имя не может быть пустым!")
        return
    
    if not all(c.isalpha() or c.isspace() or c == '-' for c in name):
        messagebox.showerror("❌ Ошибка", "Имя должно содержать только буквы, пробелы и дефис!")
        return
    
    if not age_str:
        messagebox.showerror("❌ Ошибка", "Возраст не может быть пустым!")
        return
    
    try:
        age = int(age_str)
    except ValueError:
        messagebox.showerror("❌ Ошибка", "Возраст должен быть целым числом!")
        return
    
    if age < 1 or age > 130:
        messagebox.showerror("❌ Ошибка", "Возраст должен быть от 1 до 130 лет!")
        return
    
    message = (
        f"С днём рождения\n"
        f"{age} летний {name}!\n"
    )
    
    messagebox.showinfo("🎉 Поздравление", message)
    
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    
    entry_name.focus()

def reset_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_name.focus()

# Создание окна
root = tk.Tk()
root.title("С днём рождения")
root.geometry("450x400")
root.resizable(False, False)
root.configure(bg="#f0f0f5")

FONT_TITLE = ("Arial", 14, "bold")
FONT_LABEL = ("Arial", 11)
FONT_ENTRY = ("Arial", 12)
BG_COLOR = "#f0f0f5"
FRAME_COLOR = "#ffffff"

title_frame = tk.Frame(root, bg="#4a90d9", height=60)
title_frame.pack(fill="x")
title_frame.pack_propagate(False)

tk.Label(
    title_frame,
    text="🎈 Поздравление с Днём Рождения 🎈",
    font=("Arial", 16, "bold"),
    bg="#4a90d9",
    fg="white"
).pack(expand=True)

form_frame = tk.Frame(root, bg=BG_COLOR)
form_frame.pack(pady=20, padx=30, fill="both", expand=True)

tk.Label(
    form_frame,
    text="👤 Введите ваше имя:",
    font=FONT_LABEL,
    bg=BG_COLOR
).pack(anchor="w", pady=(10, 5))

entry_name = tk.Entry(
    form_frame,
    font=FONT_ENTRY,
    bg=FRAME_COLOR,
    relief="solid",
    bd=1
)
entry_name.pack(fill="x", ipady=5)
entry_name.focus()

tk.Label(
    form_frame,
    text="🎂 Введите ваш возраст:",
    font=FONT_LABEL,
    bg=BG_COLOR
).pack(anchor="w", pady=(15, 5))

entry_age = tk.Entry(
    form_frame,
    font=FONT_ENTRY,
    bg=FRAME_COLOR,
    relief="solid",
    bd=1
)
entry_age.pack(fill="x", ipady=5)

# Кнопки в одной строке
buttons_frame = tk.Frame(form_frame, bg=BG_COLOR)
buttons_frame.pack(pady=25)

btn_congrat = tk.Button(
    buttons_frame,
    text="🎉 Поздравить",
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=congratulate
)
btn_congrat.pack(side="left", padx=5, ipadx=20, ipady=5)

btn_reset = tk.Button(
    buttons_frame,
    text="🧹 Очистить",
    font=("Arial", 12),
    bg="#f44336",
    fg="white",
    activebackground="#d32f2f",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=reset_fields
)
btn_reset.pack(side="left", padx=5, ipadx=20, ipady=5)

footer_frame = tk.Frame(root, bg="#e0e0e0", height=25)
footer_frame.pack(fill="x", side="bottom")
footer_frame.pack_propagate(False)

root.bind('<Return>', lambda event: congratulate())

root.mainloop()