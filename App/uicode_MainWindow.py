from PySide6.QtCore import Signal, QThread
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
    QVBoxLayout
)

import sys
import json
import source_Misc as mc
import source_Train as tr
import source_Forecast as fc
import source_Indicators as ic

from ui_form_main import Ui_MainWindow

from uicode_CreateModelWindow import CreateModelWindow
from uicode_IndicatorWindow import IndicatorWindow
from uisource_GraphWidget import GraphWidget

# helper worker thread class to run the forecast function
class TrainingThread(QThread):
    finished = Signal(object, object, object)

    def __init__(self, df, layers_config, training_cols, epochs, step_future, step_past, dropout, optimizer, loss):
        super().__init__()
        self.df = df
        self.layers_config = layers_config
        self.training_cols = training_cols
        self.epochs = epochs
        self.step_future = step_future
        self.step_past = step_past
        self.dropout = dropout
        self.optimizer = optimizer
        self.loss = loss

    def run(self):
        try:
            model, scaler, cols = tr.train(self.df, self.layers_config, self.training_cols, self.epochs, self.step_future,
                self.step_past, self.dropout, self.optimizer, self.loss)

            self.finished.emit(model, scaler, cols)
        except Exception as e:
            self.finished.emit(e)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.df = None
        self.model_params = None

        # saved model
        self.model = None
        self.scaler = None
        self.cols = None
        self.trainX = None

        # setup combobox
        for ticker in mc.list_sp500_tickers():
            self.ui.ticker_combobox.addItem(ticker, ticker)
        self.ui.ticker_combobox.setCurrentIndex(-1)

        self.ui.forecast_progress_label.setVisible(False)

        self.ui.createmodel_button.setEnabled(False)
        self.ui.train_button.setEnabled(False)
        self.ui.forecast_button.setEnabled(False)
        self.ui.clearmodel_button.setVisible(False)

        # adding the graph widget
        self.graph_widget = GraphWidget()
        self.ui.graph_layout = QVBoxLayout(self.ui.graph_placeholder_widget)
        self.ui.graph_layout.addWidget(self.graph_widget)

        self.ui.datapointtime_combobox.addItems(['Daily']) # TODOOOOOOOO hardcoded until we have more data (brokerage)

        # ---- CONNECT SIGNALS ----

        # charting data
        self.ui.ticker_combobox.currentIndexChanged.connect(self.on_ticker_combobox_changed)

        # model stuff
        self.ui.createmodel_button.clicked.connect(self.on_createmodel_button_clicked)
        self.ui.train_button.clicked.connect(self.on_train_button_clicked)
        self.ui.forecast_button.clicked.connect(self.on_forecast_button_clicked)
        self.ui.clearmodel_button.clicked.connect(self.on_clearmodel_button_clicked)

        # graph stuff
        self.ui.candle_button.clicked.connect(self.on_candle_button_clicked)
        self.ui.line_button.clicked.connect(self.on_line_button_clicked)
        self.ui.arrow_button.clicked.connect(self.on_arrow_button_clicked)

        self.ui.window50_button.clicked.connect(self.on_timewindow50_changed)
        self.ui.window100_button.clicked.connect(self.on_timewindow100_changed)
        self.ui.window500_button.clicked.connect(self.on_timewindow500_changed)
        self.ui.windowmax_button.clicked.connect(self.on_timewindowmax_changed)

        self.ui.indicators_button.clicked.connect(self.on_indicators_button_clicked)

    # ---- SLOT FUNCTIONS ----

    #
    # data import stuff
    #
    def on_ticker_combobox_changed(self):
        ticker = self.ui.ticker_combobox.currentText()
        self.df = mc.get_data(ticker)

        if self.model is None:
            self.ui.createmodel_button.setEnabled(True)

        self.graph_widget.set_data(self.df, 'close') # closing price hard coded for the line graph


    #
    # graph stuff
    #

    def on_candle_button_clicked(self):
        self.graph_widget.set_lorc(False)
    def on_line_button_clicked(self):
        self.graph_widget.set_lorc(True)

    def on_arrow_button_clicked(self):
        self.graph_widget.goto_last()

    def on_timewindow50_changed(self):
        if self.df is not None:
            self.graph_widget.change_window(50)
    def on_timewindow100_changed(self):
        if self.df is not None:
            self.graph_widget.change_window(100)
    def on_timewindow500_changed(self):
        if self.df is not None:
            self.graph_widget.change_window(500)
    def on_timewindowmax_changed(self):
        if self.df is not None:
            self.graph_widget.change_window('max')

    def on_indicators_button_clicked(self):
        self.window = IndicatorWindow()
        # for data recieved
        self.window.data_submitted.connect(self.data_from_indicators)
        self.window.show()
    def data_from_indicators(self, indicator_data):
        print(indicator_data)


    #
    # forecast model stuff
    #

    def on_createmodel_button_clicked(self):
        filtered_df = self.df.drop(columns=['date'], errors='ignore')
        column_names = filtered_df.columns.tolist()
        target_variable = 'close' # TODOOOOOOOOOOOO hardcoded

        self.window = CreateModelWindow(column_names, target_variable)
        # for data recieved
        self.window.data_submitted.connect(self.data_from_create_model)
        self.window.show()
    def data_from_create_model(self, data):
        self.model_params = data

        self.ui.forecast_progress_label.setVisible(True)
        self.ui.forecast_progress_label.setText('Ready')
        self.ui.train_button.setEnabled(True)

    def on_train_button_clicked(self):
        # disable stuff while forecasting in progress
        self.ui.createmodel_button.setEnabled(False)
        self.ui.train_button.setEnabled(False)
        self.ui.clearmodel_button.setVisible(False)
        self.ui.forecast_progress_label.setText('Training...')

        layer_data = self.model_params['layer_widgets_dict']
        # create layer config and initialize dropout (dropout is in the layer_widgets_dict)
        layer_neuron_list = []
        layer_type_list = []
        layer_return_list = []
        dropout = 0
        for i, layer in enumerate(layer_data):
            if i != len(layer_data)-1:
                layer_neuron_list.append(layer['neuron_spinbox'])
                layer_type_list.append(layer['type_combobox'])
                layer_return_list.append(layer['rseq'])
            else:
                dropout = layer['dropout_spinbox'] / 100
        layer_count = len(layer_data) - 1 # not including the last dropout layer
        layers_config = mc.create_layer_config(layer_count, layer_neuron_list, layer_type_list, layer_return_list)

        self.training_thread = TrainingThread(self.df, layers_config, self.model_params['training_cols'], self.model_params['epochs'],
            self.model_params['step_future'], self.model_params['step_past'], dropout, self.model_params['optimizer'], self.model_params['loss'])

        self.training_thread.finished.connect(self.on_training_complete)
        self.training_thread.start()

    def on_training_complete(self, model, scaler, cols):
        self.ui.forecast_progress_label.setText('Saved')
        self.ui.clearmodel_button.setVisible(True)
        self.ui.forecast_button.setEnabled(True)
        self.ui.train_button.setEnabled(False)
        self.ui.createmodel_button.setEnabled(False)

        self.model = model
        self.scaler = scaler
        self.cols = cols

    def on_forecast_button_clicked(self):
        self.graph_widget.clear_forecast()

        print(self.scaler)
        try:
            forecast_df = fc.forecast(self.df, self.cols, self.model, self.scaler, self.model_params['target_variable'],
                self.model_params['forecast_period'], self.model_params['step_future'], self.model_params['step_past'])

            result = forecast_df.iloc[1:]
            self.graph_widget.set_forecast_result(result)
        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Forecast Error")
            error_dialog.setText("An error occurred while forecasting.")
            error_dialog.setInformativeText(str(e))  # show the exception message
            error_dialog.exec()

    def on_clearmodel_button_clicked(self):
        self.ui.clearmodel_button.setVisible(False)
        self.ui.forecast_progress_label.setVisible(False)
        self.ui.forecast_button.setEnabled(False)
        self.ui.createmodel_button.setEnabled(True)

        self.model = None
        self.scaler = None
        self.cols = None

        self.graph_widget.clear_forecast()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
