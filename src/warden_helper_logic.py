#отображение кодов наказаний к длительности
penalty_duration = {
    "XX1": 5,  # 5 минут
    "XX2": 10, # 10 минут
    "XX3": 15, # 15 минут
    "XX4": 25, # 25 минут
    "XX5": "Пожизненное заключение",
    "XX6": "Высшая мера наказания"
}

articles = {
        "11X": ["Оскорбление символов власти", "Сопротивление органам власти", "Забастовка", "", "Неподчинение в ЧС", "Мятеж"],
        "12X": ["Неуважение к суду", "Сокрытие преступления", "Побег из места заключения", "Неисполнение приговора суда", "Сокрытие крупного преступления", "Побег из места пожизненного заключения"],
        "13X": ["Пропаганда запрещённых организаций", "", "Саботаж", "", "Членство в преступных группировках", "Крупный саботаж"],
        "14X": ["Неисполнение особых распоряжений", "Халатность", "", "Грубая халатность", "Самоуправство"],
        "21X": ["", "Нанесение легких телесных повреждений", "Причинение среднего вреда здоровью", "Причинение тяжкого вреда здоровью", "Причинение смерти", "Уничтожение тела"],
        "22X": ["Оскорбление, клевета", "", "Дача ложных показаний", "Незаконное ограничение свободы", "", ""],
        "31X": ["Мелкая кража", "Кража", "Грабеж", "Крупное хищение", "Разбой", "Хищение особо ценного имущества"],
        "32X": ["Порча имущества", "Порча ценного имущества", "Уничтожение имущества", "Уничтожение ценного имущества", "", "Уничтожение особо ценного имущества"],
        "41X": ["Хулиганство", "" , "Мошенничество", "", "Крупное мошенничество", "Террористический акт"],
        "42X": ["Необоснованное посещение технических помещений, космоса", "Проникновение на территорию отдела", "Проникновение в стратегическую точку", "Проникновение в защищенную стратегическую точку", "Незаконная эвакуация с территории комплекса", "Проникновение на территорию объекта NanoTrasen"],
        "43X": ["Злоупотребление экипировкой, лекарствами", "Незаконное владение опасным инструментом", "Незаконное владение регулируемым снаряжением", "Незаконное владение регулируемыми веществами", "Незаконное владение оружием", "Незаконное владение вражеским снаряжением"]
}


modifiers = {
    "организатор": 10,
    "преступление против должностного лица": 10,
    "должностное преступление": 10,
    "расизм": 10,
    "рецидив": 5,
    "преступление, совершенное по неосторожности": -5,
    "безуспешный добровольный отказ от преступления": -5,
    "явка с повинной": -5
}


# Наказания для статей, основываясь на их кодах
article_codes_to_penalties = {
    "111": "XX1",  # Оскорбление символов власти
    "112": "XX2",  # Несоблюдение законных требований
    "113": "XX3",  # Забастовка
    "115": "XX5",  # Неисполнение законных требований квалифицированного персонала
    "116": "XX6",  # Мятеж
    "121": "XX1",  # Неуважение к суду
    "122": "XX2",  # Сокрытие преступления
    "123": "XX3",  # Побег из места заключения
    "124": "XX4",  # Неисполнение приговора суда
    "125": "XX5",  # Сокрытие крупного преступления
    "126": "XX6",  # Побег из места пожизненного заключения
    "131": "XX1",  # Пропаганда запрещённых организаций
    "133": "XX3",  # Саботаж
    "135": "XX5",  # Членство в преступных группировках
    "136": "XX6",  # Крупный саботаж
    "141": "XX1",  # Неисполнение особых распоряжений
    "142": "XX2",  # Халатность
    "144": "XX4",  # Грубая халатность
    "145": "XX5",  # Самоуправство
    "212": "XX2",  # Нанесение легких телесных повреждений
    "213": "XX3",  # Причинение среднего вреда здоровью
    "214": "XX4",  # Причинение тяжкого вреда здоровью
    "215": "XX5",  # Причинение смерти
    "216": "XX6",  # Уничтожение тела
    "221": "XX1",  # Оскорбление, клевета
    "223": "XX3",  # Дача ложных показаний
    "224": "XX4",  # Незаконное ограничение свободы
    "311": "XX1",  # Мелкая кража
    "312": "XX2",  # Кража
    "313": "XX3",  # Грабеж
    "314": "XX4",  # Крупное хищение
    "315": "XX5",  # Разбой
    "316": "XX6",  # Хищение особо ценного имущества
    "321": "XX1",  # Порча имущества
    "322": "XX2",  # Порча ценного имущества
    "323": "XX3",  # Уничтожение имущества
    "324": "XX4",  # Уничтожение ценного имущества
    "326": "XX6",  # Уничтожение особо ценного имущества
    "411": "XX1",  # Хулиганство
    "413": "XX3",  # Мошенничество
    "415": "XX5",  # Крупное мошенничество
    "416": "XX6",  # Террористический акт
    "421": "XX1",  # Необоснованное посещение технических помещений
    "422": "XX2",  # Проникновение на территорию отдела
    "423": "XX3",  # Проникновение в стратегическую точку
    "424": "XX4",  # Проникновение в защищенную стратегическую точку
    "425": "XX5",  # Незаконная эвакуация с территории комплекса
    "426": "XX6",  # Проникновение на территорию объекта NanoTrasen
    "431": "XX1",  # Злоупотребление экипировкой, лекарствами
    "432": "XX2",  # Незаконное владение опасным инструментом
    "433": "XX3",  # Незаконное владение регулируемым снаряжением
    "434": "XX4",  # Незаконное владение регулируемыми веществами
    "435": "XX5",  # Незаконное владение оружием
    "436": "XX6"   # Незаконное владение вражеским снаряжением
}


