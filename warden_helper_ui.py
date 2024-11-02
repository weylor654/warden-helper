import tkinter as tk
from warden_helper_logic import article_names_to_codes, article_codes_to_penalties, articles, modifiers, penalty_duration

# Глобальные переменные для хранения состояния
modifier_labels = {}  # Словарь с метками модификаторов
selected_cells = []  # Список выбранных ячеек
modifier_selected = set()  # Множество выбранных модификаторов


def get_modifier_value(modifier_name):

    return modifiers.get(modifier_name, 0)  # Возвращает значение модификатора или 0, если не найден

# Функция для получения кода статьи по названию
def get_article_code_by_name(name):
    return article_names_to_codes.get(name, "Неизвестный код")

# Преобразование наказания в минуты
def penalty_to_minutes(penalty_code):
    if penalty_code in penalty_duration:
        duration = penalty_duration[penalty_code]
        if isinstance(duration, int):
            return duration
        else:
            return None
    return 0

# Функция для расчета наказаний
def calculate_penalties(article_codes):
    total_minutes = 0
    has_life_sentence = False
    has_death_penalty = False
    verdict = []

    if not article_codes:
        return "Выберите хотя бы одну статью"

    for code in article_codes:
        penalty_code = article_codes_to_penalties.get(code, "Неизвестный код")
        print(f"Код статьи: {code}, Код наказания: {penalty_code}")  # Отладочная информация
        
        if penalty_code == "XX5":
            has_life_sentence = True
        elif penalty_code == "XX6":
            has_death_penalty = True
        else:
            minutes = penalty_to_minutes(penalty_code)
            print(f"Минуты наказания: {minutes}")  # Отладочная информация
            
            if minutes is not None:
                total_minutes += minutes

    # Применение модификаторов только если есть выбранные статьи
    if article_codes:
        for mod in modifier_selected:
            mod_value = get_modifier_value(mod)
            total_minutes += mod_value

    # Определение вердикта
    if has_death_penalty:
        verdict.append("Высшая мера наказания")
    elif has_life_sentence or total_minutes >= 75:
        verdict.append("Пожизненное заключение")
    elif total_minutes > 0:
        verdict.append(f"{total_minutes} минут тюремного заключения")

    return ', '.join(verdict)

def update_verdict_field(verdict_label):
    selected_articles = [label.cget('text') for label in selected_cells]
    print(f"Выбранные статьи: {selected_articles}")  # Отладочная информация
    article_codes = [get_article_code_by_name(article) for article in selected_articles]
    print(f"Коды статей: {article_codes}")  # Отладочная информация
    verdict = calculate_penalties(article_codes)
    verdict_label.config(text="Вердикт: " + verdict)

def on_modifier_click(modifier_name):
    button = modifier_labels[modifier_name]
    current_color = button.cget('bg')
    if current_color == '#272727':  # Если модификатор не выбран
        button.config(bg='#509ee3')  # Выбрать модификатор
        modifier_selected.add(modifier_name)
    else:
        button.config(bg='#272727')  # Убрать выбор модификатора
        modifier_selected.remove(modifier_name)
    update_verdict_field(verdict_label)

def lighten_color(hex_color, percent):
    """Осветляет цвет на заданный процент."""
    rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(min(int(c + (255 - c) * percent), 255) for c in rgb)

def darken_color(hex_color, percent):
    """Темняет цвет на заданный процент."""
    rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(max(int(c * (1 - percent)), 0) for c in rgb)

def toggle_selection(label, selected_cells, chapter, chapter_selections, original_bg_color, hover_color, selected_bg_color, verdict_label):
    """Переключает выделение ячейки при клике с учётом главы и обновляет вердикт."""
    if label.is_empty:
        return  # Не изменяем состояние для пустых ячеек

    if label in selected_cells:
        selected_cells.remove(label)
        chapter_selections[chapter] = None
        label.config(highlightbackground=original_bg_color, bg=original_bg_color)
    else:
        if chapter_selections[chapter]:
            previous_label = chapter_selections[chapter]
            selected_cells.remove(previous_label)
            previous_label.config(highlightbackground=previous_label.original_bg_color, bg=previous_label.original_bg_color)
        selected_cells.append(label)
        chapter_selections[chapter] = label
        label.config(highlightbackground="#00BFFF", bg=selected_bg_color)

    # Обновляем вердикт после изменения выбора
    update_verdict_field(verdict_label)

