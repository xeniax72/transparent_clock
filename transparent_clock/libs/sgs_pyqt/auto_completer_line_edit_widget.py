# TODO: ...

from PyQt5.QtWidgets import QWidget, QCompleter, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal, QStringListModel
from PyQt5.QtGui import QKeyEvent

from sgs_libs.sgs_generic.parameter_integrity_check import ParameterIntegrityCheck


class AutoCompleterLineEditW(QLineEdit):
    sgn_insertion_completed = pyqtSignal(str)

    def __init__(self, qw_parent: QWidget, l_items: list, b_new_items_accepted: bool = False):
        super(AutoCompleterLineEditW, self).__init__(parent=qw_parent)

        self.l_items = l_items  # la lista delle items già presenti per l'autocompletamento
        self.b_new_items_accepted = b_new_items_accepted  # True se nel digitare si accettato nuove parole rispetto a auelle presenti in l_items

        # creazione del completer
        self.__com_completer = QCompleter(l_items)
        self.__com_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.__com_completer.setFilterMode(Qt.MatchStartsWith)

        self.setCompleter(self.__com_completer)

    @property
    def l_items(self) -> list:
        return self.__l_items
    
    @l_items.setter
    def l_items(self, l_new_items: list):
        ParameterIntegrityCheck.check(l_new_items, "l_new_items", list, "l_items", "SGSAutoCompleterLineEdit", b_accept_empty=True)
        self.__l_items = l_new_items

    @property
    def b_new_items_accepted(self) -> bool:
        return self.__b_new_items_accepted

    @b_new_items_accepted.setter
    def b_new_items_accepted(self, b_new_items_accepted: bool):
        ParameterIntegrityCheck.check(b_new_items_accepted, "b_new_items_accepted", bool, "b_new_items_accepted", "SGSAutoComplterLineEdit", b_sized=False)
        self.__b_new_items_accepted = b_new_items_accepted

    def reset_completer(self):
        self.setText("")
        self.__com_completer.setCompletionPrefix("")

    def update_model(self, l_new_items: list):
        self.__com_completer.setModel(QStringListModel(l_new_items))

    def keyPressEvent(self, ev_key_event: QKeyEvent) -> None:
        s_already_inserted_prefix = self.__com_completer.completionPrefix()
        s_new_inserted_char = ev_key_event.text()

        if ev_key_event.key() == Qt.Key_Backspace and self.cursorPosition() > 0:
            if self.b_new_items_accepted:
                # se sono accettate nuove parole oltre a quelle della lista allora posso cancellare qualsiasi carattere
                super(AutoCompleterLineEditW, self).keyPressEvent(ev_key_event)
                self.__com_completer.setCompletionPrefix(self.text())
            else:
                # se non sono accettate nuove parole posso cancellare solo l'ultimo carattere
                # altrimenti si formerebbero nuove parole che non sono nella lista
                if self.cursorPosition() == len(self.text()):  # permette di cancellare il carattere solo se è l'ultimo
                    super(AutoCompleterLineEditW, self).keyPressEvent(ev_key_event)
                    self.__com_completer.setCompletionPrefix(s_already_inserted_prefix[:-1])
                else:
                    # se non sono alla fine del testo inserito ignore il BACKSPACE
                    ev_key_event.ignore()
        elif ev_key_event.key() == Qt.Key_Delete:  # valgono gli stessi ragionamenti fatti per il BACKSPACE
            if self.b_new_items_accepted:
                super(AutoCompleterLineEditW, self).keyPressEvent(ev_key_event)
            else:
                ev_key_event.ignore()
        elif ev_key_event.key() == Qt.Key_Return or ev_key_event.key() == Qt.Key_Enter:
            if self.b_new_items_accepted:
                # se accetto nuove parole allora ho finito ed emetto il segnale di inserimento completatp
                super(AutoCompleterLineEditW, self).keyPressEvent(ev_key_event)
                self.sgn_insertion_completed.emit(self.text())
            else:
                # se è una parola già completamente formata ed è nella lista allora abbiamo finito
                if self.text() in self.l_items:
                    self.sgn_insertion_completed.emit(self.text())
                else:  # se non è formata completamente
                    # se è l'inizio di parole nella lista si restituisce la prima
                    if self.__com_completer.completionCount() > 0:
                        self.setText(self.__com_completer.currentIndex().data())
                        self.sgn_insertion_completed.emit(self.text())
                    # un altro modo di gestire una parola non completamente foramta è ignorare l'invio
                    # ev_key_event.ignore()
        elif ev_key_event.key() == Qt.Key_Escape:
            # se premo esc termino la sessione di inserimento e non restituisco nulla
            # ossia il tasto esc serve per uscire dall'inserimento quando non voglio inserire nulla
            self.sgn_insertion_completed.emit("")
        else:  # gestione di tutti gli altri tasti
            if self.b_new_items_accepted:
                super(AutoCompleterLineEditW, self).keyPressEvent(ev_key_event)
                self.__com_completer.setCompletionPrefix(self.text())
            else:
                # se non accetto nuove parole aggiorno il prefisso con il nuovo carattere inserito
                self.__com_completer.setCompletionPrefix(s_already_inserted_prefix + s_new_inserted_char)
                # poi provo a vedere se ci sono inizi di parole compatibili con il testo inserito
                if self.__com_completer.completionCount() == 0:
                    # se non si sono inizi compatibili tolgo il carattere appena inserito e ignoro la pressione del tasto
                    self.__com_completer.setCompletionPrefix(s_already_inserted_prefix)
                    ev_key_event.ignore()
                else:
                    # se ci sono inizi compatibili ripristino il prefisso che c'era prima della pressione del tasto
                    # e processo la pressione del tasto
                    self.__com_completer.setCompletionPrefix(s_already_inserted_prefix)
                    super(AutoCompleterLineEditW, self).keyPressEvent(ev_key_event)


if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QVBoxLayout
    from PyQt5.QtWidgets import QApplication

    l_test_items = ["Mc 12,34 45", "Mc12,34-45", "Marco 12, 34-45", "Mc 12,34-45", "Mc 12, 34-45", "Acqua", "Fuoco",
                    "Terra", "Aria", "Aria fritta", "Errore", "Ferro", "Fernando", "Acquario di Pomposa",
                    "Acquedotto di Roma", "Otto"]

    qa_app = QApplication(sys.argv)
    qw_main_window = QWidget()

    acle_line_edit = AutoCompleterLineEditW(qw_main_window, l_test_items, b_new_items_accepted=False)
    acle_line_edit.sgn_insertion_completed.connect(qw_main_window.close)

    lo_vbox = QVBoxLayout()
    lo_vbox.setAlignment(Qt.AlignCenter)
    lo_vbox.addWidget(acle_line_edit)

    qw_main_window.setLayout(lo_vbox)
    qw_main_window.show()

    qa_app.exec()
    print(acle_line_edit.text())
