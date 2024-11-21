from flask import Flask, request, jsonify
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import pandas as pd

app = Flask(__name__)

# Load the pre-trained model
model = load_model('stress_detection_model.keras')

# Load and fit the MinMaxScaler
try:
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError:
    # Fallback in case the scaler wasn't saved correctly
    scaler = MinMaxScaler()
    scaler.fit(np.array([[50, 5, 1], [100, 10, 10]]))  # Placeholder range for features

@app.route('/predict_single', methods=['POST'])
def predict_stress_single():
    try:
        data = request.json
        print(f"Received data: {data}")

        # Extract individual inputs
        heart_rate = data.get('heart_rate')
        sleep_hours = data.get('sleep_hours')
        activity_level = data.get('activity_level')

        # Ensure all fields are present
        if heart_rate is None or sleep_hours is None or activity_level is None:
            return jsonify({'error': 'Missing input fields.'}), 400

        # Process input for a single entry
        user_data = pd.DataFrame({
            'heart_rate': [float(heart_rate)],
            'sleep_hours': [float(sleep_hours)],
            'activity_level': [float(activity_level)]
        })

        # Scale data
        user_data_scaled = scaler.transform(user_data)

        # Reshape data for the model (single entry)
        user_data_scaled = np.reshape(user_data_scaled, (1, 1, 3))  # Shape: [batch_size, timesteps, features]

        # Predict using the model
        prediction = model.predict(user_data_scaled, verbose=0)[0][0]
        print(f"Prediction shape: {prediction.shape}")
        print(f"Prediction: {prediction}")

        # Determine stress level
        stress_level = "Stressed" if prediction > 0.00012 else "Not Stressed"

        response = {
            'prediction': stress_level,
            'message': f'Stress level determined based on your input: {stress_level}.'
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict_seven_days', methods=['POST'])
def predict_stress_seven_days():
    try:
        data = request.json
        print(f"Received data for 7 days: {data}")

        # Ensure we have data for exactly 7 days
        sequence = data.get('sequence')
        if not sequence or len(sequence) != 7:
            return jsonify({'error': 'Missing or incorrect input sequence (expected 7 days).'}), 400

        # Process the sequence of 7 days
        sequence_data = np.array(sequence)
        user_data = pd.DataFrame(sequence_data, columns=['heart_rate', 'sleep_hours', 'activity_level'])

        # Scale data
        user_data_scaled = scaler.transform(user_data)

        # Reshape data for the model (7-day sequence)
        user_data_scaled = np.reshape(user_data_scaled, (1, 7, 3))  # Shape: [batch_size, timesteps, features]

        # Predict using the model
        prediction = model.predict(user_data_scaled, verbose=0)[0][0]
        print(f"Prediction shape: {prediction.shape}")
        print(f"Prediction: {prediction}")

        # Determine stress level based on prediction
        stress_level = "Stressed" if prediction > 3.0 else "Not Stressed"

        # Future prediction (next day's stress level)
        future_prediction = "Stressed" if prediction > 3.0 else "Not Stressed"

        response = {
            'prediction': stress_level,
            'future_prediction': future_prediction,
            'message': f'Stress level determined based on your input: {stress_level}.'
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