def on_enter(label, selected_cells, hover_color, selected_bg_color):
    """Меняет цвет при наведении курсора, если ячейка не выбрана."""
    if label not in selected_cells:
        label.config(bg=hover_color)
    else:
        label.config(bg=selected_bg_color)

def on_leave(label, selected_cells, original_bg_color, selected_bg_color):
    """Возвращает цвет после ухода курсора, если ячейка не выбрана."""
    if label not in selected_cells:
        label.config(bg=original_bg_color)
    else:
        label.config(bg=selected_bg_color)
        
def create_colored_label(frame, text, bg_color, row, column, selected_cells, chapter, chapter_selections):
    original_bg_color = bg_color
    if bg_color == "#000000":
        hover_color = lighten_color(bg_color, 0.1)
        selected_bg_color = lighten_color(bg_color, 0.3)
    else:
        hover_color = darken_color(bg_color, 0.2)
        selected_bg_color = darken_color(bg_color, 0.3)
    
    label = tk.Label(frame, text=text, bg=bg_color, fg="#EFEBD8", padx=5, pady=5,
                    width=25, height=3, anchor="center", wraplength=150, justify="center",
                    borderwidth=0, relief="flat", highlightthickness=2, highlightbackground=bg_color,
                    font=("Verdana", 9, "bold italic"))  # Жирный и курсивный шрифт
    label.grid(row=row, column=column, sticky="nsew")
    
    label.original_bg_color = bg_color
    label.is_empty = not text.strip()  # Устанавливаем флаг для пустых ячеек
    
    if not label.is_empty:
        label.bind("<Enter>", lambda e: on_enter(label, selected_cells, hover_color, selected_bg_color))
        label.bind("<Leave>", lambda e: on_leave(label, selected_cells, original_bg_color, selected_bg_color))
        label.bind("<Button-1>", lambda e: toggle_selection(label, selected_cells, chapter, chapter_selections, original_bg_color, hover_color, selected_bg_color, verdict_label))

    return label


def on_modifier_enter(label, modifier_selected, hover_color):
    """Меняет цвет при наведении курсора на модификатор."""
    if label not in modifier_selected:
        label.config(bg=darken_color(label.original_bg_color, 0.1))

def on_modifier_leave(label, modifier_selected, original_bg_color):
    """Возвращает цвет после ухода курсора с модификатора."""
    if label not in modifier_selected:
        label.config(bg=original_bg_color)

def toggle_modifier_info(mod_name):
    """Переключает выделение модификатора.""" 
    label = modifier_labels[mod_name]
    if mod_name in modifier_selected:
        modifier_selected.remove(mod_name)
        label.config(bg="#444444", fg="#EFEBD8", highlightbackground="#444444")
    else:
        modifier_selected.add(mod_name)
        label.config(bg="#444444", fg="#EFEBD8", highlightbackground="#00BFFF")
    update_verdict_field(verdict_label)

def create_colored_modifier_label(frame, mod_name, bg_color, row, column, modifier_selected):
    label = tk.Label(frame, text=mod_name, bg=bg_color, fg="#EFEBD8", padx=5, pady=10,
                    width=20, height=2, anchor="center", wraplength=150, justify="center",
                    borderwidth=0, relief="flat", highlightthickness=2, highlightbackground=bg_color,
                    font=("Verdana", 10, "bold"))

    label.grid(row=row, column=column, sticky="nsew")
    
    label.original_bg_color = bg_color
    
    # Обработка событий для модификаторов
    label.bind("<Enter>", lambda e: on_modifier_enter(label, modifier_selected, darken_color(bg_color, 0.1)))
    label.bind("<Leave>", lambda e: on_modifier_leave(label, modifier_selected, bg_color))
    label.bind("<Button-1>", lambda e, mod_name=mod_name: toggle_modifier_info(mod_name))
    
    return label

