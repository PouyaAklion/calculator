import sys
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


class Calculator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi tabs calculator")

        self.app_layout = QVBoxLayout()
        self.output_layout = QHBoxLayout()
        self.buttons_layout = QGridLayout()

        self.output_layout.addWidget(QLabel("0"))

        self.app_layout.addLayout(self.output_layout)
        self.app_layout.addLayout(self.buttons_layout)
        self.buttons()
        self.setLayout(self.app_layout)

    def buttons(self):
        self.buttons = {}
        buttons_text = [
            ['7','8','9','/'],
            ['4','5','6','x'],
            ['1','2','3','-'],
            ['0','.','=','+']
        ]
        for row,_ in enumerate(buttons_text):
            for col,key in enumerate(buttons_text[row]):
                self.buttons[key] = QPushButton(key)
                self.buttons[key].clicked.connect(lambda: self.button_click(key))
                self.buttons_layout.addWidget(self.buttons[key],row,col)
    def button_click(self,key):
        print(key)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
