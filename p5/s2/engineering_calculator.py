import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from enum import Enum
from calculator import Calculator
import math


def create_btn(label, on_click=None, color='lightgray', width=80):
    button = QPushButton(label)
    button.setFixedSize(width, 60)
    button.setFont(QFont('Arial', 12))
    button.setStyleSheet(
        f'background-color: {color}; border: 1px solid gray; border-radius: 8px;'
    )
    if on_click:
        button.clicked.connect(on_click)
    return button


class EngineeringCalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = EngineeringCalculator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Engineering Calculator')
        self.setFixedSize(800, 500)
        self.center()

        # 메인 레이아웃
        main_layout = QVBoxLayout()

        # 디스플레이 영역
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setFont(QFont('Arial', 24))
        self.display.setStyleSheet(
            'background-color: black; color: white; padding: 15px; border-radius: 8px;'
        )
        self.display.setFixedHeight(80)
        main_layout.addWidget(self.display)

        # 버튼 영역
        self.grid = QGridLayout()
        self.grid.setSpacing(3)

        # 첫 번째 행 - 공학 함수들
        self.grid.addWidget(create_btn('(', color='lightblue'), 0, 0)
        self.grid.addWidget(create_btn(')', color='lightblue'), 0, 1)
        self.grid.addWidget(create_btn('mc', color='lightblue'), 0, 2)
        self.grid.addWidget(create_btn('m+', color='lightblue'), 0, 3)
        self.grid.addWidget(create_btn('m-', color='lightblue'), 0, 4)
        self.grid.addWidget(create_btn('mr', color='lightblue'), 0, 5)
        self.grid.addWidget(create_btn('AC', self.on_ac_click, 'lightblue'), 0, 6)
        self.grid.addWidget(
            create_btn('+/-', lambda: self.on_unary_operator_click('+/-'), 'lightblue'),
            0,
            7,
        )
        self.grid.addWidget(
            create_btn('%', lambda: self.on_binary_operator_click('%'), 'lightblue'),
            0,
            8,
        )
        self.grid.addWidget(
            create_btn('÷', lambda: self.on_binary_operator_click('÷'), 'orange'), 0, 9
        )

        # 두 번째 행
        self.grid.addWidget(create_btn('2nd', color='lightblue'), 1, 0)
        self.grid.addWidget(
            create_btn('x²', lambda: self.on_unary_operator_click('x²'), 'lightblue'),
            1,
            1,
        )
        self.grid.addWidget(
            create_btn('x³', lambda: self.on_unary_operator_click('x³'), 'lightblue'),
            1,
            2,
        )
        self.grid.addWidget(create_btn('xʸ', color='lightblue'), 1, 3)
        self.grid.addWidget(create_btn('eˣ', color='lightblue'), 1, 4)
        self.grid.addWidget(create_btn('10ˣ', color='lightblue'), 1, 5)
        self.grid.addWidget(create_btn('7', lambda: self.on_number_click('7')), 1, 6)
        self.grid.addWidget(create_btn('8', lambda: self.on_number_click('8')), 1, 7)
        self.grid.addWidget(create_btn('9', lambda: self.on_number_click('9')), 1, 8)
        self.grid.addWidget(
            create_btn('×', lambda: self.on_binary_operator_click('×'), 'orange'), 1, 9
        )

        # 세 번째 행
        self.grid.addWidget(create_btn('1/x', color='lightblue'), 2, 0)
        self.grid.addWidget(create_btn('²√x', color='lightblue'), 2, 1)
        self.grid.addWidget(create_btn('³√x', color='lightblue'), 2, 2)
        self.grid.addWidget(create_btn('ʸ√x', color='lightblue'), 2, 3)
        self.grid.addWidget(create_btn('ln', color='lightblue'), 2, 4)
        self.grid.addWidget(create_btn('log₁₀', color='lightblue'), 2, 5)
        self.grid.addWidget(create_btn('4', lambda: self.on_number_click('4')), 2, 6)
        self.grid.addWidget(create_btn('5', lambda: self.on_number_click('5')), 2, 7)
        self.grid.addWidget(create_btn('6', lambda: self.on_number_click('6')), 2, 8)
        self.grid.addWidget(
            create_btn('-', lambda: self.on_binary_operator_click('-'), 'orange'), 2, 9
        )

        # 네 번째 행
        self.grid.addWidget(create_btn('x!', color='lightblue'), 3, 0)
        self.grid.addWidget(
            create_btn('sin', lambda: self.on_unary_operator_click('sin'), 'lightblue'),
            3,
            1,
        )
        self.grid.addWidget(
            create_btn('cos', lambda: self.on_unary_operator_click('cos'), 'lightblue'),
            3,
            2,
        )
        self.grid.addWidget(
            create_btn('tan', lambda: self.on_unary_operator_click('tan'), 'lightblue'),
            3,
            3,
        )
        self.grid.addWidget(create_btn('e', color='lightblue'), 3, 4)
        self.grid.addWidget(create_btn('EE', color='lightblue'), 3, 5)
        self.grid.addWidget(create_btn('1', lambda: self.on_number_click('1')), 3, 6)
        self.grid.addWidget(create_btn('2', lambda: self.on_number_click('2')), 3, 7)
        self.grid.addWidget(create_btn('3', lambda: self.on_number_click('3')), 3, 8)
        self.grid.addWidget(
            create_btn('+', lambda: self.on_binary_operator_click('+'), 'orange'), 3, 9
        )

        # 다섯 번째 행
        self.grid.addWidget(create_btn('Rad', color='lightblue'), 4, 0)
        self.grid.addWidget(
            create_btn(
                'sinh', lambda: self.on_unary_operator_click('sinh'), 'lightblue'
            ),
            4,
            1,
        )
        self.grid.addWidget(
            create_btn(
                'cosh', lambda: self.on_unary_operator_click('cosh'), 'lightblue'
            ),
            4,
            2,
        )
        self.grid.addWidget(
            create_btn(
                'tanh', lambda: self.on_unary_operator_click('tanh'), 'lightblue'
            ),
            4,
            3,
        )
        self.grid.addWidget(
            create_btn('π', lambda: self.on_unary_operator_click('π'), 'lightblue'),
            4,
            4,
        )
        self.grid.addWidget(create_btn('Rand', color='lightblue'), 4, 5)

        # 0버튼은 2칸 차지
        self.grid.addWidget(
            create_btn('0', lambda: self.on_number_click('0'), width=165), 4, 6, 1, 2
        )

        self.grid.addWidget(
            create_btn('.', lambda: self.on_unary_operator_click('.')), 4, 8
        )
        self.grid.addWidget(create_btn('=', self.on_equal_click, 'orange'), 4, 9)

        main_layout.addLayout(self.grid)
        self.setLayout(main_layout)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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


class EngineeringCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.unary = {
            **self.unary,
            'x²': self.double,
            'x³': self.triple,
            'π': self.pi,
            'sin': self.sin,
            'cos': self.cos,
            'tan': self.tan,
            'sinh': self.sinh,
            'cosh': self.cosh,
            'tanh': self.tanh,
        }

    def double(self):
        self.result = math.pow(float(self.display), 2)
        self.display = str(self.result)

    def triple(self):
        self.result = math.pow(float(self.display), 3)
        self.display = str(self.result)

    def pi(self):
        self.result = math.pi
        self.display = str(self.result)

    def sin(self):
        self.result = math.sin(float(self.display))
        self.display = str(self.result)

    def cos(self):
        self.result = math.cos(float(self.display))
        self.display = str(self.result)

    def tan(self):
        self.result = math.tan(float(self.display))
        self.display = str(self.result)

    def sinh(self):
        self.result = math.sinh(float(self.display))
        self.display = str(self.result)

    def cosh(self):
        self.result = math.cosh(float(self.display))
        self.display = str(self.result)

    def tanh(self):
        self.result = math.tanh(float(self.display))
        self.display = str(self.result)


def main():
    app = QApplication(sys.argv)
    ex = EngineeringCalculatorUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
