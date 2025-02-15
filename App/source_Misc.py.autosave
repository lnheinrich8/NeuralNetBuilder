import yfinance as yf
import pandas as pd
import numpy as np
import pywt
import requests
from bs4 import BeautifulSoup

# DATASET ALTERATION

def wavelet_transform(df, col):
    coeffs = pywt.wavedec(df[col], 'db38', mode='symmetric')
    k = 4
    while True:
        try:
            for i in range(k):
                coeffs[i + k] = np.zeros(coeffs[i + k].shape)
            denoised = pywt.waverec(coeffs, 'db38', mode='symmetric')
            break
        except IndexError:
            k -= 1
    return denoised if len(denoised) == len(df) else denoised[1:]


# MISC

def get_data(ticker, length='max'):
    try:
        stock = yf.Ticker(ticker)
        historical_data = stock.history(period=length)
        df = historical_data[["Open", "High", "Low", "Close", "Volume"]].copy()
        df.columns = df.columns.str.lower()
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])

        # check if time step is in days
        min_diff = df['Date'].diff().dropna().dt.days.min()
        if min_diff >= 1:
            df['Date'] = df['Date'].dt.date

        df.rename(columns={"Date": "date"}, inplace=True)
        return df
    except:
        print(f'issue is probably that ticker {ticker} does not exist idk tho')
        return

def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.lower()  # Standardize column names to lowercase

        # Get the name of the first column (could be date or timestep)
        time_column = df.columns[0]  # First column

        # Check if the first column is related to time and convert it to datetime
        df[time_column] = pd.to_datetime(df[time_column])

        # Check if time step is in days
        min_diff = df[time_column].diff().dropna().dt.days.min()
        if min_diff >= 1:
            df[time_column] = df[time_column].dt.date  # Only keep the date part

        # Rename the first column to 'date' to standardize
        df.rename(columns={time_column: 'date'}, inplace=True)

        df.reset_index(drop=True, inplace=True)  # Reset index and drop the old one
        return df
    except FileNotFoundError:
        print(f"File {file_path} does not exist.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

def list_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    tickers = [row.find('td').text.strip() for row in table.find_all('tr')[1:]]
    return tickers

#   - n_layers - number of sequential layers in the model NOT INCLUDING OUTPUT LAYER
#       * the optional params must have the same number of elements as n_layers
#   - layer_type_list - optional list param used for different types of layers (defualt sets all layers to LSTM)
#       * example: ['lstm', 'gru', 'gru'] - makes layer1 type lstm and layers 2 and 3 type gru
#   - layer_neuron_list - optional list param used for neuron count on different layers (default sets all layer neuron counts to 64)
#       * example: [32, 64] - layer1 uses 32 neurons and layer2 uses 64
#   - layer_return_list - optional list param that declares return_sequences bool for each layer
#       * example: [True, False] - you get it
def create_layer_config(n_layers=2, layer_neuron_list=None, layer_type_list=None, layer_return_list=None):
    if layer_neuron_list is None:
        layer_neuron_list = [64] * n_layers
    if layer_type_list is None:
        layer_type_list = ['LSTM'] * n_layers
    if layer_return_list is None:
        layer_return_list = [True] + [False] * (n_layers - 1)

    if len(layer_type_list) != n_layers:
        raise ValueError(
            f"`layer_type_list` length must be equal to `n_layers`. "
            f"Expected {n_layers}, but got {len(layer_type_list)}."
        )
    if len(layer_neuron_list) != n_layers:
        raise ValueError(
            f"`layer_neuron_list` length must be equal to `n_layers`. "
            f"Expected {n_layers}, but got {len(layer_neuron_list)}."
        )
    if len(layer_return_list) != n_layers:
        raise ValueError(
            f"`layer_return_list` length must be equal to `n_layers`. "
            f"Expected {n_layers}, but got {len(layer_return_list)}."
        )

    # Build the configuration for each layer
    layers_config = []
    for i in range(n_layers):
        layers_config.append({
            'neurons': layer_neuron_list[i],
            'layer_type': layer_type_list[i],
            'return_sequences': layer_return_list[i]
        })

    return layers_config
