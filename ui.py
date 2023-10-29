import tkinter as tk
from tkinter import ttk
import database

class EmployeeListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список сотрудников компании")

        # создание виджета Treeview для отображения списка сотрудников
        self.tree = ttk.Treeview(self.root, columns=('id', 'name', 'phone', 'email', 'salary'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Email')
        self.tree.heading('salary', text='Зарплата')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # создание кнопок для управления списком сотрудников
        add_button = tk.Button(self.root, text='Добавить', command=self.add_employee)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = tk.Button(self.root, text='Изменить', command=self.update_employee)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self.root, text='Удалить', command=self.delete_employee)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        search_button = tk.Button(self.root, text='Поиск', command=self.search_employee)
        search_button.pack(side=tk.LEFT, padx=5, pady=5)

        refresh_button = tk.Button(self.root, text='Обновить', command=self.show_employees)
        refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        # отображение списка сотрудников при запуске приложения
        self.show_employees()

    def add_employee(self):
        # создание диалогового окна для добавления нового сотрудника
        add_window = tk.Toplevel(self.root)
        add_window.title('Добавление сотрудника')

        name_label = tk.Label(add_window, text='ФИО')
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        phone_label = tk.Label(add_window, text='Телефон')
        phone_label.grid(row=1, column=0, padx=5, pady=5)

        phone_entry = tk.Entry(add_window)
        phone_entry.grid(row=1, column=1, padx=5, pady=5)

        email_label = tk.Label(add_window, text='Email')
        email_label.grid(row=2, column=0, padx=5, pady=5)

        email_entry = tk.Entry(add_window)
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        salary_label = tk.Label(add_window, text='Зарплата')
        salary_label.grid(row=3, column=0, padx=5, pady=5)

        salary_entry = tk.Entry(add_window)
        salary_entry.grid(row=3, column=1, padx=5, pady=5)

        # создание кнопки для добавления нового сотрудника в БД
        add_button = tk.Button(add_window, text='Добавить', command=lambda: self.add_employee_db(name_entry.get(), phone_entry.get(), email_entry.get(), salary_entry.get()))
        add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def add_employee_db(self, name, phone, email, salary):
        # вызов функции для добавления нового сотрудника в БД
        database.add_employee(name, phone, email, salary)

        # обновление списка сотрудников
        self.show_employees()

    def update_employee(self):
        # получение выделенной строки в списке сотрудников
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item)['values']

        # создание диалогового окна для изменения текущего сотрудника
        update_window = tk.Toplevel(self.root)
        update_window.title('Изменение сотрудника')

        name_label = tk.Label(update_window, text='ФИО')
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = tk.Entry(update_window)
        name_entry.insert(0, item_values[1])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        phone_label = tk.Label(update_window, text='Телефон')
        phone_label.grid(row=1, column=0, padx=5, pady=5)

        phone_entry = tk.Entry(update_window)
        phone_entry.insert(0, item_values[2])
        phone_entry.grid(row=1, column=1, padx=5, pady=5)

        email_label = tk.Label(update_window, text='Email')
        email_label.grid(row=2, column=0, padx=5, pady=5)

        email_entry = tk.Entry(update_window)
        email_entry.insert(0, item_values[3])
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        salary_label = tk.Label(update_window, text='Зарплата')
        salary_label.grid(row=3, column=0, padx=5, pady=5)

        salary_entry = tk.Entry(update_window)
        salary_entry.insert(0, item_values[4])
        salary_entry.grid(row=3, column=1, padx=5, pady=5)

        # создание кнопки для изменения текущего сотрудника в БД
        update_button = tk.Button(update_window, text='Изменить', command=lambda: self.update_employee_db(item_values[0], name_entry.get(), phone_entry.get(), email_entry.get(), salary_entry.get()))
        update_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def update_employee_db(self, id, name, phone, email, salary):
        # вызов функции для изменения текущего сотрудника в БД
        database.update_employee(id, name, phone, email, salary)

        # обновление списка сотрудников
        self.show_employees()

    def delete_employee(self):
        # получение выделенной строки в списке сотрудников
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item)['values']

        # создание диалогового окна для подтверждения удаления сотрудника
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title('Подтверждение удаления')

        confirm_label = tk.Label(confirm_window, text=f'Вы действительно хотите удалить сотрудника "{item_values[1]}"?')
        confirm_label.pack(padx=5, pady=5)

        # создание кнопки для удаления сотрудника из БД
        delete_button = tk.Button(confirm_window, text='Удалить', command=lambda: self.delete_employee_db(item_values[0]))
        delete_button.pack(padx=5, pady=5)

    def delete_employee_db(self, id):
        # вызов функции для удаления сотрудника из БД
        database.delete_employee(id)

        # обновление списка сотрудников
        self.show_employees()

    def search_employee(self):
        # создание диалогового окна для поиска сотрудника по ФИО
        search_window = tk.Toplevel(self.root)
        search_window.title('Поиск сотрудника')

        search_label = tk.Label(search_window, text='Введите ФИО сотрудника:')
        search_label.pack(padx=5, pady=5)

        search_entry = tk.Entry(search_window)
        search_entry.pack(padx=5, pady=5)

        # создание кнопки для поиска сотрудника в БД
        search_button = tk.Button(search_window, text='Найти', command=lambda: self.search_employee_db(search_entry.get()))
        search_button.pack(padx=5, pady=5)

    def search_employee_db(self, name):
        # вызов функции для поиска сотрудника в БД
        rows = database.search_employee(name)

        # очистка списка сотрудников
        for item in self.tree.get_children():
            self.tree.delete(item)

        # отображение найденных сотрудников в списке
        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def show_employees(self):
        # вызов функции для отображения всех сотрудников в БД
        rows = database.show_employees()

        # очистка списка сотрудников
        for item in self.tree.get_children():
            self.tree.delete(item)

        # отображение всех сотрудников в списке
        for row in rows:
            self.tree.insert('', tk.END, values=row)

if __name__ == '__main__':
    root = tk.Tk()
    app = EmployeeListApp(root)
    root.mainloop()