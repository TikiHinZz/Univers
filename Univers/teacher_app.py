import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from database import AuditoriumScheduler

class TeacherApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Приложение преподавателя | {username}")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.scheduler = AuditoriumScheduler()
        self.username = username

        # Заголовок
        tk.Label(
            self.root,
            text=f"Добро пожаловать, {username} (Преподаватель)!",
            bg="#f0f0f0",
            font=("Arial", 14)
        ).pack(pady=10)

        # Кнопки
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=5)

        tk.Button(
            buttons_frame,
            text="Забронировать аудиторию",
            command=self.book_auditorium,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Мои бронирования",
            command=self.view_my_bookings,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Запрос оборудования",
            command=self.request_equipment,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Отменить бронирование",
            command=self.cancel_booking,
            bg="#FF5722",
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

    def book_auditorium(self):
        """Окно для бронирования аудитории"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Бронирование аудитории")
        dialog.geometry("350x250")
        dialog.configure(bg="#f0f0f0")

        frame = tk.Frame(dialog, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(expand=True)

        # Выбор аудитории
        tk.Label(frame, text="Номер аудитории:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        auditorium_combobox = ttk.Combobox(frame, values=self.get_auditoriums(), font=("Arial", 12))
        auditorium_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Выбор временного слота
        tk.Label(frame, text="Временной слот:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        time_slots = ["9:00–10:30", "10:45–12:15", "12:30–14:00", "14:15–15:45", "16:00–17:30", "17:45–19:15"]
        time_combobox = ttk.Combobox(frame, values=time_slots, font=("Arial", 12))
        time_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Название мероприятия
        tk.Label(frame, text="Название мероприятия:", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        event_entry = tk.Entry(frame, font=("Arial", 12))
        event_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка подтверждения
        tk.Button(
            frame,
            text="Подтвердить",
            command=lambda: self.confirm_booking(
                auditorium_combobox.get(),
                time_combobox.get(),
                event_entry.get(),
                dialog
            ),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)

    def confirm_booking(self, auditorium, time, event, dialog):
        """Подтверждение бронирования аудитории"""
        if not auditorium or not time or not event:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        result = self.scheduler.book_auditorium(auditorium, time, event, self.username)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    def view_my_bookings(self):
        """Просмотр всех бронирований преподавателя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Мои бронирования")
        dialog.geometry("500x300")
        dialog.configure(bg="#f0f0f0")

        frame = tk.Frame(dialog, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(expand=True)

        # Получаем бронирования преподавателя
        bookings = self.scheduler.get_teacher_bookings(self.username)

        if not bookings:
            tk.Label(frame, text="У вас нет активных бронирований.", bg="#f0f0f0", font=("Arial", 12)).pack()
            return

        for booking in bookings:
            auditorium, time, event = booking
            tk.Label(
                frame,
                text=f"Аудитория: {auditorium}, Время: {time}, Мероприятие: {event}",
                bg="#f0f0f0",
                font=("Arial", 12)
            ).pack(anchor=tk.W)

    def request_equipment(self):
        """Запрос оборудования"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Запрос оборудования")
        dialog.geometry("350x200")
        dialog.configure(bg="#f0f0f0")

        frame = tk.Frame(dialog, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(expand=True)

        # Выбор аудитории
        tk.Label(frame, text="Номер аудитории:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        auditorium_combobox = ttk.Combobox(frame, values=self.get_auditoriums(), font=("Arial", 12))
        auditorium_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Выбор оборудования
        tk.Label(frame, text="Оборудование:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        equipment_combobox = ttk.Combobox(frame, values=["Проектор", "Микрофон", "Доска", "Компьютер"], font=("Arial", 12))
        equipment_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Кнопка подтверждения
        tk.Button(
            frame,
            text="Отправить запрос",
            command=lambda: self.confirm_equipment_request(
                auditorium_combobox.get(),
                equipment_combobox.get(),
                dialog
            ),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.EW)

    def confirm_equipment_request(self, auditorium, equipment, dialog):
        """Подтверждение запроса оборудования"""
        if not auditorium or not equipment:
            messagebox.showerror("Ошибка", "Выберите аудиторию и оборудование.")
            return

        result = self.scheduler.request_equipment(auditorium, equipment, self.username)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    def cancel_booking(self):
        """Окно для отмены бронирования"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Отмена бронирования")
        dialog.geometry("350x200")
        dialog.configure(bg="#f0f0f0")

        frame = tk.Frame(dialog, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(expand=True)

        # Выбор аудитории
        tk.Label(frame, text="Номер аудитории:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        auditorium_combobox = ttk.Combobox(frame, values=self.get_auditoriums(), font=("Arial", 12))
        auditorium_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Выбор временного слота
        tk.Label(frame, text="Временной слот:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        time_slots = ["9:00–10:30", "10:45–12:15", "12:30–14:00", "14:15–15:45", "16:00–17:30", "17:45–19:15"]
        time_combobox = ttk.Combobox(frame, values=time_slots, font=("Arial", 12))
        time_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Кнопка подтверждения
        tk.Button(
            frame,
            text="Отменить",
            command=lambda: self.confirm_cancel(
                auditorium_combobox.get(),
                time_combobox.get(),
                dialog
            ),
            bg="#FF5722",
            fg="white",
            font=("Arial", 12)
        ).grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.EW)

    def confirm_cancel(self, auditorium, time, dialog):
        """Подтверждение отмены бронирования"""
        if not auditorium or not time:
            messagebox.showerror("Ошибка", "Выберите аудиторию и временной слот.")
            return

        result = self.scheduler.cancel_booking(auditorium, time)
        messagebox.showinfo("Результат", result)
        dialog.destroy()

    def get_auditoriums(self):
        """Получение списка всех аудиторий из базы данных"""
        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()
        cursor.execute('SELECT auditorium_number FROM auditoriums')
        auditoriums = [row[0] for row in cursor.fetchall()]
        conn.close()
        return auditoriums

    def logout(self):
        """Выход из аккаунта преподавателя"""
        self.root.destroy()
        from main import start_login
        start_login()