<?php
include_once 'header.php';
?>

<section class="signup-form">
    <h2 class="login">Stress Prediction</h2>
    <div class="signup-form-form">
    <form id="sevenDayForm" method="POST" action="">
        <?php for ($day = 1; $day <= 7; $day++): ?>
            <h4>Day <?php echo $day; ?></h4>
            <label for="day<?php echo $day; ?>HeartRate">Heart Rate (BPM):</label>
            <input type="number" id="day<?php echo $day; ?>HeartRate" name="day<?php echo $day; ?>HeartRate" step="any" required><br><br>

            <label for="day<?php echo $day; ?>SleepHours">Hours of Sleep:</label>
            <input type="number" id="day<?php echo $day; ?>SleepHours" name="day<?php echo $day; ?>SleepHours" step="any" required><br><br>

            <label for="day<?php echo $day; ?>ActivityLevel">Activity Level (1-10):</label>
            <input type="number" id="day<?php echo $day; ?>ActivityLevel" name="day<?php echo $day; ?>ActivityLevel" step="any" required><br><br>
        <?php endfor; ?>

        <button type="submit">Predict Future Stress Level</button>
    </form>
    </div>
    <div id="result">
        <?php
        // Handle form submission
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $sequence = [];
            for ($day = 1; $day <= 7; $day++) {
                $heartRate = $_POST["day{$day}HeartRate"];
                $sleepHours = $_POST["day{$day}SleepHours"];
                $activityLevel = $_POST["day{$day}ActivityLevel"];
                $sequence[] = [$heartRate, $sleepHours, $activityLevel];
            }
        
            // Prepare data for the API
            $data = json_encode([
                'sequence' => $sequence
            ]);
        
            // Initialize cURL for the 7-day sequence prediction
            $ch = curl_init('http://localhost:5000/predict_seven_days');
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_HTTPHEADER, [
                'Content-Type: application/json',
                'Content-Length: ' . strlen($data)
            ]);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
        
            // Execute cURL and fetch response
            $response = curl_exec($ch);
            curl_close($ch);
        
            // Decode and display the result
            $responseData = json_decode($response, true);
            echo "<div style='text-align: center;'>Predicted Future Stress Level: " . $responseData['future_prediction'] . " - " . $responseData['message'] . "</div>";
        }
        ?>
    </div>
</section>

<?php
include_once 'footer.php';
?>