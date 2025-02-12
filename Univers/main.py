# main.py

import tkinter as tk
from login_window import LoginWindow
from database import AuditoriumScheduler
import sqlite3

def initialize_admin_user():
    """Добавляет администратора Tiki в базу данных, если его еще нет."""
    scheduler = AuditoriumScheduler()
    username = "Tiki"
    password = "123"
    role = "admin"

    # Хешируем пароль перед сохранением
    hashed_password = hash_password(password)

    try:
        # Проверяем, существует ли пользователь
        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if not user:
            cursor.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                (username, hashed_password, role)
            )
            conn.commit()
            print(f"Пользователь {username} успешно создан!")
        else:
            print(f"Пользователь {username} уже существует.")
    except Exception as e:
        print(f"Ошибка при создании пользователя: {str(e)}")
    finally:
        conn.close()


@staticmethod
def hash_password(password):
    """Хеширует пароль для безопасного хранения."""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def start_login():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    # Инициализация базы данных
    AuditoriumScheduler.initialize_database()

    initialize_admin_user()

    start_login()