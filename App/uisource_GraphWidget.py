from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent

import pandas as pd

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = None
        self.forecast_len = None
        self.graph_variable = None
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

        self.visible_start = 0  # start index of visible data
        self.visible_window = 100  # number of data points visible at a time


    def set_data(self, df, graph_variable):
        self.forecast_len = None
        self.df = None
        self.df = df
        self.graph_variable = None
        self.graph_variable = graph_variable

        self.visible_start = max(0, len(df) - self.visible_window) # last n points
        self.update()

    def set_forecast_result(self, result_df):
        self.df = pd.concat([self.df, result_df], ignore_index=True)
        self.forecast_len = len(result_df)
        self.visible_start = max(0, len(self.df) - self.visible_window) # last n points
        self.update()

    def set_params(self, window):
        if window != 'max':
            new_window = window
            if new_window < self.visible_window:  # window is decreasing
                # adjust visible start to keep the most recent (rightmost) data point constant
                self.visible_window = new_window
                self.visible_start = max(0, len(self.df) - new_window)
            else:
                self.visible_window = new_window
                max_visible_start = len(self.df) - self.visible_window
                self.visible_start = max(0, min(max_visible_start, self.visible_start))
        else:
            self.visible_window = len(self.df)
            max_visible_start = len(self.df) - self.visible_window
            self.visible_start = max(0, min(max_visible_start, self.visible_start))

        self.update()


    def clear_graph(self):
        self.df = None
        self.forecast_len = None
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)

        # draw background
        painter.fillRect(self.rect(), self.background_color)
        # draw axes
        self.draw_sumlines(painter)
        # draw graph
        if self.df is not None and len(self.df) > 0:
            self.draw_graph(painter)
        # draw crosshair
        if self.mouse_pos is not None:
            self.draw_crosshair(painter)


    def draw_sumlines(self, painter):
        painter.setPen(QPen(self.axis_color, 1))
        rect = self.rect()

        # vertical grid lines
        for i in range(1, 4):
            x = rect.width() / 4 * i
            painter.drawLine(x, rect.height(), x, 0)


    def draw_graph(self, painter):
        painter.setPen(QPen(self.line_color, 1))
        rect = self.rect()

        # visible slice of data
        visible_data = self.df.iloc[self.visible_start:self.visible_start + self.visible_window]
        if visible_data.empty:
            return

        column_data = pd.to_numeric(visible_data[self.graph_variable])

        # normalize data to center it around the middle line
        data_min = column_data.min()
        data_max = column_data.max()
        data_range = data_max - data_min
        midline_y = rect.height() / 2  # y-coordinate for the middle line

        # scale data so it fits in the vertical range of the widget
        if data_range == 0:
            y_scale = 0
        else:
            y_scale = (rect.height() - 2 * self.margin) / data_range

        points = []
        for i, value in enumerate(column_data):
            x = self.margin + i * ((rect.width() - 2 * self.margin) / (len(visible_data) - 1))
            y = midline_y - (value - (data_min + data_range / 2)) * y_scale
            points.append((x, y))

        # draw the graph
        if self.forecast_len is not None:
            for i in range(len(points) - 1):
                if i < len(points) - self.forecast_len - 1:
                    painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
                else:
                    painter.setPen(QPen(self.forecast_line_color, 1))
                    painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
        else:
            for i in range(len(points) - 1):
                painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])



    def draw_crosshair(self, painter):
        if self.mouse_pos == QPointF(-1, -1):
            return

        painter.setPen(QPen(self.crosshair_color, 1))
        rect = self.rect()

        # vertical line of the crosshair
        painter.drawLine(self.mouse_pos.x(), rect.height(), self.mouse_pos.x(), 0)
        # horizontal line of the crosshair
        painter.drawLine(rect.width(), self.mouse_pos.y(), 0, self.mouse_pos.y())

        # draw the variable
        if self.df is not None and self.graph_variable is not None:
            # get the visible slice of data
            visible_data = self.df.iloc[self.visible_start:self.visible_start + self.visible_window]
            if visible_data.empty:
                return

            column_data = pd.to_numeric(visible_data[self.graph_variable]).dropna()

            # calculate the corresponding index in the data (round to the nearest data point)
            graph_width = rect.width() - 2 * self.margin
            index_offset = (self.mouse_pos.x() - self.margin) / (graph_width / (len(column_data) - 1))
            index = int(round(index_offset))

            # ensure the index is within valid bounds
            index = max(0, min(len(column_data) - 1, index))

            # draw the graph variable on the crosshair
            if not column_data.empty:
                painter = QPainter(self)
                painter.setPen(QPen(self.crosshair_color, 1))

                # data point value
                data_value = column_data.iloc[index]
                val_text = f"{self.graph_variable}: {data_value:.2f}"
                font_metrics = painter.fontMetrics()
                val_text_width = font_metrics.horizontalAdvance(val_text)
                painter.drawText(self.mouse_pos.x() - val_text_width - 5, self.mouse_pos.y() - 5, val_text)
                # data point date
                date = visible_data['date'].iloc[index]
                date_text = f"date: {date}"
                date_text_width = font_metrics.horizontalAdvance(date_text)
                painter.drawText(self.mouse_pos.x() - date_text_width - 5, self.mouse_pos.y() + 14, date_text)

                # draw the circle at the current data point
                x_pos = self.margin + index * ((rect.width() - 2 * self.margin) / (len(visible_data) - 1))
                y_pos = rect.height() / 2 - (data_value - (column_data.min() + (column_data.max() - column_data.min()) / 2)) * ((rect.height() - 2 * self.margin) / (column_data.max() - column_data.min()))
                painter.setPen(QPen(QColor(35, 225, 232)))
                painter.setBrush(QColor(35, 225, 232))
                painter.drawEllipse(QPointF(x_pos, y_pos), 3, 3)


    # --- EVENTS ---

    def wheelEvent(self, event):
        if self.df is not None:
            delta = event.angleDelta().y() // -120  # scroll direction (1 step per scroll tick)
            new_start = self.visible_start - delta * 1  # move 5 data points per scroll tick
            self.visible_start = max(0, min(len(self.df) - self.visible_window, new_start))

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
