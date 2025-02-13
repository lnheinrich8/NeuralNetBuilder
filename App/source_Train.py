import sys
import numpy as np
from sklearn.preprocessing import StandardScaler

from source_SequentialModel import SequentialModel

sys.stdout.reconfigure(encoding='utf-8')

def train(df, layers_config, training_cols=["open", "high", "low", "close", "volume"], epochs=5, step_future=4, step_past=16, dropout=0.2, optimizer='adam', loss='mse'):

    cols = training_cols

    # Using this df for training
    df_for_training = df[cols].astype(float)

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

    return model, scaler, cols

