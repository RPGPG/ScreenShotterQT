import sys

import pyautogui
from PySide6 import QtCore, QtGui
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('mon.png'))
        self.setWindowTitle("Screenshotter")
        self.setWindowOpacity(0.5)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.label = Label("Draw a rectangle to save screenshot\nPress Esc to exit")
        self.label.setStyleSheet("color: rgb(170, 170, 170)")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QtGui.QFont("Times", 30, QtGui.QFont.Weight.Bold))
        self.setCentralWidget(self.label)
        self.showMaximized()

    def mouseMoveEvent(self, e):
        if self.label.pressed:
            canvas = QtGui.QPixmap(pyautogui.size().width, pyautogui.size().height)
            painter = QtGui.QPainter(canvas)
            painter.setBrush(QColor('cyan'))
            x = e.position().x()
            y = e.position().y()
            painter.drawRect(self.label.move_x, self.label.move_y,
                             x - self.label.move_x, y - self.label.move_y)
            painter.end()
            self.label.setPixmap(canvas)


class Label(QLabel):
    def __init__(self, val):
        super().__init__(val)
        self.screenshot_start = 0
        self.screenshot_end = 0
        self.move_x = 0
        self.move_y = 0
        self.pressed = False

    def mousePressEvent(self, e):
        self.screenshot_start = pyautogui.position()
        self.move_x = e.position().x()
        self.move_y = e.position().y()
        self.pressed = True

    def mouseReleaseEvent(self, e):
        window.hide()
        self.screenshot_end = pyautogui.position()
        if self.screenshot_start.x < self.screenshot_end.x and self.screenshot_start.y < self.screenshot_end.y:
            pyautogui.screenshot("scr.png", region=(self.screenshot_start.x, self.screenshot_start.y,
                                                    self.screenshot_end.x - self.screenshot_start.x,
                                                    self.screenshot_end.y - self.screenshot_start.y))
        elif self.screenshot_start.x < self.screenshot_end.x and self.screenshot_start.y > self.screenshot_end.y:
            pyautogui.screenshot("scr.png", region=(self.screenshot_start.x, self.screenshot_end.y,
                                                    self.screenshot_end.x - self.screenshot_start.x,
                                                    self.screenshot_start.y - self.screenshot_end.y))
        elif self.screenshot_start.x > self.screenshot_end.x and self.screenshot_start.y > self.screenshot_end.y:
            pyautogui.screenshot("scr.png", region=(self.screenshot_end.x, self.screenshot_end.y,
                                                    self.screenshot_start.x - self.screenshot_end.x,
                                                    self.screenshot_start.y - self.screenshot_end.y))
        else:
            pyautogui.screenshot("scr.png", region=(self.screenshot_end.x, self.screenshot_start.y,
                                                    self.screenshot_start.x - self.screenshot_end.x,
                                                    self.screenshot_end.y - self.screenshot_start.y))

        pyautogui.alert(title="ScreenshotterQT", text="Screenshot saved as scr.png")
        sys.exit()


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
