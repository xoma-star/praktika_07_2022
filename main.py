import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QGridLayout, \
    QGroupBox, QComboBox, QLabel, QDoubleSpinBox, QSpinBox, QLineEdit, QAction, QFileDialog, \
    QMessageBox


class MainWindow(QMainWindow):
    size_index = 2

    def __init__(self):
        super().__init__()

        self.create_dictionary()
        self.create_actions()
        self.create_menu()
        self.create_central_widget()

        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("Практика")
        self.setMinimumSize(160, 160)
        self.resize(800, 600)

    def create_actions(self):
        self.save_as_act = QAction("Сохранить как", self)
        self.save_as_act.setShortcut("Ctrl+S")
        self.save_as_act.triggered.connect(self.save_as)

        self.exit_act = QAction("Выход", self)
        self.exit_act.setShortcut("Ctrl+Q")
        self.exit_act.triggered.connect(self.close)

        self.about_act = QAction("О приложении", self)
        self.about_act.triggered.connect(self.about)


    def create_dictionary(self):
        self.about_text = """
                В голоморфной динамике мно́жество Жюлиа́ J(f) рационального отображения — 
                множество точек, динамика в окрестности которых в определённом смысле неустойчива по отношению к малым возмущениям 
                начального положения. В случае, если f — полином, рассматривают также заполненное множество Жюлиа — множество точек, 
                не стремящихся к бесконечности. Обычное множество Жюлиа при этом является его границей.
                
                Чтобы визуализировать множество с заданными параметрами нажмите "применить"
                Чтобы сохранить изображение используйте Ctrl + S
                Чтобы выйти Ctrl + Q
                """

    def save_as(self):
        filename, _ = QFileDialog.getSaveFileName(self)
        if filename:
            return self.save_file(filename)

    def save_file(self, filename):
        return self.mj_sets_widget.q_image.save(f"{filename}.png", "PNG", -1)

    def about(self):
        QMessageBox.about(self, "О приложении", self.about_text)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("Файл")
        self.file_menu.addAction(self.save_as_act)
        self.file_menu.addAction(self.exit_act)

        self.help_menu = self.menuBar().addMenu("Помощь")
        self.help_menu.addAction(self.about_act)

    def create_central_widget(self):
        self.central_widget = QWidget()

        self.create_mj_sets_widget()
        self.create_grid_group_box()

        main_layout = QGridLayout()

        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 2)

        main_layout.addWidget(self.group_box, 0, 0)
        main_layout.addWidget(self.mj_sets_widget, 0, 1)

        self.central_widget.setLayout(main_layout)

    def create_grid_group_box(self):
        self.group_box = QGroupBox()

        self.set_combo_box = QComboBox()
        self.set_combo_box.addItem("Жюлиа", 0)
        self.set_combo_box.addItem("Мандельброт", 1)
        self.set_combo_box.activated.connect(self.changed_set)

        self.c_line_edit = QLineEdit()
        self.c_line_edit.setText(str(self.mj_sets_widget.c).strip('()'))
        self.c_line_edit.setReadOnly(False)

        self.image_size_combo_box = QComboBox()
        self.image_size_combo_box.addItem("800x800", (800, 800))
        self.image_size_combo_box.addItem("400x400", (400, 400))
        self.image_size_combo_box.addItem("200x200", (200, 200))
        self.image_size_combo_box.addItem("100x100", (100, 100))
        self.image_size_combo_box.setCurrentIndex(3)

        self.diverge_number_spin_box = QSpinBox()
        self.diverge_number_spin_box.setRange(1, 200)
        self.diverge_number_spin_box.setValue(self.mj_sets_widget.num)

        self.x_min_spin_box = QDoubleSpinBox()
        self.x_max_spin_box = QDoubleSpinBox()
        self.y_min_spin_box = QDoubleSpinBox()
        self.y_max_spin_box = QDoubleSpinBox()

        self.x_min_spin_box.setSingleStep(0.01)
        self.x_max_spin_box.setSingleStep(0.01)
        self.y_min_spin_box.setSingleStep(0.01)
        self.y_max_spin_box.setSingleStep(0.01)

        self.x_min_spin_box.setRange(-5, 5)
        self.x_max_spin_box.setRange(-5, 5)
        self.y_min_spin_box.setRange(-5, 5)
        self.y_max_spin_box.setRange(-5, 5)

        self.x_min_spin_box.setValue(self.mj_sets_widget.x_min)
        self.x_max_spin_box.setValue(self.mj_sets_widget.x_max)
        self.y_min_spin_box.setValue(self.mj_sets_widget.y_min)
        self.y_max_spin_box.setValue(self.mj_sets_widget.y_max)

        self.x_min_label = QLabel("X от:")
        self.x_max_label = QLabel("X до:")
        self.y_min_label = QLabel("Y от:")
        self.y_max_label = QLabel("Y до:")

        self.set_label = QLabel("Множнство:")

        self.c_line_edit_label = QLabel("c-параметр:")

        self.image_size_label = QLabel("Разрешение:")

        self.diverge_number_label = QLabel("Кол-во итераций:")

        self.apply_button = QPushButton("Применить")
        self.apply_button.clicked.connect(self.apply_pressed)

        layout = QGridLayout()

        layout.addWidget(self.set_label, 0, 0, Qt.AlignRight)
        layout.addWidget(self.set_combo_box, 0, 1, 1, 3)
        layout.addWidget(self.x_min_label, 1, 0, Qt.AlignRight)
        layout.addWidget(self.x_min_spin_box, 1, 1)
        layout.addWidget(self.x_max_label, 1, 2, Qt.AlignRight)
        layout.addWidget(self.x_max_spin_box, 1, 3)
        layout.addWidget(self.y_min_label, 2, 0, Qt.AlignRight)
        layout.addWidget(self.y_min_spin_box, 2, 1)
        layout.addWidget(self.y_max_label, 2, 2, Qt.AlignRight)
        layout.addWidget(self.y_max_spin_box, 2, 3)
        layout.addWidget(self.image_size_label, 3, 0, 1, 2, Qt.AlignRight)
        layout.addWidget(self.image_size_combo_box, 3, 2, 1, 2)
        layout.addWidget(self.diverge_number_label, 4, 0, 1, 2, Qt.AlignRight)
        layout.addWidget(self.diverge_number_spin_box, 4, 2, 1, 2)
        layout.addWidget(self.c_line_edit_label, 5, 0, 1, 2, Qt.AlignRight)
        layout.addWidget(self.c_line_edit, 5, 2, 1, 2)
        layout.addWidget(self.apply_button, 6, 1, 1, 2)

        self.group_box.setLayout(layout)

    def create_mj_sets_widget(self):
        self.mj_sets_widget = MandelbrotJuliaWidget()
        self.mj_sets_widget.setContentsMargins(0, 0, 0, 0)

    def changed_set(self):
        if self.set_combo_box.currentIndex() == 1:
            self.c_line_edit.setReadOnly(True)
        else:
            self.c_line_edit.setReadOnly(False)

    def apply_pressed(self):
        self.mj_sets_widget.set_parameters(self.x_min_spin_box.value(), self.x_max_spin_box.value(),
                                           self.y_min_spin_box.value(), self.y_max_spin_box.value(),
                                           self.image_size_combo_box.currentData()[0],
                                           self.image_size_combo_box.currentData()[1],
                                           self.diverge_number_spin_box.value(),
                                           complex(self.c_line_edit.text().replace(" ", "")),
                                           self.set_combo_box.currentIndex())


class MandelbrotJuliaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.set_parameters()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        painter.drawPixmap(self.rect(), QPixmap(self.q_image))

    def set_parameters(self, x_min=-2, x_max=2, y_min=-2, y_max=2,
                       width=400, height=400, diverge_number=100, c=-0.8 + 0.156j,
                       index=0):
        # Range of x-values
        self.x_min = x_min
        self.x_max = x_max

        # Range of y-values
        self.y_min = y_min
        self.y_max = y_max

        # Calculate the range
        self.x_range = x_max - x_min
        self.y_range = y_max - y_min

        # Image size
        self.width, self.height = width, height

        # Image scale values
        self.x_scale = float(self.x_range) / self.width
        self.y_scale = float(self.y_range) / self.height

        # Diverge parameter
        self.num = diverge_number

        # Julia parameter
        self.c = c

        self.function_for_set = self.func_array[index]

        data = np.fromfunction(np.vectorize(self.get_color_from_pixel), (self.width, self.height))
        self.q_image = QtGui.QImage(data, data.shape[0], data.shape[1], QtGui.QImage.Format_RGB32)

        self.update()

    @staticmethod
    def rgba_to_hex(r, g, b, a):
        lst = [r, g, b, a]
        lst = [255 if x > 255 else x for x in lst]
        lst = [0 if x < 0 else x for x in lst]
        r, g, b, a = lst
        return int('0x{:02x}{:02x}{:02x}{:02x}'.format(a, r, g, b), 16)

    def get_color_from_pixel(self, y, x):
        z = (self.x_min + x * self.x_scale) + (self.y_max - y * self.y_scale) * 1j

        # Put it into the mandelbrot function
        count = self.function_for_set(self, z)

        set_color = self.rgba_to_hex(0, 0, 0, 0)

        HSV = (255, 3 * count, 255)
        hue, sat, value = HSV
        hsv = QColor.fromHsv(hue, sat, value, 255)
        r, g, b = hsv.red(), hsv.green(), hsv.blue()
        diverge_color = self.rgba_to_hex(r, g, b, 0)

        return set_color if count == self.num else diverge_color

    def mandelbrot(self, z):
        """ Runs the process num times
        and returns the 'diverge' count """
        count = 0

        # Define z1 as z
        z_n = z

        # Iterate num times
        while count <= self.num:
            # Check for divergence
            if abs(z_n) > 2.0:
                # Return the step it diverged on
                return count

            # Iterate z
            z_n = z_n * z_n + z
            count += 1

        # If z hasn't diverged by the end
        return self.num

    def julia(self, z):
        """ Runs the process num times
        and returns the 'diverge' count """
        count = 0

        # Define z1 as z
        z_n = z

        # Iterate num times
        while count <= self.num:
            # Check for divergence
            if abs(z_n) > 2.0:
                # Return the step it diverged on
                return count

            # Iterate z
            z_n = z_n * z_n + self.c
            count += 1

        # If z hasn't diverged by the end
        return self.num

    func_array = (julia, mandelbrot)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
