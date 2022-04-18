from enum import Enum
from PySide6.QtWidgets import (
    QApplication, QWidget, QFrame, QHBoxLayout,
    QVBoxLayout, QLineEdit, QMainWindow, QLabel,QSizePolicy, QPushButton)
from PySide6.QtGui import QValidator, QFont, QCursor
from PySide6.QtCore import QEvent, Qt, QObject, QSize, Signal
from pynput.keyboard import Key, Controller

keyboard = Controller()


alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

class Keys(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    ENTER = Key.enter
    DELETE = Key.backspace


BUTTONS = {}
# #3a3a3c -> Not in word
# #538d4e -> in word
# #b59f3b -> wrong pos
class KeyboardButton(QPushButton):
    clicked = Signal()
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        font = QFont()
        font.setPixelSize(13)
        font.setFamily(u"Segoe UI")
        # font.setWeight(QFont.ExtraBold)
        font.setBold(True)
        # self.setFlat(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFont(font)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    def setLetter(self, letter):
        self.letter = letter
        self.setText(letter)

class KeyboardRow(QFrame):

    def __init__(self, parent=None, keys:list(Keys)=None):
        super().__init__(parent=parent)
        self.keys = [] if keys is None else keys
        self.initUi()

    def initUi(self):
        layout = QHBoxLayout(self)
        for key in self.keys:
            button = KeyboardButton(self)
            button.setStyleSheet("""
                background:#818384; 
                border-radius: 4px; 
                padding: 10px;
                color: rgb(255, 255, 255);
                border: 0px;
                """)
            button.setFixedHeight(58)
            button.setMinimumWidth(43)
            button.setLetter(key.name.upper())
            layout.addWidget(button)
            button.clicked.connect(lambda val=key.value: press_key(val))
            BUTTONS[key.name.upper()] = button

        layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)


class QuertyKeyboard(QFrame):
    keys = [
        [Keys.Q, Keys.W, Keys.E, Keys.R, Keys.T, Keys.Y, Keys.U, Keys.I, Keys.O, Keys.P],
        [Keys.A, Keys.S, Keys.D, Keys.F, Keys.G, Keys.H, Keys.J, Keys.K, Keys.L],
        [Keys.ENTER, Keys.Z, Keys.X, Keys.C, Keys.V, Keys.B, Keys.N, Keys.M, Keys.DELETE]
    ]

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUi()

    def initUi(self):
        layout = QVBoxLayout(self)
        for key_group in self.keys:
            row = KeyboardRow(self, keys=key_group)
            layout.addWidget(row, 0, Qt.AlignCenter)
        layout.setSpacing(2)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
