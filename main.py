import json
from enum import Enum
import random
from PySide6.QtWidgets import (
    QApplication, QWidget, QFrame, QHBoxLayout,
    QVBoxLayout, QLineEdit, QMainWindow, QLabel,QSizePolicy, QPushButton)
from PySide6.QtGui import QValidator, QFont, QCursor
from PySide6.QtCore import QEvent, Qt, QObject, QSize, Signal

from keyboard import QuertyKeyboard
from custom_exceptions import NotEnoughLetters, NotInWordList
from styles import Style
from utils import itemIndex, nextItem, previousItem
from board import Board, Guess, InputBox
from config import WORD_LIST, alphabets



class AlertWidget(QFrame):
    def __init__(self):
        super().__init__(parent=None)

    

    def hide(self):
        super().hide()
        self.deleteLater()


class MainWindow(QWidget):
    # keyPressed = Signal(QEvent)
    def __init__(self):
        super().__init__()
        self.initUi()
        self.setFixedSize(480, 640)
        self.setWindowTitle('Wordle')
        
        self.solution = random.choice(WORD_LIST)

    def initUi(self):
        self.setStyleSheet("""
            background: #121213;
        """)

        layout = QVBoxLayout(self)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)

        self.label = QLabel(self)
        self.label.setMaximumSize(QSize(16777215, 81))
        self.label.setStyleSheet(u"color:white;\n"
                                 "font-variant: small-caps;\n"
                                 "border-bottom: 4px solid #00c4cc; \n"
                                 "font-weight: 800;\n"
                                 "padding-bottom:30px;")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")

        layout.addWidget(self.label)

        self.board = Board(self)
        layout.addWidget(self.board)

        self.keybaord = QuertyKeyboard(self)
        layout.addWidget(self.keybaord)

        self.setAllText()

    def setAllText(self):
        self.label.setText('Wordle')

    def getActiveGuess(self) -> Guess:
        return self.board.active_guess

    def getActiveInput(self) -> InputBox:
        return self.board.active_guess.active_input

    def keyPressEvent(self, event):
        """
        Handles all keystrokes.
        """
        if not self.board.game_over:
            if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
                try:
                    text = self.getActiveGuess().getWord()
                    if self.getActiveGuess().check_guess(self.solution):
                        self.board.game_over = True
                        return
                    self.getActiveGuess().checked = True

                    if not self.board.moveToNextGuess():
                        print('Game has ended')
                        print(self.solution)
                        self.board.game_over = True
                    self.getActiveGuess().setDisabled(True)
                except NotEnoughLetters:
                    print('Not enough words')
                except NotInWordList:
                    print('Not in word list')

            elif event.key() == Qt.Key_Backspace:
                active_input = self.getActiveInput()
                if active_input.text():   
                    active_input.setText('')
                else:
                    self.getActiveGuess().moveToPreviousLetter()
                    self.getActiveInput().setText('')

            if event.text().upper() in alphabets:
                if not self.getActiveInput().text():
                    self.getActiveInput().setText(event.text())
                if not self.getActiveGuess().moveToNextLetter() and self.getActiveGuess().checked:
                    self.board.moveToNextGuess()

            event.accept()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec()
