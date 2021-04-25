# TODO: rivedere l'intero file e sistemarlo secondo i miei criteri
#       eventualmente provare anche a derivarne uno mio in modo indipendente partendo dall'esempio C++

from random import randint
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import (QApplication, QLayout, QPushButton, QSizePolicy, QWidget)


class FlowLayout(QLayout):
    def __init__(self, qw_parent: QWidget = None, i_margin: int = 0, i_spacing: int = -1):
        super(FlowLayout, self).__init__(qw_parent)

        if qw_parent is not None:
            self.setContentsMargins(i_margin, i_margin, i_margin, i_margin)

        self.setSpacing(i_spacing)

        self.l_items = []

    def __del__(self):
        qw_item = self.takeAt(0)
        while qw_item:
            qw_item = self.takeAt(0)

    def addItem(self, qw_new_item: QWidget):
        self.l_items.append(qw_new_item)

    def count(self) -> int:
        return len(self.l_items)

    def itemAt(self, index: int) -> QWidget:
        if 0 <= index < len(self.l_items):
            return self.l_items[index]

        return None

    def takeAt(self, index) -> QWidget:
        if 0 <= index < len(self.l_items):
            return self.l_items.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, i_width: int) -> int:
        i_height = self.doLayout(QRect(0, 0, i_width, 0), True)
        return i_height

    def setGeometry(self, qo_rect: QRect):
        super(FlowLayout, self).setGeometry(qo_rect)
        self.doLayout(qo_rect, False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self):
        qo_size = QSize()

        for item in self.l_items:
            qo_size = qo_size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        qo_size += QSize(2 * margin, 2 * margin)
        return qo_size

    def doLayout(self, qo_rect: QRect, b_test_only: bool):
        i_x = qo_rect.x()
        i_y = qo_rect.y()
        i_line_height = 0

        for qo_item in self.l_items:
            qw_widget = qo_item.widget()
            i_space_x = self.spacing() + qw_widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            i_space_y = self.spacing() + qw_widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            i_next_x = i_x + qo_item.sizeHint().width() + i_space_x
            if i_next_x - i_space_x > qo_rect.right() and i_line_height > 0:
                i_x = qo_rect.x()
                i_y = i_y + i_line_height + i_space_y
                i_next_x = i_x + qo_item.sizeHint().width() + i_space_x
                i_line_height = 0

            if not b_test_only:
                qo_item.setGeometry(QRect(QPoint(i_x, i_y), qo_item.sizeHint()))

            i_x = i_next_x
            i_line_height = max(i_line_height, qo_item.sizeHint().height())

        return i_y + i_line_height - qo_rect.y()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.flowLayout = FlowLayout(self)
        self.setLayout(self.flowLayout)

        self.setWindowTitle("Flow Layout")

    def keyPressEvent(self, key_event: QKeyEvent) -> None:
        if key_event.key() == Qt.Key_Return:
            self.flowLayout.addWidget(QPushButton("{} bot {} tone {}".format("-"*randint(1, 8), " "*randint(1, 8), "-"*randint(1, 8))))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec())
