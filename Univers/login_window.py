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
        self.root.geometry("800x700")  # Увеличили размер окна
        self.root.configure(bg="#f0f0f0")

        # Стиль кнопок
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.map(
            "TButton",
            foreground=[("active", "#FFFFFF")],
            background=[("active", "#45A049")],
        )

        # Заголовок
        header_frame = tk.Frame(self.root, bg="#4CAF50", height=50)
        header_frame.pack(fill="x")
        tk.Label(
            header_frame,
            text="Университетский Портал",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 14, "bold"),
        ).pack(side="left", padx=10, pady=10)

        # Форма входа
        content_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        content_frame.pack(expand=True, fill="both")

        tk.Label(content_frame, text="Логин:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(content_frame, font=("Arial", 12))
        self.username_entry.pack(pady=5, fill="x")

        tk.Label(content_frame, text="Пароль:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(content_frame, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5, fill="x")

        tk.Button(
            content_frame,
            text="Войти",
            command=self.login,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
        ).pack(pady=10, fill="x")

        tk.Button(
            content_frame,
            text="Зарегистрироваться",
            command=self.register,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
        ).pack(pady=5, fill="x")

    @staticmethod
    def hash_password(password):
        """Хеширует пароль для безопасного хранения."""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        """Обработка входа пользователя."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Ошибка", "Логин и пароль должны быть заполнены.")
            return

        # Хешируем введенный пароль
        hashed_password = self.hash_password(password)

        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            role = user[2]
            self.root.destroy()
            root = tk.Tk()

            # Открываем соответствующее приложение в зависимости от роли
            if role == 'admin':
                from admin_app import AdminApp
                AdminApp(root, username)
            elif role == 'teacher':
                from teacher_app import TeacherApp
                TeacherApp(root, username)
            elif role == 'student':
                from student_app import StudentApp
                StudentApp(root, username)

            root.mainloop()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    def register(self):
        """Открывает форму регистрации нового пользователя."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Регистрация")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f0f0")

        # Логин
        tk.Label(dialog, text="Логин:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        username_entry = tk.Entry(dialog, font=("Arial", 12))
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Пароль
        tk.Label(dialog, text="Пароль:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        password_entry = tk.Entry(dialog, show="*", font=("Arial", 12))
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Подтверждение пароля
        tk.Label(dialog, text="Подтвердите пароль:", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        confirm_password_entry = tk.Entry(dialog, show="*", font=("Arial", 12))
        confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Роль
        tk.Label(dialog, text="Роль (teacher/student):", bg="#f0f0f0", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        role_combobox = ttk.Combobox(dialog, values=["admin", "teacher", "student"], font=("Arial", 12))
        role_combobox.grid(row=3, column=1, padx=5, pady=5)
        role_combobox.set("student")  # Установка значения по умолчанию

        # Кнопка подтверждения регистрации
        tk.Button(
            dialog,
            text="Зарегистрироваться",
            command=lambda: self.confirm_register(
                username_entry.get(),
                password_entry.get(),
                confirm_password_entry.get(),
                role_combobox.get(),
                dialog
            ),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
        ).grid(row=4, column=0, columnspan=2, pady=10)

    def confirm_register(self, username, password, confirm_password, role, dialog):
        """Подтверждает регистрацию нового пользователя."""
        if not all([username, password, confirm_password, role]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        if password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают.")
            return

        if role not in ["teacher", "student"]:
            messagebox.showerror("Ошибка", "Выберите допустимую роль: teacher или student.")
            return

        # Хешируем пароль
        hashed_password = self.hash_password(password)

        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed_password, role))
            conn.commit()
            messagebox.showinfo("Успех", f"Пользователь {username} успешно зарегистрирован!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", f"Пользователь с логином {username} уже существует.")
        finally:
            conn.close()
            dialog.destroy()