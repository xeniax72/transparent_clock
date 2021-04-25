from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class TransparentW(QWidget):
    '''
    Crea un widget che ha lo sfondo completamente trasparente...
    è possibile spostare la finetra usando il mouse...
    '''
    def __init__(self, qw_parent: QWidget = None):
        super(QWidget, self).__init__(parent=qw_parent)

        # toglie dalla finestra la barra dei menu e gli altri bottoni
        self.setWindowFlags(Qt.FramelessWindowHint)
        # invita la finestra a rimanere sempre in primo piano
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # sgancia la finestra dal gestore finestra del sistema operativo
        self.setWindowFlag(Qt.X11BypassWindowManagerHint)
        # crea lo sfondo trasparente
        self.setAttribute(Qt.WA_TranslucentBackground)
