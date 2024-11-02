import tkinter as tk
from tkinter import ttk
from warden_helper_logic import calculate_penalties

# Список доступных модификаторов
MODIFIER_OPTIONS = [
    "организатор", 
    "преступление против должностного лица", 
    "должностное преступление", 
    "расизм", 
    "рецидив", 
    "преступление, совершенное по неосторожности", 
    "безуспешный добровольный отказ от преступления", 
    "явка с повинной"
]

def run_abridged_version():
    # Функция для расчета времени заключения
    def _calculate_verdict():
        article_input = article_entry.get().strip()
        modifier_input = modifier_entry.get().strip().lower()
        articles = [item.strip() for item in article_input.split()]
        modifiers = [item.strip() for item in modifier_input.split(';')]
        verdict = calculate_penalties(articles, modifiers)
        verdict_label.config(text=f"Вердикт: {verdict}")

    def calculate_verdict():
        root.after(1, _calculate_verdict)

    # Обработчик добавления выбранного модификатора в поле ввода
    def add_modifier(event=None):
        selected_modifier = modifier_autocomplete.get()
        if selected_modifier and selected_modifier not in modifier_entry.get().lower():
            current_text = modifier_entry.get().strip()
            if current_text:
                modifier_entry.insert(tk.END, f"; {selected_modifier}")
            else:
                modifier_entry.insert(tk.END, f"{selected_modifier}")
        modifier_autocomplete.set('Список статей')
        modifier_entry.focus()  # Убираем фокус с дропбокса, переводим на поле ввода модификаторов

    # Основное окно
    root = tk.Tk()
    root.title("Warden Helper")
    root.config(bg='#1B1B1F')

    # Создаем стиль для ttk
    style = ttk.Style()
    style.theme_use('default')

    # Изменяем параметры выбора для дропбокса
    root.option_add('*TCombobox*Listbox.selectBackground', '#272727') # Цвет фона выбранного элемента
    root.option_add('*TCombobox*Listbox.selectForeground', 'white')    # Цвет текста выбранного элемента

    # Основной фрейм
    main_frame = tk.Frame(root, bg='#1B1B1F')
    main_frame.pack(padx=10, pady=10, fill='both', expand=True)

    # Метка и поле ввода для статей
    article_label = tk.Label(main_frame, text="Статьи (через пробел):", bg='#1B1B1F', fg='white', font=('Arial', 12))
    article_label.pack(pady=(10, 5), anchor='w')

    article_entry = tk.Entry(main_frame, bg='#333', fg='white', font=('Arial', 12), bd=0, insertbackground='white')
    article_entry.pack(pady=(0, 10), fill='x')

    # Метка и поле ввода для модификаторов
    modifier_label = tk.Label(main_frame, text="Модификаторы (выберите и добавьте):", bg='#1B1B1F', fg='white', font=('Arial', 12))
    modifier_label.pack(pady=(10, 5), anchor='w')

    # Поле для ввода модификаторов
    modifier_entry = tk.Entry(main_frame, bg='#333', fg='white', font=('Arial', 12), bd=0, insertbackground='white')
    modifier_entry.pack(pady=(0, 10), fill='x')

    # Поле для автозаполнения модификаторов
    modifier_autocomplete = ttk.Combobox(main_frame, values=MODIFIER_OPTIONS, font=('Arial', 12), state='readonly', style="TCombobox")
    modifier_autocomplete.set("Список модификаторов")  # Текст по умолчанию
    modifier_autocomplete.pack(fill='x')
    modifier_autocomplete.bind("<<ComboboxSelected>>", add_modifier)

    # Кнопка для расчета вердикта
    calc_button = tk.Button(main_frame, text="Рассчитать время", bg="#272727", fg="#B3B3B3", bd=0, relief="flat",
                           activebackground="#5193CC", activeforeground="black", font=('Arial', 12),
                           highlightthickness=0)
    calc_button.pack(pady=20, ipadx=5, ipady=5)

    # Метка для отображения вердикта
    verdict_label = tk.Label(main_frame, text="Вердикт:", bg="#1B1B1F", fg="white", padx=10, pady=10, font=('Arial', 12))
    verdict_label.pack()

    # Красная полоса под вердиктом
    verdict_separator = tk.Canvas(main_frame, height=2, bg='#FF0000', highlightthickness=0)
    verdict_separator.pack(fill='x', pady=(10, 0))

    # Функция для подсветки кнопки при наведении курсора
    def on_enter(e):
        calc_button.config(bg="#509ee3", fg="white")

    # Функция для возвращения кнопки в исходное состояние
    def on_leave(e):
        calc_button.config(bg="#272727", fg="#B3B3B3")

    # Связываем события с кнопкой
    calc_button.bind("<Enter>", on_enter)
    calc_button.bind("<Leave>", on_leave)

    # Обрабатываем нажатие на кнопку
    calc_button.config(command=calculate_verdict)

    root.mainloop()
