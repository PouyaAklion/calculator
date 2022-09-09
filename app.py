import sys
import re
from functools import partial
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
from PyQt5.QtCore import QEvent,QSize
from PyQt5.QtGui import QFont,QKeyEvent


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

        self.tabs = CustomTabWidget()


class CustomTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.new_tab_button = QPushButton('+')
        self.new_tab_button.setParent(self)
        self.new_tab_button.setFixedSize(28,28)
        self.new_tab_button.clicked.connect(self.create_new_tab)
        h = self.geometry().top()
        w = self.width()
        #self.new_tab_button.move(w-25, h)
        self.move_new_tab_button()
    
    #def sizeHint(self):
    #    sizeHint = super().sizeHint()
    #    width = sizeHint.width()
    #    height = sizeHint.height()
    #    return QSize(width, height)

    def create_new_tab(self):
        pass
    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.move_new_tab_button()

    def move_new_tab_button(self):
        size = sum([self.widget(i).width() for i in range(self.count())])
        h = self.geometry().top()
        w = self.width()
        if size > w: 
            self.new_tab_button.move(w-25, h)
        else:
            self.new_tab_button.move(size, h)


class Calculator(QWidget):
    OPERATORS = ('+', '-', '*', '/')
    p = re.compile('[-+]?\d+(\.\d+)?')

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

        self.create_buttons()
        self.setLayout(self.layout)
        parent.tabs.addTab(self, name)
        parent.setCentralWidget(parent.tabs)

        self._last_operator = ''
        self._last_result = ''
        self.user_inputs = ['0']
        self.history = []
        self.setFocus()
    
    @property
    def last_input(self):
        return self.user_inputs[-1]
    
    @last_input.setter
    def last_input(self, value):
        self.user_inputs[-1] = value


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
        if event.key() == Qt.Key_Backspace:
            self.update_user_input('backspace')
        if event.key() == Qt.Key_Delete:
            self.update_user_input('del')
        if event.key() == Qt.Key_Escape:
            self.update_user_input('esc')
        if event.key() == Qt.Key_Period:
            self.update_user_input('.')
        if event.key() in (Qt.Key_Plus, Qt.Key_Minus,  Qt.Key_Asterisk, Qt.Key_Slash, Qt.Key_Enter):
            if event.key() == Qt.Key_Enter:
                self.update_user_input('+')
            self.calculate_operation()
                
    def calculate_operation(self):
        if len(self.user_inputs) <=2:
            if self._last_result == '':
                self.update_output('',self.user_inputs)
            else:
                self.update_output('',[str(self._last_result)] + self.user_inputs)
        if len(self.user_inputs) % 2 == 0 and len(self.user_inputs) > 2 and self._last_result =='':
            self._last_result = self.calculate(self.user_inputs[:-1])
            self._last_operator = self.last_input
            self.history.append(self.user_inputs[:-1]) 
            self.update_output(str(self._last_result), self.user_inputs[:-1] + ['='])
            self.user_inputs = [str(self._last_operator)]
            
        if self._last_result != '' and len(self.user_inputs) >= 2:
            self.user_inputs = [str(self._last_result)] + self.user_inputs
            self._last_result = self.calculate(self.user_inputs[:-1])
            self._last_operator = self.last_input
            self.history.append(self.user_inputs[:-1]) 
            self.update_output(str(self._last_result), self.user_inputs[:-1] + ['='])
            self.user_inputs = [str(self._last_operator)]
    
    def update_user_input(self, key):
        if Calculator.p.match(key) and Calculator.p.match(self.last_input):
            if self.last_input == '0':
                self.last_input = key
            else:
                self.last_input = self.last_input + key
            self.update_output(self.last_input)
        elif Calculator.p.match(key) and not Calculator.p.match(self.last_input):
            self.user_inputs.append(key)
            self.update_output(key)
        elif key in Calculator.OPERATORS:
            if self.last_input in Calculator.OPERATORS:
                self.last_input = key
            else:
                self.user_inputs.append(key)
            self.update_output('')
        elif key == 'backspace' and Calculator.p.match(self.last_input):
            self.last_input = self.last_input[:-1]
            self.update_output(self.last_input)
        elif key == '.' and Calculator.p.match(self.last_input):
            if not '.' in self.last_input:
                self.last_input = self.last_input + key
                self.update_output(self.last_input)
        elif key == 'CE' or key == 'del':
            if Calculator.p.match(self.last_input):
                self.last_input = '0'
            self.update_output('0')
        elif key == 'C' or key == 'esc':
            self.reset()
        elif key == '=':
            print(key)
            self.calculate_operation()

        if self.last_input == '':
            self.last_input = '0'

    def update_output(self, output, prev_operation=[]):
        assert isinstance(output, str)
        self.output_label.setText(self.thousands_separator(output))
        self.history_label.setText("".join(map(self.thousands_separator, prev_operation)))
    
    def thousands_separator(self,number):
        if not Calculator.p.match(number):
            return number
        if number.endswith('.0'):
            return "{:,}".format(int(number[:-2]))
        if '.' in number:
            return "{:,}".format(float(number))
        return "{:,}".format(int(number))

    def calculate(self, infix_expr):
        postfix = self.infix_to_postfix(infix_expr)
        stack = []
        for item in postfix:
            if Calculator.p.match(item):
                stack.append(float(item))
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
            if Calculator.p.match(item):
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

    def reset(self):
        self.user_inputs = ['0']
        self._last_result = ''
        self._last_operator = ''
        self.update_output('0')

    def create_buttons(self):
        self.buttons = {}
        buttons_text = [
            ['C', 'CE', 'back', '#'],
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
        key_map = {
            'back': 'Backspace',
            '=': 'Enter',
            '+': 'Plus',
            '-': 'Minus',
            '*': 'Asterisk',
            '/': 'Slash',
            'C': 'Escape',
            'CE': 'Delete',
        }
        if key.isdigit():
            self.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress,getattr(Qt,f'Key_{key}'),Qt.NoModifier))
        elif key in key_map.keys():
            self.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress,getattr(Qt,f'Key_{key_map[key]}'),Qt.NoModifier))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    calculator = Calculator(ex, '&1')
    calculator2 = Calculator(ex, '&2')
    ex.show()
    sys.exit(app.exec_())
