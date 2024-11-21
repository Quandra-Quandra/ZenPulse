import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
import os
import json

# Seed for reproducibility
np.random.seed(42)

# Simulating some physiological and behavioral data
def simulate_data(n_samples=1000):
    heart_rate = np.random.normal(70, 10, n_samples)
    sleep_hours = np.random.normal(7, 1.5, n_samples)
    activity_level = np.random.normal(3, 0.5, n_samples)
    stress_level = (0.3 * heart_rate + 0.4 * sleep_hours + 0.3 * activity_level + np.random.normal(0, 5, n_samples)) > 80

    data = pd.DataFrame({
        'heart_rate': heart_rate,
        'sleep_hours': sleep_hours,
        'activity_level': activity_level,
        'stress_level': stress_level.astype(int)
    })

    return data

# Generate synthetic data
data = simulate_data(1000)

# Features and target
features = data[['heart_rate', 'sleep_hours', 'activity_level']]
target = data['stress_level']

# Normalize features using Min-Max Scaling
scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

# Split the data into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(features_scaled, target, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Reshape features to 3D format for LSTM (samples, timesteps, features)
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_val = np.reshape(X_val, (X_val.shape[0], 1, X_val.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# Build the LSTM model
model = Sequential([
    Input(shape=(1, X_train.shape[2])),
    LSTM(units=50, return_sequences=False),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val), verbose=1)

# Save the model in Keras native format
model.save('stress_detection_model.keras')

# Load the saved model
model = load_model('stress_detection_model.keras')
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Profile system to store user data
user_profiles = {}

# Load profiles from file if it exists
if os.path.exists("user_profiles.json"):
    with open("user_profiles.json", "r") as file:
        user_profiles = json.load(file)

def save_profiles():
    """Save the user profiles to a JSON file."""
    with open("user_profiles.json", "w") as file:
        json.dump(user_profiles, file)

def create_or_select_profile():
    """Create or select a user profile."""
    username = input("Enter your username: ")
    if username not in user_profiles:
        print(f"Creating new profile for {username}...")
        user_profiles[username] = []
    else:
        print(f"Welcome back, {username}!")
    return username

def get_user_input():
    """Collect user input for physiological and behavioral data."""
    print("\nPlease provide your physiological and behavioral data.")
    heart_rate = float(input("Heart Rate (BPM): "))
    sleep_hours = float(input("Hours of Sleep: "))
    activity_level = float(input("Activity Level (1-10 scale): "))

    user_data = pd.DataFrame({
        'heart_rate': [heart_rate],
        'sleep_hours': [sleep_hours],
        'activity_level': [activity_level]
    })

    user_data_scaled = scaler.transform(user_data)
    user_data_scaled = np.reshape(user_data_scaled, (1, 1, user_data_scaled.shape[1]))

    return heart_rate, sleep_hours, activity_level, user_data_scaled

def stress_management_tips(is_stressed):
    """Provide tailored stress management tips based on the user's stress level."""
    print("\n### Stress Management Tips ###")
    if is_stressed:
        print("It seems you may be experiencing stress. Here are some tips to help manage it:")
        print("1. Try deep breathing exercises or short meditation sessions to calm your mind.")
        print("2. Ensure you're getting enough sleep. Aim for 7-8 hours per night.")
        print("3. Incorporate light exercise, like a 10-minute walk, into your daily routine.")
        print("\n### Helpful Resources ###")
        print("- Headspace or Calm (Mindfulness Apps)")
        print("- BetterHelp (Online Therapy)")
    else:
        print("You're not showing significant signs of stress. Here are some tips to maintain well-being:")
        print("1. Continue regular physical activity and ensure adequate sleep.")
        print("2. Stay connected with loved ones and reflect on positive moments.")
        print("\n### Resources for Maintaining Well-Being ###")
        print("- TED Talk: 'The Happy Secret to Better Work' by Shawn Achor")

def plot_and_save_results(username, data):
    """Plot and save the user's stress history."""
    history_df = pd.DataFrame(data)
    history_df['Submission'] = range(1, len(history_df) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(history_df['Submission'], history_df['prediction'].apply(lambda x: 1 if x == 'Stressed' else 0), marker='o', linestyle='-')
    plt.title(f"Stress Prediction History for {username}")
    plt.xlabel("Submission")
    plt.ylabel("Stress Level (1 = Stressed, 0 = Not Stressed)")
    plt.xticks(history_df['Submission'])
    plt.grid(True)
    plt.savefig(f"{username}_stress_history.png")
    plt.show()

def predict_stress(username):
    """Predict stress level and provide tailored output based on the result."""
    heart_rate, sleep_hours, activity_level, user_data_scaled = get_user_input()

    # Predict stress level
    _ = model.predict(np.zeros((1, 1, 3)))  # Warm-up
    prediction = model.predict(user_data_scaled, verbose=0)
    model_stress = (prediction > 0.5).astype(int)[0][0]

    predefined_stress = heart_rate < 60 or heart_rate > 80 or sleep_hours < 4 or sleep_hours > 10
    is_stressed = predefined_stress or model_stress

    result = "Stressed" if is_stressed else "Not Stressed"
    print(f"\nPrediction: You are {result}.")

    if predefined_stress:
        print(f"Factors include heart rate ({heart_rate} BPM) or sleep hours ({sleep_hours}) out of range.")

    # Save the result to user's profile
    submission_data = {
        'heart_rate': heart_rate,
        'sleep_hours': sleep_hours,
        'activity_level': activity_level,
        'prediction': result
    }
    user_profiles[username].append(submission_data)
    save_profiles()
    stress_management_tips(is_stressed)
    plot_and_save_results(username, user_profiles[username])

def view_history(username):
    """View the user's submission history."""
    if user_profiles[username]:
        print(f"\n### Submission History for {username} ###")
        for i, entry in enumerate(user_profiles[username], start=1):
            print(f"\nSubmission {i}:")
            print(f"  Heart Rate: {entry['heart_rate']} BPM")
            print(f"  Sleep Hours: {entry['sleep_hours']}")
            print(f"  Activity Level: {entry['activity_level']}")
            print(f"  Prediction: {entry['prediction']}")
    else:
        print("No history available.")

if __name__ == "__main__":
    username = create_or_select_profile()
    while True:
        print("\n1. Predict Stress")
        print("2. View Submission History")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            predict_stress(username)
        elif choice == '2':
            view_history(username)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")