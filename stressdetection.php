<?php
include_once 'header.php';
include_once 'includes/dbh.inc.php'; // Include your database connection file

// Initialize variables for form inputs and results
$heartRate = $sleepHours = $activityLevel = "";
$stressLevel = $message = "";

// Check if the form is submitted
if (isset($_POST['submit'])) {
    // Collect input data
    $heartRate = $_POST['heartRate'];
    $sleepHours = $_POST['sleepHours'];
    $activityLevel = $_POST['activityLevel'];
    $userId = $_SESSION['userid']; // Ensure the user is logged in and their ID is stored in the session

    // Create the data array to send to Flask
    $data = json_encode([
        'heart_rate' => (float)$heartRate,
        'sleep_hours' => (float)$sleepHours,
        'activity_level' => (float)$activityLevel
    ]);

    // Send data to Flask backend using cURL
    $ch = curl_init('http://localhost:5000/predict_single');  // Flask backend URL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    // Execute the cURL request and get the response
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    // Decode the JSON response from Flask
    $responseData = json_decode($response, true);

    // Check if response is valid
    if ($httpCode === 200 && $responseData && isset($responseData['prediction'])) {
        $stressLevel = $responseData['prediction'];
        $message = $responseData['message'] ?? 'No additional message.';

        // Insert data into the database
        $sql = "INSERT INTO userInputs (userId, heartRate, sleepHours, activityLevel)
                VALUES (?, ?, ?, ?)";
        $stmt = mysqli_stmt_init($conn);

        if (mysqli_stmt_prepare($stmt, $sql)) {
            mysqli_stmt_bind_param($stmt, "iddd", $userId, $heartRate, $sleepHours, $activityLevel);
            mysqli_stmt_execute($stmt);
            echo "<div style='text-align: center;'>Your input has been recorded!</div>";
        } else {
            echo "<div style='text-align: center;'>Error: " . mysqli_error($conn) . "</div>";
        }
    } else {
        echo "<div style='text-align: center;'>Error: Unable to get a valid response from Flask backend.</div>";
    }
}
?>

<section class="signup-form">
    <h2 class="login">Stress Detection</h2>
    <div class="signup-form-form">
        <form id="stressForm" method="POST" action="">
            <label for="heartRate">Heart Rate (BPM):</label>
            <input type="number" id="heartRate" name="heartRate" step="any" required><br><br>

            <label for="sleepHours">Hours of Sleep:</label>
            <input type="number" id="sleepHours" name="sleepHours" step="any" required><br><br>

            <label for="activityLevel">Activity Level (1-10):</label>
            <input type="number" id="activityLevel" name="activityLevel" step="any" required><br><br>

            <button type="submit" name="submit">Detect Stress Level</button>
        </form>
    </div>

    <div id="result">
        <?php
        if (!empty($stressLevel)) {
            echo "<div style='text-align: center;'>";
            echo "<h3>Stress Level: $stressLevel</h3>";
            echo "<p><strong>Message:</strong> $message</p>";
            echo "</div>";
        }
        ?>
    </div>
</section>

<?php
include_once 'footer.php';
?>