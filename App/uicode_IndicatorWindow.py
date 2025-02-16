from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QFrame
)

from ui_form_indicator import Ui_Indicator

class IndicatorWindow(QMainWindow):

    data_submitted = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Indicator()
        self.ui.setupUi(self)

        self.available_indicators = ['SMA'] # TODOOO add indicator names here after implementation

        # initialize available indicators
        self.available_indicators_container = QWidget()
        self.available_indicators_layout = QVBoxLayout(self.available_indicators_container)
        self.available_indicators_container.setLayout(self.available_indicators_layout)
        self.ui.available_indicators_area.setWidget(self.available_indicators_container)
        self.ui.available_indicators_area.setWidgetResizable(True)
        self.available_indicators_layout.setAlignment(Qt.AlignTop)

        for indicator_name in self.available_indicators:
            clickable_item = ClickableFrame(indicator_name, False, self)
            self.available_indicators_layout.addWidget(clickable_item)


        # initialize current indicators
        self.current_indicators_container = QWidget()
        self.current_indicators_layout = QVBoxLayout(self.current_indicators_container)
        self.current_indicators_container.setLayout(self.current_indicators_layout)
        self.ui.current_indicators_area.setWidget(self.current_indicators_container)
        self.ui.current_indicators_area.setWidgetResizable(True)
        self.current_indicators_layout.setAlignment(Qt.AlignTop)


        # ---- CONNECT SIGNALS ----
        self.ui.apply_button.clicked.connect(self.on_apply_button_clicked)


    # ---- SLOT FUNCTIONS ----

    def add_indicator_to_current(self, indicator_name):
        clickable_item = ClickableFrame(indicator_name, True, self)
        self.current_indicators_layout.addWidget(clickable_item)

    def on_apply_button_clicked(self):

        # TODOOOOOOOO calculate indicator df for whatever is in current and send back
        test = ['hi']
        self.data_submitted.emit(test)
        self.close()


# helper class to have clickable items in available_indicators_area
class ClickableFrame(QFrame):
    def __init__(self, name, incurrent, parent_window, parent=None):
        super().__init__(parent)
        self.parent_window = parent_window
        self.incurrent = incurrent

        self.setFrameShape(QFrame.StyledPanel)

        self.layout = QHBoxLayout(self)
        self.setFixedHeight(26)
        self.layout.setContentsMargins(5, 0, 0, 1)
        self.layout.setSpacing(0)

        self.label = QLabel(name)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def mouseDoubleClickEvent(self, event):
        if self.incurrent:
            indicator_name = self.label.text()
            # TODOOOOO show properties
        else:
            indicator_name = self.label.text()
            self.parent_window.add_indicator_to_current(indicator_name)

