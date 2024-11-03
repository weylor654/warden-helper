import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from my_bar import MyBar  # Импортируем класс MyBar из вашего файла my_bar

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Окно без системного заголовка
        self.setMinimumSize(300, 150)  # Задаем минимальные размеры окна
        self.always_on_top = False  # Изначально окно не закреплено

        # Основной интерфейс
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.layout.setSpacing(0)  # Убираем промежуток между элементами
        self.setLayout(self.layout)  # Устанавливаем layout для окна

        # Создаем и добавляем панель MyBar
        self.my_bar = MyBar(self)  # Добавляем кастомную панель
        self.layout.addWidget(self.my_bar)

        # Создание кнопок
        self.full_version_button = self.create_button("Полная версия", self.open_full_version)
        self.abridged_version_button = self.create_button("Сокращенная версия", self.open_abridged_version)

        # Добавляем кнопки в основной layout
        self.layout.addWidget(self.full_version_button, alignment=Qt.AlignCenter)  # Центрируем кнопку
        self.layout.addWidget(self.abridged_version_button, alignment=Qt.AlignCenter)  # Центрируем кнопку

        # Установка стиля окна
        self.setStyleSheet("background-color: #1B1B1F;")  # Цвет фона окна

    def create_button(self, text, command):
        """Создает кнопку с заданным текстом и командой."""
        button = QPushButton(text)
        button.setFixedHeight(40)
        button.setFixedWidth(200)  # Задаем фиксированную ширину кнопок

        # Обработка событий наведения и нажатия
        button.setStyleSheet("""
            QPushButton {
                background-color: #272727; 
                color: #d0d0d0;  /* Светло-серый текст */
                font-size: 14px;  /* Увеличиваем размер шрифта */
                border: none; 
                padding: 10px;
                border-radius: 10px;  /* Закругление краёв */
            }
            QPushButton:hover {
                background-color: #509ee3;  /* Цвет кнопки при наведении */
                color: white;  /* Цвет текста при наведении */
            }
            QPushButton:pressed {
                background-color: #0073a1;  /* Темный цвет при нажатии (темно-голубой) */
                color: white;  /* Цвет текста при нажатии */
            }
        """)
        button.clicked.connect(command)  # Подключаем кнопку к команде
        return button

    def toggle_always_on_top(self):
        """Переключение окна между обычным состоянием и 'всегда сверху'."""
        self.always_on_top = not self.always_on_top  # Переключаем состояние

        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Установить флаг 'всегда сверху'
            self.my_bar.btn_pin.setIcon(QIcon('data/unpin.png'))  # Изменяем иконку на закрепленную
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)  # Снять флаг 'всегда сверху'
            self.my_bar.btn_pin.setIcon(QIcon('data/pin.png'))  # Возвращаем иконку на обычную

        self.show()  # Обновляем окно

    def open_full_version(self):
        from GUI_test import run_table_version
        run_table_version()

    def open_abridged_version(self):
        from warden_helper_ui_abridged import run_abridged_version
        run_abridged_version()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
