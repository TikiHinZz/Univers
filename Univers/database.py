import sqlite3
import json

class DatabaseManager:
    """Класс для управления подключением к базе данных и выполнения запросов."""

    def __init__(self, db_name='university.db'):
        self.db_name = db_name

    def __enter__(self):
        """Открывает соединение с базой данных."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрывает соединение с базой данных."""
        self.conn.close()

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос."""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

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

    def view_auditoriums(self):
        """Возвращает список всех аудиторий."""
        with self.db_manager as db:
            return db.fetch_all('SELECT * FROM auditoriums')

    def add_auditorium(self, auditorium_number):
        """Добавляет новую аудиторию."""
        with self.db_manager as db:
            try:
                db.execute_query(
                    'INSERT INTO auditoriums (auditorium_number, schedule) VALUES (?, ?)',
                    (auditorium_number, '[]')
                )
                return f"Аудитория {auditorium_number} успешно добавлена."
            except sqlite3.IntegrityError:
                return f"Аудитория {auditorium_number} уже существует."

    def delete_auditorium(self, auditorium_number):
        """Удаляет аудиторию."""
        with self.db_manager as db:
            db.execute_query('DELETE FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
            db.execute_query('DELETE FROM teacher_assignments WHERE auditorium_number = ?', (auditorium_number,))
            if db.cursor.rowcount > 0:
                return f"Аудитория {auditorium_number} удалена."
            else:
                return f"Аудитория {auditorium_number} не найдена."

    def book_auditorium(self, auditorium_number, time_slot, event_name):
        """Бронирует аудиторию на указанное время."""
        with self.db_manager as db:
            result = db.fetch_one('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
            if not result:
                return f"Аудитория {auditorium_number} не найдена."

            schedule = json.loads(result[0]) if result[0] else []
            for slot in schedule:
                if slot["time"] == time_slot:
                    return f"Аудитория {auditorium_number} занята в это время ({time_slot})."

            schedule.append({"time": time_slot, "event": event_name})
            db.execute_query(
                'UPDATE auditoriums SET schedule = ? WHERE auditorium_number = ?',
                (json.dumps(schedule), auditorium_number)
            )
            return f"Аудитория {auditorium_number} забронирована на {time_slot} для {event_name}."

    def check_availability(self, auditorium_number, time_slot):
        """Проверяет доступность аудитории на указанное время."""
        with self.db_manager as db:
            result = db.fetch_one('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
            if not result:
                return f"Аудитория {auditorium_number} не найдена."

            schedule = json.loads(result[0]) if result[0] else []
            for slot in schedule:
                if slot["time"] == time_slot:
                    return f"Аудитория {auditorium_number} занята в это время ({time_slot})."

            return f"Аудитория {auditorium_number} свободна в это время ({time_slot})."

    def cancel_booking(self, auditorium_number, time_slot):
        """Отменяет бронирование аудитории на указанное время."""
        with self.db_manager as db:
            result = db.fetch_one('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
            if not result:
                return f"Аудитория {auditorium_number} не найдена."

            schedule = json.loads(result[0]) if result[0] else []
            updated_schedule = [slot for slot in schedule if slot["time"] != time_slot]

            if len(updated_schedule) == len(schedule):
                return f"Нет бронирования в аудитории {auditorium_number} на {time_slot}."
            else:
                db.execute_query(
                    'UPDATE auditoriums SET schedule = ? WHERE auditorium_number = ?',
                    (json.dumps(updated_schedule), auditorium_number)
                )
                return f"Бронирование в аудитории {auditorium_number} на {time_slot} отменено."

    def assign_teacher(self, teacher, auditorium_number):
        """Назначает преподавателя на аудиторию."""
        with self.db_manager as db:
            if not db.fetch_one('SELECT * FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,)):
                return f"Аудитория {auditorium_number} не найдена."

            db.execute_query('DELETE FROM teacher_assignments WHERE teacher = ?', (teacher,))
            db.execute_query(
                'INSERT INTO teacher_assignments (teacher, auditorium_number) VALUES (?, ?)',
                (teacher, auditorium_number)
            )
            return f"Преподаватель {teacher} назначен в аудиторию {auditorium_number}."

    def get_auditorium_schedule(self, auditorium_number):
        """Возвращает расписание для указанной аудитории."""
        with self.db_manager as db:
            result = db.fetch_one('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
            if not result or not result[0]:
                return []  # Если расписание пустое

            schedule = json.loads(result[0])
            teacher_name = self.get_teacher_for_auditorium(auditorium_number)
            return [(slot["time"], slot["event"], teacher_name) for slot in schedule]

    def get_teacher_for_auditorium(self, auditorium_number):
        """Возвращает преподавателя, назначенного на аудиторию."""
        with self.db_manager as db:
            result = db.fetch_one('SELECT teacher FROM teacher_assignments WHERE auditorium_number = ?', (auditorium_number,))
            return result[0] if result else None

    def get_auditoriums(self):
        """Возвращает список всех аудиторий."""
        with self.db_manager as db:
            return [row[0] for row in db.fetch_all('SELECT auditorium_number FROM auditoriums')]

    def get_teachers(self):
        """Возвращает список всех преподавателей."""
        with self.db_manager as db:
            return [row[0] for row in db.fetch_all('SELECT teacher_name FROM teachers')]

    def get_teacher_bookings(self, teacher_name):
        """Возвращает все бронирования для указанного преподавателя."""
        with self.db_manager as db:
            return db.fetch_all('SELECT auditorium_number, time, event FROM bookings WHERE teacher = ?', (teacher_name,))

    def request_equipment(self, auditorium, equipment, teacher_name):
        """Отправляет запрос на оборудование для аудитории."""
        with self.db_manager as db:
            db.execute_query(
                'INSERT INTO equipment_requests (auditorium_number, equipment, teacher) VALUES (?, ?, ?)',
                (auditorium, equipment, teacher_name)
            )
            return "Запрос на оборудование отправлен."