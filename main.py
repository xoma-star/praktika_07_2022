from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import numpy as np
from PyQt5.QtGui import QPainter, QPen, QColor


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent, flags=Qt.Window)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cellular automatons")
        self.resize(800, 900)
        self.setMinimumSize(500, 500)
        self.central = CentralWidget(self)
        self.setCentralWidget(self.central)
        menuBar = QtWidgets.QMenuBar(self)
        self.setMenuBar(menuBar)
        menuBar.setVisible(True)
        menuGen = menuBar.addMenu("File")
        action = menuGen.addAction("Generate", self.central.generateNewField)
        menuProp = menuBar.addMenu("Properties")
        action = menuProp.addAction("About", self.about)

    def about(self):
        text = "Rules and other"
        QtWidgets.QMessageBox.about(self, "About", text)


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.probability = 0.2
        self.is_animate = False
        self.timer_id = 0
        self.initUI()

    def initUI(self):
        self.spin = QtWidgets.QDoubleSpinBox(self)
        self.spin.setRange(0, 1)
        self.spin.setValue(self.probability)
        self.spin.setSingleStep(0.05)

        self.btnGen = QtWidgets.QPushButton('Generate', self)
        self.btnStartStop = QtWidgets.QPushButton('Start | Stop', self)
        self.field = FieldWidget(self)
        # alignment
        self.grid = QtWidgets.QGridLayout(self)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setSpacing(10)
        self.grid.addWidget(self.spin, 0, 0)
        self.grid.addWidget(self.btnGen, 0, 1)
        self.grid.addWidget(self.btnStartStop, 0, 2)
        self.grid.addWidget(self.field, 1, 0, 1, 3)

        self.setLayout(self.grid)

        self.btnGen.clicked.connect(self.generateNewField)
        self.btnStartStop.clicked.connect(self.startOrStop)

    def generateNewField(self):
        self.probability = self.spin.value()
        self.field.set_random(self.probability)

    def startOrStop(self):
        self.is_animate = not self.is_animate
        if self.is_animate:
            self.timer_id = self.startTimer(200, timerType=Qt.CoarseTimer)
            self.btnGen.setEnabled(False)
        else:
            self.killTimer(self.timer_id)
            self.timer_id = 0
            self.btnGen.setEnabled(True)

    def timerEvent(self, event: 'QTimerEvent') -> None:
        self.field.next_field()


class FieldWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.dim = 50
        self.birth = [4, 5, 6, 7, 8]
        self.survival = [2, 3, 4, 5]
        self.board = np.zeros((self.dim, self.dim),
                              dtype=np.uint8)
        self.update()


    def set_random(self, probability):
        self.board = (np.random.random(self.board.shape)
                      < probability).astype(np.uint8)
        self.update()

    def next_field(self):
        neighbors = sum([
            np.roll(np.roll(self.board, -1, 1), 1, 0),
            np.roll(np.roll(self.board, 1, 1), -1, 0),
            np.roll(np.roll(self.board, 1, 1), 1, 0),
            np.roll(np.roll(self.board, -1, 1), -1, 0),
            np.roll(self.board, 1, 1),
            np.roll(self.board, -1, 1),
            np.roll(self.board, 1, 0),
            np.roll(self.board, -1, 0)])
        self.board = ((self.board == 0) & sum([(neighbors == i)
                                               for i in self.birth]) |
                      (self.board == 1) & sum([(neighbors == i)
                                               for i in self.survival])).\
            astype(np.uint8)
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)
        pen = QPen()
        #pen.setStyle(Qt.SolidLine)
        pen.setColor(QColor(255, 0, 0))
        qp.setPen(pen)
        cell_h_size = self.width() // self.dim
        cell_v_size = self.height() // self.dim
        for row in range(self.dim):
            for col in range(self.dim):
                if self.board[row, col] == 1:
                    qp.setBrush(QColor(0, 0, 0))
                    qp.drawRect(col * cell_h_size, row * cell_v_size,
                                cell_h_size, cell_v_size)
                else:
                    qp.setBrush(QColor(255, 255, 255))
                    qp.drawRect(col * cell_h_size, row * cell_v_size,
                                cell_h_size, cell_v_size)
        qp.end()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.resize(800, 1000)
    window.show()
    sys.exit(app.exec_())