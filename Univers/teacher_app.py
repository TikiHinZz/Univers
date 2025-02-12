# teacher_app.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Для Combobox
import sqlite3
from database import AuditoriumScheduler


class TeacherApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Приложение преподавателя | {username}")
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
            text=f"Добро пожаловать, {username} (Преподаватель)!",
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
            ("Управление бронированиями", self.manage_bookings),
            ("Запрос оборудования", self.request_equipment),
            ("Отчеты", self.generate_reports),
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
        schedule = self.scheduler.get_teacher_schedule(self.username)
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
        self.add_form_fields(["Номер аудитории", "Временной слот", "Название мероприятия"], rows=3)
        time_slots = ["9:00–10:30", "10:45–12:15", "12:30–14:00", "14:15–15:45", "16:00–17:30", "17:45–19:15"]
        self.set_combobox_values("Временной слот", time_slots)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Забронировать",
            command=self.confirm_booking,
        )
        confirm_button.grid(row=3, column=0, columnspan=2, pady=10)

    def confirm_booking(self):
        fields = self.get_form_fields()
        if not all(fields.values()):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        result = self.scheduler.book_auditorium(
            fields["Номер аудитории"],
            fields["Временной слот"],
            fields["Название мероприятия"],
            self.username,
        )
        messagebox.showinfo("Результат", result)

    # Управление бронированиями
    def manage_bookings(self):
        bookings = self.scheduler.get_teacher_bookings(self.username)
        if not bookings:
            tk.Label(
                self.content_frame,
                text="У вас нет активных бронирований.",
                bg="#f0f0f0",
                font=("Arial", 14),
            ).pack(pady=20)
            return

        tk.Label(
            self.content_frame,
            text="Ваши бронирования:",
            bg="#f0f0f0",
            font=("Arial", 14),
        ).pack(pady=10)

        for booking in bookings:
            auditorium, time, event = booking
            tk.Label(
                self.content_frame,
                text=f"Аудитория: {auditorium}, Время: {time}, Мероприятие: {event}",
                bg="#f0f0f0",
                font=("Arial", 12),
            ).pack(anchor="w", pady=5)

    # Запрос оборудования
    def request_equipment(self):
        self.add_form_fields(["Номер аудитории", "Оборудование"], rows=2)
        equipment_options = ["Проектор", "Микрофон", "Доска", "Компьютер"]
        self.set_combobox_values("Оборудование", equipment_options)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Отправить запрос",
            command=self.confirm_equipment_request,
        )
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def confirm_equipment_request(self):
        fields = self.get_form_fields()
        if not all(fields.values()):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        result = self.scheduler.request_equipment(
            fields["Номер аудитории"], fields["Оборудование"], self.username
        )
        messagebox.showinfo("Результат", result)

    # Отчеты
    def generate_reports(self):
        self.add_form_fields(["Период (YYYY-MM-DD):"], rows=1)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Сгенерировать",
            command=self.generate_usage_report,
        )
        confirm_button.grid(row=1, column=0, columnspan=2, pady=10)

    def generate_usage_report(self):
        period = self.get_form_field_value("Период (YYYY-MM-DD):")
        if not period:
            messagebox.showerror("Ошибка", "Введите период.")
            return

        data = self.scheduler.generate_teacher_report(self.username, period)
        messagebox.showinfo("Отчет", f"Ваш отчет:\n{data}")

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