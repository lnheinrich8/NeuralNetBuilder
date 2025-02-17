from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent

import pandas as pd

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # main data stuff
        self.df = None
        self.graph_variable = None
        self.draw_linegraph = False

        # dictionary of indicators
        self.indicators = {}

        self.forecast_len = None

        self.margin = 10
        self.line_color = QColor(242, 7, 74)
        self.forecast_line_color = QColor(0, 0, 255)
        self.background_color = QColor(0, 0, 0)
        self.axis_color = QColor(60, 60, 60)

        # cursor shi
        self.setCursor(Qt.BlankCursor)
        self.setAttribute(Qt.WA_Hover, True)
        self.setMouseTracking(True)
        self.mouse_pos = None
        self.crosshair_color = QColor(200, 200, 200)

        self.visible_end = 0
        self.visible_window = 50  # number of data points visible at a time


    def set_data(self, df, graph_variable):
        self.forecast_len = None
        self.df = df
        self.graph_variable = graph_variable
        self.visible_end = len(df)
        self.indicators.clear()
        self.update()
    def change_window(self, window):
        if window != 'max':
            self.visible_window = window
        else:
            self.visible_window = len(self.df)
            self.visible_end = len(self.df)
        self.update()
    def set_lorc(self, line): # line or candle
        self.draw_linegraph = line
        self.update()

    def set_forecast_result(self, result_df):
        self.df = pd.concat([self.df, result_df], ignore_index=True)
        self.forecast_len = len(result_df)
        self.visible_end = len(self.df)
        self.update()

    def add_indicator(self, indicator_key, indicator_df):
        self.indicators[indicator_key] = indicator_df
        self.update()
    def remove_indicator(self, indicator_key): # needs testing
        self.indicators.pop(indicator_key, None)
        self.update()
    def clear_indicators(self): # needs testing
        self.indicators.clear()
        self.update()

    def clear_forecast(self):
        if self.forecast_len is not None:
            self.df = self.df.iloc[:-self.forecast_len]
            self.forecast_len = None
        self.update()
    def clear_graph(self):
        self.df = None
        self.forecast_len = None
        self.update()
    def goto_last(self):
        self.visible_end = len(self.df)
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)

        # draw background
        painter.fillRect(self.rect(), self.background_color)
        # draw background lines
        self.draw_sumlines(painter)
        # draw graph
        painter.setRenderHint(QPainter.Antialiasing, True)
        if self.df is not None and len(self.df) > 0:
            if self.visible_window > 200 or self.draw_linegraph:
                self.draw_line(painter, self.df)
            else:
                self.draw_candles(painter, self.df)
        # draw indicators
        if len(self.indicators) != 0:
            self.draw_indicators(painter, self.indicators)
        # draw crosshair
        painter.setRenderHint(QPainter.Antialiasing, False)
        if self.mouse_pos is not None:
            self.draw_crosshair(painter)


    def draw_sumlines(self, painter):
        painter.setPen(QPen(self.axis_color, 1))
        rect = self.rect()

        # vertical grid lines
        for i in range(1, 4):
            x = rect.width() / 4 * i
            painter.drawLine(x, rect.height(), x, 0)


    def draw_line(self, painter, df):
        painter.setPen(QPen(self.line_color, 2))
        rect = self.rect()

        # visible slice of data
        visible_data = df.iloc[self.visible_end - self.visible_window:self.visible_end]
        if visible_data.empty:
            return

        column_data = pd.to_numeric(visible_data[self.graph_variable])

        data_min, data_max = self.get_global_minmax()
        data_range = data_max - data_min

        midline_y = rect.height() / 2  # y-coordinate for the middle line

        # scale data so it fits in the vertical range of the widget
        if data_range == 0:
            y_scale = 0
        else:
            y_scale = (rect.height() - 2 * self.margin) / data_range

        points = []
        for i, value in enumerate(column_data):
            x = self.margin + i * ((rect.width() - 2 * self.margin) / (self.visible_window - 1))
            y = midline_y - (value - (data_min + data_range / 2)) * y_scale
            points.append((x, y))

        # draw the graph
        if self.forecast_len is not None:
            for i in range(len(points) - 1):
                if i < len(points) - self.forecast_len - 1:
                    painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
                else:
                    painter.setPen(QPen(self.forecast_line_color, 2))
                    painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
        else:
            for i in range(len(points) - 1):
                painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])


    def draw_candles(self, painter, df):
        painter.setPen(QPen(self.line_color, 2))
        rect = self.rect()

        # visible slice of data
        visible_data = df.iloc[self.visible_end - self.visible_window:self.visible_end]
        if visible_data.empty:
            return

        data_min, data_max = self.get_global_minmax()
        data_range = data_max - data_min

        y_scale = (rect.height() - 2 * self.margin) / data_range

        # candle width
        candle_width = max(5, (rect.width() - 2 * self.margin) / (self.visible_window * 2))

        if self.forecast_len is not None:
            points = []
            forecast_start_index = self.visible_window - self.forecast_len  # forecast start

            for i, (index, row) in enumerate(visible_data.iterrows()):
                x = self.margin + i * ((rect.width() - 2 * self.margin) / (self.visible_window - 1))
                close_y = rect.height() - self.margin - (row['close'] - data_min) * y_scale

                if i < forecast_start_index:
                    if i == forecast_start_index-1: # this isn't a forecasted value but a start for the first line drawn
                        points.append((x, close_y))

                    high_y = rect.height() - self.margin - (row['high'] - data_min) * y_scale
                    low_y = rect.height() - self.margin - (row['low'] - data_min) * y_scale
                    open_y = rect.height() - self.margin - (row['open'] - data_min) * y_scale

                    if row['close'] >= row['open']:
                        candle_color = QColor("green")  # Bullish
                    else:
                        candle_color = QColor("red")    # Bearish

                    painter.setPen(QPen(candle_color, 1))
                    painter.drawLine(int(x), int(high_y), int(x), int(low_y))  # wick

                    painter.setPen(candle_color)
                    painter.setBrush(candle_color)
                    painter.drawRect(int(x - candle_width / 2), int(min(open_y, close_y)),
                                    int(candle_width), int(abs(open_y - close_y)))
                else:
                    # forecasted values for line drawing
                    points.append((x, close_y))

            # draw the forecasted values as a line
            if len(points) > 1:
                painter.setPen(QPen(self.forecast_line_color, 2, Qt.SolidLine))
                for i in range(len(points) - 1):
                    painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])

        else:
            for i, (index, row) in enumerate(visible_data.iterrows()):

                x = self.margin + i * ((rect.width() - 2 * self.margin) / (self.visible_window - 1))

                high_y = rect.height() - self.margin - (row['high'] - data_min) * y_scale
                low_y = rect.height() - self.margin - (row['low'] - data_min) * y_scale
                open_y = rect.height() - self.margin - (row['open'] - data_min) * y_scale
                close_y = rect.height() - self.margin - (row['close'] - data_min) * y_scale

                if row['close'] >= row['open']:
                    candle_color = QColor("green")  # Bullish
                else:
                    candle_color = QColor("red")    # Bearish

                painter.setPen(QPen(candle_color, 1))
                painter.drawLine(int(x), int(high_y), int(x), int(low_y))

                painter.setPen(candle_color)
                painter.setBrush(candle_color)
                painter.drawRect(int(x - candle_width / 2), int(min(open_y, close_y)),
                                 int(candle_width), int(abs(open_y - close_y)))


    def draw_indicators(self, painter, indicators):
        painter.setPen(QPen(self.forecast_line_color, 2)) # TODOOOOOOOOOO change color based on set indicator color
        rect = self.rect()

        data_min, data_max = self.get_global_minmax()
        data_range = data_max - data_min

        if data_range == 0:
            return

        y_scale = (rect.height() - 2 * self.margin) / data_range

        for key, df in indicators.items():
            visible_data = df.iloc[self.visible_end - self.visible_window:self.visible_end]

            column_data = pd.to_numeric(visible_data)

            points = []
            for i, value in enumerate(column_data):
                x = self.margin + i * ((rect.width() - 2 * self.margin) / (self.visible_window - 1))

                y = rect.height() - self.margin - (value - data_min) * y_scale
                points.append((x, y))

            # draw indicator line
            for i in range(len(points) - 1):
                painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])


    def get_global_minmax(self):
        visible_price_data = self.df.iloc[self.visible_end - self.visible_window:self.visible_end]

        # min/max for the price data
        price_min = visible_price_data[['low']].min().values[0]
        price_max = visible_price_data[['high']].max().values[0]

        # min/max for indicators
        indicator_min, indicator_max = float('inf'), float('-inf')
        for key, ind_df in self.indicators.items():
            visible_data = ind_df.iloc[self.visible_end - self.visible_window:self.visible_end]
            if visible_data.empty:
                continue
            col_data = pd.to_numeric(visible_data)
            indicator_min = min(indicator_min, col_data.min())
            indicator_max = max(indicator_max, col_data.max())

        global_min = min(price_min, indicator_min)
        global_max = max(price_max, indicator_max)

        return global_min, global_max



    def draw_crosshair(self, painter):
        if self.mouse_pos == QPointF(-1, -1):
            return
        painter.setPen(QPen(self.crosshair_color, 1))
        rect = self.rect()
        # vertical and horizontal lines of the crosshair
        painter.drawLine(self.mouse_pos.x(), rect.height(), self.mouse_pos.x(), 0)
        painter.drawLine(rect.width(), self.mouse_pos.y(), 0, self.mouse_pos.y())
        if self.df is None or self.df.empty:
            return

        # visible slice of data
        visible_data = self.df.iloc[self.visible_end - self.visible_window:self.visible_end]
        if visible_data.empty:
            return
        # min and max price values in the current window
        data_min = visible_data["low"].min()
        data_max = visible_data["high"].max()
        # convert Y-position to a price value
        price_range = data_max - data_min
        if price_range == 0:
            return
        y_scale = (rect.height() - 2 * self.margin) / price_range
        price_at_cursor = data_max - ((self.mouse_pos.y() - self.margin) / y_scale)

        # display the price
        price_text = f"{price_at_cursor:.2f}"
        text_rect = painter.boundingRect(rect, Qt.AlignLeft, price_text)
        text_x = rect.width() - text_rect.width() - 5
        text_y = max(self.mouse_pos.y() - 10, 15)  # Adjust to avoid going off-screen
        painter.setPen(QPen(Qt.white))
        painter.drawText(text_x, text_y, price_text)

        # display the date
        graph_width = rect.width() - 2 * self.margin
        index_offset = (self.mouse_pos.x() - self.margin) / (graph_width / (len(visible_data) - 1))
        index = int(round(index_offset))
        index = max(0, min(len(visible_data) - 1, index))
        date = visible_data['date'].iloc[index]
        date_text = f"{date}"
        font_metrics = painter.fontMetrics()
        date_text_width = font_metrics.horizontalAdvance(date_text)
        text_x = self.mouse_pos.x() - date_text_width - 5
        text_y = rect.height() - font_metrics.height() + 5  # Place near the bottom
        painter.setPen(QPen(Qt.white))
        painter.drawText(text_x, text_y, date_text)


    # --- EVENTS ---

    def wheelEvent(self, event):
        if self.df is not None and self.visible_window != len(self.df):
            delta = event.angleDelta().y() // -120  # scroll direction (1 step per scroll tick)
            change_end = self.visible_end - delta * 1  # move 1 data points per scroll tick
            self.visible_end = min(len(self.df), change_end)

            if self.forecast_len is not None:
                self.df = self.df.iloc[:-self.forecast_len]
                self.forecast_len = None

            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.mouse_pos = event.pos()  # mouse position relative to the widget
        self.update()

    def leaveEvent(self, event):
        self.mouse_pos = QPointF(-1, -1) # set crosshair to a hidden point
        self.update()
