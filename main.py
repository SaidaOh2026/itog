import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Глобальные переменные
expenses = []  # Список всех расходов
tree = None    # Таблица для отображения расходов

def load_data():
    """Загружает расходы из файла expenses.json."""
    global expenses
    try:
        with open("expenses.json", "r", encoding="utf-8") as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = []

def save_data():
    """Сохраняет расходы в файл expenses.json с обработкой ошибок."""
    try:
        with open("expenses.json", "w", encoding="utf-8") as f:
            json.dump(expenses, f, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")

def update_tree(filtered=None):
    """Обновляет таблицу расходов. Если передан filtered — отображает только отфильтрованные."""
    for i in tree.get_children():
        tree.delete(i)
    data = filtered if filtered is not None else expenses
    for e in data:
        # Форматируем сумму с запятой и двумя знаками после запятой
        formatted_amount = f"{e['amount']:.2f}".replace('.', ',')
        tree.insert("", "end", values=(formatted_amount, e["category"], e["date"]))

def add_expense():
    """Добавляет новый расход после проверки введённых данных."""
    amount = amount_entry.get().strip().replace(',', '.')
    category = category_entry.get().strip()
    date = date_entry.get().strip()

    # Проверка суммы: допускаем запятую и точку, убираем пробелы
    if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
        messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
        return

    # Проверка даты
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Дата в формате ГГГГ-ММ-ДД")
        return

    expense = {"amount": float(amount), "category": category, "date": date}
    expenses.append(expense)
    update_tree()
    save_data()

    # Обновляем список категорий в фильтре
    update_categories()

def filter_expenses():
    """Фильтрует расходы по выбранной категории."""
    cat = filter_category.get()
    filtered = expenses if cat == "Все" else [e for e in expenses if e["category"] == cat]
    update_tree(filtered)

def sum_period():
    """Считает сумму расходов за выбранный период."""
    date_from = date_from_entry.get().strip()
    date_to = date_to_entry.get().strip()
    try:
        d_from = datetime.strptime(date_from, "%Y-%m-%d")
        d_to = datetime.strptime(date_to, "%Y-%m-%d")
        total = sum(e["amount"] for e in expenses if d_from <= datetime.strptime(e["date"], "%Y-%m-%d") <= d_to)
        messagebox.showinfo("Сумма", f"Сумма за период: {total:.2f}".replace('.', ','))
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте формат дат (ГГГГ-ММ-ДД)")

def update_categories():
    """Обновляет список категорий в Combobox после добавления нового расхода."""
    categories = ["Все"] + sorted(list(set([e["category"] for e in expenses])))
    filter_category['values'] = categories
    filter_category.set("Все")

# --- Создание окна ---
root = tk.Tk()
root.title("Expense Tracker")
load_data()

# --- Поля ввода ---
ttk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
amount_entry = ttk.Entry(root)
amount_entry.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
category_entry = ttk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)
ttk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5)
date_entry = ttk.Entry(root)
date_entry.grid(row=2, column=1, padx=5, pady=5)

# --- Кнопка ---
ttk.Button(root, text="Добавить расход", command=add_expense).grid(row=3, column=0, columnspan=2, pady=10)

# --- Таблица ---
tree = ttk.Treeview(root, columns=("amount", "category", "date"), show='headings')
tree.heading("amount", text="Сумма")
tree.heading("category", text="Категория")
tree.heading("date", text="Дата")
tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
update_tree()

# --- Фильтр ---
ttk.Label(root, text="Фильтр по категории:").grid(row=5, column=0, padx=5, pady=5)
filter_category = ttk.Combobox(root)
update_categories()  # Инициализация списка категорий
filter_category.grid(row=5, column=1, padx=5, pady=5)
ttk.Button(root, text="Фильтровать", command=filter_expenses).grid(row=6, column=0, columnspan=2, pady=5)

# --- Сумма за период ---
ttk.Label(root, text="Период (с - по):").grid(row=7, column=0, padx=5, pady=5)
date_from_entry = ttk.Entry(root)
date_from_entry.grid(row=7, column=1, padx=5, pady=5)
date_to_entry = ttk.Entry(root)
date_to_entry.grid(row=8, column=1, padx=5, pady=5)
ttk.Button(root, text="Сумма за период", command=sum_period).grid(row=9, column=0, columnspan=2, pady=10)

root.mainloop()