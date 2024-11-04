import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from my_bar import MyBar, resource_path
from warden_helper_logic import (
    article_names_to_codes, article_codes_to_penalties, articles, modifiers, penalty_duration
)
class WardenHelper(QMainWindow):
    def __init__(self):
        super().__init__()

        # Устанавливаем флаги для окна без системного заголовка
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(resource_path("data/warden_helper_icon.png")))
        self.setStyleSheet("background-color: #1B1B1F; color: #EFEBD8;")
        self.setGeometry(100, 100, 1000, 800)

        self.selected_cells = {}
        self.modifier_selected = set()
        self.modifier_labels = {}

        # Главный контейнер
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Добавляем кастомный заголовок
        self.my_bar = MyBar(self)
        main_layout.addWidget(self.my_bar)

        # Создаем фрейм для таблиц и добавляем его в макет
        tables_frame = QFrame()
        tables_layout = QVBoxLayout(tables_frame)
        tables_layout.setSpacing(0)
        tables_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(tables_frame)

        # Создаем таблицу статей
        self.create_article_frame(tables_layout)

        # Создаем таблицу модификаторов
        self.create_modifier_frame(tables_layout)

        # Добавляем поле для вердикта
        verdict_frame = QFrame()
        verdict_layout = QVBoxLayout(verdict_frame)
        verdict_layout.setContentsMargins(0, 0, 0, 0)

        self.verdict_label = QLabel("Вердикт:", self)
        self.verdict_label.setStyleSheet("font: 18pt 'Verdana'; color: #d0d0d0;")
        self.verdict_label.setAlignment(Qt.AlignLeft)
        verdict_layout.addWidget(self.verdict_label)

        # Добавляем красную линию под вердиктом
        red_line = QFrame()
        red_line.setStyleSheet("background-color: red;")
        red_line.setFixedHeight(2)
        verdict_layout.addWidget(red_line)

        main_layout.addWidget(verdict_frame)

    def create_article_frame(self, layout):
        # Настройка таблицы статей
        frame = QFrame()
        grid_layout = QGridLayout(frame)
        grid_layout.setSpacing(0)  # Убираем промежутки между ячейками
        grid_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)

        columns = ["XX1", "XX2", "XX3", "XX4", "XX5", "XX6"]
        chapters = ["11X", "12X", "13X", "14X", "21X", "22X", "31X", "32X", "41X", "42X", "43X"]
        colors = {
            "XX1": "#0F4F27", "XX2": "#414700", "XX3": "#5f3800",
            "XX4": "#611300", "XX5": "#57000C", "XX6": "#000000"
        }

        # Заголовок для строки "Глава"
        chapter_label = QLabel("Глава", self)
        chapter_label.setStyleSheet("background-color: #333; color: white; font: bold 10pt 'Verdana';")
        chapter_label.setAlignment(Qt.AlignCenter)
        chapter_label.setFixedSize(100, 40)  # Ширина выровнена по слову "Глава"
        grid_layout.addWidget(chapter_label, 0, 0)

        # Создаем заголовки столбцов
        for i, col in enumerate(columns):
            label = QLabel(col, self)
            label.setStyleSheet(f"background-color: {colors[col]}; color: white; font: bold 10pt 'Verdana';")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(214, 40)  # Широкие заголовки, уменьшенная высота
            grid_layout.addWidget(label, 0, i + 1)

        # Создаем ячейки статей
        for i, chapter in enumerate(chapters):
            chapter_label = QLabel(chapter, self)
            chapter_label.setStyleSheet("background-color: #333; color: white; font: 10pt 'Verdana';")
            chapter_label.setAlignment(Qt.AlignCenter)
            chapter_label.setFixedSize(100, 60)  # Ширина для глав
            grid_layout.addWidget(chapter_label, i + 1, 0)

            for j, col in enumerate(columns):
                article = articles.get(chapter, [""])[j] if j < len(articles.get(chapter, [])) else ""
                label = QLabel(article, self)
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(214, 60)  # Широкие ячейки, уменьшенная высота
                label.setWordWrap(True)

                # Устанавливаем стиль с курсивным и жирным текстом
                label.setStyleSheet(f"background-color: {colors[col]}; color: #EFEBD8; font: bold italic 9pt 'Verdana';")
                label.original_color = colors[col]  # Сохраняем исходный цвет
                label.is_xx6 = (col == "XX6")  # Флаг для столбца XX6

                if article:  # Если в ячейке есть текст, добавляем события
                    label.mousePressEvent = lambda event, lbl=label, ch=chapter: self.toggle_selection(lbl, ch)
                    label.enterEvent = lambda event, lbl=label: self.on_hover_enter(lbl)
                    label.leaveEvent = lambda event, lbl=label: self.on_hover_leave(lbl)

                grid_layout.addWidget(label, i + 1, j + 1)

    def create_modifier_frame(self, layout):
        # Настройка таблицы модификаторов
        frame = QFrame()
        grid_layout = QGridLayout(frame)
        grid_layout.setSpacing(0)  # Убираем промежутки между ячейками
        grid_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)

        # Добавляем метки модификаторов
        for i, (mod_name, _) in enumerate(modifiers.items()):
            label = QLabel(mod_name, self)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(173, 80)  # Уменьшаем длину и увеличиваем высоту ячеек модификаторов
            label.setWordWrap(True)
            label.setStyleSheet("background-color: #444444; color: #EFEBD8; font: bold italic 9pt 'Verdana';")
            label.original_color = "#444444"  # Сохраняем исходный цвет

            # Добавляем события для модификаторов
            label.mousePressEvent = lambda event, lbl=label: self.toggle_modifier(lbl)
            label.enterEvent = lambda event, lbl=label: self.on_hover_enter(lbl)
            label.leaveEvent = lambda event, lbl=label: self.on_hover_leave(lbl)

            grid_layout.addWidget(label, 0, i)

    def on_hover_enter(self, label):
        # Эффект при наведении: подсветка для XX6, затемнение для остальных
        if label not in self.selected_cells.values() and label not in self.modifier_selected:
            if getattr(label, "is_xx6", False):  # Проверяем, является ли ячейка из столбца XX6
                highlight_color = self.brighten_color(label.original_color, 0.2)
                label.setStyleSheet(f"background-color: {highlight_color}; color: #EFEBD8; font: bold italic 9pt 'Verdana';")
            else:
                darker_color = self.darken_color(label.original_color, 0.2)
                label.setStyleSheet(f"background-color: {darker_color}; color: #EFEBD8; font: bold italic 9pt 'Verdana';")

    def on_hover_leave(self, label):
        # Возвращаем цвет, если ячейка не выбрана, иначе оставляем стиль выбранной ячейки
        if label not in self.selected_cells.values() and label not in self.modifier_selected:
            label.setStyleSheet(f"background-color: {label.original_color}; color: #EFEBD8; font: bold italic 9pt 'Verdana';")
        else:
            label.setStyleSheet(f"background-color: {self.darken_color(label.original_color, 0.2)}; "
                                "color: #EFEBD8; font: bold italic 9pt 'Verdana'; border: 2px solid #00BFFF;")

    def toggle_selection(self, label, chapter):
        """Переключение выбора статьи."""
        # Если статья уже выбрана, снимаем выделение
        if label in self.selected_cells.values():
            label.setStyleSheet(f"background-color: {label.original_color}; color: #EFEBD8; font: bold italic 9pt 'Verdana';")
            self.selected_cells.pop(chapter, None)
        else:
            # Убираем выделение с предыдущей выбранной статьи в этой главе
            if chapter in self.selected_cells:
                previous_label = self.selected_cells[chapter]
                previous_label.setStyleSheet(f"background-color: {previous_label.original_color}; color: #EFEBD8; font: bold italic 9pt 'Verdana';")

            label.setStyleSheet(f"background-color: {self.darken_color(label.original_color, 0.2)}; "
                                "color: #EFEBD8; font: bold italic 9pt 'Verdana'; border: 2px solid #00BFFF;")
            self.selected_cells[chapter] = label

        # Если ни одна статья не выбрана, сбрасываем модификаторы
        if not self.selected_cells:
            self.reset_modifiers()

        self.update_verdict_field()

    def toggle_modifier(self, label):
        """Переключение модификатора и обновление вердикта."""
        # Проверяем, выбрана ли хотя бы одна статья
        if not self.selected_cells:
            self.verdict_label.setText("Вердикт: Выберите хотя бы одну статью")
            return
        
        # Если модификатор уже выбран, снимаем выделение
        if label in self.modifier_selected:
            label.setStyleSheet(f"background-color: {label.original_color}; color: #EFEBD8; font: bold italic 9pt 'Verdana';")
            self.modifier_selected.remove(label)
        else:
            label.setStyleSheet(f"background-color: {self.darken_color(label.original_color, 0.2)}; "
                                "color: #EFEBD8; font: bold italic 9pt 'Verdana'; border: 2px solid #00BFFF;")
            self.modifier_selected.add(label)

        self.update_verdict_field()
        
    def reset_modifiers(self):
        """Сбрасывает все выбранные модификаторы."""
        for label in self.modifier_selected:
            label.setStyleSheet("background-color: #444444; color: #EFEBD8; font: bold italic 9pt 'Verdana';")
        self.modifier_selected.clear()


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
                total_minutes += modifiers.get(mod.text(), 0)

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

    def brighten_color(self, hex_color, percent):
        """Утилита для подсветки цвета."""
        rgb = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
        brightened_rgb = [min(int(c + (255 - c) * percent), 255) for c in rgb]
        return f'#{brightened_rgb[0]:02x}{brightened_rgb[1]:02x}{brightened_rgb[2]:02x}'
    
    def toggle_always_on_top(self):
        """Переключение окна между обычным состоянием и 'всегда сверху'."""
        self.always_on_top = not getattr(self, "always_on_top", False)

        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.my_bar.btn_pin.setIcon(QIcon(resource_path('data/unpin.png')))  # Изменяем иконку на закрепленную
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.my_bar.btn_pin.setIcon(QIcon(resource_path('data/pin.png')))  # Возвращаем иконку на обычную

        self.show()  # Обновляем окно

# Функция для запуска полной версии таблицы
def run_table_version():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    main_window = WardenHelper()
    main_window.show()

    if not QApplication.instance().thread().isRunning():
        sys.exit(app.exec_())

if __name__ == "__main__":
    run_table_version()
