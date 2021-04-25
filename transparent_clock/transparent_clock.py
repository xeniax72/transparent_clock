########################################################################################################################
#
# BUGS: al momento non risultano bugs...
#
########################################################################################################################
#
# TODO  1 - il metodo change_font non gestisce il grasseto, il corsivo ecc... ecc... ora è tutto grassetto... vedere
#           se esiste un font dialog più completo di quello usato attualmente
#
########################################################################################################################


from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QMenu, QAction, QFontDialog, QColorDialog, QInputDialog
from PyQt5.QtCore import QTime, QDate, QTimer
from PyQt5.QtGui import QFont, QColor, QContextMenuEvent, QPalette

from loguru import logger

from transparent_clock_globals import *

from transparent_clock_widget import TransparentClockWidget
from transparent_clock_transparency_dialog import TransparentClockTransparencyDialog
from transparent_clock_appearances_manager import TransparentClockAppearancesManager, TransparentClockAppearanceData

# context menu actions names
TC_CONTEXT_MENU___CHANGE_APPEARANCE = "Change appearance"
TC_CONTEXT_MENU___SAVE_APPEARANCE = "Save appearance"
TC_CONTEXT_MENU___CHANGE_FONT = "Change Font"
TC_CONTEXT_MENU___CHANGE_COLOR = "Change Color"
TC_CONTEXT_MENU___TRANSPARENCY = "Transparency"
TC_CONTEXT_MENU___QUIT = "Quit"

# texts string for "save appearance dialog" in transparent_clock.py
TC_SAVE_APPEARANCE_DIALOG___TITLE = "New Clock Assets"
TC_SAVE_APPEARANCE_DIALOG___INPUT = "Insert assets name: "


