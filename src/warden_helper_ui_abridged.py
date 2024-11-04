import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QLabel, QPushButton,
    QVBoxLayout, QFrame, QTextEdit, QToolButton, QMenu, QSizePolicy 
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from my_bar import MyBar, resource_path
from warden_helper_logic import calculate_penalties

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

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(resource_path("data/warden_helper_icon.png"))) # иконка приложения
        self.setMinimumSize(400, 280)  # Измененные размеры окна
        self.always_on_top = False

        # Установка цветовой схемы
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        # Основной интерфейс
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Добавляем кастомную панель заголовка
        self.my_bar = MyBar(self)
        self.my_bar.setFixedHeight(40)
        self.layout.addWidget(self.my_bar)

        # Основной контент
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.layout.addLayout(self.content_layout)

        # Поле для ввода статей
        self.article_label = QLabel("Статьи (через пробел):", self)
        self.article_label.setStyleSheet("color: white; font-size: 16px;")
        self.content_layout.addWidget(self.article_label)
        self.article_entry = QLineEdit(self)
        self.article_entry.setStyleSheet(
            "background-color: #2E2E2E; color: white; font-size: 16px; border: 1px solid #3A3A3A; padding: 10px; border-radius: 10px;"
        )
        self.content_layout.addWidget(self.article_entry)
        
        self.content_layout.addSpacing(20)
        
        # Создание контекстного меню для выбора модификаторов
        self.modifier_menu_label = QLabel("Модификаторы:", self)
        self.modifier_menu_label.setStyleSheet("color: white; font-size: 16px;")
        self.content_layout.addWidget(self.modifier_menu_label)
        self.modifier_menu = QMenu(self)
        for modifier in MODIFIER_OPTIONS:
            action = self.modifier_menu.addAction(modifier)
            action.triggered.connect(lambda checked, text=modifier: self.add_modifier(text))  # Передаем текст модификатора

        # Установка цвета текста в меню
        self.modifier_menu.setStyleSheet("QMenu { background-color: #2E2E2E; } QMenu::item { color: white; } QMenu::item:selected { background-color: #509ee3; }")

        # Создание кнопки выбора модификаторов
        self.modifier_autocomplete = QToolButton(self)
        self.modifier_autocomplete.setText("Выберите модификатор")
        self.modifier_autocomplete.setStyleSheet(
            """
            QToolButton {
                background-color: #2E2E2E;
                color: white;
                font-size: 16px;
                border: 1px solid #3A3A3A;
                padding: 10px;  /* Добавляем отступ справа для сдвига стрелочки */
                border-radius: 10px;
                qproperty-iconSize: 20px;  /* Размер стрелочки */
            }
            QToolButton::menu-indicator {
                subcontrol-origin: content;  /* Расположение стрелочки внутри кнопки */
                subcontrol-position: right center;  /* Стрелочка по центру вертикали справа */
                width: 16px;  /* Ширина стрелочки */
                height: 16px;  /* Высота стрелочки */
            }
            """
        )    
        self.modifier_autocomplete.setMenu(self.modifier_menu)  # Установка меню для кнопки
        self.modifier_autocomplete.setPopupMode(QToolButton.InstantPopup)  # Установка режима всплывающего меню

        # Установка кнопки в layout
        self.content_layout.addWidget(self.modifier_autocomplete, alignment=Qt.AlignCenter)

        # Установка политики размера для кнопки
        self.modifier_autocomplete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.modifier_autocomplete.setMinimumWidth(400)  # Минимальная ширина кнопки

        # Кнопка для удаления модификатора
        self.remove_modifier_button = QPushButton("Удалить модификатор", self)
        self.remove_modifier_button.setStyleSheet(
            "QPushButton { background-color: #272727; color: white; font-size: 16px; border: none; padding: 10px; border-radius: 10px; }"
            "QPushButton:hover { background-color: #c0392b; color: white; }"
            "QPushButton:pressed { background-color: #8B2727; color: white; }"
        )
        self.remove_modifier_button.clicked.connect(self.remove_modifier)
        self.content_layout.addWidget(self.remove_modifier_button)

        # Поле для отображения модификаторов
        self.modifier_entry = QTextEdit(self)
        self.modifier_entry.setReadOnly(True)
        self.modifier_entry.setStyleSheet(
            "background-color: #2E2E2E; color: white; font-size: 16px; border: 1px solid #3A3A3A; padding: 10px; border-radius: 10px;"
        )
        self.modifier_entry.setFixedHeight(90)  # Установка фиксированной высоты
        self.content_layout.addWidget(self.modifier_entry)

        self.content_layout.addSpacing(20)

        # Кнопка для расчета времени
        self.calc_button = QPushButton("Рассчитать время", self)
        self.calc_button.setStyleSheet(
            "QPushButton { background-color: #272727; color: white; font-size: 16px; border: none; padding: 10px; border-radius: 10px; }"
            "QPushButton:hover { background-color: #509ee3; color: white; }"
            "QPushButton:pressed { background-color: #1E6FA7; color: white; }"
        )
        self.calc_button.clicked.connect(self.calculate_verdict)
        self.content_layout.addWidget(self.calc_button)

        self.verdict_label = QLabel("Вердикт:", self)
        self.verdict_label.setStyleSheet("color: white; font-size: 16px;")
        self.content_layout.addWidget(self.verdict_label)

        self.red_line = QFrame(self)
        self.red_line.setFrameShape(QFrame.HLine)
        self.red_line.setFrameShadow(QFrame.Sunken)
        self.red_line.setStyleSheet("background-color: red; height: 2px; border-radius: 10px;")
        self.content_layout.addWidget(self.red_line)

        self.setStyleSheet("background-color: #1B1B1F;")


    def toggle_always_on_top(self):
        """Переключение окна между обычным состоянием и 'всегда сверху'."""
        self.always_on_top = not self.always_on_top  # Переключаем состояние

        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Установить флаг 'всегда сверху'
            self.my_bar.btn_pin.setIcon(QIcon(resource_path('data/unpin.png')))  # Изменяем иконку на закрепленную
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)  # Снять флаг 'всегда сверху'
            self.my_bar.btn_pin.setIcon(QIcon(resource_path('data/pin.png')))  # Возвращаем иконку на обычную

        self.show()  # Обновляем окно

    def add_modifier(self, selected_modifier):
        current_text = self.modifier_entry.toPlainText().strip()
        if current_text:
            # Нумеруем модификаторы
            modifiers = [line for line in current_text.split('\n') if line.strip()]
            new_modifier_number = len(modifiers) + 1
            self.modifier_entry.append(f"{new_modifier_number}. {selected_modifier}")
        else:
            self.modifier_entry.setPlainText(f"1. {selected_modifier}")


    def remove_modifier(self):
        current_text = self.modifier_entry.toPlainText().strip()
        if current_text:
            modifiers = [line.strip() for line in current_text.split('\n') if line.strip()]
            if modifiers:
                modifiers.pop()  # Удаляем последний модификатор
                # Нумеруем оставшиеся модификаторы
                for index, modifier in enumerate(modifiers):
                    modifiers[index] = f"{index + 1}. {modifier.split('. ', 1)[1]}"
                self.modifier_entry.setPlainText('\n'.join(modifiers))
            else:
                self.modifier_entry.clear()  # Если это единственный модификатор, очищаем поле
                
    def calculate_verdict(self):
        # Получаем статьи из поля ввода и удаляем пустые строки
        articles = [article for article in self.article_entry.text().strip().split() if article]
        if len(articles) > 3:
            return None
        # Проверяем, есть ли статьи
        if not articles:
            self.verdict_label.setText("Вердикт: Введите хотя бы одну статью")
            return

        # Разделяем строку модификаторов по символу '\n' и удаляем лишние пробелы
        modifiers = [modifier.strip().split('. ', 1)[1] for modifier in self.modifier_entry.toPlainText().split('\n') if modifier.strip()]
        
        # Передаем список статей и модификаторов в функцию calculate_penalties
        verdict = calculate_penalties(articles, modifiers)
        self.verdict_label.setText(f"Вердикт: {verdict}")


def run_abridged_version():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    if not QApplication.instance().thread().isRunning():
        sys.exit(app.exec_())

if __name__ == "__main__":
    run_abridged_version()
