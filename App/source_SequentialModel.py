# to hide tensor flow logs too annoying rn
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dropout, Dense, GRU, SimpleRNN # type: ignore

class SequentialModel:

    def __init__(self, input_shape, output_shape, layers_config, dropout, optimizer, loss):
        """
        Initializes the neural network model.

        Parameters:
        - input_shape: Tuple (timesteps, features) specifying input data shape.
        - output_shape: Integer specifying the number of output features.
        - layers_config: List of dictionaries specifying the configuration for each layer.
                         Each dictionary should have keys 'neurons', 'layer_type', and additional layer-specific parameters.
        - net_type: String specifying the type of neural network ('LSTM', 'GRU', 'SimpleRNN', etc.).
        - dropout: Float specifying dropout rate (default: 0.2).
        - optimizer: String specifying the optimizer to use (default: 'adam').
        - loss: String specifying the loss function to use (default: 'mse').
        """
        self.model = Sequential()

        # Add layers based on configuration
        for i, layer in enumerate(layers_config):
            layer_type = layer.get('layer_type')
            neurons = layer.get('neurons')
            return_sequences = layer.get('return_sequences')

            if layer_type == 'Dense':
                if i == 0:
                    self.model.add(Dense(neurons, input_shape=input_shape))
                else:
                    self.model.add(Dense(neurons))
            elif layer_type == 'LSTM':
                if i == 0:
                    self.model.add(LSTM(neurons, input_shape=input_shape, return_sequences=return_sequences))
                else:
                    self.model.add(LSTM(neurons, return_sequences=return_sequences))
            elif layer_type == 'GRU':
                if i == 0:
                    self.model.add(GRU(neurons, input_shape=input_shape, return_sequences=return_sequences))
                else:
                    self.model.add(GRU(neurons, return_sequences=return_sequences))
            elif layer_type == 'SimpleRNN':
                if i == 0:
                    self.model.add(SimpleRNN(neurons, input_shape=input_shape, return_sequences=return_sequences))
                else:
                    self.model.add(SimpleRNN(neurons, return_sequences=return_sequences))
            else:
                raise ValueError(f"Unsupported layer type: {layer_type}")

        self.model.add(Dropout(dropout))
        self.model.add(Dense(output_shape))
        self.model.compile(optimizer=optimizer, loss=loss)

    def get_model(self):
        """
        Returns the compiled neural network model.
        """
        return self.model








