from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from function import numbers_flout, numbers_int, numbers_10
from calc import Calc
# ЭТОТ КЛАСС ПРЕДСТАВЛЯЕТ РЕАЛИЗАЦИЮ ФРЕЙМА "СИСТЕМЫ СЧИСЛЕНИЯ"
class FrameSystemNumbers(Calc):
    def __init__(self, widgets, change_frame, box_main):
        super(FrameSystemNumbers, self).__init__(widgets, change_frame, box_main)
        self.call_functions = {'CE': self.clear_all_result, '%': self.operations_with_percent, '=': self.operation, '+/-': self.revere}
        self.styles_buttons = {'CE': ('', 'DelAll'), '=': ('', 'equally'),
                       '/': ('icons/divid.png', 'divid'), 'x': ('icons/mul.png', 'mul')}

        self.widgets_text = [('A', 'B', 'C', 'D', 'E', 'F'),
                             ('<<', '()', '7', '4', '1', '+/-'),
                             ('>>', '', '8', '5', '2', '0'),
                             ('CE', '%', '9', '6', '3', '.'),
                             ('', '/', 'x', '-', '+', '=')]

    def frame2(self):
        pass
        self.box_hr = QHBoxLayout()
        self.box_v_num = QVBoxLayout()
        self.box_numbers = QHBoxLayout()  # блок который хранит регулятор основания Ссч и окно вывода
        self.make_opiration_label()
        self.make_buttons(self.widgets_text)

        self.list_mod.addItems(['Системы счисления', 'Калькулятор'])
        self.box_numbers.addStretch()
        self.box_numbers.addWidget(self.widgets['label_output'][-1])

        self.box_main.addWidget(self.widgets['list_mod'][-1], Qt.AlignTop | Qt.AlignRight)
        self.box_main.addWidget(self.widgets['labels'][-1], Qt.AlignTop)
        self.box_main.addLayout(self.box_numbers)

        self.box_main.addLayout(self.box_hr)
        self.box_main.setAlignment(Qt.AlignTop)
        self.list_mod.activated.connect(self.change_frame)

    def clear_all(self):
        'Удаляет весь текст у виджитах во фрейме2'
        self.label_output.clear()
        self.widgets['lines'][0].clear()
        self.widgets['lines'][1].clear()
        self.widgets['lines'][2].clear()

    def function_for_frame2(self):
        '''Инициализурует функций по системам счисления'''
        number = self.widgets['lines'][0].text()  # число
        q = int(self.widgets['lines'][1].text())  # основане Ссч
        Nq = int(self.widgets['lines'][2].text())  # Ссч в которую нужно перевезти
        if q == 10:
            if '.' in number:
                result = numbers_flout(float(number), Nq)
            else:
                result = numbers_int(int(number), Nq)
        elif Nq == 10:
            result = numbers_10(number, q)

        self.label_output.setText(result)

