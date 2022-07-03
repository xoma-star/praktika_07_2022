from PyQt5.QtWidgets import *
import numpy as np
from PIL import Image
import sys


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.qtbutton1 = QPushButton('Выберите изображение', self)
        self.qtbutton1.setStyleSheet('')
        self.qtbutton1.clicked.connect(self.clickHandler)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Praktika')
        self.setStyleSheet('padding: 10px; text-align: center;')
        self.show()

    def clickHandler(self):
        fname = QFileDialog.getOpenFileName(self, 'Выберите файл', '', '*.jpg')[0]
        im = np.array(Image.open(fname))
        im2 = Image.fromarray(255 - im)  # инвертировать изображение
        im2.save('return.jpg')
        im2.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())