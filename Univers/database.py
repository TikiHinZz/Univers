import sqlite3
import json


class DatabaseManager:
    """Класс для управления подключением к базе данных."""
    def __init__(self, db_name='university.db'):
        self.db_name = db_name

    def __enter__(self):
        """Открывает соединение с базой данных."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрывает соединение с базой данных."""
        self.conn.commit()
        self.conn.close()

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос."""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def fetch_one(self, query, params=None):
        """Возвращает одну строку результата запроса."""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        """Возвращает все строки результата запроса."""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()


class AuditoriumScheduler:
    """Класс для управления аудиториями и их расписанием."""
    def __init__(self):
        self.db_manager = DatabaseManager()

    @staticmethod
    def initialize_database(db_name='university.db'):
        """Инициализация базы данных и создание необходимых таблиц."""
        with DatabaseManager(db_name) as db:
            # Таблица пользователей
            db.execute_query('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')

            # Таблица аудиторий
            db.execute_query('''
                CREATE TABLE IF NOT EXISTS auditoriums (
                    auditorium_number TEXT PRIMARY KEY,
                    capacity INTEGER,
                    equipment TEXT,
                    auditorium_type TEXT
                )
            ''')

            # Таблица бронирований
            db.execute_query('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    auditorium_number TEXT,
                    time_slot TEXT,
                    event_name TEXT,
                    booked_by TEXT,
                    FOREIGN KEY (auditorium_number) REFERENCES auditoriums (auditorium_number),
                    FOREIGN KEY (booked_by) REFERENCES users (username)
                )
            ''')

            # Таблица запросов на оборудование
            db.execute_query('''
                CREATE TABLE IF NOT EXISTS equipment_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    auditorium_number TEXT,
                    equipment TEXT,
                    requested_by TEXT,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY (auditorium_number) REFERENCES auditoriums (auditorium_number),
                    FOREIGN KEY (requested_by) REFERENCES users (username)
                )
            ''')

            # Таблица тикетов обратной связи
            db.execute_query('''
                CREATE TABLE IF NOT EXISTS feedback_tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    created_by TEXT,
                    status TEXT DEFAULT 'open',
                    FOREIGN KEY (created_by) REFERENCES users (username)
                )
            ''')

    def add_auditorium(self, auditorium_number, capacity, equipment, auditorium_type):
        """Добавляет новую аудиторию."""
        with self.db_manager as db:
            try:
                db.execute_query(
                    'INSERT INTO auditoriums (auditorium_number, capacity, equipment, auditorium_type) VALUES (?, ?, ?, ?)',
                    (auditorium_number, capacity, equipment, auditorium_type)
                )
                return f"Аудитория {auditorium_number} успешно добавлена."
            except sqlite3.IntegrityError:
                return f"Аудитория {auditorium_number} уже существует."

    def view_auditoriums(self):
        """Просмотр всех аудиторий."""
        with self.db_manager as db:
            return db.fetch_all('SELECT * FROM auditoriums')

    def book_auditorium(self, auditorium_number, time_slot, event_name, booked_by):
        """Бронирует аудиторию."""
        with self.db_manager as db:
            # Проверяем доступность аудитории
            existing_booking = db.fetch_one(
                'SELECT * FROM bookings WHERE auditorium_number = ? AND time_slot = ?',
                (auditorium_number, time_slot)
            )
            if existing_booking:
                return f"Аудитория {auditorium_number} занята в это время ({time_slot})."

            # Добавляем бронирование
            db.execute_query(
                'INSERT INTO bookings (auditorium_number, time_slot, event_name, booked_by) VALUES (?, ?, ?, ?)',
                (auditorium_number, time_slot, event_name, booked_by)
            )
            return f"Аудитория {auditorium_number} забронирована на {time_slot} для {event_name}."

    def cancel_booking(self, auditorium_number, time_slot):
        """Отменяет бронирование."""
        with self.db_manager as db:
            db.execute_query(
                'DELETE FROM bookings WHERE auditorium_number = ? AND time_slot = ?',
                (auditorium_number, time_slot)
            )
            if db.cursor.rowcount > 0:
                return f"Бронирование в аудитории {auditorium_number} на {time_slot} отменено."
            else:
                return f"Нет бронирования в аудитории {auditorium_number} на {time_slot}."

    def request_equipment(self, auditorium_number, equipment, requested_by):
        """Отправляет запрос на оборудование."""
        with self.db_manager as db:
            db.execute_query(
                'INSERT INTO equipment_requests (auditorium_number, equipment, requested_by) VALUES (?, ?, ?)',
                (auditorium_number, equipment, requested_by)
            )
            return "Запрос на оборудование отправлен."

    def create_feedback_ticket(self, title, description, created_by):
        """Создает тикет обратной связи."""
        with self.db_manager as db:
            db.execute_query(
                'INSERT INTO feedback_tickets (title, description, created_by) VALUES (?, ?, ?)',
                (title, description, created_by)
            )
            return "Тикет создан успешно."

    def get_auditoriums(self):
        """Возвращает список всех аудиторий."""
        with self.db_manager as db:
            return [row[0] for row in db.fetch_all('SELECT auditorium_number FROM auditoriums')]

    def find_free_auditoriums(self, time_slot):
        """Находит свободные аудитории в указанное время."""
        with self.db_manager as db:
            all_auditoriums = set(row[0] for row in db.fetch_all('SELECT auditorium_number FROM auditoriums'))
            booked_auditoriums = set(row[0] for row in db.fetch_all(
                'SELECT auditorium_number FROM bookings WHERE time_slot = ?', (time_slot,)
            ))
            free_auditoriums = all_auditoriums - booked_auditoriums
            return list(free_auditoriums)

    def get_teacher_bookings(self, teacher_name):
        """Возвращает все бронирования для преподавателя."""
        with self.db_manager as db:
            return db.fetch_all('SELECT * FROM bookings WHERE booked_by = ?', (teacher_name,))
    