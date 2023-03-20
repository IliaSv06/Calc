from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from function import numbers_flout, numbers_int, numbers_10, conversion_expression, counting
from calc import Calc

class FrameSystemNumbers(Calc):

    """ЭТОТ КЛАСС ПРЕДСТАВЛЯЕТ РЕАЛИЗАЦИЮ ФРЕЙМА "СИСТЕМЫ СЧИСЛЕНИЯ"""""

    def __init__(self, widgets, change_frame, box_main):
        super(FrameSystemNumbers, self).__init__(widgets, change_frame, box_main)
        self.call_functions = {'CE': self.clear_all_result, '%': self.operations_with_percent, '=': self.operation,
                               '+/-': self.revere}
        self.styles_buttons = {'CE': ('', 'DelAll'), '=': ('', 'resultNumbers'),
                               '/': ('icons/divid.png', 'divid'), 'x': ('icons/mul.png', 'mul')}
        self.signNumbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')

        self.widgets_text = [('A', 'B', 'C', 'D', 'E', 'F'),
                             ('x²', '()', '7', '4', '1', '+/-'),
                             ('xⁿ', '√', '8', '5', '2', '0'),
                             ('CE', '%', '9', '6', '3', '.'),
                             ('/', 'x', '-', '+', '=')]

    def frame2(self):
        self.box_hr_top = QHBoxLayout() # будет хронить кнопку
        self.box_hr = QHBoxLayout()
        self.box_v_num = QVBoxLayout()
        self.box_numbers = QHBoxLayout()  # блок который хранит регулятор основания Ссч и окно вывода
        self.system_numbers = QSpinBox()
        self.make_buttons(self.widgets_text)
        self.make_opiration_label()

        # реализация регулятора Ссч
        self.widgets['spin_boxes'].append(self.system_numbers)
        self.system_numbers.setValue(10)
        self.number_first = self.system_numbers.value()
        self.box_v_num.addWidget(self.widgets['spin_boxes'][-1])
        self.box_v_num.setAlignment(Qt.AlignBottom)

        # кнопка удаления
        self.box_hr_top.addStretch()
        self.box_hr_top.addWidget(self.widgets['button'][-1])

        self.list_mod.addItems(['Системы счисления', 'Калькулятор'])

        self.box_numbers.addStretch()
        self.box_numbers.addWidget(self.widgets['label_output'][-1], Qt.AlignRight)
        self.box_numbers.addLayout(self.box_v_num, stretch=0)

        # отображение всех виджитов
        self.open_widgets()
        self.blockButtons()

        self.list_mod.activated.connect(self.change_frame)
        self.button_del.clicked.connect(self.clear_number)
        self.system_numbers.valueChanged.connect(self.blockButtons)

    def blockButtons(self, number=10):
        """Блокирует кнопки с числами, которые неотносятся к данной системе счисления"""
        if number > 16 or number < 2:
            self.system_numbers.setValue(self.number_first)
            return None
        self.convert(self.number_first)
        for button in self.widgets['button']:
            # разблокирует кнопки предавая им исходный стиль
            if button.text() in self.signNumbers[:number]:
                button.setEnabled(True)
                button.setStyleSheet("QPushButton {background-color: rgb(50, 50, 50); color: white;}"
                                     "QPushButton::hover {background-color : rgb(38, 38, 38);}")
            # блокирует кнопки
            if button.text() in self.signNumbers[number:] and number != 16:
                button.setStyleSheet('background-color: rgb(40, 40, 40); color: rgb(50, 50, 50);')
                button.setEnabled(False)
        self.count_now()
        self.number_first = number


    def convert(self, number):
        """Меняет числа в выражении"""
        self.label_output.setText(
            conversion_expression(self.label_output.text(), number, int(self.system_numbers.text())))  # меняет текст в label_output

    def eval_notation(self, expression):
        """Функция считает результат"""
        notation = self.system_numbers.value()
        expression = conversion_expression(expression, notation, 10) # переволит числа в выражении в нужную Ссч
        if '(' in expression or '√' in expression:
            expression = self.close_brackets(expression)
            expression = self.rootExstration(expression)

        expression = expression.replace('^', '**')
        expression_10 = eval(expression) # вычисляет выражение работая с десятичными числами
        return numbers_flout(expression_10, notation)  # переводит результат в нужнную Ссч

