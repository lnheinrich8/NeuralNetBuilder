import sys
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from sklearn.preprocessing import StandardScaler

from source_SequentialModel import SequentialModel

sys.stdout.reconfigure(encoding='utf-8')

# forecast n days into the future using GRU neural net
# params:
#   - df - dataframe of time series price data (requires a 'Date' column)
#   - layers_config - custom neural net layer layout
#   - target_variable - the variable that will be forecasted (must be included in the data set)
#   - training_cols - columns used for training the model where the first column is the forecasted variable.
#       * Specified columns must be in the dataframe parameter
#   - forecast_period - days to forecast into the future
#   - epochs - number of passes through the training dataset
#   - step_future - days to predict in the future for training
#   - step_past - days in past used to predict future for training
#   - dropout - percent random dropped neurons in training (value 0.0 to 1.0)
#   - optimizer - optimizer function for model (see keras documentation)
#   - loss - loss function for model (see keras documentation)
#   - past_years_iter - optional paramater to mock forecasting in the past and compare to the actual data

def forecast(df, layers_config, target_variable, training_cols=["open", "high", "low", "close", "volume"], forecast_period=10, epochs=10, step_future=2, step_past=16, dropout=0.2, optimizer='adam', loss='mse', past_years_iter=0):
    today = df['date'].max()
    year_iter = past_years_iter
    forecast_variable = training_cols[0]

    for i in range(year_iter, -1, -1):
        df2 = df.copy()
        ending_date = today.replace(year=today.year - i)
        df2 = df2.loc[df2['date'] <= ending_date]  # Training dataset is up until ending_date
        train_dates = pd.to_datetime(df2['date'])

        cols = training_cols

        # Using this df for training
        df_for_training = df2[cols].astype(float)

        # Scaling
        scaler = StandardScaler()
        scaler = scaler.fit(df_for_training)
        df_for_training_scaled = scaler.transform(df_for_training)

        trainX = []
        trainY = []

        n_future = step_future
        n_past = step_past

        for i in range(n_past, len(df_for_training_scaled) - n_future + 1):
            trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])
            trainY.append(df_for_training_scaled[i + n_future - 1:i + n_future, 0])

        trainX, trainY = np.array(trainX), np.array(trainY)

        m = SequentialModel(input_shape=(trainX.shape[1], trainX.shape[2]), output_shape=trainY.shape[1], layers_config=layers_config, dropout=dropout, optimizer=optimizer, loss=loss)
        model = m.get_model()

        # history object contains information about the training process like loss and validation loss (unused right now)
        history = model.fit(trainX, trainY, epochs=epochs, batch_size=16, validation_split=0.1, verbose=1)

        # Forecast period
        forecast_future = forecast_period
        forecast_period_dates = pd.date_range(list(train_dates)[-1], periods=forecast_future, freq='1d').tolist()
        forecast = model.predict(trainX[-forecast_future:])

        # Unscale forecasted data
        forecast_copies = np.repeat(forecast, df_for_training.shape[1], axis=-1)
        y_pred_future = scaler.inverse_transform(forecast_copies)[:, 0]

        # Prepare forecasted dates
        forecast_dates = [time_i.date() for time_i in forecast_period_dates]
        df_forecast = pd.DataFrame({'date': forecast_dates, forecast_variable: y_pred_future})
        df_forecast['date'] = pd.to_datetime(df_forecast['date']).dt.date
        # df_forecast['date'] = pd.to_datetime(df_forecast['date'])
        last_forecast_date = df_forecast['date'].max()

        # Actual Data
        df_actual = df.copy()
        df_actual.reset_index(inplace=True)
        df_actual['date'] = pd.to_datetime(df['date'])

        # Prepare training data
        training = df2[['date', forecast_variable]].copy()
        training['date'] = pd.to_datetime(training['date'])
        # Subtract 6 months from the ending date
        nine_months_ago = pd.to_datetime(ending_date) - relativedelta(months=9)
        # Filter training data
        training = training.loc[training['date'] >= nine_months_ago]
        last_training_date = training['date'].iloc[-1]

        # Fixing forecast offset
        last_training_price = training[forecast_variable].iloc[-1]
        first_forecast_price = df_forecast[forecast_variable].iloc[0]
        offset = last_training_price - first_forecast_price
        i = 0
        for price in df_forecast[forecast_variable]:
            df_forecast[forecast_variable].iloc[i] = price + offset
            i += 1


        return df_forecast

        # # Prepare actual data for comparison
        # actual = df_actual[['date', forecast_variable]]
        # actual['date'] = pd.to_datetime(actual['date'])
        # actual = actual.loc[actual['date'] >= last_training_date]  # Start from the day after the last date in 'original'
        # actual = actual.loc[actual['date'] <= last_forecast_date]


        # fig = go.Figure()
        # fig.add_trace(go.Scatter(x=training['date'], y=training[forecast_variable], mode='lines', name='Historical'))
        # fig.add_trace(go.Scatter(x=df_forecast['date'], y=df_forecast[forecast_variable], mode='lines', name='Forecasted'))
        # fig.add_trace(go.Scatter(x=actual['date'], y=actual[forecast_variable], mode='lines', name='Actual'))
        # fig.update_layout(
        #     title='Stock Data and Forecast: ' + last_training_date.strftime('%Y-%m-%d'),
        #     xaxis_title='Date',
        #     yaxis_title=forecast_variable,
        #     hovermode='x unified'  # Enable hover on the same x-axis
        # )

        # fig.show()
