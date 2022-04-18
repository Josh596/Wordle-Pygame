from PySide6.QtWidgets import (
    QFrame, QHBoxLayout,QVBoxLayout, QLabel,QSizePolicy, QPushButton)
from PySide6.QtCore import Qt 

from custom_exceptions import NotEnoughLetters, NotInWordList
from styles import Style
from utils import itemIndex, nextItem, previousItem
from config import LENGTH_WORD,WORD_LIST,MAX_GUESSES, State

class InputBox(QLabel):
    def __init__(self, parent, width=51, height=51):
        super().__init__(parent=parent)
        self.setFixedSize(width, height)
        self.setStyleSheet(Style.style_input_standard.replace("FONTSIZE", str(height-10)))
        self.setAlignment(Qt.AlignCenter)
        self._state = None

    def setText(self, text: str) -> None:
        return super().setText(text.upper())

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state:State):
        if new_state == State.FAIL:
            self.setProperty('state', 'fail')
        elif new_state == State.SUCCESS:
            self.setProperty('state', 'success')
        elif new_state == State.NEUTRAL:
            self.setProperty('state', 'neutral')
        self.style().unpolish(self)
        self.style().polish(self)

    def get_text(self):
        if self.text():
            return self.text()
    


class Guess(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.letters = [InputBox(self) for _ in range(LENGTH_WORD)]
        self.initUi()
        self.active_input = self.letters[0]
        self.checked = False        

    def initUi(self):
        layout = QHBoxLayout(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        for letter in self.letters:
            layout.addWidget(letter)
        layout.setSpacing(3)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setSizePolicy(sizePolicy)

    def getWord(self) -> str:
        word = ''
        for letter in self.letters:
            if letter.get_text():
                word += letter.get_text()
            else:
                raise NotEnoughLetters('Not Enough Letters')
        return word
        

    def moveToNextLetter(self):
        next_letter = nextItem(self.active_input)
        if next_letter:
            self.active_input = next_letter
            return True

    def moveToPreviousLetter(self):
        prev_letter = previousItem(self.active_input)
        if prev_letter:
            self.active_input = prev_letter
            return True

    def check_guess(self, solution:str):
        if self.getWord().lower() not in WORD_LIST:
            raise NotInWordList
        words_data = {}
        for index, letter in enumerate(solution.upper()):
            if letter in words_data:
                words_data[letter]['index'].append(index)
                words_data[letter]['count'] += 1
            else:
                words_data[letter] = {'index':[index], 'count':solution.count(letter.upper())}
        
        for index, letter in enumerate(self.getWord()):
            if words_data.get(letter.upper()):
                possible_indexes = words_data[letter]['index']
                if index in possible_indexes:
                    self.letters[index].state = State.SUCCESS
                else:
                    self.letters[index].state = State.NEUTRAL
            else:
                self.letters[index].state = State.FAIL
        if self.getWord().upper() == solution.upper():
            return True
        # Implement logic for wordle here
        # Get all the letters in the solution and their count and index in solution
        # {X:{index:0, count: 1}}
        # For each letter in word_data, check if any exists in word_given
        # If it has more than one occurence, prioritize the one in right position, then wrong position, then incorrect
        # If the letter appears once, then every other occurence should fail, not neutral
        # If it occurs twice, then check if any of the occurences are in the right index


        # Check if the word[0] == solution[0] and reduce the count of that letter by 1
        # If the word is in the solution and is in right index, set input to green and reduce count by 1, else
        # If the word is in the solution but wrong index, set input to yellow and reduce count by 1
        # If the word not in solution, set input to red
        # return whether game over or not
    # def getActiveInput(self):
    #     return self.active


class Board(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.guesses = [Guess() for _ in range(MAX_GUESSES)]
        self.initUi()
        self.active_guess = self.guesses[0]
        self.game_over = False

    def initUi(self):
        layout = QVBoxLayout(self)
        for guess in self.guesses:
            layout.addWidget(guess, 0, Qt.AlignCenter)
        layout.setSpacing(0)

    def moveToNextGuess(self):
        next_guess = nextItem(self.active_guess)
        if next_guess:
            self.active_guess = next_guess
            return True
