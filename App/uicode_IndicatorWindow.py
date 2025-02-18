from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QColorDialog
)

import inspect
import source_Indicators as ic

from ui_form_indicator import Ui_Indicator

# helper class to have clickable items in available_indicators_area
class ClickableFrame(QFrame):
    def __init__(self, name, incurrent, parent_window, parent=None):
        super().__init__(parent)
        self.parent_window = parent_window

        self.incurrent = incurrent

        self.layout = QHBoxLayout(self)
        self.setFixedHeight(18)
        self.layout.setContentsMargins(5, 0, 0, 1)
        self.layout.setSpacing(0)

        self.label = QLabel(name)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def mouseDoubleClickEvent(self, event):
        if self.incurrent:
            indicator_name = self.label.text()
            self.parent_window.show_properties(indicator_name)
        else:
            indicator_name = self.label.text()
            self.parent_window.add_indicator_to_current(indicator_name)


class IndicatorWindow(QMainWindow):
    data_submitted = Signal(object)

    def __init__(self, current_indicators, parent=None):
        super().__init__(parent)
        self.ui = Ui_Indicator()
        self.ui.setupUi(self)

        self.function_dict = ic.get_indicator_function_dict()

        # initialize available indicators
        self.available_indicators_container = QWidget()
        self.available_indicators_layout = QVBoxLayout(self.available_indicators_container)
        self.available_indicators_container.setLayout(self.available_indicators_layout)
        self.ui.available_indicators_area.setWidget(self.available_indicators_container)
        self.ui.available_indicators_area.setWidgetResizable(True)
        self.available_indicators_layout.setAlignment(Qt.AlignTop)

        for indicator_name in ic.get_indicator_list():
            clickable_item = ClickableFrame(indicator_name, False, self)
            self.available_indicators_layout.addWidget(clickable_item)


        # initialize current indicators
        self.current_indicators_container = QWidget()
        self.current_indicators_layout = QVBoxLayout(self.current_indicators_container)
        self.current_indicators_container.setLayout(self.current_indicators_layout)
        self.ui.current_indicators_area.setWidget(self.current_indicators_container)
        self.ui.current_indicators_area.setWidgetResizable(True)
        self.current_indicators_layout.setAlignment(Qt.AlignTop)

        for key, params in current_indicators.items():
            clickable_item = ClickableFrame(key, True, self)
            self.current_indicators_layout.addWidget(clickable_item)


        # initialize properties
        self.properties_container = QWidget()
        self.properties_layout = QVBoxLayout(self.properties_container)
        self.properties_container.setLayout(self.properties_layout)
        self.ui.properties_area.setWidget(self.properties_container)
        self.ui.properties_area.setWidgetResizable(True)
        self.properties_layout.setAlignment(Qt.AlignTop)


        # ---- CONNECT SIGNALS ----
        self.ui.apply_button.clicked.connect(self.on_apply_button_clicked)


    # ---- SLOT FUNCTIONS ----

    def add_indicator_to_current(self, indicator_name):
        clickable_item = ClickableFrame(indicator_name, True, self)
        self.current_indicators_layout.addWidget(clickable_item)

    def open_color_picker(self, color_button):
        color = QColorDialog.getColor() # open dialog
        if color.isValid():
            color_button.setStyleSheet(f"background-color: {color.name()};")  # change button color
            # TODOOOOO set color in some data structure for current indicators

    def on_apply_button_clicked(self):
        indicator_data = {}
        for i in range(self.current_indicators_layout.count()):
            widget = self.current_indicators_layout.itemAt(i).widget()
            ind_text = widget.label.text()
            params = "shi idk"
            indicator_data[ind_text] = params

        self.data_submitted.emit(indicator_data)
        self.close()

    def show_properties(self, indicator_name):
        while self.properties_layout.count():
            item = self.properties_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        param_list = self.get_function_parameters(indicator_name)

        for param in list(param_list)[1:]: # skip ohlc param
            param_layout = QHBoxLayout()
            param_layout.setSpacing(2)
            param_layout.setContentsMargins(0, 2, 0, 0)
            label = QLabel(param)
            param_layout.addWidget(label)
            # TODOOOOO figure out user input stuff and put in param_layout
            self.properties_layout.addWidget(label)

        # add color picker
        colorpicker_layout = QHBoxLayout()
        colorpicker_layout.setSpacing(2)
        colorpicker_layout.setContentsMargins(0, 2, 0, 0)
        colorpicker_layout.setAlignment(Qt.AlignLeft)
        color_label = QLabel("color:")
        colorpicker_layout.addWidget(color_label)

        color_button = QPushButton()
        colorpicker_layout.addWidget(color_button)
        color_button.clicked.connect(lambda: self.open_color_picker(color_button))
        colorpicker_widget = QWidget()
        colorpicker_widget.setLayout(colorpicker_layout)
        self.properties_layout.addWidget(colorpicker_widget)


    # --- SPECIAL ---

    def get_function_parameters(self, key):
        return [param.name for param in inspect.signature(self.function_dict[key]).parameters.values()]