class TransparentClockClock(TransparentClockWidget):
    def __init__(self, parent=None):
        super(TransparentClockClock, self).__init__(parent)

        # carica il file di tutte le configurazioni dei vari clocks
        self.__appearances_manager = TransparentClockAppearancesManager(TC_PATH_NAME___APPEARANCES_FILE)
        # mette come configurazione corrent quella di Default
        self.__current_appearance = self.__appearances_manager.get_appearance(TC___DEFAULT_APPEARANCE)

        # creazione del timer
        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.on_timer_event)
        self.__timer.start(1000)

        # label widget per la visualizzazione dell'orario
        self.__time_lbl = QLabel(QTime.currentTime().toString(TC___TIME_FORMAT_STRING))
        self.__time_lbl.setFont(QFont(self.__current_appearance.font_family, self.__current_appearance.font_size, QFont.Bold))

        start_color = QColor(self.__current_appearance.font_color)
        start_color.setAlphaF(self.__current_appearance.font_alphaF)
        palette = self.__time_lbl.palette()
        palette.setColor(QPalette.Inactive, QPalette.WindowText, start_color)
        self.__time_lbl.setPalette(palette)

        # creazione del layout principale e aggiunta del clock
        self.__main_layout = QVBoxLayout()
        self.__main_layout.addWidget(self.__time_lbl)
        self.setLayout(self.__main_layout)

        # preparo la finestra nella posizione giusta
        self.move(self.__current_appearance.x_pos, self.__current_appearance.y_pos)

    def on_timer_event(self) -> None:
        # recupera data e ora correnti
        current_date = QDate.currentDate()
        current_date_str = current_date.toString(TC___DATE_FORMAT_STRING)  # si lascia per eventuali utilizzi futuri
        current_time = QTime.currentTime()
        current_time_str = current_time.toString(TC___TIME_FORMAT_STRING)

        # aggiorna il clock
        self.__time_lbl.setText(current_time_str)

    def contextMenuEvent(self, context_menu_event: QContextMenuEvent) -> None:
        # creazion del menu contestuale sul clock
        menu = QMenu(self)
        change_assets = menu.addMenu(TC_CONTEXT_MENU___CHANGE_APPEARANCE)

        for conf_name in self.__appearances_manager.get_appearances_names():
            action = QAction(conf_name, change_assets)
            action.setCheckable(True)
            if conf_name == self.__current_appearance.name:
                action.setChecked(True)
            change_assets.addAction(action)

        save_appearance = menu.addAction(TC_CONTEXT_MENU___SAVE_APPEARANCE)
        change_font = menu.addAction(TC_CONTEXT_MENU___CHANGE_FONT)
        change_color = menu.addAction(TC_CONTEXT_MENU___CHANGE_COLOR)
        change_transparency = menu.addAction(TC_CONTEXT_MENU___TRANSPARENCY)
        quit_action = menu.addAction(TC_CONTEXT_MENU___QUIT)

        # esecuzione del menu contestuale
        action = menu.exec(self.mapToGlobal(context_menu_event.pos()))

        # analisi della scelta fatta e conseguente chiamata del metodo corrispondente
        if action == save_appearance:
            self.open_save_appearance_dialog()
        elif action == change_font:
            self.open_change_font_dialog()
        elif action == change_color:
            self.open_change_color_dialog()
        elif action == change_transparency:
            self.open_change_transparency_dialog()
        elif action == quit_action:
            self.close()
        else:
            if action:
                self.change_appearance(action.text())

    def change_appearance(self, action_text: str) -> None:
        for appearance_name in self.__appearances_manager.get_appearances_names():
            if appearance_name == action_text:
                selected_appearance = self.__appearances_manager.get_appearance(appearance_name)
                self.__current_appearance.update_with(selected_appearance)

                self.__time_lbl.setFont(QFont(self.__current_appearance.font_family, self.__current_appearance.font_size, QFont.Bold))
                color = QColor(self.__current_appearance.font_color)
                color.setAlphaF(self.__current_appearance.font_alphaF)
                palette = self.__time_lbl.palette()
                palette.setColor(QPalette.Inactive, QPalette.WindowText, color)
                self.__time_lbl.setPalette(palette)

                self.move(self.__current_appearance.x_pos, self.__current_appearance.y_pos)

    def open_save_appearance_dialog(self) -> None:
        appearance_name, accepted = QInputDialog.getText(None, TC_SAVE_APPEARANCE_DIALOG___TITLE, TC_SAVE_APPEARANCE_DIALOG___INPUT,
                                             text=self.__current_appearance.name)
        if accepted and appearance_name:
            self.__current_appearance.x_pos = self.x()
            self.__current_appearance.y_pos = self.y()
            conf_with_name = self.__appearances_manager.get_appearance(appearance_name)
            if conf_with_name:
                conf_with_name.update_with(self.__current_appearance)
                self.__appearances_manager.update_appearance(conf_with_name)
            else:
                new_conf = TransparentClockAppearanceData(appearance_name, self.__current_appearance.font_family, self.__current_appearance.font_size,
                                                          self.__current_appearance.font_color, self.__current_appearance.font_alphaF,
                                                          self.__current_appearance.x_pos, self.__current_appearance.y_pos)
                self.__appearances_manager.add_appearance(new_conf)
            self.change_appearance(appearance_name)
            self.__appearances_manager.save_appearances()

    def open_change_font_dialog(self) -> None:
        # Apre il dialog per la scelta del font... new_font è di tipo QFont
        new_font, ok = QFontDialog.getFont(self.__time_lbl.font(), self)

        # se sono uscito dal diologo premendo ok allora cambio il font
        if ok:
            self.__time_lbl.setFont(new_font)
            self.__current_appearance.font_family = new_font.family()
            self.__current_appearance.font_size = self.__time_lbl.font().pointSize()

    def open_change_color_dialog(self) -> None:
        # Apre il dialogo per la scelta dei colori... new_color è di tipo QColor
        new_color = QColorDialog.getColor(initial=self.__time_lbl.palette().color(QPalette.Inactive, QPalette.WindowText), parent=self)

        # Se sono uscito dal dialogo prendo ok e il colore è valido allora lo cambio
        if new_color.isValid():
            self.__current_appearance.font_color = new_color.name()
            color = QColor(new_color)
            color.setAlphaF(self.__current_appearance.font_alphaF)
            palette = self.__time_lbl.palette()
            palette.setColor(QPalette.Inactive, QPalette.WindowText, color)
            self.__time_lbl.setPalette(palette)

    def open_change_transparency_dialog(self) -> None:
        trans_dialog = TransparentClockTransparencyDialog(None, self.__time_lbl.text(), self.__time_lbl.font(),
                                                          self.__time_lbl.palette().color(QPalette.Inactive, QPalette.WindowText),
                                                          self.__time_lbl.palette().color(QPalette.Inactive, QPalette.WindowText).alphaF())
        accept = trans_dialog.exec()
        if accept:
            palette = self.__time_lbl.palette()
            color = palette.color(QPalette.Inactive, QPalette.WindowText)
            color.setAlphaF(trans_dialog.text_alphaF)
            palette.setColor(QPalette.Inactive, QPalette.WindowText, color)
            self.__time_lbl.setPalette(palette)
            self.__current_appearance.font_alphaF = trans_dialog.text_alphaF


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = TransparentClockClock()
    win.show()
    sys.exit(app.exec())