# Обратное отображение от названий статей к их кодам
article_names_to_codes = {
    "Оскорбление символов власти": "111",
    "Сопротивление органам власти": "112",
    "Забастовка": "113",
    "Неподчинение в ЧС": "115",
    "Мятеж": "116",
    "Неуважение к суду": "121",
    "Сокрытие преступления": "122",
    "Побег из места заключения": "123",
    "Неисполнение приговора суда": "124",
    "Сокрытие крупного преступления": "125",
    "Побег из места пожизненного заключения": "126",
    "Пропаганда запрещённых организаций": "131",
    "Саботаж": "133",
    "Членство в преступных группировках": "135",
    "Крупный саботаж": "136",
    "Неисполнение особых распоряжений": "141",
    "Халатность": "142",
    "Грубая халатность": "144",
    "Самоуправство": "145",
    "Нанесение легких телесных повреждений": "212",
    "Причинение среднего вреда здоровью": "213",
    "Причинение тяжкого вреда здоровью": "214",
    "Причинение смерти": "215",
    "Уничтожение тела": "216",
    "Оскорбление, клевета": "221",
    "Дача ложных показаний": "223",
    "Незаконное ограничение свободы": "224",
    "Мелкая кража": "311",
    "Кража": "312",
    "Грабеж": "313",
    "Крупное хищение": "314",
    "Разбой": "315",
    "Хищение особо ценного имущества": "316",
    "Порча имущества": "321",
    "Порча ценного имущества": "322",
    "Уничтожение имущества": "323",
    "Уничтожение ценного имущества": "324",
    "Уничтожение особо ценного имущества": "326",
    "Хулиганство": "411",
    "Мошенничество": "413",
    "Крупное мошенничество": "415",
    "Террористический акт": "416",
    "Необоснованное посещение технических помещений, космоса": "421",
    "Проникновение на территорию отдела": "422",
    "Проникновение в стратегическую точку": "423",
    "Проникновение в защищенную стратегическую точку": "424",
    "Незаконная эвакуация с территории комплекса": "425",
    "Проникновение на территорию объекта NanoTrasen": "426",
    "Злоупотребление экипировкой, лекарствами": "431",
    "Незаконное владение опасным инструментом": "432",
    "Незаконное владение регулируемым снаряжением": "433",
    "Незаконное владение регулируемыми веществами": "434",
    "Незаконное владение оружием": "435",
    "Незаконное владение вражеским снаряжением": "436"
}

# Структура данных: разделы -> главы -> статьи (1-6)
sections = {
    1: {
        1: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"},
        2: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"},
        3: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"},
        4: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"}
    },
    2: {
        1: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"},
        2: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"},
    },
    3: {
        1: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"},
        2: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"}
    },
    4: {
        1: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"},
        2: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"},
        3: {1: 5, 2: 10, 3: 15, 4: 25, 5: "пожизненное заключение", 6: "высшая мера"},
    }
}



# Функция для разделения строки на раздел, главу и статью
def parse_violation(violation_str):
    try:
        # Проверяем, чтобы строка состояла не более чем из трех символов
        if len(violation_str) > 3:
            return None
        section = int(violation_str[0])  # Первый символ - раздел
        chapter = int(violation_str[1])  # Второй символ - глава
        article = int(violation_str[2])  # Третий символ - статья
        return section, chapter, article
    except (IndexError, ValueError):
        return None


# Функция для расчета наказания по статьям
def calculate_penalties(violations, selected_modifiers):
    chapter_violations = {}
    has_capital_punishment = False
    has_life_sentence = False
    total_modifiers = 0

    for violation_str in violations:
        result = parse_violation(violation_str)
        if result:
            section, chapter, article = result
            if section in sections and chapter in sections[section] and article in sections[section][chapter]:
                penalty = sections[section][chapter][article]
                if penalty == "высшая мера":
                    has_capital_punishment = True
                elif penalty == "пожизненное заключение":
                    has_life_sentence = True
                else:
                    if (section, chapter) not in chapter_violations:
                        chapter_violations[(section, chapter)] = []
                    chapter_violations[(section, chapter)].append(penalty)
    
    if has_capital_punishment:
        return "Высшая мера"
    if has_life_sentence:
        return "Пожизненное заключение"
    
    total_penalty = 0
    for chapter, penalties in chapter_violations.items():
        total_penalty += max(penalties)
    
    # Применяем модификаторы
    for modifier in selected_modifiers:
        if modifier in modifiers:
            total_modifiers += modifiers[modifier]

    # Применяем модификаторы
    total_penalty += total_modifiers

    # Убедимся, что итоговое время не может быть отрицательным
    if total_penalty < 0:
        total_penalty = 0

    if total_penalty >= 75:
        return f"пожизненное заключение"
    else:
        return f"{total_penalty} минут"
