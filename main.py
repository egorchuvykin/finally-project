import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# создание базы данных и таблицы
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT, salary INTEGER)')

# функция для добавления нового сотрудника
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    if name and phone and email and salary:
        cursor.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)', (name, phone, email, salary))
        conn.commit()
        messagebox.showinfo('Success', 'Employee added successfully')
        clear_entries()
        show_employees()
    else:
        messagebox.showerror('Error', 'All fields are required')

# функция для изменения текущего сотрудника
def update_employee():
    selected = tree.selection()
    if selected:
        id = tree.item(selected)['values'][0]
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = salary_entry.get()
        if name and phone and email and salary:
            cursor.execute('UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?', (name, phone, email, salary, id))
            conn.commit()
            messagebox.showinfo('Success', 'Employee updated successfully')
            clear_entries()
            show_employees()
        else:
            messagebox.showerror('Error', 'All fields are required')
    else:
        messagebox.showerror('Error', 'Please select an employee to update')

# функция для удаления сотрудника
def delete_employee():
    selected = tree.selection()
    if selected:
        if messagebox.askyesno('Confirm', 'Are you sure you want to delete this employee?'):
            id = tree.item(selected)['values'][0]
            cursor.execute('DELETE FROM employees WHERE id=?', (id,))
            conn.commit()
            messagebox.showinfo('Success', 'Employee deleted successfully')
            show_employees()
    else:
        messagebox.showerror('Error', 'Please select an employee to delete')

# функция для поиска сотрудника по ФИО
def search_employee():
    name = search_entry.get()
    if name:
        cursor.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + name + '%',))
        rows = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert('', 'end', values=row)
    else:
        show_employees()

# функция для отображения всех сотрудников
def show_employees():
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)

# функция для очистки полей ввода
def clear_entries():
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)
    salary_entry.delete(0, END)

# создание главного окна
root = Tk()
root.title('Employee List')
root.geometry('800x500')

# создание фреймов
add_frame = Frame(root)
update_frame = Frame(root)
search_frame = Frame(root)
tree_frame = Frame(root)

# создание виджетов для добавления нового сотрудника
name_label = Label(add_frame, text='Name:')
name_entry = Entry(add_frame)
phone_label = Label(add_frame, text='Phone:')
phone_entry = Entry(add_frame)
email_label = Label(add_frame, text='Email:')
email_entry = Entry(add_frame)
salary_label = Label(add_frame, text='Salary:')
salary_entry = Entry(add_frame)
add_button = Button(add_frame, text='Add Employee', command=add_employee)

# создание виджетов для изменения текущего сотрудника
name_label2 = Label(update_frame, text='Name:')
name_entry2 = Entry(update_frame)
phone_label2 = Label(update_frame, text='Phone:')
phone_entry2 = Entry(update_frame)
email_label2 = Label(update_frame, text='Email:')
email_entry2 = Entry(update_frame)
salary_label2 = Label(update_frame, text='Salary:')
salary_entry2 = Entry(update_frame)
update_button = Button(update_frame, text='Update Employee', command=update_employee)

# создание виджетов для поиска сотрудника по ФИО
search_label = Label(search_frame, text='Search by name:')
search_entry = Entry(search_frame)
search_button = Button(search_frame, text='Search', command=search_employee)

# создание виджета для отображения списка сотрудников
tree = ttk.Treeview(tree_frame, columns=('id', 'name', 'phone', 'email', 'salary'), show='headings')
tree.heading('id', text='ID')
tree.heading('name', text='Name')
tree.heading('phone', text='Phone')
tree.heading('email', text='Email')
tree.heading('salary', text='Salary')
tree.column('id', width=50)
tree.column('name', width=150)
tree.column('phone', width=100)
tree.column('email', width=200)
tree.column('salary', width=100)
tree.bind('<ButtonRelease-1>', lambda e: select_employee())

# функция для выбора сотрудника из списка
def select_employee():
    selected = tree.selection()
    if selected:
        id = tree.item(selected)['values'][0]
        name = tree.item(selected)['values'][1]
        phone = tree.item(selected)['values'][2]
        email = tree.item(selected)['values'][3]
        salary = tree.item(selected)['values'][4]
        name_entry2.delete(0, END)
        name_entry2.insert(0, name)
        phone_entry2.delete(0, END)
        phone_entry2.insert(0, phone)
        email_entry2.delete(0, END)
        email_entry2.insert(0, email)
        salary_entry2.delete(0, END)
        salary_entry2.insert(0, salary)

# расположение виджетов на фреймах
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry.grid(row=0, column=1, padx=5, pady=5)
phone_label.grid(row=1, column=0, padx=5, pady=5)
phone_entry.grid(row=1, column=1, padx=5, pady=5)
email_label.grid(row=2, column=0, padx=5, pady=5)
email_entry.grid(row=2, column=1, padx=5, pady=5)
salary_label.grid(row=3, column=0, padx=5, pady=5)
salary_entry.grid(row=3, column=1, padx=5, pady=5)
add_button.grid(row=4, columnspan=2, padx=5, pady=5)

name_label2.grid(row=0, column=0, padx=5, pady=5)
name_entry2.grid(row=0, column=1, padx=5, pady=5)
phone_label2.grid(row=1, column=0, padx=5, pady=5)
phone_entry2.grid(row=1, column=1, padx=5, pady=5)
email_label2.grid(row=2, column=0, padx=5, pady=5)
email_entry2.grid(row=2, column=1, padx=5, pady=5)
salary_label2.grid(row=3, column=0, padx=5, pady=5)
salary_entry2.grid(row=3, column=1, padx=5, pady=5)
update_button.grid(row=4, columnspan=2, padx=5, pady=5)

search_label.grid(row=0, column=0, padx=5, pady=5)
search_entry.grid(row=0, column=1, padx=5, pady=5)
search_button.grid(row=0, column=2, padx=5, pady=5)

# расположение фреймов на главном окне
add_frame.pack(side='top', fill='both', expand=True)
update_frame.pack(side='top', fill='both', expand=True)
search_frame.pack(side='top', fill='both', expand=True)
tree_frame.pack(side='top', fill='both', expand=True)

# отображение списка сотрудников при запуске приложения
show_employees()

# запуск главного цикла
root.mainloop()

# закрытие базы данных
cursor.close()
conn.close()