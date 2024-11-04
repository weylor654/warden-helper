import os
import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

# Без этого в приложении не отображаются иконки пина при нажатии
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Окно без системного заголовка
        self.setMinimumSize(800, 400)
        self.always_on_top = False  # Переменная для отслеживания состояния "всегда сверху"

        # Основной интерфейс
        self.layout = QVBoxLayout()
        self.my_bar = MyBar(self)  # кастомная панель
        self.layout.addWidget(self.my_bar)
        self.layout.addStretch() 
        self.setLayout(self.layout)

        # Убираем отступы и промежутки в основной компоновке
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def toggle_always_on_top(self):
        """Переключение окна между обычным состоянием и 'всегда сверху'."""
        self.always_on_top = not self.always_on_top  # Переключаем состояние

        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Установить флаг 'всегда сверху'
            self.my_bar.btn_pin.setIcon(QIcon(resource_path('data/unpin.png')))  # иконку на закрепленную
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)  # Снять флаг 'всегда сверху'
            self.my_bar.btn_pin.setIcon(QIcon(resource_path('data/pin.png')))  # Возвращаем иконку на обычную

        self.show()  # Обновляем окно


class MyBar(QWidget):
    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Убираем промежутки между кнопками

        # Темный стиль заголовка окна
        self.setStyleSheet(""" 
            background-color: #272727;  /* Темно-серый цвет заголовка */
            color: white;
            font-weight: bold;
        """)

        # Заголовок окна
        self.title = QLabel("Warden Helper")
        self.title.setFixedHeight(35)  # Фиксируем высоту заголовка
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # Добавляем кнопки
        self.add_buttons()

        self.setLayout(self.layout)

        self.start_pos = QPoint(0, 0)
        self.pressing = False

    def add_buttons(self):
        """Добавление кнопок в заголовок окна."""
        self.btn_pin = QPushButton()
        self.btn_pin.setFixedSize(35, 35)
        self.btn_pin.setIcon(QIcon(resource_path('data/pin.png')))  # Обновлённый путь, без resource_path в приложении нет png файлов
        self.btn_pin.setStyleSheet(self.button_style())
        self.btn_pin.clicked.connect(self.parent.toggle_always_on_top)

        self.btn_min = QPushButton()
        self.btn_min.setFixedSize(35, 35)
        self.btn_min.setIcon(QIcon(resource_path('data/under_line.png')))
        self.btn_min.setStyleSheet(self.button_style())
        self.btn_min.clicked.connect(self.parent.showMinimized)

        self.btn_close = QPushButton()
        self.btn_close.setFixedSize(35, 35)
        self.btn_close.setIcon(QIcon(resource_path('data/krest.png')))
        self.btn_close.setStyleSheet(self.button_style())
        self.btn_close.clicked.connect(self.parent.close)

        self.layout.addWidget(self.btn_pin)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)


    def button_style(self):
        """Возвращает стиль кнопки."""
        return """
            QPushButton {
                background-color: #272727;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background-color: #4f4f4f;
            }
            QPushButton:pressed {
                background-color: #3b3b3b;
            }
        """

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            delta = event.globalPos() - self.start_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.pressing = False

    def toggle_maximized(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
