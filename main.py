import sys
from PyQt6.QtWidgets import QApplication
from mainWindows import MainWindow
from getscreeninfo import get_size

# Запуск программы
if __name__ == '__main__':
    width, height = get_size()
    app = QApplication(sys.argv)
    window = MainWindow(width, height)
    window.show()
    sys.exit(app.exec())
