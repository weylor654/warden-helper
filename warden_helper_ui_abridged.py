import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QComboBox, QVBoxLayout, QFrame, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from my_bar import MyBar
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
        self.setMinimumSize(500, 400)
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

        # Поле для ввода модификаторов
        self.modifier_label = QLabel("Модификаторы:", self)
        self.modifier_label.setStyleSheet("color: white; font-size: 16px;")
        self.content_layout.addWidget(self.modifier_label)

        # Дропбокс для выбора модификаторов
        self.modifier_autocomplete = QComboBox(self)
        self.modifier_autocomplete.addItems(MODIFIER_OPTIONS)
        self.modifier_autocomplete.setStyleSheet(
            "background-color: #2E2E2E; color: white; font-size: 16px; padding: 10px; border: 1px solid #3A3A3A; border-radius: 10px;"
        )
        self.content_layout.addWidget(self.modifier_autocomplete)

        # Кнопка для добавления модификатора
        self.add_modifier_button = QPushButton("Добавить модификатор", self)
        self.add_modifier_button.setStyleSheet(
            "QPushButton { background-color: #272727; color: white; font-size: 16px; border: none; padding: 10px; border-radius: 10px; }"
            "QPushButton:hover { background-color: #509ee3; color: white; }"
            "QPushButton:pressed { background-color: #1E6FA7; color: white; }"
        )
        self.add_modifier_button.clicked.connect(self.add_modifier)
        self.content_layout.addWidget(self.add_modifier_button)

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
        self.modifier_entry.setFixedHeight(150)  # Установка фиксированной высоты
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
        self.always_on_top = not self.always_on_top

        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.my_bar.btn_pin.setIcon(QIcon('data/unpin.png'))
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.my_bar.btn_pin.setIcon(QIcon('data/pin.png'))

        self.show()

    def add_modifier(self):
        selected_modifier = self.modifier_autocomplete.currentText()
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
        articles = self.article_entry.text().strip().split()
        
        # Разделяем строку модификаторов по символу '\n' и удаляем лишние пробелы
        modifiers = [modifier.strip().split('. ', 1)[1] for modifier in self.modifier_entry.toPlainText().split('\n') if modifier.strip()]
        
        # Передаем список модификаторов в функцию calculate_penalties
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
