from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent


class MouseMovingW(QWidget):
    def __init__(self, qw_parent: QWidget = None):
        super(MouseMovingW, self).__init__(parent=qw_parent)

        # usata per spostare la finestra con il mouse
        self.__qo_mouse_delta_pos = QPoint(0, 0)

        # usata per capire se sto spostando la finestra con il mouse
        self.__b_is_moving = False

        # usata per catturare gli eventi del mouse
        self.setMouseTracking(True)

    def mousePressEvent(self, mouse_event: QMouseEvent) -> None:
        '''
        Cattura l'evento pressione del tasto sinistro per iniziare uno spostamento della finestra
        :param mouse_event: l'evento generato dalla pressione del tasto del mouse
        :return: None
        '''
        if mouse_event.button() == Qt.LeftButton:
            self.__b_is_moving = True
            qo_local_point = QPoint(mouse_event.x(), mouse_event.y())
            self.__qo_mouse_delta_pos = QPoint(self.mapToGlobal(qo_local_point))

    def mouseMoveEvent(self, mouse_event: QMouseEvent) -> None:
        '''
        Cattura l'evento di spostamento del mouse e se precedentemente ho premuto il tasto sinistro muove la finestra
        :param mouse_event: l'evento generato dal movimento del mouse
        :return: None
        '''
        if self.__b_is_moving:
            qo_local_point = QPoint(mouse_event.x(), mouse_event.y())
            qo_old_mouse_pos = QPoint(self.__qo_mouse_delta_pos)
            self.__qo_mouse_delta_pos = QPoint(self.mapToGlobal(qo_local_point))
            self.move(self.__qo_mouse_delta_pos - qo_old_mouse_pos + self.pos())

    def mouseReleaseEvent(self, mouse_event: QMouseEvent) -> None:
        '''
        Cattura l'evento di rilascio del bottone del mouse e se precedentemente stavo spostando la finestra termina
        lo spostamento
        :param mouse_event: l'evento generato dal rilascio del bottone del mouse
        :return: None
        '''
        if self.__b_is_moving:
            qo_local_point = QPoint(mouse_event.x(), mouse_event.y())
            qo_old_mouse_pos = QPoint(self.__qo_mouse_delta_pos)
            self.__qo_mouse_delta_pos = QPoint(self.mapToGlobal(qo_local_point))
            self.move(self.__qo_mouse_delta_pos - qo_old_mouse_pos + self.pos())
            self.__b_is_moving = False
