import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

def forecast(df, cols, model, scaler, trainX, target_variable, forecast_period=10):
    forecast_variable = target_variable
    df_for_training = df[cols].astype(float)

    train_dates = pd.to_datetime(df['date'])

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

    # Prepare training data
    training = df[['date', forecast_variable]].copy()
    training['date'] = pd.to_datetime(training['date'])

    # Fixing forecast offset
    last_training_price = training[forecast_variable].iloc[-1]
    first_forecast_price = df_forecast[forecast_variable].iloc[0]
    offset = last_training_price - first_forecast_price
    i = 0
    for price in df_forecast[forecast_variable]:
        df_forecast[forecast_variable].iloc[i] = price + offset
        i += 1

    return df_forecast
