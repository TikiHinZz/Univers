# login_window.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Для Combobox
import sqlite3

from admin_app import AdminApp
from teacher_app import TeacherApp
from student_app import StudentApp

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Вход")
        self.root.geometry("300x200")
        self.root.configure(bg="#f0f0f0")

        tk.Label(root, text="Логин:", bg="#f0f0f0").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Пароль:", bg="#f0f0f0").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(
            root,
            text="Войти",
            command=self.login,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=10)

        tk.Button(
            root,
            text="Зарегистрироваться",
            command=self.register,
            bg="#2196F3",
            fg="white"
        ).pack(pady=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Ошибка", "Логин и пароль должны быть заполнены.")
            return

        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            role = user[2]
            self.root.destroy()
            root = tk.Tk()
            if role == 'admin':
                AdminApp(root, username)
            elif role == 'teacher':
                TeacherApp(root, username)
            elif role == 'student':
                StudentApp(root, username)
            root.mainloop()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    def register(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Регистрация")
        dialog.geometry("300x200")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Логин:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        username_entry = tk.Entry(dialog)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Пароль:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        password_entry = tk.Entry(dialog, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Роль (teacher/student):", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        role_combobox = ttk.Combobox(dialog, values=["teacher", "student"])  # Используем ttk.Combobox
        role_combobox.grid(row=2, column=1, padx=5, pady=5)
        role_combobox.set("student")  # Установка значения по умолчанию

        tk.Button(
            dialog,
            text="Зарегистрироваться",
            command=lambda: self.confirm_register(username_entry.get(), password_entry.get(), role_combobox.get(), dialog),
            bg="#4CAF50",
            fg="white"
        ).grid(row=3, column=0, columnspan=2, pady=10)

    def confirm_register(self, username, password, role, dialog):
        if not username or not password or not role:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        if role not in ["teacher", "student"]:
            messagebox.showerror("Ошибка", "Выберите допустимую роль: teacher или student.")
            return

        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            messagebox.showinfo("Успех", "Вы успешно зарегистрировались!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует.")
        finally:
            conn.close()
            dialog.destroy()