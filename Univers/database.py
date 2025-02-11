# database.py
import sqlite3
import json

class AuditoriumScheduler:
    def __init__(self):
        self.conn = sqlite3.connect('university.db')
        self.cursor = self.conn.cursor()

    # Просмотр всех аудиторий
    def view_auditoriums(self):
        self.cursor.execute('SELECT * FROM auditoriums')
        return self.cursor.fetchall()

    # Добавление аудитории
    def add_auditorium(self, auditorium_number):
        try:
            self.cursor.execute('INSERT INTO auditoriums (auditorium_number, schedule) VALUES (?, ?)', 
                                (auditorium_number, '[]'))
            self.conn.commit()
            return f"Аудитория {auditorium_number} успешно добавлена."
        except sqlite3.IntegrityError:
            return f"Аудитория {auditorium_number} уже существует."

    # Удаление аудитории
    def delete_auditorium(self, auditorium_number):
        self.cursor.execute('DELETE FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        self.cursor.execute('DELETE FROM teacher_assignments WHERE auditorium_number = ?', (auditorium_number,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return f"Аудитория {auditorium_number} удалена."
        else:
            return f"Аудитория {auditorium_number} не найдена."

    # Бронирование аудитории
    def book_auditorium(self, auditorium_number, time_slot, event_name):
        self.cursor.execute('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        result = self.cursor.fetchone()

        if not result:
            return f"Аудитория {auditorium_number} не найдена."

        schedule = json.loads(result[0]) if result[0] else []

        for slot in schedule:
            if slot["time"] == time_slot:
                return f"Аудитория {auditorium_number} занята в это время ({time_slot})."

        schedule.append({"time": time_slot, "event": event_name})
        self.cursor.execute('UPDATE auditoriums SET schedule = ? WHERE auditorium_number = ?', 
                            (json.dumps(schedule), auditorium_number))
        self.conn.commit()
        return f"Аудитория {auditorium_number} забронирована на {time_slot} для {event_name}."

    # Проверка доступности аудитории
    def check_availability(self, auditorium_number, time_slot):
        self.cursor.execute('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        result = self.cursor.fetchone()

        if not result:
            return f"Аудитория {auditorium_number} не найдена."

        schedule = json.loads(result[0]) if result[0] else []

        for slot in schedule:
            if slot["time"] == time_slot:
                return f"Аудитория {auditorium_number} занята в это время ({time_slot})."

        return f"Аудитория {auditorium_number} свободна в это время ({time_slot})."

    # Отмена бронирования
    def cancel_booking(self, auditorium_number, time_slot):
        self.cursor.execute('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        result = self.cursor.fetchone()

        if not result:
            return f"Аудитория {auditorium_number} не найдена."

        schedule = json.loads(result[0]) if result[0] else []
        updated_schedule = [slot for slot in schedule if slot["time"] != time_slot]

        if len(updated_schedule) == len(schedule):
            return f"Нет бронирования в аудитории {auditorium_number} на {time_slot}."
        else:
            self.cursor.execute('UPDATE auditoriums SET schedule = ? WHERE auditorium_number = ?', 
                                (json.dumps(updated_schedule), auditorium_number))
            self.conn.commit()
            return f"Бронирование в аудитории {auditorium_number} на {time_slot} отменено."

    # Назначение преподавателя
    def assign_teacher(self, teacher, auditorium_number):
        self.cursor.execute('SELECT * FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        if not self.cursor.fetchone():
            return f"Аудитория {auditorium_number} не найдена."

        self.cursor.execute('DELETE FROM teacher_assignments WHERE teacher = ?', (teacher,))
        self.cursor.execute('INSERT INTO teacher_assignments (teacher, auditorium_number) VALUES (?, ?)', 
                            (teacher, auditorium_number))
        self.conn.commit()
        return f"Преподаватель {teacher} назначен в аудиторию {auditorium_number}."

    # Получение расписания для конкретной аудитории
    def get_auditorium_schedule(self, auditorium_number):
        self.cursor.execute('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        result = self.cursor.fetchone()

        if not result or not result[0]:
            return []  # Если расписание пустое

        schedule = json.loads(result[0])

        # Получаем назначенного преподавателя
        teacher_name = self.get_teacher_for_auditorium(auditorium_number)

        # Формируем данные для вывода
        schedule_data = []
        for slot in schedule:
            schedule_data.append((slot["time"], slot["event"], teacher_name))

        return schedule_data

    # Получение преподавателя для аудитории
    def get_teacher_for_auditorium(self, auditorium_number):
        self.cursor.execute('SELECT teacher FROM teacher_assignments WHERE auditorium_number = ?', (auditorium_number,))
        result = self.cursor.fetchone()
        return result[0] if result else None


    # Добавляем тестовых преподавателей и их предметы
    teachers_data = [
        ("Анна Иванова", "Математика"),
        ("Петр Сергеев", "Физика"),
        ("Ольга Кузнецова", "Химия"),
        ("Игорь Петров", "История"),
        ("Елена Михайлова", "Литература"),
        ("Александр Андреев", "Программирование"),
        ("Мария Дмитриева", "Экономика"),
        ("Денис Васильев", "Биология"),
        ("Наталья Александрова", "Психология"),
        ("Виктория Романова", "Право"),
        ("Сергей Игоревич", "Философия"),
        ("Татьяна Владимировна", "География"),
        ("Андрей Юрьевич", "Английский язык"),
        ("Ирина Олеговна", "Французский язык"),
        ("Дмитрий Алексеевич", "Китайский язык"),
        ("Юлия Викторовна", "Испанский язык"),
        ("Максим Петрович", "Статистика"),
        ("Екатерина Сергеевна", "Маркетинг"),
        ("Алексей Николаевич", "Робототехника"),
        ("Владимир Анатольевич", "Электроника")
    ]
class AuditoriumScheduler:
    def __init__(self):
        self.conn = sqlite3.connect('university.db')
        self.cursor = self.conn.cursor()

    def view_auditoriums(self):
        self.cursor.execute('SELECT * FROM auditoriums')
        return self.cursor.fetchall()

    def add_auditorium(self, auditorium_number):
        try:
            self.cursor.execute('INSERT INTO auditoriums (auditorium_number, schedule) VALUES (?, ?)', 
                                (auditorium_number, '[]'))
            self.conn.commit()
            return f"Аудитория {auditorium_number} успешно добавлена."
        except sqlite3.IntegrityError:
            return f"Аудитория {auditorium_number} уже существует."


    def delete_auditorium(self, auditorium_number):
        self.cursor.execute('DELETE FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        self.cursor.execute('DELETE FROM teacher_assignments WHERE auditorium_number = ?', (auditorium_number,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return f"Аудитория {auditorium_number} удалена."
        else:
            return f"Аудитория {auditorium_number} не найдена."

    def book_auditorium(self, auditorium_number, time_slot, event_name):
        self.cursor.execute('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        result = self.cursor.fetchone()

        if not result:
            return f"Аудитория {auditorium_number} не найдена."

        schedule = json.loads(result[0]) if result[0] else []

        for slot in schedule:
            if slot["time"] == time_slot:
                return f"Аудитория {auditorium_number} занята в это время ({time_slot})."

        schedule.append({"time": time_slot, "event": event_name})
        self.cursor.execute('UPDATE auditoriums SET schedule = ? WHERE auditorium_number = ?', 
                            (json.dumps(schedule), auditorium_number))
        self.conn.commit()
        return f"Аудитория {auditorium_number} забронирована на {time_slot} для {event_name}."

    def check_availability(self, auditorium_number, time_slot):
        self.cursor.execute('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        result = self.cursor.fetchone()

        if not result:
            return f"Аудитория {auditorium_number} не найдена."

        schedule = json.loads(result[0]) if result[0] else []

        for slot in schedule:
            if slot["time"] == time_slot:
                return f"Аудитория {auditorium_number} занята в это время ({time_slot})."

        return f"Аудитория {auditorium_number} свободна в это время ({time_slot})."

    def cancel_booking(self, auditorium_number, time_slot):
        self.cursor.execute('SELECT schedule FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        result = self.cursor.fetchone()

        if not result:
            return f"Аудитория {auditorium_number} не найдена."

        schedule = json.loads(result[0]) if result[0] else []
        updated_schedule = [slot for slot in schedule if slot["time"] != time_slot]

        if len(updated_schedule) == len(schedule):
            return f"Нет бронирования в аудитории {auditorium_number} на {time_slot}."
        else:
            self.cursor.execute('UPDATE auditoriums SET schedule = ? WHERE auditorium_number = ?', 
                                (json.dumps(updated_schedule), auditorium_number))
            self.conn.commit()
            return f"Бронирование в аудитории {auditorium_number} на {time_slot} отменено."

    def assign_teacher(self, teacher, auditorium_number):
        self.cursor.execute('SELECT * FROM auditoriums WHERE auditorium_number = ?', (auditorium_number,))
        if not self.cursor.fetchone():
            return f"Аудитория {auditorium_number} не найдена."

        self.cursor.execute('DELETE FROM teacher_assignments WHERE teacher = ?', (teacher,))
        self.cursor.execute('INSERT INTO teacher_assignments (teacher, auditorium_number) VALUES (?, ?)', 
                            (teacher, auditorium_number))
        self.conn.commit()
        return f"Преподаватель {teacher} назначен в аудиторию {auditorium_number}."

    def get_auditoriums(self):
        self.cursor.execute('SELECT auditoriu   m_number FROM auditoriums')
        return [row[0] for row in self.cursor.fetchall()]

    def get_teachers(self):
        self.cursor.execute('SELECT teacher_name FROM teachers')
        return [row[0] for row in self.cursor.fetchall()]
    
def get_teacher_bookings(self, teacher_name):
    """Получение всех бронирований преподавателя"""
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('SELECT auditorium_number, time, event FROM bookings WHERE teacher = ?', (teacher_name,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def get_teacher_bookings(self, teacher_name):
    """Получение всех бронирований преподавателя"""
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('SELECT auditorium_number, time, event FROM bookings WHERE teacher = ?', (teacher_name,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def request_equipment(self, auditorium, equipment, teacher_name):
    """Запрос оборудования для аудитории"""
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO equipment_requests (auditorium_number, equipment, teacher) VALUES (?, ?, ?)', (auditorium, equipment, teacher_name))
    conn.commit()
    conn.close()
    return "Запрос на оборудование отправлен."