#!/usr/bin/env python3
# coding=utf-8

import re
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

list_of_numbers = []


class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('uis/main.ui', self)

        self.setWindowTitle('Работа с массивами')

        self.btn_upload_data.clicked.connect(self.upload_data_from_file)
        self.btn_process_data.clicked.connect(self.process_data)
        self.btn_save_data.clicked.connect(self.save_data_in_file)
        self.btn_clear.clicked.connect(self.clear)

    def upload_data_from_file(self):
        """
        загружаем данные из файла
        :return: pass
        """
        global path_to_file
        path_to_file = QFileDialog.getOpenFileName(self, 'Открыть файл', '', "Text Files (*.txt)")[0]

        if path_to_file:
            file = open(path_to_file, 'r')

            data = file.read()
            # выводим считанные данные на экран
            self.plainTextEdit.appendPlainText(" Полученные данные: \n" + data + "\n")

            global list_of_numbers
            list_of_numbers = []

            # \b -- ищет границы слов
            # [0-9] -- описывает что ищем
            # + -- говорит, что искать нужно минимум от 1 символа
            for num in re.findall(r'-?[0-9]+\b', data):
                list_of_numbers.append("{0:3}".format(int(num)))

    def process_data(self):
        if validation_of_data():
            max_num_info = find_max()
            min_num_info = find_min()
            sum = find_sum_of_elements()
            print(min_num_info[0], min_num_info[1], max_num_info[0], max_num_info[1])
            # -*- выполнение задания -*-
            if sum > 100:
                solve(max_num_info[0],min_num_info[0],max_num_info[1],min_num_info[1])

                self.plainTextEdit.appendPlainText(" Данные обработаны! " + '\n')

                # выводим список на экран
                for k, i in enumerate (list_of_numbers):
                    if k > 24 or (k > 14 and k < 20) :
                        self.plainTextEdit.insertPlainText(" " + str(i))
                    else:
                        self.plainTextEdit.insertPlainText(str(i) + " ")
                    # чтобы текст был в виде таблицы, делаем отступ после
                    # 6 элемента
                    if ((k + 1) % 5) == 0:
                        self.plainTextEdit.appendPlainText("")
            else:
                self.plainTextEdit.appendPlainText(
                    "Сумма элементов меньше 100! \n")
        else:
            self.plainTextEdit.appendPlainText("Неправильно введены данные! "
                                               "Таблица должна быть размером "
                                               "5х6 и состоять из чисел! \n")

    def save_data_in_file(self):
        """
        сохраняем данные в выбранный нами файл
        :return:
        """

        if path_to_file:
            file = open(path_to_file.split(".")[0] + '-Output.txt', 'w')

            for k, i in enumerate(list_of_numbers):
                file.write(i + " ")
                if ((k+1) % 5) == 0:
                    file.write("\n")

            file.close()

            self.plainTextEdit.appendPlainText("Файл был успешно загружен! \n")
        else:
            self.plainTextEdit.appendPlainText("Для начала загрузите файл!")

    def clear(self):
        self.plainTextEdit.clear()


def find_max():
    """
    находим максимальное число в списке
    :return: максимальное число
    """
    max_num = float('-inf')
    max_pos = 0
    for k, i in enumerate(list_of_numbers):
        if max_num <= int(i):
            max_num = int(i)
            max_pos = k
    return [max_num, max_pos]

def find_min():
    min_num = float('inf')
    min_pos = 0
    for k, i in enumerate(list_of_numbers):
        if min_num >= int(i):
            min_num = int(i)
            min_pos = k
    return [min_num, min_pos]

def validation_of_data():
    """
    проверяем данные на валидность: всего должно быть ровно 30 ЧИСЕЛ
    :return: True - данные корректны, False - нет
    """
    if len(list_of_numbers) == 30:
        for i in list_of_numbers:
            try:
                float(i)
            except Exception:
                return False
        return True
    else:
        return False


def solve(max_num,min_num,max_pos,min_pos):
    """
    увеличение максимального числа в два раза
    :param max_num: максимальное число
    :return: pass
    """
    for n, i in enumerate(list_of_numbers):
        if int(i) == max_num:
            list_of_numbers[max_pos] = str(min_num)
        if int(i) == min_num:
            list_of_numbers[min_pos] = str(max_num)


    for j in range(2,len(list_of_numbers),5):
        list_of_numbers[j] = int(list_of_numbers[j]) // 2
    pass


def find_sum_of_elements():
    """
    находим сумму чисел из первой строки таблицы
    :return: сумму чисел из первой строки
    """
    sum = 0
    for i in range(len(list_of_numbers)):  # в строке должно быть ровно 6 чисел
        sum += int(list_of_numbers[i])
    return sum


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
