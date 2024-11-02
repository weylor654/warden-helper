import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor, QIcon
from my_bar import MyBar  # Импортируем кастомный заголовок
from PyQt5.QtCore import Qt, QEvent

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(1600, 800)
        self.always_on_top = False

        # Убираем стандартный заголовок
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Основной интерфейс
        self.layout = QVBoxLayout()
        self.my_bar = MyBar(self)
        self.layout.addWidget(self.my_bar)

        # Создаем таблицу
        self.create_table()
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Переменная для хранения оригинального цвета ячейки
        self.original_color = None
        self.last_hovered_item = None

    def create_table(self):
        """Создание таблицы без заголовков и без сетки."""
        self.table = QTableWidget(11, 7)
        self.table.setShowGrid(False)
        self.table.setMouseTracking(True)  # Включаем отслеживание мыши

        # Устанавливаем заголовок для нового столбца
        self.table.setHorizontalHeaderLabels(["Глава", "XX1", "XX2", "XX3", "XX4", "XX5", "XX6"])

        # Задаем цвета для столбцов
        self.colors = ['#0f4f27', '#414700', '#5f3800', '#611300', '#611300', '#121212']
        for i, color in enumerate(self.colors):
            self.table.setColumnWidth(i + 1, 180)

        # Заполняем первую строку
        header_labels = ["Глава", "XX1", "XX2", "XX3", "XX4", "XX5", "XX6"]
        for column in range(7):
            item = QTableWidgetItem(header_labels[column])
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QColor('white'))
            item.setBackground(QColor('#333333') if column == 0 else QColor(self.colors[column - 1]))
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEditable)  # Делаем ячейку неизменяемой
            self.table.setItem(0, column, item)

        # Заполняем ячейки в первом столбце с главами
        chapter_labels = ["11X", "12X", "13X", "14X", "21X", "22X", "31X", "32X", "41X", "42X", "43X"]
        for row in range(1, 12):
            if row - 1 < len(chapter_labels):
                item = QTableWidgetItem(chapter_labels[row - 1])
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor('white'))
                item.setBackground(QColor('#333333'))
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEditable)  # Делаем ячейку неизменяемой
                self.table.setItem(row, 0, item)

        # Устанавливаем цвета и заполняем ячейки для остальных столбцов
        for row in range(1, 11):
            for column in range(1, 7):
                item = QTableWidgetItem(f"Item {row},{column}")
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor('white'))
                item.setBackground(QColor(self.colors[column - 1]))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Делаем ячейку неизменяемой
                self.table.setItem(row, column, item)

        for row in range(11):
            self.table.setRowHeight(row, 50)

        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        # Обрабатываем наведение мыши
        self.table.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove and source == self.table.viewport():
            pos = event.pos()
            index = self.table.indexAt(pos)
            if index.isValid():
                row, column = index.row(), index.column()
                item = self.table.item(row, column)

                # Проверяем, чтобы наведение было только на ячейки, которые не в первом столбце и не в первой строке
                if item and row != 0 and column != 0 and item != self.last_hovered_item:
                    # Восстанавливаем цвет предыдущей ячейки
                    if self.last_hovered_item:
                        self.last_hovered_item.setBackground(QColor(self.original_color))

                    # Сохраняем оригинальный цвет текущей ячейки
                    self.original_color = item.background().color()

                    # Изменяем цвет на более тёмный/светлый при наведении
                    if self.original_color == QColor('#333333'):
                        hover_color = self.original_color.lighter(130)  # Осветляем чёрный цвет
                    else:
                        hover_color = self.original_color.darker(130)  # Затемняем другие цвета

                    item.setBackground(hover_color)
                    self.last_hovered_item = item  # Сохраняем текущую ячейку как последнюю наведённую
            return True
        elif event.type() == QEvent.Leave and source == self.table.viewport():
            # Восстанавливаем цвет последней наведенной ячейки, если курсор покинул таблицу
            if self.last_hovered_item:
                self.last_hovered_item.setBackground(QColor(self.original_color))
                self.last_hovered_item = None
            return True

        return super(MainWindow, self).eventFilter(source, event)

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.my_bar.btn_pin.setIcon(QIcon('data/unpin.png'))
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.my_bar.btn_pin.setIcon(QIcon('data/pin.png'))
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