def run_table_version():
    global modifier_selected, modifier_labels, selected_cells, verdict_label

    root = tk.Tk()
    root.title("Warden Helper")
    root.config(bg='#1B1B1F')

    colors = {
        "XX1": "#0F4F27",
        "XX2": "#414700",
        "XX3": "#5f3800",
        "XX4": "#611300",
        "XX5": "#57000C",
        "XX6": "#000000"
    }
      
    # Настраиваем главный фрейм для таблиц статей и модификаторов
    main_frame = tk.Frame(root, bg='#1B1B1F')
    main_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nsew")  # Убираем отступы снизу

    # Настройка сетки для масштабирования
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Фрейм для таблицы статей
    article_frame = tk.Frame(main_frame, bg='#1B1B1F')
    article_frame.grid(row=0, column=0, sticky="nsew")  # Полное заполнение фрейма

    # Заголовки для таблицы статей
    columns = ["XX1", "XX2", "XX3", "XX4", "XX5", "XX6"]
    chapters = ["11X", "12X", "13X", "14X", "21X", "22X", "31X", "32X", "41X", "42X", "43X"]

    selected_cells = []
    chapter_selections = {chapter: None for chapter in chapters}

    # Устанавливаем фиксированную ширину для столбца "Глава"
    article_frame.grid_columnconfigure(0, minsize=100)  # Фиксированная ширина для первого столбца

    # Настройка гибкости остальных колонок
    for i in range(1, len(columns) + 1):
        article_frame.grid_columnconfigure(i, weight=1, minsize=80)  # Остальные столбцы растягиваются, но с минимальной шириной

    # Заголовки столбцов
    for i, col in enumerate(columns):
        label = tk.Label(article_frame, text=col, bg=colors[col], fg="white", padx=5, pady=5,
                         anchor="center", wraplength=150, justify="center",
                         font=("Verdana", 10, "bold"))  # Жирный шрифт
        label.grid(row=0, column=i+1, sticky="nsew")
        
    # Ячейка "Раздел" над 11X с жирным шрифтом
    label = tk.Label(article_frame, text="Глава", bg="#333", fg="white", padx=5, pady=5,
                    anchor="center", wraplength=150, justify="center",
                    font=("Verdana", 10, "bold"))  # Жирный шрифт
    label.grid(row=0, column=0, sticky="nsew")

    # Заголовки строк
    for i, chapter in enumerate(chapters):
        label = tk.Label(article_frame, text=chapter, padx=5, pady=5, bg="#333", fg="white",
                         anchor="center", wraplength=150, justify="center",
                         font=("Verdana", 10, "bold"))  # Жирный шрифт
        label.grid(row=i+2, column=0, sticky="nsew")

    # Заполнение таблицы
    for i, chapter in enumerate(chapters):
        for j, col in enumerate(columns):
            if chapter in articles:
                if len(articles[chapter]) > j:
                    article = articles[chapter][j]
                    is_active = True
                else:
                    article = ""
                    is_active = False
            else:
                article = ""
                is_active = False

            label = create_colored_label(article_frame, article, colors[col], i+2, j+1, selected_cells, chapter, chapter_selections)
            label.is_active = is_active

    # Создание фрейма для модификаторов
    modifier_frame = tk.Frame(main_frame, bg='#1B1B1F')
    modifier_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 0))  # Без отступов между фреймами

    modifier_frame.grid_rowconfigure(0, weight=1)
    modifier_frame.grid_columnconfigure(tuple(range(len(modifiers))), weight=1)

    # Инициализация списка для хранения выбранных модификаторов и меток
    modifier_selected = set()
    modifier_labels = {}

    # Добавление меток модификаторов
    for i, (mod_name, _) in enumerate(modifiers.items()):
        label = create_colored_modifier_label(modifier_frame, mod_name, "#444444", 0, i, modifier_selected)
        label.config(height=3)  # Увеличение высоты ячейки
        modifier_labels[mod_name] = label

    # Добавление надписи "Вердикт" и красной линии
    verdict_label = tk.Label(root, text="Вердикт:", bg='#1B1B1F', fg='#d0d0d0', font=('Verdana', 18))
    verdict_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

    verdict_frame = tk.Frame(root, bg='#1B1B1F')
    verdict_frame.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="nsew")

    verdict_line = tk.Canvas(verdict_frame, height=2, bg='red', bd=0, highlightthickness=0)
    verdict_line.pack(fill='x')

    # Запуск главного цикла
    root.mainloop()
