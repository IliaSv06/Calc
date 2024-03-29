from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
import os
import History_Calc as hc
from calc import Calc
from systemNumbers import FrameSystemNumbers
from variables import *
from function import filter

class MainWindow(QWidget):
    """ЯДРО ПРОЕКТА. ОНО СВЯЗЫВАЕТ МОДЫ КАЛЬКУЛЯТОРА (БАЗОВЫЙ И СИСТЕМЫ СЧИСЛЕНИЯ)"""
    def __init__(self, parent = None):
        super().__init__(parent)
        self.resize(380, 550)
        self.move(500, 20)
        self.setWindowTitle('Calc')
        self.widgets = {
            'button': [],
            'label_output': [],
            'list_mod': [],
            'lines': [],      # словарь для хранения всех активных виджитов
            'labels': [],
            'list_history': [],
            'line': [],
            'spin_boxes': []
        }
        self.box_main = QVBoxLayout()
        self.calc = Calc(self.widgets, self.change_frame, self.box_main)
        self.system_number_frame = FrameSystemNumbers(self.widgets, self.change_frame, self.box_main)
        self.new_frame_1()
        self.setLayout(self.box_main)
        self.setFocus() # фокусировка на окно приложения (чтобы была возможность печать текст с клавиатуры)

    def clear_widgets(self):
        """Очищает экран от виджетов"""
        for widget in self.widgets:
            if self.widgets[widget] != []:
                for i in range(0, len(self.widgets[widget])):
                    self.widgets[widget][-1].hide()
                    self.widgets[widget].pop()

    def change_frame(self):
        """Мненяет фрейм у приложения"""
        sender_text = self.widgets['list_mod'][-1].currentText()
        if sender_text == 'Калькулятор':
            self.widgets = self.calc.widgets
            self.new_frame_1()

        elif sender_text == 'Системы счисления':
            self.widgets = self.system_number_frame.widgets
            self.new_frame_2()

        self.setFocus() 

    def new_frame_1(self):
        """Пререход в мод калькулятор"""
        for i in range(2):
            self.clear_widgets()
            self.calc.frame1()
            self.box_main = self.calc.box_main
            self.calc.open_brackets = 0

    def new_frame_2(self):
        """Пререход в мод Системы счисления"""
        self.clear_widgets()
        self.system_number_frame.frame2()
        self.box_main = self.system_number_frame.box_main
        self.system_number_frame.open_brackets = 0

    def keyPressEvent(self, event):
        """Печатает данные, полученные от нажатых кномпок клавиатуры"""
        sender_text = self.widgets['list_mod'][-1].currentText()
        if event.key() == Qt.Key_Escape:
            sys.exit()

        elif event.text() in list_operation or event.text() in num:
            if sender_text == "Калькулятор":
                sign = filter(event.text())
                if sign:
                    self.calc.write_number(sign)
            else:
                number = self.system_number_frame.system_numbers.currentText() # основание Ссч 
                sign = filter(event.text(), int(number))
                if sign:
                    self.system_number_frame.write_number(sign)

        elif event.text() in '()' and event.key() not in limit_buttons:
            if sender_text == "Калькулятор":
                self.calc.brackets()
            else:
                self.system_number_frame.brackets()

        elif event.key() == Qt.Key_Backspace:
            if sender_text == "Калькулятор":
                self.calc.clear_number()
            else:
                self.system_number_frame.clear_number()

if __name__ == '__main__':
    if not os.path.isfile('History.db'):
        hc.CreateDB()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    with open('styles_calc.css', 'r') as file_css:
        _style = file_css.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec_())