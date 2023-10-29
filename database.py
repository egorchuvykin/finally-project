import sqlite3

# создание базы данных и таблицы
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT, salary INTEGER)')

# функция для добавления нового сотрудника
def add_employee(name, phone, email, salary):
    cursor.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)', (name, phone, email, salary))
    conn.commit()

# функция для изменения текущего сотрудника
def update_employee(id, name, phone, email, salary):
    cursor.execute('UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?', (name, phone, email, salary, id))
    conn.commit()

# функция для удаления сотрудника
def delete_employee(id):
    cursor.execute('DELETE FROM employees WHERE id=?', (id,))
    conn.commit()

# функция для поиска сотрудника по ФИО
def search_employee(name):
    cursor.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + name + '%',))
    rows = cursor.fetchall()
    return rows

# функция для отображения всех сотрудников
def show_employees():
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    return rows

# закрытие базы данных
def close_db():
    cursor.close()
    conn.close()
