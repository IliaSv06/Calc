from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from variables import *
import History_Calc as hc


class Calc(QWidget):
    """ЭТОТ КЛАСС РЕАЛИЗУЕТ БАЗОВЫЙ МОД КАЛЬКУЛЯТОРА"""
    def __init__(self, widgets, change_frame, box_main):
        super().__init__(parent=None)
        self.widgets = widgets
        self.box_main = box_main
        self.change_frame = change_frame
        self.list_operation = list_operation
        self.num = num
        self.open_brackets = 0  # открытые скобки
        self.widgets_sinvols = [('C', '7', '4', '1', '+/-'),
                                ('()', '8', '5', '2', '0'),
                                ('√', '9', '6', '3', '.'),
                                ('/', 'x', '-', '+', '=')]
        self.call_functions = {'C': self.clear_all_result, '%': self.operations_with_percent, '=': self.operation,
                               '+/-': self.revere, '()': self.brackets, '√': self.root_print}
        self.styles_buttons = {'C': ('', 'DelAll'), '=': ('', 'equally'),
                               '/': ('icons/divid.png', 'divid'), 'x': ('icons/mul.png', 'mul')}

    def frame1(self):
        """Мод - Калькулятор"""
        self.system_numbers = QSpinBox()
        self.system_numbers.setValue(10)
        self.box_numbers = QHBoxLayout()  # блок который хранит окно вывода
        self.line = self.HLine()
        self.box_hr_top = QHBoxLayout()
        self.box_hr = QHBoxLayout()

        # реализует блок с основными копками калькулятора (нижняя часть)
        self.make_buttons(self.widgets_sinvols)

        # реализация верхней части калькулятора
        self.make_opiration_label()
        self.list_mod.addItems(['Калькулятор', 'Системы счисления'])

        # реализация иконки для кнопок
        self.button_del.setIcon(QIcon('icons/del.png'))
        self.button_del.setIconSize(QSize(30, 30))

        self.box_hr_top.addStretch()
        self.box_hr_top.addWidget(self.widgets['button'][-1])

        self.box_numbers.addStretch()
        self.box_numbers.addWidget(self.widgets['label_output'][-1])

        # отображение всех виджитов
        self.open_widgets()

        self.button_del.clicked.connect(self.clear_number)
        self.list_mod.activated.connect(self.change_frame)

    def open_widgets(self):
        """Отображение всех виджитов"""
        self.box_main.addWidget(self.widgets['list_mod'][-1], Qt.AlignTop | Qt.AlignRight)
        self.box_main.addWidget(self.widgets['labels'][-1], Qt.AlignTop)
        self.box_main.addLayout(self.box_numbers)
        self.box_main.addLayout(self.box_hr_top)
        self.box_main.addWidget(self.widgets['line'][-1], Qt.AlignTop)

        self.box_main.addLayout(self.box_hr)
        self.box_main.setAlignment(Qt.AlignTop)

    def make_opiration_label(self):
        """Реализация верхней части калькулятора"""
        self.button_del = QPushButton('')
        self.label_output = QLabel('')
        self.label_output_opiration = QLabel('')
        self.list_mod = QComboBox()
        self.line = self.HLine() # сдесь горизонтальная линия

        # реализация конпки удаления
        self.button_del.setIcon(QIcon('icons/del.png'))
        self.button_del.setIconSize(QSize(30, 30))
        self.button_del.setObjectName('del')

        self.label_output.setAlignment(Qt.AlignTop | Qt.AlignRight)
        self.label_output_opiration.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.label_output_opiration.setObjectName('label_opir')

        self.widgets['line'].append(self.line)
        self.widgets['list_mod'].append(self.list_mod)
        self.widgets['labels'].append(self.label_output_opiration)
        self.widgets['label_output'].append(self.label_output)
        self.widgets['button'].append(self.button_del)

    def make_buttons(self, widgets_sinvols):
        """Реализует кнопки"""
        for widgets in widgets_sinvols:
            box_vertical = QVBoxLayout()
            for widget in widgets:
                button = QPushButton(widget)
                if widget in self.styles_buttons.keys():
                    button.setIcon(QIcon(self.styles_buttons[widget][0]))
                    button.setIconSize(QSize(25, 25))
                    button.setObjectName(self.styles_buttons[widget][1])
                if widget in self.call_functions.keys():
                    button.clicked.connect(self.call_functions[widget])
                else:
                    button.clicked.connect(self.write_number)
                self.widgets['button'].append(button)
                box_vertical.addWidget(self.widgets['button'][-1])

            self.box_hr.addLayout(box_vertical)

    def HLine(self):
        """Создает горизонтальную линию во frame1 и frame2"""
        line = QFrame()
        line.setStyleSheet("background-color: #250250250")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def write_number(self):
        """Выводит число"""
        sender = self.sender().text()  # определяет нажутю кнопку
        opiration = self.label_output.text()
        if sender == 'x²' or sender == 'xⁿ':
            self.print_degree(sender)

        elif len(opiration) == 0 and sender not in list_operation:
            self.label_output.setText(opiration + sender)

        elif len(opiration) > 0 and sender in num:
            if opiration[-1] == '√':
                self.label_output.setText(opiration + '(' + sender)
                self.open_brackets += 1
            elif opiration[-1] == ')':
                self.label_output.setText(opiration + 'x' + sender)
            else:
                self.label_output.setText(opiration + sender)

        elif len(opiration) > 0 and sender in list_operation:
            if opiration[-1] in list_operation and opiration[-2] in '(√' and sender in list_operation[:3]:
                self.label_output.setText(opiration[:-1])
            elif opiration[-1] in list_operation:
                self.label_output.setText(opiration[:-1] + sender)

            elif opiration[-1] in '(√' and sender in list_operation[:3]:
                return None
            else:
                self.label_output.setText(opiration + sender)

        self.count_now()  # запустит функцию автоматического вычисления

    def root_print(self):
        """Выводит корень на экран"""
        try:
            if len(self.label_output.text()) == 0:
                self.label_output.setText(self.label_output.text() + '√(')
                self.open_brackets += 1
            elif len(self.label_output.text()) != 0:
                if any([self.label_output.text()[-1] in self.list_operation, self.label_output.text()[-1] == '(',
                       self.label_output.text()[-1] == '√(']):
                    self.label_output.setText(self.label_output.text() + '√(')
                    self.open_brackets += 1
                elif self.label_output.text()[-1] in self.num:
                    self.label_output.setText(self.label_output.text() + 'x√(')
                    self.open_brackets += 1
        except:
            pass

    def brackets(self):
        """Расставляет скобки"""
        try:
            if len(self.label_output.text()) == 0:
                self.label_output.setText('(')
                self.open_brackets += 1
            elif len(self.label_output.text()) != 0:
                if all([self.label_output.text()[-1] not in self.list_operation,
                        self.open_brackets > 0,
                        self.label_output.text()[-1] != '(']):
                    self.label_output.setText(self.label_output.text() + ')')
                    self.open_brackets -= 1
                elif any([self.label_output.text()[-1] in self.num,
                          self.label_output.text()[-1] == ')']):
                    self.label_output.setText(self.label_output.text() + 'x(')
                    self.open_brackets += 1
                elif any([self.label_output.text()[-1] in self.list_operation,
                          self.label_output.text()[-1] == '(',
                          self.label_output.text()[-1] == '√']):
                    self.label_output.setText(self.label_output.text() + '(')
                    self.open_brackets += 1
        except:
            pass
    def print_degree(self, button):
        """Печатает степень"""
        opiration = self.label_output.text()
        if len(opiration) == 0:
            return None
        elif button == 'x²':
            if opiration[-1] in self.num or opiration[-1] == ')':
                self.label_output.setText(opiration + '^(2)')
            elif opiration[-1] in self.list_operation:
                self.label_output.setText(opiration[:-1] + '^(2)')

        elif button == 'xⁿ' and opiration[-1] != '(':
            if opiration[-1] in self.num or opiration[-1] == ')':
                self.label_output.setText(opiration + '^(')
            elif opiration[-1] in self.list_operation:
                self.label_output.setText(opiration[:-1] + '^(')
            self.open_brackets += 1

        self.count_now()

    def close_brackets(self, expression):
        """Закрывает скобки для расчёта"""
        return expression + ')' * self.open_brackets

    def revere(self):
        """Меняет знак последнего числа"""
        opiration = self.label_output.text()
        if len(opiration) == 0:
            self.open_brackets += 1
            self.label_output.setText('(-')

        elif opiration[-2:] == '(-':
            self.label_output.setText(opiration[:-2])
            self.open_brackets -= 1

        elif opiration[:2] == '(-':
            self.label_output.setText(opiration[2:])
            self.open_brackets -= 1

        elif opiration[-1] == ')':
            self.label_output.setText(opiration + 'x(-')
            self.open_brackets += 1

        elif not self.synvol_search():  # если оператор не содержится в выражении (только для числа)
            self.label_output.setText(f'(-{opiration}')
            self.open_brackets += 1

        elif opiration[-1] in self.list_operation:
            self.label_output.setText(opiration + '(-')
            self.open_brackets += 1

        elif opiration[-1] in self.num:  # добавляет знак перед числом если есть операторы в выражении
            i = -1
            while opiration[i] in self.num:
                i -= 1
            if opiration[i - 1:i + 1] != '(-':
                self.label_output.setText(opiration[:i + 1] + '(-' + opiration[i + 1:])
                self.open_brackets += 1

            elif opiration[i - 1:i + 1] == '(-':
                self.label_output.setText(opiration[:i - 1] + opiration[i + 1:])
                self.open_brackets -= 1
        self.count_now()

    def count_now(self):
        """Автоматически вычисляет выражение"""
        try:
            expression = self.label_output.text().replace('x', '*')
            result = self.metod_opiration(expression)
            if isinstance(result, float):
                result = round(result, 4)
            self.label_output_opiration.setText('=' + str(result))
        except:
            pass

    def metod_opiration(self, expression : str):
        """Выбирает какой метод вычислений выбрать для определенных модов калькулятора"""
        if self.list_mod.currentText() == 'Системы счисления':
            result = self.eval_notation(expression)
        else:
            expression = self.close_brackets(expression)
            expression = self.rootExstration(expression)
            expression = expression.replace('^', '**')
            result = eval(expression)
        return result

    def operation(self):
        """Запускает вычисление над выражением и фиксирует результат"""
        try:
            opiration = self.label_output.text()
            if opiration[-1] in self.list_operation:
                self.label_output.setText(opiration[:-1])
            elif opiration[-1] == '(':
                self.label_output.setText(opiration[:-2])
                self.open_brackets -= 1
            if len(opiration) != 0:
                opiration = self.label_output.text()
                expression = opiration.replace('x', '*') # заменяет x на * для вычисления
                result = self.metod_opiration(expression)
                self.open_barckets = 0
                if isinstance(result, float):
                    result = round(result, 4)
                result = str(result)
                hc.InsertData(opiration, result)
                opiration = self.close_brackets(opiration)
                self.label_output_opiration.setText(opiration + '=')
                self.label_output.clear()
                self.label_output.setText(result)
                self.list_history.clear()
                self.list_history.addItems([''] + hc.SelectData())
                self.list_history.setItemIcon(0, self.icon_history)
                self.list_history.setIconSize(QSize(20, 20))
        except:
            pass

    def operations_with_percent(self):
        """Перевод в проценты"""
        try:
            expression = self.label_output_opiration.text()
            self.label_output.clear()
            self.label_output.setText(str(float(expression[1:]) / 100))
            self.open_brackets = 0
        except:
            self.label_output.clear()
            self.open_brackets = 0

    def clear_number(self):
        """Удаляет один элемент текста"""
        try:
            self.removing_brackets()  # удаление скобок
            self.label_output.setText(self.label_output.text()[:-1:])
            if len(self.label_output.text()) == 0:
                self.label_output_opiration.setText('')

            elif self.label_output.text()[-1] not in self.list_operation:
                self.count_now()
        except:
            pass

    def removing_brackets(self):
        """Удаляет скобки"""
        if self.label_output.text()[-1] == '(' and self.open_brackets > 0:
            self.open_brackets -= 1
        elif self.label_output.text()[-1] == ')':
            self.open_brackets += 1

    def clear_all_result(self):
        """Отчищает виджеты от данных"""
        self.open_brackets = 0
        self.label_output.clear()
        self.label_output_opiration.clear()

    def synvol_search(self):
        """Ищет оператор(+ / - *) в тексте виджита"""
        for i in self.list_operation:
            if i in self.label_output.text():
                return True
        return False

    def rootExstration(self, expression: str):
        """Подготавливает выражение для извлечения корня"""
        if '√' in expression:
            result = ''
            root = []  # фиксирует нашедший корень (в виде **0.5)
            expression = list(expression)

            for sign in range(len(expression)):
                if expression[sign] == '(':
                    if expression[sign - 1] == '√' and sign != 0:
                        root.append('**0.5)')
                    else:
                        root.append(')')
                    result += expression[sign] + '('

                elif expression[sign] == ')':
                    result += expression[sign] + root[-1]
                    root.pop(-1)
                elif expression[sign] != '√':
                    result += expression[sign]
            return result
        return expression


