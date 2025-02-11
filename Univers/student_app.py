import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from database import AuditoriumScheduler

class StudentApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Приложение студента | {username}")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.scheduler = AuditoriumScheduler()
        self.username = username

        # Заголовок
        tk.Label(
            self.root,
            text=f"Добро пожаловать, {username} (Студент)!",
            bg="#f0f0f0",
            font=("Arial", 14)
        ).pack(pady=10)

        # Кнопки
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=5)

        tk.Button(
            buttons_frame,
            text="Просмотреть расписание",
            command=self.view_auditoriums,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            buttons_frame,
            text="Найти свободные аудитории",
            command=self.find_free_auditoriums,
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

    def view_auditoriums(self):
        """Просмотр расписания аудиторий"""
        auditoriums = self.scheduler.view_auditoriums()
        message = "Список аудиторий:\n"

        for auditorium in auditoriums:
            auditorium_number, schedule = auditorium
            teacher_name = self.get_teacher_for_auditorium(auditorium_number)
            schedule = eval(schedule) if schedule else []

            message += f"Аудитория {auditorium_number}:"
            if teacher_name:
                message += f" Назначен преподаватель: {teacher_name}\n"
            else:
                message += " Преподаватель не назначен\n"

            if not schedule:
                message += "  Свободна.\n"
            else:
                for slot in schedule:
                    message += f"  Занята: {slot['time']} ({slot['event']})\n"

        messagebox.showinfo("Список аудиторий", message)

    def find_free_auditoriums(self):
        """Поиск свободных аудиторий"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Поиск свободных аудиторий")
        dialog.geometry("400x200")
        dialog.configure(bg="#f0f0f0")

        frame = tk.Frame(dialog, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(expand=True)

        # Выбор временного слота
        tk.Label(frame, text="Временной слот:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        time_slots = ["9:00–10:30", "10:45–12:15", "12:30–14:00", "14:15–15:45", "16:00–17:30", "17:45–19:15"]
        time_combobox = ttk.Combobox(frame, values=time_slots, font=("Arial", 12))
        time_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Кнопка поиска
        tk.Button(
            frame,
            text="Найти",
            command=lambda: self.show_free_auditoriums(time_combobox.get(), dialog),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.EW)

    def show_free_auditoriums(self, time, dialog):
        """Отображение свободных аудиторий"""
        if not time:
            messagebox.showerror("Ошибка", "Выберите временной слот.")
            return

        free_auditoriums = self.scheduler.find_free_auditoriums(time)
        if not free_auditoriums:
            messagebox.showinfo("Результат", "Нет свободных аудиторий на выбранное время.")
        else:
            message = "Свободные аудитории:\n"
            for auditorium in free_auditoriums:
                message += f"Аудитория {auditorium}\n"
            messagebox.showinfo("Результат", message)
        dialog.destroy()

    def get_teacher_for_auditorium(self, auditorium_number):
        """Получение преподавателя для аудитории"""
        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()
        cursor.execute('SELECT teacher FROM teacher_assignments WHERE auditorium_number = ?', (auditorium_number,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def logout(self):
        """Выход из аккаунта студента"""
        self.root.destroy()
        from main import start_login
        start_login()