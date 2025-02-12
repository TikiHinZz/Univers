# student_app.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Для Combobox
import sqlite3
from database import AuditoriumScheduler


class StudentApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Приложение студента | {username}")
        self.root.geometry("800x700")  # Увеличили размер окна
        self.root.configure(bg="#f0f0f0")

        self.scheduler = AuditoriumScheduler()
        self.username = username

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
            text=f"Добро пожаловать, {username} (Студент)!",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 14),
        ).pack(side="left", padx=10, pady=10)

        # Логотип или название приложения
        tk.Label(
            header_frame,
            text="Университетский Портал",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 14, "bold"),
        ).pack(side="right", padx=10, pady=10)

        # Боковое меню
        sidebar_frame = tk.Frame(self.root, bg="#ECECEC", width=200)
        sidebar_frame.pack(side="left", fill="y")

        buttons = [
            ("Личный кабинет", self.personal_cabinet),
            ("Мое расписание", self.view_schedule),
            ("Бронирование аудиторий", self.book_auditorium),
            ("Поиск свободных аудиторий", self.find_free_auditoriums),
            ("Доступ к материалам", self.access_materials),
            ("Обратная связь", self.feedback_system),
            ("Выйти", self.logout),
        ]

        for i, (text, command) in enumerate(buttons):
            button = ttk.Button(
                sidebar_frame,
                text=text,
                command=lambda cmd=command: self.show_content(cmd),
                style="TButton",
                width=20,
            )
            button.pack(pady=5, padx=10, fill="x")

        # Главная область для контента
        self.content_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Приветственное сообщение
        welcome_label = tk.Label(
            self.content_frame,
            text="Выберите действие слева.",
            bg="#f0f0f0",
            font=("Arial", 14),
        )
        welcome_label.pack(pady=50)

    def show_content(self, content_function):
        """Очищает текущее содержимое и показывает новое."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        content_function()

    # Личный кабинет
    def personal_cabinet(self):
        tk.Label(
            self.content_frame,
            text=f"Личный кабинет\nПривет, {self.username}",
            bg="#f0f0f0",
            font=("Arial", 14),
        ).pack(pady=20)

    # Мое расписание
    def view_schedule(self):
        schedule = self.scheduler.get_student_schedule(self.username)
        if not schedule:
            tk.Label(
                self.content_frame,
                text="У вас нет занятий в расписании.",
                bg="#f0f0f0",
                font=("Arial", 14),
            ).pack(pady=20)
            return

        tk.Label(
            self.content_frame,
            text="Ваше расписание:",
            bg="#f0f0f0",
            font=("Arial", 14),
        ).pack(pady=10)

        for entry in schedule:
            auditorium, time, event = entry
            tk.Label(
                self.content_frame,
                text=f"Аудитория: {auditorium}, Время: {time}, Мероприятие: {event}",
                bg="#f0f0f0",
                font=("Arial", 12),
            ).pack(anchor="w", pady=5)

    # Бронирование аудиторий
    def book_auditorium(self):
        self.add_form_fields(["Номер аудитории", "Временной слот"], rows=2)
        time_slots = ["9:00–10:30", "10:45–12:15", "12:30–14:00", "14:15–15:45", "16:00–17:30", "17:45–19:15"]
        self.set_combobox_values("Временной слот", time_slots)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Забронировать",
            command=self.confirm_booking,
        )
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def confirm_booking(self):
        fields = self.get_form_fields()
        if not all(fields.values()):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        result = self.scheduler.book_auditorium(
            fields["Номер аудитории"],
            fields["Временной слот"],
            f"Студент {self.username}",
            self.username,
        )
        messagebox.showinfo("Результат", result)

    # Поиск свободных аудиторий
    def find_free_auditoriums(self):
        self.add_form_fields(["Временной слот:"], rows=1)
        time_slots = ["9:00–10:30", "10:45–12:15", "12:30–14:00", "14:15–15:45", "16:00–17:30", "17:45–19:15"]
        self.set_combobox_values("Временной слот:", time_slots)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Найти",
            command=self.search_auditoriums,
        )
        confirm_button.grid(row=1, column=0, columnspan=2, pady=10)

    def search_auditoriums(self):
        time_slot = self.get_form_field_value("Временной слот:")
        if not time_slot:
            messagebox.showerror("Ошибка", "Выберите временной слот.")
            return

        free_auditoriums = self.scheduler.find_free_auditoriums(time_slot)
        if not free_auditoriums:
            messagebox.showinfo("Результат", "Нет свободных аудиторий на выбранное время.")
            return

        message = "Свободные аудитории:\n"
        for auditorium in free_auditoriums:
            message += f"Аудитория {auditorium}\n"

        messagebox.showinfo("Результат", message)

    # Доступ к материалам
    def access_materials(self):
        materials = self.scheduler.get_student_materials(self.username)
        if not materials:
            tk.Label(
                self.content_frame,
                text="У вас нет доступных материалов.",
                bg="#f0f0f0",
                font=("Arial", 14),
            ).pack(pady=20)
            return

        tk.Label(
            self.content_frame,
            text="Доступные материалы:",
            bg="#f0f0f0",
            font=("Arial", 14),
        ).pack(pady=10)

        for material in materials:
            tk.Label(
                self.content_frame,
                text=f"Материал: {material}",
                bg="#f0f0f0",
                font=("Arial", 12),
            ).pack(anchor="w", pady=5)

    # Обратная связь
    def feedback_system(self):
        self.add_form_fields(["Тикет (заголовок)", "Описание"], rows=2)
        self.form_fields["Описание"] = tk.Text(self.content_frame, height=5, width=30, font=("Arial", 12))
        self.form_fields["Описание"].grid(row=1, column=1, padx=5, pady=5)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Создать тикет",
            command=self.create_ticket,
        )
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def create_ticket(self):
        title = self.get_form_field_value("Тикет (заголовок)")
        description = self.form_fields["Описание"].get("1.0", tk.END).strip()
        if not all([title, description]):
            messagebox.showerror("Ошибка", "Заполните все поля.")
            return

        result = self.scheduler.create_ticket(self.username, title, description)
        messagebox.showinfo("Тикет", result)

    # Выход из аккаунта
    def logout(self):
        self.root.destroy()
        from main import start_login
        start_login()

    # Вспомогательные методы
    def add_form_fields(self, labels, rows=None):
        """Добавляет поля ввода в правую часть интерфейса."""
        self.form_fields = {}
        for i, label_text in enumerate(labels):
            tk.Label(
                self.content_frame, text=label_text, bg="#f0f0f0", font=("Arial", 12)
            ).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(self.content_frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.form_fields[label_text] = entry

        if rows is not None:
            self.content_frame.grid_rowconfigure(rows, weight=1)

    def set_combobox_values(self, label, values):
        """Устанавливает значения для Combobox."""
        row = len(self.form_fields)
        tk.Label(
            self.content_frame, text=label, bg="#f0f0f0", font=("Arial", 12)
        ).grid(row=row, column=0, padx=5, pady=5, sticky="w")
        combobox = ttk.Combobox(self.content_frame, values=values, font=("Arial", 12))
        combobox.grid(row=row, column=1, padx=5, pady=5)
        self.form_fields[label] = combobox

    def get_form_fields(self):
        """Получает значения всех полей формы."""
        return {label: field.get() for label, field in self.form_fields.items()}

    def get_form_field_value(self, label):
        """Получает значение конкретного поля формы."""
        return self.form_fields.get(label, tk.Entry()).get()