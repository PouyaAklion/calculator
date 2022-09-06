import sys
from functools import partial
import re
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QWidget,

)
from PyQt5.Qt import Qt


class Calculator(QWidget):
    OPERATORS = ('+', '-', '*', '/')

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi tabs calculator")

        self.app_layout = QVBoxLayout()
        self.output_layout = QVBoxLayout()
        self.buttons_layout = QGridLayout()

        self.output_label = QLabel("0")
        self.history_label = QLabel('')
        self.output_layout.addWidget(self.history_label)
        self.output_layout.addWidget(self.output_label)

        self.app_layout.addLayout(self.output_layout)
        self.app_layout.addLayout(self.buttons_layout)
        self.buttons()
        self.setLayout(self.app_layout)

        self._last_operator = ''
        self._last_operand = ''
        self._last_result = ''
        self.user_inputs = ['0']

    def keyPressEvent(self, event):
        for i in range(10):
            if event.key() == getattr(Qt, f'Key_{i}'):
                self.update_user_input(str(i))
                if len(self.user_inputs) % 2 == 1 and len(self.user_inputs) > 1:
                    self.calculate()
        if event.key() == Qt.Key_Plus:
            self.update_user_input('+')
        if event.key() == Qt.Key_Minus:
            self.update_user_input('-')
        if event.key() == Qt.Key_Asterisk:
            self.update_user_input('*')
        if event.key() == Qt.Key_Slash:
            self.update_user_input('/')
        if event.key() == Qt.Key_Backspace:
            self.update_user_input('backspace')

    def update_user_input(self, key):
        if key.isdigit() and self.user_inputs[-1].isdigit():
            if self.user_inputs[-1] == '0':
                self.user_inputs[-1] = key
            else:
                self.user_inputs[-1] = self.user_inputs[-1] + key
            self.update_output(self.user_inputs[-1])
        elif key.isdigit() and not self.user_inputs[-1].isdigit():
            self.user_inputs.append(key)
            self.update_output(key)
        elif key in Calculator.OPERATORS:
            if self.user_inputs[-1] in Calculator.OPERATORS:
                self.user_inputs[-1] = key
            else:
                self.user_inputs.append(key)
            self.update_output('')
        elif key == 'backspace' and self.user_inputs[-1].isdigit():
            self.user_inputs[-1] = self.user_inputs[-1][:-1]
            self.update_output(self.output_label.text()[:-1])
        if self.user_inputs[-1] == '':
            self.user_inputs[-1] = '0'

    def update_output(self, text):
        assert isinstance(text, str)
        self.output_label.setText(text)
        self.history_label.setText("".join(self.user_inputs))

    def calculate(self):
        postfix = self.infix_to_postfix(self.user_inputs)
        stack = []
        for item in postfix:
            if item.isdigit():
                stack.append(int(item))
            else:
                if item == '+':
                    stack.append(stack.pop() + stack.pop())
                if item == '-':
                    stack.append(stack.pop() - stack.pop())
                if item == '*':
                    stack.append(stack.pop() * stack.pop())
                if item == '/':
                    stack.append(stack.pop() / stack.pop())
        print(stack)

    def infix_to_postfix(self, expr):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        postfix = []
        stack = []
        for item in expr:
            if item.isdigit():
                postfix.append(item)
            else:
                if not stack:
                    stack.append(item)
                else:
                    if precedence[item] > precedence[stack[-1]]:
                        stack.append(item)
                    else:
                        while precedence[item] <= precedence[stack[-1]]:
                            postfix.append(stack.pop())
                            if not stack:
                                break
                        stack.append(item)
        while stack:
            postfix.append(stack.pop())
        return postfix

    def buttons(self):
        self.buttons = {}
        buttons_text = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', 'x'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]
        for row, _ in enumerate(buttons_text):
            for col, key in enumerate(buttons_text[row]):
                self.buttons[key] = QPushButton(key)
                self.buttons[key].clicked.connect(partial(self.button_click, key=key))
                self.buttons_layout.addWidget(self.buttons[key], row, col)

    def button_click(self, key):
        pass

    def test():
        print('test')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
