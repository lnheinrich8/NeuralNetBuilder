from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QAbstractSpinBox,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QListWidget
)

import json

from ui_form_createmodel import Ui_CreateModel
from uisource_DrawingWidget import DrawingWidget

class CreateModelWindow(QMainWindow):

    data_submitted = Signal(str)

    def __init__(self, column_names, target_variable, parent=None):
        super().__init__(parent)
        self.ui = Ui_CreateModel()
        self.ui.setupUi(self)

        # column names from passed df in MainWindow
        self.column_names = column_names
        self.target_variable = target_variable
        self.ui.target_placeholder_label.setText(self.target_variable)

        # right side params initialization

        self.ui.optimizer_combobox.addItems(["SGD", "RMSprop", "Adam","Adamw",
        "Adadelta", "Adagrad", "Adamax", "Nadam", "Ftrl", "Lion"])
        self.ui.optimizer_combobox.setCurrentText("Adam")

        self.ui.loss_combobox.addItems(["binary_crossentropy", "categorical_crossentropy",
        "sparse_categorical_crossentropy", "poisson", "ctc", "kl_divergence", "mean_squared_error",
        "mean_absolute_error", "mean_absolute_percentage_error", "mean_squared_logarithmic_error",
        "cosine_similarity", "huber", "log_cosh", "hinge", "squared_hinge", "categorical_hinge"])
        self.ui.loss_combobox.setCurrentText("mean_squared_error")

        self.ui.trainingcols_listwidget.addItems(self.column_names)
        self.ui.trainingcols_listwidget.setSelectionMode(QListWidget.MultiSelection)


        self.updating_layers = False
        self.layer_count = 0
        self.checkbox_index = None
        self.dropout_val = None

        self.layer_widgets_dict = []  # store dictionaries for each layer
        self.layer_neuron_values = [] # store neuron values for each layer
        self.layer_type_values = [] # store type values for each layer
        self.ui.layercount_spinBox.setValue(2)

        # Add the DrawingWidget
        self.drawing_widget = DrawingWidget()
        self.ui.drawing_layout = QVBoxLayout(self.ui.widget)
        self.ui.drawing_layout.addWidget(self.drawing_widget)

        # Initialize layer options container
        self.layer_options_container = QWidget()
        self.layer_options_layout = QVBoxLayout(self.layer_options_container)
        self.layer_options_container.setLayout(self.layer_options_layout)
        self.ui.layerCustomizationArea.setWidget(self.layer_options_container)
        self.ui.layerCustomizationArea.setWidgetResizable(True)

        # ---- CONNECT SIGNALS ----
        self.ui.layercount_spinBox.valueChanged.connect(self.layercount_spinbox_changed)
        self.ui.layercount_spinBox.valueChanged.connect(self.update_layer_options)

        # left side
        self.ui.restore_button.clicked.connect(self.on_restore_button_clicked)
        # right side
        self.ui.selectalltcols_button.clicked.connect(self.on_selectalltcols_button_clicked)
        self.ui.deselectalltcols_button.clicked.connect(self.on_deselectalltcols_button_clicked)

        # final signals
        self.ui.setmodel_button.clicked.connect(self.on_setmodel_button_clicked)

        # Initial drawing
        self.layercount_spinbox_changed(self.ui.layercount_spinBox.value())
        self.update_layer_options()

    # ---- SLOT FUNCTIONS ----

    # updates the layer drawing in the drawing widget
    def layercount_spinbox_changed(self, value):
        self.drawing_widget.draw_layers(value)

    def update_layer_options(self):
        # Re-create the layer options container and layout
        self.layer_options_container.deleteLater()
        self.layer_options_container = QWidget()  # Create a new container widget
        self.layer_options_layout = QVBoxLayout(self.layer_options_container)  # Create a new layout
        self.layer_options_container.setLayout(self.layer_options_layout)  # Set the new layout to the container
        self.ui.layerCustomizationArea.setWidget(self.layer_options_container)

        self.layer_options_layout.setAlignment(Qt.AlignTop)
        self.layer_widgets_dict.clear() # clear the layer widget dictionary

        # Add the horizontal layout for customization of each layer
        self.layer_count = self.ui.layercount_spinBox.value()
        for i in range(self.layer_count):
            layer_data = {}  # Dictionary to store widgets for this layer

            if i == self.layer_count - 1:
                layer_layout = QHBoxLayout()
                layer_label = QLabel("Output dropout %")
                layer_layout.addWidget(layer_label, alignment=Qt.AlignLeft)
                dropout_spinbox = QSpinBox(self)
                dropout_spinbox.setMinimum(1)
                dropout_spinbox.setMaximum(100)
                if self.dropout_val is None:
                    dropout_spinbox.setValue(20)  # Default value
                else:
                    dropout_spinbox.setValue(self.dropout_val)
                dropout_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
                layer_layout.addWidget(dropout_spinbox, alignment=Qt.AlignLeft)

                layer_data['dropout_spinbox'] = dropout_spinbox

            else:
                layer_layout = QHBoxLayout()

                # label for neurons
                layer_label = QLabel(f"L{i + 1}:")
                layer_layout.addWidget(layer_label, alignment=Qt.AlignLeft)
                # spinbox for neurons
                neuron_spinbox = QSpinBox(self)
                neuron_spinbox.setMinimum(1)  # Minimum number of neurons
                neuron_spinbox.setMaximum(500)  # Maximum number of neurons
                neuron_spinbox.setValue(32)  # Default value
                neuron_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
                layer_layout.addWidget(neuron_spinbox, alignment=Qt.AlignLeft)
                layer_data['neuron_spinbox'] = neuron_spinbox

                # label for type of layer
                type_label = QLabel("T:")
                layer_layout.addWidget(type_label, alignment=Qt.AlignLeft)
                # combobox for type of layer
                type_combobox = QComboBox(self)
                type_combobox.setFixedSize(140,20)
                type_combobox.addItems(["LSTM", "GRU", "SimpleRNN", "Dense"]) # Example types
                layer_layout.addWidget(type_combobox, alignment=Qt.AlignLeft)
                layer_data['type_combobox'] = type_combobox

            # Add the horizontal layout to the main vertical layout
            self.layer_options_layout.addLayout(layer_layout)
            self.layer_widgets_dict.append(layer_data)

        # shitty way of doing this but whatever
        self.updating_layers = True
        self.update_neuron_spinboxes()
        self.update_type_comboboxes()
        self.updating_layers = False

        self.set_neuron_spinboxes_signals()
        self.set_type_comboboxes_signals()
        self.set_dropout_spinbox_signal()


    # --- Neuron Shi ---
    def set_neuron_spinboxes_signals(self):
        for i, layer in enumerate(self.layer_widgets_dict):
            if i != len(self.layer_widgets_dict)-1:
                layer['neuron_spinbox'].valueChanged.connect(self.update_neuron_spinboxes)

                if i < len(self.layer_neuron_values):
                    self.layer_neuron_values[i] = layer['neuron_spinbox'].value()
                else:
                    self.layer_neuron_values.append(layer['neuron_spinbox'].value())
    def update_neuron_spinboxes(self):
        if self.updating_layers: # this is set to true when the layer count is changing
            for k in range(len(self.layer_neuron_values)):
                if k < self.layer_count-1:
                    self.layer_widgets_dict[k]['neuron_spinbox'].setValue(self.layer_neuron_values[k])
        else:
            for i, layer in enumerate(self.layer_widgets_dict):
                if i != len(self.layer_widgets_dict)-1:
                    self.layer_neuron_values[i] = layer['neuron_spinbox'].value()

    # --- Type Shi ---
    def set_type_comboboxes_signals(self):
        for i, layer in enumerate(self.layer_widgets_dict):
            if i != len(self.layer_widgets_dict)-1:
                layer['type_combobox'].currentIndexChanged.connect(self.update_type_comboboxes)

                if i < len(self.layer_type_values):
                    self.layer_type_values[i] = layer['type_combobox'].currentIndex()
                else:
                    self.layer_type_values.append(layer['type_combobox'].currentIndex())
    def update_type_comboboxes(self):
        if self.updating_layers:
            for k in range(len(self.layer_type_values)):
                if k < self.layer_count-1:
                    self.layer_widgets_dict[k]['type_combobox'].setCurrentIndex(self.layer_type_values[k])
        else:
            for i, layer in enumerate(self.layer_widgets_dict):
                if i != len(self.layer_widgets_dict)-1:
                    self.layer_type_values[i] = layer['type_combobox'].currentIndex()


    # --- Dropout Shi ---
    def set_dropout_spinbox_signal(self):
        dropout_spinbox = self.layer_widgets_dict[len(self.layer_widgets_dict)-1]['dropout_spinbox']
        dropout_spinbox.valueChanged.connect(self.update_dropout)
    def update_dropout(self):
        dropout_spinbox = self.layer_widgets_dict[len(self.layer_widgets_dict)-1]['dropout_spinbox']
        self.dropout_val = dropout_spinbox.value()


    def on_restore_button_clicked(self):
        self.layer_widgets_dict = []
        self.layer_neuron_values = []
        self.layer_type_values = []
        self.dropout_val = 20
        self.update_layer_options()

    def on_selectalltcols_button_clicked(self):
        for row in range(self.ui.trainingcols_listwidget.count()):
            item = self.ui.trainingcols_listwidget.item(row)
            item.setSelected(True)
    def on_deselectalltcols_button_clicked(self):
        for row in range(self.ui.trainingcols_listwidget.count()):
            item = self.ui.trainingcols_listwidget.item(row)
            item.setSelected(False)


    def add_return_seq(self):
        for i, layer in enumerate(self.layer_widgets_dict):
            if i < len(self.layer_widgets_dict)-2:
                if (layer['type_combobox'].currentText() in ['LSTM', 'GRU', 'SimpleRNN'] and
                    self.layer_widgets_dict[i+1]['type_combobox'].currentText() in ['LSTM', 'GRU', 'SimpleRNN']):
                    layer['rseq'] = True
                else:
                    layer['rseq'] = False
            else:
                if i == len(self.layer_widgets_dict)-2:
                    layer['rseq'] = False

    def on_setmodel_button_clicked(self):
        self.add_return_seq()

        step_future = self.ui.stepfuture_spinbox.value()
        step_past = self.ui.steppast_spinbox.value()
        forecast_period = self.ui.forecastperiod_spinbox.value() + 1 # +1 because first forecasted data is the same as ending trainging data
        epochs = self.ui.epochs_spinbox.value()
        optimizer = self.ui.optimizer_combobox.currentText()
        loss = self.ui.loss_combobox.currentText()
        target_variable = self.target_variable
        trainingcols = []
        for row in range(self.ui.trainingcols_listwidget.count()):
            item = self.ui.trainingcols_listwidget.item(row)
            if item.isSelected():
                trainingcols.append(item.text())

        serialized_layer_widgets_dict = []
        for layer in self.layer_widgets_dict:
            layer_dict = {}
            for key, val in layer.items():
                if isinstance(val, QSpinBox):
                    layer_dict[key] = val.value()
                elif isinstance(val, QComboBox):
                    layer_dict[key] = val.currentText()
                else:
                    layer_dict[key] = val
            serialized_layer_widgets_dict.append(layer_dict)
        serialized_layer_widgets_dict = json.dumps(serialized_layer_widgets_dict)

        model_data = {
            "layer_widgets_dict": json.loads(serialized_layer_widgets_dict),
            "step_future": step_future,
            "step_past": step_past,
            "forecast_period": forecast_period,
            "epochs": epochs,
            "optimizer": optimizer,
            "loss": loss,
            "target_variable": target_variable,
            "training_cols": trainingcols
        }

        serialized_data = json.dumps(model_data, indent=4)

        self.data_submitted.emit(serialized_data)
        self.close()
