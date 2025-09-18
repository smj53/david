import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from enum import Enum


def create_btn(label, on_click=None, color='lightgray', width=100):
    button = QPushButton(label)
    button.setFixedSize(width, 100)
    button.setFont(QFont('Arial', 20))
    button.setStyleSheet(
        f'background-color: {color}; border: 1px solid gray; border-radius: 10px;'
    )
    if on_click:
        button.clicked.connect(on_click)
    return button


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculator')
        self.center()
        self.resize(420, 600)

        main_layout = QVBoxLayout()

        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setFont(QFont('Arial', 40))
        self.display.setStyleSheet(
            'background-color: black; color: white; padding: 20px; border-radius: 10px;'
        )
        self.display.setFixedHeight(100)
        main_layout.addWidget(self.display)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        # Row 1
        self.grid.addWidget(create_btn('AC', self.on_ac_click, 'lightblue'), 0, 0)
        self.grid.addWidget(
            create_btn('+/-', lambda: self.on_unary_operator_click('+/-'), 'lightblue'),
            0,
            1,
        )
        self.grid.addWidget(
            create_btn('%', lambda: self.on_binary_operator_click('%'), 'lightblue'),
            0,
            2,
        )
        self.grid.addWidget(
            create_btn('÷', lambda: self.on_binary_operator_click('÷'), 'orange'), 0, 3
        )

        # Row 2
        self.grid.addWidget(create_btn('7', lambda: self.on_number_click('7')), 1, 0)
        self.grid.addWidget(create_btn('8', lambda: self.on_number_click('8')), 1, 1)
        self.grid.addWidget(create_btn('9', lambda: self.on_number_click('9')), 1, 2)
        self.grid.addWidget(
            create_btn('×', lambda: self.on_binary_operator_click('×'), 'orange'), 1, 3
        )

        # Row 3
        self.grid.addWidget(create_btn('4', lambda: self.on_number_click('4')), 2, 0)
        self.grid.addWidget(create_btn('5', lambda: self.on_number_click('5')), 2, 1)
        self.grid.addWidget(create_btn('6', lambda: self.on_number_click('6')), 2, 2)
        self.grid.addWidget(
            create_btn('-', lambda: self.on_binary_operator_click('-'), 'orange'), 2, 3
        )

        # Row 4
        self.grid.addWidget(create_btn('1', lambda: self.on_number_click('1')), 3, 0)
        self.grid.addWidget(create_btn('2', lambda: self.on_number_click('2')), 3, 1)
        self.grid.addWidget(create_btn('3', lambda: self.on_number_click('3')), 3, 2)
        self.grid.addWidget(
            create_btn('+', lambda: self.on_binary_operator_click('+'), 'orange'), 3, 3
        )

        # Row 5
        self.grid.addWidget(
            create_btn('0', lambda: self.on_number_click('0'), width=205), 4, 0, 1, 2
        )
        self.grid.addWidget(
            create_btn('.', lambda: self.on_unary_operator_click('.')), 4, 2
        )
        self.grid.addWidget(
            create_btn('=', lambda: self.on_equal_click(), 'orange'), 4, 3
        )

        main_layout.addLayout(self.grid)
        self.setLayout(main_layout)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_number_click(self, number):
        print(f'Number {number} clicked')
        self.calculator.set_number(number)
        self.update_display()

    def on_binary_operator_click(self, op):
        print(f'Binary Operator {op} clicked')
        self.calculator.set_binary_operator(op)
        self.update_display()

    def on_unary_operator_click(self, op):
        print(f'Unary Operator {op} clicked')
        self.calculator.set_unary_operator(op)
        self.update_display()

    def on_equal_click(self):
        print('equal click')
        self.calculator.set_equal()
        self.update_display()

    def on_ac_click(self):
        print('ac clicked')
        self.calculator.reset()
        self.update_display()

    def update_display(self):
        self.display.setText(self.calculator.display)


class Calculator:
    class Status(Enum):
        START = 1
        OP = 2
        NEXT = 3
        ERROR = 4

    def __init__(self):
        self.reset()
        self.unary = {'+/-': self.negative_positive, '.': self.dot}
        self.binary = {
            '+': self.add,
            '-': self.subtract,
            '÷': self.divide,
            '×': self.multiply,
            '%': self.percent,
        }

    def reset(self):
        self.prev = 0
        self.result = 0
        self.display = '0'
        self.operator = None
        self.status = Calculator.Status.START

    def set_number(self, number):
        print(self.status.name)
        match self.status:
            case Calculator.Status.START | Calculator.Status.NEXT:
                if self.display == '0':
                    self.display = number
                else:
                    self.display += number
            case Calculator.Status.OP:
                self.prev = float(self.display)
                self.display = number
                self.status = Calculator.Status.NEXT
            case Calculator.Status.ERROR:
                self.reset()

    def set_unary_operator(self, op):
        try:
            match self.status:
                case Calculator.Status.START | Calculator.Status.NEXT:
                    self.unary[op]()
                case Calculator.Status.OP:
                    self.unary[op]()
                    self.status = Calculator.Status.START
                case Calculator.Status.ERROR:
                    self.reset()
        except ValueError as e:
            self.display = str(e)
            self.status = Calculator.Status.ERROR
        except OverflowError:
            self.display = 'Overflow'
            self.status = Calculator.Status.ERROR
        except Exception:
            self.display = 'Error'
            self.status = Calculator.Status.ERROR

    def set_binary_operator(self, op):
        try:
            match self.status:
                case Calculator.Status.START | Calculator.Status.OP:
                    self.operator = op
                    self.status = Calculator.Status.OP
                case Calculator.Status.NEXT:
                    self.binary[self.operator]()
                    self.display = str(self.result)

                    self.operator = op
                    self.status = Calculator.Status.OP
                case Calculator.Status.ERROR:
                    self.reset()
        except ValueError as e:
            self.display = str(e)
            self.status = Calculator.Status.ERROR
        except OverflowError:
            self.display = 'Overflow'
            self.status = Calculator.Status.ERROR
        except Exception:
            self.display = 'Error'
            self.status = Calculator.Status.ERROR

    def set_equal(self):
        try:
            match self.status:
                case Calculator.Status.START | Calculator.Status.OP:
                    pass
                case Calculator.Status.NEXT:
                    self.binary[self.operator]()
                    self.display = str(self.result)

                    self.operator = None
                    self.prev = 0
                    self.status = Calculator.Status.START
                case Calculator.Status.ERROR:
                    self.reset()
        except ValueError as e:
            self.display = str(e)
            self.status = Calculator.Status.ERROR
        except OverflowError:
            self.display = 'Overflow'
            self.status = Calculator.Status.ERROR
        except Exception:
            self.display = 'Error'
            self.status = Calculator.Status.ERROR

    def get_value(self):
        return float(self.display)

    def add(self):
        self.result = self.prev + self.get_value()

    def subtract(self):
        self.result = self.prev - self.get_value()

    def multiply(self):
        self.result = self.prev * self.get_value()

    def divide(self):
        v = self.get_value()
        if v == 0:
            raise ValueError('0으로 나누기')
        self.result = self.prev / v

    def negative_positive(self):
        self.result = -self.get_value()
        self.display = str(self.result)

    def percent(self):
        v = self.get_value()
        if v == 0:
            raise ValueError('0으로 나누기')
        self.result = self.prev % self.get_value()

    def dot(self):
        if '.' in self.display:
            return
        self.display += '.'


def main():
    app = QApplication(sys.argv)
    ex = CalculatorUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
