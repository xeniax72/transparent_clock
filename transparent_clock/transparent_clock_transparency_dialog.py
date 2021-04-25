# TODO:
#       1 - vedere di creare uno sfondo in contrasto col colore del font che mi viene passato
#       3 - migliorare l'estetica della finestra di dialogo e impedire ridimensionamento


from PyQt5.QtWidgets import QDialog, QSlider, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt


class TransparentClockTransparencyDialog(QDialog):
    def __init__(self, parent, text, text_font: QFont, text_color: QColor, text_alphaF: float):
        super(TransparentClockTransparencyDialog, self).__init__(parent)

        self.setWindowTitle("Transparency")

        # toglie dalla finestra la barra dei menu e gli altri bottoni
        #self.setWindowFlags(Qt.Resize)
        # crea lo sfondo trasparente
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.__text = text
        self.__text_font = text_font
        self.__text_color = text_color
        self.__text_alphaF = text_alphaF

        self.__time_lbl = QLabel(self.__text)
        self.__time_lbl.setFont(self.__text_font)

        self.__text_color.setAlphaF(self.__text_alphaF)
        palette = self.__time_lbl.palette()
        palette.setColor(QPalette.Active, QPalette.WindowText, self.__text_color)
        self.__time_lbl.setPalette(palette)

        self.__time_lbl.setAlignment(Qt.AlignCenter)

        self.__transparency_slider = QSlider(Qt.Horizontal)
        self.__transparency_slider.setMinimum(0)
        self.__transparency_slider.setValue(self.__text_alphaF * 100)
        self.__transparency_slider.setMaximum(100)
        self.__transparency_slider.setTickPosition(QSlider.TicksBelow)
        self.__transparency_slider.setTickInterval(5)
        self.__transparency_slider.valueChanged.connect(self.change_transparency)

        self.__ok_btn = QPushButton("Ok")
        self.__ok_btn.clicked.connect(self.accept)
        self.__cancel_btn = QPushButton("Cancel")
        self.__cancel_btn.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.__time_lbl)
        layout.addWidget(self.__transparency_slider)
        layout.addWidget(self.__ok_btn)
        layout.addWidget(self.__cancel_btn)
        self.setLayout(layout)

    def change_transparency(self):
        self.__text_alphaF = (self.__transparency_slider.value()) / 100

        self.__text_color.setAlphaF(self.__text_alphaF)
        palette = self.__time_lbl.palette()
        palette.setColor(QPalette.Active, QPalette.WindowText, self.__text_color)
        self.__time_lbl.setPalette(palette)

    @property
    def text_alphaF(self):
        return self.__text_alphaF


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = TransparentClockTransparencyDialog(None, "This is only a test...", QFont("FreeMono", 32, QFont.Bold), QColor(255, 0, 0), 0.5)
    win.exec()
    sys.exit(app.exec())
