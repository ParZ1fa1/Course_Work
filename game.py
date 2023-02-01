from PyQt5 import QtCore, QtGui, QtWidgets
from check_db import *
from des import *
import sys
from main import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywin = Interface()
    mywin.show()
    sys.exit(app.exec_())
