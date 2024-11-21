import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Seed for reproducibility
np.random.seed(42)

# Simulating time-series data
def simulate_time_series_data(n_samples=1000, sequence_length=7):
    # Simulate daily metrics for a sequence
    heart_rate = np.random.normal(70, 10, (n_samples, sequence_length))
    sleep_hours = np.random.normal(7, 1.5, (n_samples, sequence_length))
    activity_level = np.random.normal(3, 0.5, (n_samples, sequence_length))
    
    # Create stress levels (binary) for the next day based on weighted sums
    future_stress_level = (0.3 * heart_rate[:, -1] + 0.4 * sleep_hours[:, -1] +
                           0.3 * activity_level[:, -1] + np.random.normal(0, 5, n_samples)) > 80
    
    data = np.stack([heart_rate, sleep_hours, activity_level], axis=-1)
    return data, future_stress_level.astype(int)

# Generate synthetic time-series data
X, y = simulate_time_series_data(1000, sequence_length=7)

# Normalize features using Min-Max Scaling
scaler = MinMaxScaler()
X_scaled = np.zeros_like(X)
for i in range(X.shape[2]):
    X_scaled[:, :, i] = scaler.fit_transform(X[:, :, i])

# Split the data into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print("Training data shape:", X_train.shape)

# Build the LSTM model for prediction
model = Sequential()

# LSTM layers
model.add(LSTM(units=50, return_sequences=False, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))

# Dense output layer (binary classification)
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Model summary
model.summary()

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val), verbose=1)

# Plot training & validation accuracy and loss
plt.plot(history.history['accuracy'], label='train_accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(loc='upper left')
plt.show()

plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(loc='upper left')
plt.show()

# Evaluate the model on test data
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy}")

# Predict on test data
predictions = (model.predict(X_test) > 0.5).astype(int)

# Print first 10 predictions
print("Predictions:", predictions[:10].flatten())
print("True Values:", y_test[:10])
