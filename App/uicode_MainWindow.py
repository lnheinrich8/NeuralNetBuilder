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
import source_Forecast as fc

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form_main import Ui_MainWindow
from uicode_CreateModelWindow import CreateModelWindow
from uisource_GraphWidget import GraphWidget

# helper worker thread class to run the forecast function
class ForecastWorker(QThread):
    finished = Signal(object)

    def __init__(self, df, layers_config, target_var, training_cols, forecast_period, epochs, step_future, step_past, dropout, optimizer, loss):
        super().__init__()
        self.df = df
        self.layers_config = layers_config
        self.target_var = target_var
        self.training_cols = training_cols
        self.forecast_period = forecast_period
        self.epochs = epochs
        self.step_future = step_future
        self.step_past = step_past
        self.dropout = dropout
        self.optimizer = optimizer
        self.loss = loss

    def run(self):
        forecast_df = None
        try:
            forecast_df = fc.forecast(self.df, self.layers_config, self.target_var, training_cols=self.training_cols,
                forecast_period=self.forecast_period, epochs=self.epochs, step_future=self.step_future, step_past=self.step_past,
                dropout=self.dropout, optimizer=self.optimizer, loss=self.loss)
            self.finished.emit(forecast_df)
        except Exception as e:
            self.finished.emit(e)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.df = None
        self.data_loaded = False
        self.model_params = None

        # setup combobox
        for ticker in mc.list_sp500_tickers():
            self.ui.ticker_combobox.addItem(ticker, ticker)
        self.ui.ticker_combobox.setCurrentIndex(-1)

        self.ui.forecast_progress_label.setVisible(False)

        self.ui.createmodel_button.setEnabled(False)
        self.ui.forecast_button.setEnabled(False)

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
        self.ui.forecast_button.clicked.connect(self.on_forecast_button_clicked)
        # self.ui.cols_combobox.currentIndexChanged.connect(self.on_cols_combobox_changed) # TODOOO edit this behavior

        # graph stuff
        self.ui.candle_button.clicked.connect(self.on_candle_button_clicked)
        self.ui.line_button.clicked.connect(self.on_line_button_clicked)
        self.ui.arrow_button.clicked.connect(self.on_arrow_button_clicked)

        self.ui.window10_button.clicked.connect(self.on_timewindow10_changed)
        self.ui.window50_button.clicked.connect(self.on_timewindow50_changed)
        self.ui.window100_button.clicked.connect(self.on_timewindow100_changed)
        self.ui.window500_button.clicked.connect(self.on_timewindow500_changed)
        self.ui.window1000_button.clicked.connect(self.on_timewindow1000_changed)
        self.ui.windowmax_button.clicked.connect(self.on_timewindowmax_changed)


    # ---- SLOT FUNCTIONS ----

    #
    # data import stuff
    #
    def on_ticker_combobox_changed(self):
        ticker = self.ui.ticker_combobox.currentText()
        self.df = mc.get_data(ticker)

        self.ui.createmodel_button.setEnabled(True)

        self.data_loaded = True
        self.show_column_options(True)
        self.graph_widget.set_data(self.df, 'close') # closing price hard coded for the line graph

    def show_column_options(self, show):
        self.ui.cols_combobox.clear()
        if show:
            filtered_df = self.df.drop(columns=['date'], errors='ignore')
            column_names = filtered_df.columns.tolist()
            self.ui.cols_combobox.addItems(column_names)

    #
    # graph stuff
    #

    def on_candle_button_clicked(self):
        self.graph_widget.set_lorc(False)
    def on_line_button_clicked(self):
        self.graph_widget.set_lorc(True)

    def on_arrow_button_clicked(self):
        self.graph_widget.goto_last()

    def on_timewindow10_changed(self):
        if self.df is not None:
            self.graph_widget.set_params(10)
    def on_timewindow50_changed(self):
        if self.df is not None:
            self.graph_widget.set_params(50)
    def on_timewindow100_changed(self):
        if self.df is not None:
            self.graph_widget.set_params(100)
    def on_timewindow500_changed(self):
        if self.df is not None:
            self.graph_widget.set_params(500)
    def on_timewindow1000_changed(self):
        if self.df is not None:
            self.graph_widget.set_params(1000)
    def on_timewindowmax_changed(self):
        if self.df is not None:
            self.graph_widget.set_params('max')


    #
    # forecast model stuff
    #

    # def on_cols_combobox_changed(self):
    #     if self.ui.cols_combobox.count() != 0:
    #         self.graph_widget.set_data(self.df, self.ui.cols_combobox.currentText())

    def on_createmodel_button_clicked(self):
        filtered_df = self.df.drop(columns=['date'], errors='ignore')
        column_names = filtered_df.columns.tolist()
        target_variable = self.ui.cols_combobox.currentText()

        self.window = CreateModelWindow(column_names, target_variable)
        # for data recieved
        self.window.data_submitted.connect(self.data_from_create_model)
        self.window.show()
    def data_from_create_model(self, serialized_data):
        self.model_params = json.loads(serialized_data)
        self.ui.forecast_button.setEnabled(True)

    def on_forecast_button_clicked(self):
        # disable stuff while forecasting in progress
        self.enableb_forecast(False)

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

        # run the forecast in a separate thread
        self.ui.forecast_progress_label.setVisible(True)

        self.forecast_worker = ForecastWorker(self.df, layers_config, self.model_params['target_variable'], self.model_params['training_cols'],
            self.model_params['forecast_period'], self.model_params['epochs'], self.model_params['step_future'], self.model_params['step_past'],
            dropout, self.model_params['optimizer'], self.model_params['loss'])

        self.forecast_worker.finished.connect(self.on_forecast_complete)
        self.forecast_worker.start()

    # this might grow with more functions later in dev
    def enableb_forecast(self, bool):
        self.ui.createmodel_button.setEnabled(bool)
        self.ui.forecast_button.setEnabled(bool)

    def on_forecast_complete(self, result):
        self.ui.forecast_progress_label.setVisible(False)
        self.enableb_forecast(True) # enable all the buttons here where the thread finishes

        if isinstance(result, Exception):
            # handle the exception
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Forecast Error")
            error_dialog.setText("An error occurred while forecasting.")
            print(result)
            error_dialog.setInformativeText(str(result))  # show the exception message
            error_dialog.exec()
        else:
            result = result.iloc[1:]
            self.graph_widget.set_forecast_result(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
