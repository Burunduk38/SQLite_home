import os
import sqlite3
class University:
    def __init__(self, name, database_folder=None):
        if database_folder:
            self.database_path = os.path.join(database_folder, 'students.db')
        else:
            self.database_path = 'students.db'

        self.conn = sqlite3.connect(self.database_path)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL CHECK(length(name) > 0),  -- Поле name должно быть непустым
                            age INTEGER NOT NULL CHECK(age >= 0)  -- Поле grade не должно быть пустым
                            )''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS grades (
                            id INTEGER PRIMARY KEY,
                            student_id INTEGER,
                            subject TEXT NOT NULL CHECK(length(subject) > 0),  -- Поле subject должно быть непустым
                            grade REAL NOT NULL CHECK(grade >= 0),  -- Поле grade не должно быть пустым и должно быть неотрицательным
                            FOREIGN KEY (student_id) REFERENCES students(id)
                            )''')
        self.conn.commit()

    def add_student(self, name, age):
        self.cur.execute('''INSERT INTO students (name, age) VALUES (?, ?)''', (name, age))
        self.conn.commit()

    def add_grade(self, student_id, subject, grade):
        self.cur.execute('''INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)''',
                         (student_id, subject, grade))
        self.conn.commit()

    def get_students(self, subject=None):
        if subject:
            self.cur.execute('''SELECT students.id, students.name, students.age, grades.subject, grades.grade 
                            FROM students 
                            JOIN grades ON students.id = grades.student_id 
                            WHERE grades.subject = ?''', (subject,))
        else:
            self.cur.execute('''SELECT students.id, students.name, students.age, grades.subject, grades.grade 
                            FROM students 
                            JOIN grades ON students.id = grades.student_id''')

        return self.cur.fetchall()

# Пример использования
u1 = University('Университет Urban', r'D:\ISZF\py_projects\SQLite_home' )

# u1.add_student('Ivan', 26) # id - 1
# u1.add_student('Ilya', 24) # id - 2

u1.add_grade(1, 'Python', 4.8)
u1.add_grade(2, 'PHP', 4.3)

print(u1.get_students())
print(u1.get_students('Python'))

rows1 = u1.get_students()
rows2 = u1.get_students('Python')

for row in rows1:
    id = row['id']
    name = row['name']
    age = row['age']
    subject = row['subject']
    grade = row['grade']
    print(f"Id: {id}, Name: {name}, Age: {age}, Subject: {subject}, Grade: {grade}")


