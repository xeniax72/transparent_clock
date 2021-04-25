from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent


class TransparentClockWidget(QWidget):
    '''
    Crea un widget che ha lo sfondo completamente trasparente... è possibile spostare la finetra usando il mouse...
    '''
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        # toglie dalla finestra la barra dei menu e gli altri bottoni
        self.setWindowFlags(Qt.FramelessWindowHint)
        # invita la finestra a rimanere sempre in primo piano
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # sgancia la finestra dal gestore finestra del sistema operativo
        self.setWindowFlag(Qt.X11BypassWindowManagerHint)
        # crea lo sfondo trasparente
        self.setAttribute(Qt.WA_TranslucentBackground)

        # usata per spostare la finestra con il mouse
        self.__mouse_delta_pos = QPoint(0, 0)

        # usata per capire se sto spostando la finestra con il mouse
        self.is_moving = False

        # usata per catturare gli eventi del mouse
        self.setMouseTracking(True)

    def mousePressEvent(self, mouse_event: QMouseEvent) -> None:
        '''
        Cattura l'evento pressione del tasto sinistro per iniziare uno spostamento della finestra
        :param mouse_event: l'evento generato dalla pressione del tasto del mouse
        :return: None
        '''
        if mouse_event.button() == Qt.LeftButton:
            self.is_moving = True
            local_point = QPoint(mouse_event.x(), mouse_event.y())
            self.__mouse_delta_pos = QPoint(self.mapToGlobal(local_point))

    def mouseMoveEvent(self, mouse_event: QMouseEvent) -> None:
        '''
        Cattura l'evento di spostamento del mouse e se precedentemente ho premuto il tasto sinistro muove la finestra
        :param mouse_event: l'evento generato dal movimento del mouse
        :return: None
        '''
        if self.is_moving:
            local_point = QPoint(mouse_event.x(), mouse_event.y())
            old_mouse_pos = QPoint(self.__mouse_delta_pos)
            self.__mouse_delta_pos = QPoint(self.mapToGlobal(local_point))
            self.move(self.__mouse_delta_pos - old_mouse_pos + self.pos())

    def mouseReleaseEvent(self, mouse_event: QMouseEvent) -> None:
        '''
        Cattura l'evento di rilascio del bottone del mouse e se precedentemente stavo spostando la finestra termina
        lo spostamento
        :param mouse_event: l'evento generato dal rilascio del bottone del mouse
        :return: None
        '''
        if self.is_moving:
            local_point = QPoint(mouse_event.x(), mouse_event.y())
            old_mouse_pos = QPoint(self.__mouse_delta_pos)
            self.__mouse_delta_pos = QPoint(self.mapToGlobal(local_point))
            self.move(self.__mouse_delta_pos - old_mouse_pos + self.pos())
            self.is_moving = False


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QPushButton, QSizePolicy
    from PyQt5.QtGui import QFont
    import sys

    app = QApplication(sys.argv)

    win = TransparentClockWidget()
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
