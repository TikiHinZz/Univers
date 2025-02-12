import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Для Combobox
import sqlite3
import csv  # Для работы с CSV
import shutil  # Для резервного копирования
import json
from database import AuditoriumScheduler



class AdminApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Админ-панель | {username}")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        self.scheduler = AuditoriumScheduler()  # Инициализация планировщика аудиторий
        self.username = username  # Сохраняем имя пользователя

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
            text=f"Добро пожаловать, {username} (Админ)!",
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

        # Кнопки в боковом меню
        buttons = [
            ("Управление аудиториями", self.manage_auditoriums),
            ("Расписание занятий", self.schedule_management),
            ("Бронирование аудиторий", self.booking_management),
            ("Учет занятости", self.occupancy_report),
            ("Отчеты и аналитика", self.generate_reports),
            ("Управление пользователями", self.user_management),
            ("Уведомления", self.notifications),
            ("Поиск и фильтрация", self.search_and_filter),
            ("Резервное копирование", self.backup_db),
            ("Обратная связь", self.feedback_system),
            ("Автоматизация уборки", self.cleaning_schedule),
            ("Контроль доступа", self.access_control),
            ("Выход", self.logout),
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
        self.content_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Приветственное сообщение
        self.welcome_label = tk.Label(
            self.content_frame,
            text="Выберите действие слева.",
            bg="#f0f0f0",
            font=("Arial", 14),
        )
        self.welcome_label.pack(pady=50)

    def show_content(self, content_function):
        """Очищает текущее содержимое и показывает новое."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        content_function()

    # Управление аудиториями
    def manage_auditoriums(self):
        self.add_form_fields(["Номер аудитории", "Вместимость", "Оборудование", "Тип аудитории"])

        confirm_button = ttk.Button(
            self.content_frame,
            text="Добавить аудиторию",
            command=self.confirm_add_auditorium,
        )
        confirm_button.grid(row=4, column=0, columnspan=2, pady=10)

        edit_button = ttk.Button(
            self.content_frame,
            text="Редактировать аудиторию",
            command=self.confirm_edit_auditorium,
        )
        edit_button.grid(row=5, column=0, columnspan=2, pady=5)

        mark_unavailable_button = ttk.Button(
            self.content_frame,
            text="Пометить как недоступную",
            command=self.mark_auditorium_unavailable,
            style="Warning.TButton",
        )
        mark_unavailable_button.grid(row=6, column=0, columnspan=2, pady=5)

    def confirm_add_auditorium(self):
        fields = self.get_form_fields()
        if not all(fields.values()):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return
        result = self.scheduler.add_auditorium(
            fields["Номер аудитории"], fields["Вместимость"], fields["Оборудование"], fields["Тип аудитории"]
        )
        messagebox.showinfo("Результат", result)

    def confirm_edit_auditorium(self):
        fields = self.get_form_fields()
        if not all(fields.values()):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return
        result = self.scheduler.edit_auditorium(
            fields["Номер аудитории"], fields["Вместимость"], fields["Оборудование"], fields["Тип аудитории"]
        )
        messagebox.showinfo("Результат", result)

    def mark_auditorium_unavailable(self):
        auditorium_number = self.get_form_field_value("Номер аудитории")
        if not auditorium_number:
            messagebox.showerror("Ошибка", "Введите номер аудитории.")
            return
        result = self.scheduler.mark_auditorium_unavailable(auditorium_number, "На ремонте")
        messagebox.showinfo("Результат", result)

    # Расписание занятий
    def schedule_management(self):
        self.add_form_fields(["Загрузить расписание из CSV:"], rows=1)

        load_button = ttk.Button(
            self.content_frame,
            text="Загрузить",
            command=lambda: self.load_schedule_from_csv("schedule.csv"),
        )
        load_button.grid(row=1, column=0, columnspan=2, pady=10)

        check_conflicts_button = ttk.Button(
            self.content_frame,
            text="Проверить пересечения",
            command=self.check_schedule_conflicts,
        )
        check_conflicts_button.grid(row=2, column=0, columnspan=2, pady=5)

    def load_schedule_from_csv(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    result = self.scheduler.book_auditorium(
                        row["auditorium_number"], row["time_slot"], row["event_name"]
                    )
                    if "занята" in result:
                        messagebox.showwarning("Конфликт", f"Конфликт: {result}")
            messagebox.showinfo("Успех", "Расписание успешно загружено.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")

    def check_schedule_conflicts(self):
        conflicts = []
        auditoriums = self.scheduler.view_auditoriums()
        for auditorium in auditoriums:
            auditorium_number, schedule = auditorium
            schedule = eval(schedule) if schedule else []
            times = [slot["time"] for slot in schedule]
            if len(times) != len(set(times)):
                conflicts.append(auditorium_number)
        if conflicts:
            messagebox.showwarning(
                "Конфликты", f"Обнаружены конфликты в следующих аудиториях: {', '.join(conflicts)}."
            )
        else:
            messagebox.showinfo("Конфликты", "Конфликтов не обнаружено.")

    # Бронирование аудиторий
    def booking_management(self):
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
            fields["Номер аудитории"], fields["Временной слот"], fields["Название мероприятия"]
        )
        messagebox.showinfo("Результат", result)

    # Учет занятости
    def occupancy_report(self):
        self.add_form_fields(["Дата", "Временной слот"], rows=2)
        time_slots = ["9:00–10:30", "10:45–12:15", "12:30–14:00", "14:15–15:45", "16:00–17:30", "17:45–19:15"]
        self.set_combobox_values("Временной слот", time_slots)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Просмотреть",
            command=self.view_occupancy,
        )
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def view_occupancy(self):
        date = self.get_form_field_value("Дата")
        time = self.get_form_field_value("Временной слот")
        if not all([date, time]):
            messagebox.showerror("Ошибка", "Введите дату и временной слот.")
            return
        result = self.scheduler.get_auditorium_occupancy(date, time)
        messagebox.showinfo("Занятость аудиторий", result)

    # Отчеты и аналитика
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
        data = self.scheduler.generate_report(period)
        self.scheduler.generate_pdf_report(data, "usage_report.pdf")
        messagebox.showinfo("Отчет", "Отчет успешно сгенерирован и сохранен как usage_report.pdf.")

    # Управление пользователями
    def user_management(self):
        self.add_form_fields(
            ["Логин пользователя", "Новая роль (admin/teacher/student)"], rows=2
        )
        roles = ["admin", "teacher", "student"]
        self.set_combobox_values("Новая роль (admin/teacher/student)", roles)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Изменить роль",
            command=self.change_user_role,
        )
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def change_user_role(self):
        username = self.get_form_field_value("Логин пользователя")
        role = self.get_form_field_value("Новая роль (admin/teacher/student)")
        if not all([username, role]):
            messagebox.showerror("Ошибка", "Заполните все поля.")
            return
        result = self.scheduler.manage_users(username, role)
        messagebox.showinfo("Результат", result)

    # Уведомления
    def notifications(self):
        self.add_form_fields(["Логин получателя", "Сообщение"], rows=2)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Отправить уведомление",
            command=self.send_notification,
        )
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def send_notification(self):
        recipient = self.get_form_field_value("Логин получателя")
        message = self.get_form_field_value("Сообщение")
        if not all([recipient, message]):
            messagebox.showerror("Ошибка", "Заполните все поля.")
            return
        result = self.scheduler.send_email_notification(recipient, "Уведомление от администратора", message)
        messagebox.showinfo("Результат", result)

    # Поиск и фильтрация
    def search_and_filter(self):
        self.add_form_fields(["Вместимость ≥ ", "Оборудование"], rows=2)

        confirm_button = ttk.Button(
            self.content_frame,
            text="Найти",
            command=self.search_auditoriums,
        )
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def search_auditoriums(self):
        capacity = self.get_form_field_value("Вместимость ≥ ")
        equipment = self.get_form_field_value("Оборудование")
        if not any([capacity, equipment]):
            messagebox.showerror("Ошибка", "Заполните хотя бы одно поле для поиска.")
            return
        result = self.scheduler.search_auditoriums(capacity, equipment)
        messagebox.showinfo("Результат поиска", result)

    # Резервное копирование
    def backup_db(self):
        result = self.scheduler.backup_database("backup/university_backup.db")
        messagebox.showinfo("Резервное копирование", result)

    # Обратная связь
    def feedback_system(self):
        self.add_form_fields(["Тикет (заголовок)", "Описание"], rows=2)
        self.form_fields["Описание"] = tk.Text(self.content_frame, height=5, width=30)
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

    # Автоматизация уборки
    def cleaning_schedule(self):
        self.add_form_fields(["Номер аудитории", "Дата уборки (YYYY-MM-DD)"], rows=2)
        self.set_combobox_values("Номер аудитории", self.get_auditoriums())

        confirm_button = ttk.Button(
            self.content_frame,
            text="Запланировать уборку",
            command=self.schedule_cleaning,
        )
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def schedule_cleaning(self):
        auditorium_number = self.get_form_field_value("Номер аудитории")
        date = self.get_form_field_value("Дата уборки (YYYY-MM-DD)")
        if not all([auditorium_number, date]):
            messagebox.showerror("Ошибка", "Заполните все поля.")
            return
        result = self.scheduler.schedule_cleaning(auditorium_number, date)
        messagebox.showinfo("Результат", result)

    # Контроль доступа
    def access_control(self):
        self.add_form_fields(["Номер аудитории", "Пользователь"], rows=2)
        self.set_combobox_values("Номер аудитории", self.get_auditoriums())

        confirm_button = ttk.Button(
            self.content_frame,
            text="Зарегистрировать вход",
            command=self.log_access,
        )
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def log_access(self):
        auditorium_number = self.get_form_field_value("Номер аудитории")
        user = self.get_form_field_value("Пользователь")
        if not all([auditorium_number, user]):
            messagebox.showerror("Ошибка", "Заполните все поля.")
            return
        result = self.scheduler.log_access(auditorium_number, user, "entry")
        messagebox.showinfo("Результат", result)

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
            ).grid(row=i, column=0, padx=5, pady=5)
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
        ).grid(row=row, column=0, padx=5, pady=5)
        combobox = ttk.Combobox(self.content_frame, values=values, font=("Arial", 12))
        combobox.grid(row=row, column=1, padx=5, pady=5)
        self.form_fields[label] = combobox

    def get_form_fields(self):
        """Получает значения всех полей формы."""
        return {label: field.get() for label, field in self.form_fields.items()}

    def get_form_field_value(self, label):
        """Получает значение конкретного поля формы."""
        return self.form_fields.get(label, tk.Entry()).get()

    def get_auditoriums(self):
        """Получает список всех аудиторий."""
        return [row[0] for row in self.scheduler.view_auditoriums()]