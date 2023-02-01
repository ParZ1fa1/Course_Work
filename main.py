import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from check_db import *
from des import *
from appearance import *
from extra import *


#rusalph
a = ord('а')
rusLow = [chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)]
a = ord('А')
rusCapital = [chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)]
#engalph
a = ord('a')
engLow = [chr(i) for i in range(a,a+26)]
a = ord('A')
engCapital = [chr(i) for i in range(a,a+26)]

def encrypt(msg):
    res = ''
    for c in msg:
        # ROT15 (Шифр Цезаря) - сдвиг символов на 15 позиций 
        if c in rusLow:
            idx = rusLow.index(c)
            idx += 15
            if idx >= len(rusLow):
                idx = idx - len(rusLow)
            res += rusLow[idx]
        elif c in rusCapital:
            idx = rusCapital.index(c)
            idx += 15
            if idx >= len(rusCapital):
                idx = idx - len(rusCapital)
            res += rusCapital[idx]
        elif c in engLow:
            idx = engLow.index(c)
            idx += 15
            if idx >= len(engLow):
                idx = idx - len(engLow)
            res += engLow[idx]
        elif c in engCapital:
            idx = engCapital.index(c)
            idx += 15
            if idx >= len(engCapital):
                idx = idx - len(engCapital)
            res += engCapital[idx]
        else:
            res += c
    return res
def decrypt(msg):
    res = ''
    for c in msg:
        if c in rusLow:
            idx = rusLow.index(c)
            idx -= 15
            if idx < 0:
                idx += len(rusLow)
            res += rusLow[idx]
        elif c in rusCapital:
            idx = rusCapital.index(c)
            idx -= 15
            if idx < 0:
                idx += len(rusCapital)
            res += rusCapital[idx]
        elif c in engLow:
            idx = engLow.index(c)
            idx -= 15
            if idx < 0:
                idx += len(engLow)
            res += engLow[idx]
        elif c in engCapital:
            idx = engCapital.index(c)
            idx -= 15
            if idx < 0:
                idx += len(engCapital)
            res += engCapital[idx]
        else:
            res += c
    return res


class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


        self.ui.pushButton.clicked.connect(self.reg)
        self.ui.pushButton_2.clicked.connect(self.auth)
        self.base_line_edit = [self.ui.lineEdit, self.ui.lineEdit_2]

        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_handler)


    # Проверка правильности ввода
    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            funct(self)
        return wrapper


    # Обработчик сигналов
    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)


    @check_input
    def auth(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_login(name, passw)
        self.open_game()

    @check_input
    def reg(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_register(name, passw)



    def open_game(self):
        clock = pg.time.Clock()
        screen = pg.display.set_mode(WINDOW_SIZE)

        playboard = Playboard(screen)

        run = True
        while run:
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                     playboard.button_down(event.button, event.pos)
                if event.type == pg.MOUSEBUTTONUP:
                    playboard.button_up(event.button, event.pos)

    pg.quit()

