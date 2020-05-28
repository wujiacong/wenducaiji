import sys
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from UI import Ui_widget as Form
from PyQt5.QtCore import QTimer
import serial

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


class MainWindow(QtWidgets.QMainWindow, Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.open.clicked.connect(self.Open)
        self.cls.clicked.connect(self.Close)
        self.Readtimer = QTimer(self)
        self.Readtimer.timeout.connect(self.xunhuan)
        self.disabled()

    def Open(self):
        if self.connect():
            self.Readtimer.start(20)
            self.enabled()

    def Close(self):
        self.Readtimer.stop()
        self.unconnect()
        self.disabled()

    def connect(self):
        try:
            self.master = modbus_rtu.RtuMaster(serial.Serial(port="COM1", baudrate=9600, bytesize=8, parity="N", stopbits=1, xonxoff=0))
            self.master.set_timeout(1.0)
            self.master.set_verbose(True)
            self.master.open()
            return True

        except:
            QMessageBox.warning(self, " ", "打开失败", QMessageBox.Yes)
            return False

    def unconnect(self):
        try:
            self.master.close()
            self.master.__del__()
            return True
        except:
            QMessageBox.warning(self, " ", "关闭失败", QMessageBox.Yes)
            return False

    def enabled(self):
        self.cls.setEnabled(True)
        self.open.setEnabled(False)

    def disabled(self):
        self.cls.setEnabled(False)
        self.open.setEnabled(True)

    def xunhuan(self):
        try:
            a = self.master.execute(1, cst.READ_HOLDING_REGISTERS, 21, 6)
            self.label_7.setText(str('%.1f' % (self.get_s16(a[0]) * 0.1))+"℃")
            self.label_8.setText(str('%.1f' % (self.get_s16(a[1]) * 0.1))+"℃")
            self.label_9.setText(str('%.1f' % (self.get_s16(a[2]) * 0.1))+"℃")
            self.label_10.setText(str('%.1f' % (self.get_s16(a[3]) * 0.1))+"℃")
            self.label_11.setText(str('%.1f' % (self.get_s16(a[4]) * 0.1))+"℃")
            self.label_12.setText(str('%.1f' % (self.get_s16(a[5]) * 0.1))+"℃")

        except modbus_tk.modbus.ModbusError as exc:
            QMessageBox.warning(self, " ", str(exc), QMessageBox.Yes)
            self.Close()
        except:
            QMessageBox.warning(self, " ", "读取失败", QMessageBox.Yes)
            self.Close()


    def get_s16(self, val):
        if val < 0x8000:
            return val
        else:
            return (val - 0x10000)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
