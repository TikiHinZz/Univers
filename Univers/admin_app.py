# admin_app.py
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
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.scheduler = AuditoriumScheduler()  # Инициализация планировщика аудиторий
        self.username = username  # Сохраняем имя пользователя

        # Заголовок
        tk.Label(
            self.root,
            text=f"Добро пожаловать, {username} (Админ)!",
            bg="#f0f0f0",
            font=("Arial", 14)
        ).pack(pady=10)

        # Кнопки управления
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=5)

        tk.Button(
            buttons_frame,
            text="Управление аудиториями",
            command=self.manage_auditoriums,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Расписание занятий",
            command=self.schedule_management,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Бронирование аудиторий",
            command=self.booking_management,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Учет занятости",
            command=self.occupancy_report,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Отчеты и аналитика",
            command=self.generate_reports,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Управление пользователями",
            command=self.user_management,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Уведомления",
            command=self.notifications,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Поиск и фильтрация",
            command=self.search_and_filter,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Резервное копирование",
            command=self.backup_db,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Обратная связь",
            command=self.feedback_system,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Автоматизация уборки",
            command=self.cleaning_schedule,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Контроль доступа",
            command=self.access_control,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Выйти",
            command=self.logout,
            bg="#FF5722",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

    # Управление аудиториями
    def manage_auditoriums(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Управление аудиториями")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Номер аудитории:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        auditorium_entry = tk.Entry(dialog)
        auditorium_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Вместимость:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        capacity_entry = tk.Entry(dialog)
        capacity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Оборудование:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        equipment_entry = tk.Entry(dialog)
        equipment_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Тип аудитории:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5)
        type_entry = tk.Entry(dialog)
        type_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(
            dialog,
            text="Добавить аудиторию",
            command=lambda: self.confirm_add_auditorium(
                auditorium_entry.get(),
                capacity_entry.get(),
                equipment_entry.get(),
                type_entry.get(),
                dialog
            ),
            bg="#4CAF50",
            fg="white"
        ).grid(row=4, column=0, columnspan=2, pady=5)

        tk.Button(
            dialog,
            text="Редактировать аудиторию",
            command=lambda: self.confirm_edit_auditorium(
                auditorium_entry.get(),
                capacity_entry.get(),
                equipment_entry.get(),
                type_entry.get(),
                dialog
            ),
            bg="#4CAF50",
            fg="white"
        ).grid(row=5, column=0, columnspan=2, pady=5)

        tk.Button(
            dialog,
            text="Пометить как недоступную",
            command=lambda: self.mark_auditorium_unavailable(auditorium_entry.get(), dialog),
            bg="#FF9800",
            fg="white"
        ).grid(row=6, column=0, columnspan=2, pady=5)

    def confirm_add_auditorium(self, auditorium_number, capacity, equipment, auditorium_type, dialog):
        result = self.scheduler.add_auditorium(auditorium_number, capacity, equipment, auditorium_type)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    def confirm_edit_auditorium(self, auditorium_number, capacity, equipment, auditorium_type, dialog):
        result = self.scheduler.edit_auditorium(auditorium_number, capacity, equipment, auditorium_type)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    def mark_auditorium_unavailable(self, auditorium_number, dialog):
        reason = "На ремонте"
        result = self.scheduler.mark_auditorium_unavailable(auditorium_number, reason)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    # Расписание занятий
    def schedule_management(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Расписание занятий")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Загрузить расписание из CSV:", bg="#f0f0f0").pack(pady=5)
        tk.Button(
            dialog,
            text="Загрузить",
            command=lambda: self.load_schedule_from_csv("schedule.csv"),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=5)

        tk.Label(dialog, text="Проверка пересечений:", bg="#f0f0f0").pack(pady=5)
        tk.Button(
            dialog,
            text="Проверить",
            command=self.check_schedule_conflicts,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=5)

    def load_schedule_from_csv(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    result = self.scheduler.book_auditorium(row['auditorium_number'], row['time_slot'], row['event_name'])
                    if "занята" in result:
                        print(f"Конфликт: {result}")
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
            messagebox.showwarning("Конфликты", f"Обнаружены конфликты в следующих аудиториях: {', '.join(conflicts)}.")
        else:
            messagebox.showinfo("Конфликты", "Конфликтов не обнаружено.")

    # Бронирование аудиторий
    def booking_management(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Бронирование аудиторий")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Номер аудитории:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        auditorium_combobox = ttk.Combobox(dialog, values=self.get_auditoriums())
        auditorium_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Временной слот:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        time_slots = ["9:00–10:30", "10:45–12:15", "12:30–14:00", "14:15–15:45", "16:00–17:30", "17:45–19:15"]
        time_combobox = ttk.Combobox(dialog, values=time_slots)
        time_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Название мероприятия:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        event_entry = tk.Entry(dialog)
        event_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(
            dialog,
            text="Забронировать",
            command=lambda: self.confirm_booking(
                auditorium_combobox.get(),
                time_combobox.get(),
                event_entry.get(),
                dialog
            ),
            bg="#4CAF50",
            fg="white"
        ).grid(row=3, column=0, columnspan=2, pady=5)

    def confirm_booking(self, auditorium, time, event, dialog):
        result = self.scheduler.book_auditorium(auditorium, time, event)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    # Учет занятости
    def occupancy_report(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Учет занятости")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Дата:", bg="#f0f0f0").pack(pady=5)
        date_entry = tk.Entry(dialog)
        date_entry.pack(pady=5)

        tk.Label(dialog, text="Временной слот:", bg="#f0f0f0").pack(pady=5)
        time_combobox = ttk.Combobox(dialog, values=["9:00–10:30", "10:45–12:15", "12:30–14:00", "14:15–15:45", "16:00–17:30", "17:45–19:15"])
        time_combobox.pack(pady=5)

        tk.Button(
            dialog,
            text="Просмотреть",
            command=lambda: self.view_occupancy(date_entry.get(), time_combobox.get(), dialog),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=5)

    def view_occupancy(self, date, time, dialog):
        result = self.scheduler.get_auditorium_occupancy(date, time)
        messagebox.showinfo("Занятость аудиторий", result)
        dialog.destroy()

    # Отчеты и аналитика
    def generate_reports(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Генерация отчетов")
        dialog.geometry("400x200")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Период (YYYY-MM-DD):", bg="#f0f0f0").pack(pady=5)
        period_entry = tk.Entry(dialog)
        period_entry.pack(pady=5)

        tk.Button(
            dialog,
            text="Сгенерировать",
            command=lambda: self.generate_usage_report(period_entry.get()),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=5)

    def generate_usage_report(self, period):
        data = self.scheduler.generate_report(period)
        self.scheduler.generate_pdf_report(data, "usage_report.pdf")
        messagebox.showinfo("Отчет", "Отчет успешно сгенерирован и сохранен как usage_report.pdf.")

    # Управление пользователями
    def user_management(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Управление пользователями")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Логин пользователя:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        username_entry = tk.Entry(dialog)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Новая роль (admin/teacher/student):", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        role_combobox = ttk.Combobox(dialog, values=["admin", "teacher", "student"])
        role_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            dialog,
            text="Изменить роль",
            command=lambda: self.change_user_role(username_entry.get(), role_combobox.get(), dialog),
            bg="#4CAF50",
            fg="white"
        ).grid(row=2, column=0, columnspan=2, pady=5)

    def change_user_role(self, username, role, dialog):
        result = self.scheduler.manage_users(username, role)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    # Уведомления
    def notifications(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Уведомления")
        dialog.geometry("400x200")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Логин получателя:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        recipient_entry = tk.Entry(dialog)
        recipient_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Сообщение:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        message_entry = tk.Entry(dialog)
        message_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            dialog,
            text="Отправить уведомление",
            command=lambda: self.send_notification(recipient_entry.get(), message_entry.get(), dialog),
            bg="#4CAF50",
            fg="white"
        ).grid(row=2, column=0, columnspan=2, pady=5)

    def send_notification(self, recipient, message, dialog):
        result = self.scheduler.send_email_notification(recipient, "Уведомление от администратора", message)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    # Поиск и фильтрация
    def search_and_filter(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Поиск и фильтрация")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Вместимость ≥ :", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        capacity_entry = tk.Entry(dialog)
        capacity_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Оборудование:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        equipment_entry = tk.Entry(dialog)
        equipment_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            dialog,
            text="Найти",
            command=lambda: self.search_auditoriums(
                capacity_entry.get(),
                equipment_entry.get(),
                dialog
            ),
            bg="#4CAF50",
            fg="white"
        ).grid(row=2, column=0, columnspan=2, pady=5)

    def search_auditoriums(self, capacity, equipment, dialog):
        result = self.scheduler.search_auditoriums(capacity, equipment)
        messagebox.showinfo("Результат поиска", result)
        dialog.destroy()

    # Резервное копирование
    def backup_db(self):
        result = self.scheduler.backup_database("backup/university_backup.db")
        messagebox.showinfo("Резервное копирование", result)

    # Обратная связь
    def feedback_system(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Обратная связь")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Тикет (заголовок):", bg="#f0f0f0").pack(pady=5)
        ticket_title_entry = tk.Entry(dialog)
        ticket_title_entry.pack(pady=5)

        tk.Label(dialog, text="Описание:", bg="#f0f0f0").pack(pady=5)
        ticket_description_entry = tk.Text(dialog, height=5, width=30)
        ticket_description_entry.pack(pady=5)

        tk.Button(
            dialog,
            text="Создать тикет",
            command=lambda: self.create_ticket(
                ticket_title_entry.get(),
                ticket_description_entry.get("1.0", tk.END),
                dialog
            ),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=5)

    def create_ticket(self, title, description, dialog):
        result = self.scheduler.create_ticket(self.username, title, description.strip())
        messagebox.showinfo("Тикет", result)
        dialog.destroy()

    # Автоматизация уборки
    def cleaning_schedule(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Планирование уборки")
        dialog.geometry("400x200")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Номер аудитории:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        auditorium_combobox = ttk.Combobox(dialog, values=self.get_auditoriums())
        auditorium_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Дата уборки (YYYY-MM-DD):", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        date_entry = tk.Entry(dialog)
        date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            dialog,
            text="Запланировать уборку",
            command=lambda: self.schedule_cleaning(auditorium_combobox.get(), date_entry.get(), dialog),
            bg="#4CAF50",
            fg="white"
        ).grid(row=2, column=0, columnspan=2, pady=5)

    def schedule_cleaning(self, auditorium_number, date, dialog):
        result = self.scheduler.schedule_cleaning(auditorium_number, date)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    # Контроль доступа
    def access_control(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Контроль доступа")
        dialog.geometry("400x200")
        dialog.configure(bg="#f0f0f0")

        tk.Label(dialog, text="Номер аудитории:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        auditorium_combobox = ttk.Combobox(dialog, values=self.get_auditoriums())
        auditorium_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Пользователь:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        user_entry = tk.Entry(dialog)
        user_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            dialog,
            text="Зарегистрировать вход",
            command=lambda: self.log_access(
                auditorium_combobox.get(),
                user_entry.get(),
                "entry",
                dialog
            ),
            bg="#4CAF50",
            fg="white"
        ).grid(row=2, column=0, columnspan=2, pady=5)

    def log_access(self, auditorium_number, user, action, dialog):
        result = self.scheduler.log_access(auditorium_number, user, action)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    # Выход из аккаунта
    def logout(self):
        self.root.destroy()
        from main import start_login
        start_login()