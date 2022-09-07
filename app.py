import sys
from functools import partial
import re
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QWidget,
)
from PyQt5.Qt import Qt
from PyQt5.QtGui import QFont


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Multi tabs calculator"
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tabs = QTabWidget()


class Calculator(QWidget):
    OPERATORS = ('+', '-', '*', '/')

    def __init__(self, parent, name):
        super().__init__(parent)
        self.setWindowTitle("Multi tabs calculator")

        self.layout = QVBoxLayout()

        self.output_layout = QVBoxLayout()
        self.buttons_layout = QGridLayout()

        self.output_label = QLabel("0")
        self.output_label.setFont(QFont('Open Sans', 20))

        self.history_label = QLabel('')
        self.output_layout.addWidget(self.history_label)
        self.output_layout.addWidget(self.output_label)
        self.layout.addLayout(self.output_layout)
        self.layout.addLayout(self.buttons_layout)

        self.buttons()
        self.setLayout(self.layout)
        parent.tabs.addTab(self, name)
        parent.setCentralWidget(parent.tabs)

        self._last_operator = ''
        self._last_operand = ''
        self._last_result = ''
        self.user_inputs = ['0']
        self.setFocus()

    def keyPressEvent(self, event):
        for i in range(10):
            if event.key() == getattr(Qt, f'Key_{i}'):
                self.update_user_input(str(i))
        if event.key() == Qt.Key_Plus:
            self.update_user_input('+')
        if event.key() == Qt.Key_Minus:
            self.update_user_input('-')
        if event.key() == Qt.Key_Asterisk:
            self.update_user_input('*')
        if event.key() == Qt.Key_Slash:
            self.update_user_input('/')
        if event.key() in (Qt.Key_Plus, Qt.Key_Minus,  Qt.Key_Asterisk, Qt.Key_Slash):
            if len(self.user_inputs) % 2 == 0 and len(self.user_inputs) > 2:
                result = self.calculate(self.user_inputs[:-1])
                self.update_output(str(result))
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
            self.update_output(self.user_inputs[-1])
        if self.user_inputs[-1] == '':
            self.user_inputs[-1] = '0'

    def update_output(self, text):
        assert isinstance(text, str)
        thousands_seprator = lambda item: "{:,}".format(int(item)) if item.isdigit() else item
        self.output_label.setText(thousands_seprator(text))
        self.history_label.setText("".join(map(thousands_seprator, self.user_inputs)))

    def calculate(self, infix_expr):
        postfix = self.infix_to_postfix(infix_expr)
        stack = []
        for item in postfix:
            if item.isdigit():
                stack.append(int(item))
            else:
                a = stack.pop()
                b = stack.pop()
                if item == '+':
                    stack.append(a + b)
                if item == '-':
                    stack.append(b - a)
                if item == '*':
                    stack.append(a * b)
                if item == '/':
                    stack.append(b / a)
        return stack[0]

    def infix_to_postfix(self, expr):
        assert len(expr) % 2 == 1
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
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]
        for row, _ in enumerate(buttons_text):
            for col, key in enumerate(buttons_text[row]):
                self.buttons[key] = QPushButton(key)
                self.buttons[key].clicked.connect(partial(self.button_click, key=key))
                self.buttons_layout.addWidget(self.buttons[key], row, col)

    def button_click(self, key):
        self.update_user_input(key)

    def test():
        print('test')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    calculator = Calculator(ex,'&1')
    calculator2 = Calculator(ex, '&2')
    ex.show()
    sys.exit(app.exec_())
