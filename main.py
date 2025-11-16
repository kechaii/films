import sys
from PyQt6.QtWidgets import QApplication
from tabWidget import TabsWidgets
from getscreeninfo import get_size

# Запуск программы
if __name__ == '__main__':
    width, height = get_size()
    app = QApplication(sys.argv)
    window = TabsWidgets(width, height)
    window.show()
    sys.exit(app.exec())
