from PyQt5.QtWidgets import QWidget

from sgs_libs.sgs_pyqt.transparent_widget import TransparentW
from sgs_libs.sgs_pyqt.mouse_moving_widget import MouseMovingW


class TransparentMovingW(MouseMovingW, TransparentW):
    def __init__(self, qw_parent: QWidget = None):
        MouseMovingW.__init__(self, qw_parent=qw_parent)
        TransparentW.__init__(self, qw_parent=qw_parent)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QPushButton, QSizePolicy
    from PyQt5.QtGui import QFont
    import sys

    app = QApplication(sys.argv)

    win = TransparentMovingW()
    label = QLabel("This is only a test")
    label.setFont(QFont("FreeMono", 32, QFont.Bold))
    label.setStyleSheet("color: rgb(255, 255, 255)")
    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    label.setAlignment(Qt.AlignCenter)

    button = QPushButton("Quit")
    button.clicked.connect(app.quit)

    main_layout = QVBoxLayout()
    main_layout.addWidget(label)
    main_layout.addWidget(button)
    win.setLayout(main_layout)
    win.show()
    sys.exit(app.exec())
