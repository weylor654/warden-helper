import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGridLayout, QFrame
from PyQt5.QtCore import Qt

# Импортируем данные и функции
from warden_helper_logic import article_names_to_codes, article_codes_to_penalties, articles, modifiers, penalty_duration

class WardenHelper(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.setWindowTitle("Warden Helper")
        self.setStyleSheet("background-color: #1B1B1F; color: #EFEBD8;")
        self.setGeometry(100, 100, 1000, 900)  # Устанавливаем размер окна
        self.selected_cells = {}  # Словарь для хранения выбранных статей по главам
        self.modifier_selected = set()
        self.modifier_labels = {}

        # Главный контейнер
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(0)  # Убираем промежутки между элементами
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы по краям

        # Создаем фрейм для таблиц и добавляем его в макет
        tables_frame = QFrame()
        tables_layout = QGridLayout(tables_frame)
        tables_layout.setSpacing(0)  # Убираем промежутки между ячейками
        tables_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы по краям
        main_layout.addWidget(tables_frame)

        # Создаем таблицу статей
        self.create_article_frame(tables_layout)

        # Создаем таблицу модификаторов
        self.create_modifier_frame(tables_layout)

        # Добавляем поле для вердикта
        self.verdict_label = QLabel("Вердикт:", self)
        self.verdict_label.setStyleSheet("font: 18pt 'Verdana'; color: #d0d0d0;")
        self.verdict_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.verdict_label)

    def create_article_frame(self, layout):
        # Настройка таблицы статей
        columns = ["XX1", "XX2", "XX3", "XX4", "XX5", "XX6"]
        chapters = ["11X", "12X", "13X", "14X", "21X", "22X", "31X", "32X", "41X", "42X", "43X"]
        colors = {
            "XX1": "#0F4F27", "XX2": "#414700", "XX3": "#5f3800",
            "XX4": "#611300", "XX5": "#57000C", "XX6": "#000000"
        }

        # Заголовок для строки "Глава"
        chapter_label = QLabel("Г", self)  # Сокращаем заголовок для уменьшения ширины
        chapter_label.setStyleSheet("background-color: #333; color: white; font: bold 10pt 'Verdana';")
        chapter_label.setAlignment(Qt.AlignCenter)
        chapter_label.setFixedSize(40, 50)  # Делаем первый столбец минимальным
        layout.addWidget(chapter_label, 0, 0)

        # Создаем заголовки столбцов
        for i, col in enumerate(columns):
            label = QLabel(col, self)
            label.setStyleSheet(f"background-color: {colors[col]}; color: white; font: bold 10pt 'Verdana';")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(150, 50)  # Делаем заголовки больше
            layout.addWidget(label, 0, i + 1)

        # Создаем ячейки статей
        for i, chapter in enumerate(chapters):
            chapter_label = QLabel(chapter, self)
            chapter_label.setStyleSheet("background-color: #333; color: white; font: bold 10pt 'Verdana';")
            chapter_label.setAlignment(Qt.AlignCenter)
            chapter_label.setFixedSize(40, 80)  # Делаем ячейки для глав маленькими по ширине
            layout.addWidget(chapter_label, i + 1, 0)

            for j, col in enumerate(columns):
                article = articles.get(chapter, [""])[j] if j < len(articles.get(chapter, [])) else ""
                label = QLabel(article, self)
                label.setAlignment(Qt.AlignCenter)
                label.setFrameShape(QFrame.NoFrame)  # Убираем рамки ячеек
                label.setFixedSize(150, 80)  # Делаем ячейки для статей больше
                label.setWordWrap(True)  # Включаем перенос текста

                # Устанавливаем базовый стиль с цветом столбца
                label.setStyleSheet(f"background-color: {colors[col]}; color: #EFEBD8; font: 9pt 'Verdana';")
                label.original_color = colors[col]  # Сохраняем исходный цвет

                if article:  # Если в ячейке есть текст, делаем её кликабельной и добавляем события
                    label.mousePressEvent = lambda event, lbl=label, ch=chapter: self.toggle_selection(lbl, ch)
                    label.enterEvent = lambda event, lbl=label: self.on_hover_enter(lbl)
                    label.leaveEvent = lambda event, lbl=label: self.on_hover_leave(lbl)

                layout.addWidget(label, i + 1, j + 1)

    def create_modifier_frame(self, layout):
        # Создаем строку с модификаторами, которая начинается под "Глава" и заканчивается под "XX6"
        modifier_frame = QFrame()
        modifier_layout = QGridLayout(modifier_frame)
        modifier_layout.setSpacing(0)  # Убираем промежутки между кнопками
        modifier_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы по краям
        layout.addWidget(modifier_frame, len(articles) + 1, 0, 1, 7)  # Устанавливаем модификаторы на всю ширину таблицы

        # Добавляем метки модификаторов
        for i, (mod_name, _) in enumerate(modifiers.items()):
            button = QPushButton(mod_name, self)
            button.setStyleSheet("background-color: #444444; color: #EFEBD8; font: bold 10pt 'Verdana';")
            button.setFixedSize(150, 80)  # Увеличиваем высоту кнопок модификаторов
            modifier_layout.addWidget(button, 0, i)  # Располагаем кнопки в строку
            button.clicked.connect(lambda checked, name=mod_name: self.on_modifier_click(name))
            self.modifier_labels[mod_name] = button

    def on_hover_enter(self, label):
        # Если ячейка не выбрана, затемняем цвет при наведении
        if label not in self.selected_cells.values():
            darker_color = self.darken_color(label.original_color, 0.2)
            label.setStyleSheet(f"background-color: {darker_color}; color: #EFEBD8; font: 9pt 'Verdana';")

    def on_hover_leave(self, label):
        # Возвращаем цвет, если ячейка не выбрана, иначе оставляем стиль выбранной ячейки
        if label not in self.selected_cells.values():
            label.setStyleSheet(f"background-color: {label.original_color}; color: #EFEBD8; font: 9pt 'Verdana';")
        else:
            label.setStyleSheet(f"background-color: {self.darken_color(label.original_color, 0.2)}; "
                                "color: #EFEBD8; font: 9pt 'Verdana'; border: 2px solid #00BFFF;")

    def toggle_selection(self, label, chapter):
        # Если статья уже выбрана, снимаем выделение
        if label in self.selected_cells.values():
            label.setStyleSheet(f"background-color: {label.original_color}; color: #EFEBD8; font: 9pt 'Verdana';")
            self.selected_cells.pop(chapter, None)
        else:
            # Убираем выделение с предыдущей выбранной статьи в этой главе
            if chapter in self.selected_cells:
                previous_label = self.selected_cells[chapter]
                previous_label.setStyleSheet(f"background-color: {previous_label.original_color}; color: #EFEBD8; font: 9pt 'Verdana';")

            # Устанавливаем новое выделение с голубыми границами
            label.setStyleSheet(f"background-color: {self.darken_color(label.original_color, 0.2)}; "
                                "color: #EFEBD8; font: 9pt 'Verdana'; border: 2px solid #00BFFF;")
            self.selected_cells[chapter] = label

        self.update_verdict_field()

    def on_modifier_click(self, mod_name):
        button = self.modifier_labels[mod_name]
        if mod_name in self.modifier_selected:
            self.modifier_selected.remove(mod_name)
            button.setStyleSheet("background-color: #444444; color: #EFEBD8;")
        else:
            self.modifier_selected.add(mod_name)
            button.setStyleSheet("background-color: #509ee3; color: #EFEBD8;")
        self.update_verdict_field()

    def update_verdict_field(self):
        # Логика обновления поля вердикта
        selected_articles = [label.text() for label in self.selected_cells.values() if label]
        article_codes = [self.get_article_code_by_name(article) for article in selected_articles]
        verdict = self.calculate_penalties(article_codes)
        self.verdict_label.setText("Вердикт: " + verdict)

    def get_article_code_by_name(self, name):
        return article_names_to_codes.get(name, "Неизвестный код")

    def calculate_penalties(self, article_codes):
        # Логика расчета наказаний
        total_minutes = 0
        has_life_sentence = False
        has_death_penalty = False
        verdict = []

        for code in article_codes:
            penalty_code = article_codes_to_penalties.get(code, "Неизвестный код")
            if penalty_code == "XX5":
                has_life_sentence = True
            elif penalty_code == "XX6":
                has_death_penalty = True
            else:
                minutes = penalty_duration.get(penalty_code, 0)
                if isinstance(minutes, int):
                    total_minutes += minutes

        if self.modifier_selected:
            for mod in self.modifier_selected:
                total_minutes += modifiers.get(mod, 0)

        if has_death_penalty:
            verdict.append("Высшая мера наказания")
        elif has_life_sentence or total_minutes >= 75:
            verdict.append("Пожизненное заключение")
        elif total_minutes > 0:
            verdict.append(f"{total_minutes} минут тюремного заключения")

        return ', '.join(verdict)

    def darken_color(self, hex_color, percent):
        """Утилита для затемнения цвета."""
        rgb = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
        darkened_rgb = [max(int(c * (1 - percent)), 0) for c in rgb]
        return f'#{darkened_rgb[0]:02x}{darkened_rgb[1]:02x}{darkened_rgb[2]:02x}'


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WardenHelper()
    window.show()
    sys.exit(app.exec_())
