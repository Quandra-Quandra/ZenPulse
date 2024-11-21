<?php
include_once 'header.php';
include_once 'includes/dbh.inc.php'; 
?>
<!-- 
// ini_set('display_errors', 1);
// ini_set('display_startup_errors', 1);
// error_reporting(E_ALL); -->


<?php
// Check if the user is logged in
if (!isset($_SESSION['userid'])) {
    echo "Please log in first.";
    exit;
}

$userId = $_SESSION['userid'];

// Query to get previous inputs from the database for the logged-in user
$sql = "SELECT heartRate, sleepHours, activityLevel, entryDate FROM userInputs WHERE userId = ? ORDER BY entryDate DESC";
$stmt = mysqli_prepare($conn, $sql);
mysqli_stmt_bind_param($stmt, "i", $userId);
mysqli_stmt_execute($stmt);
$result = mysqli_stmt_get_result($stmt);

// Arrays to store data for the graph
$heartRates = [];
$sleepHours = [];
$activityLevels = [];
$dates = [];

// Fetch data
while ($row = mysqli_fetch_assoc($result)) {
    $heartRates[] = $row['heartRate'];
    $sleepHours[] = $row['sleepHours'];
    $activityLevels[] = $row['activityLevel'];
    $dates[] = $row['entryDate']; // Make sure this is in a valid format (e.g., YYYY-MM-DD)
}

// Close the statement
mysqli_stmt_close($stmt);
?>

<section class="signup-form">
    <div class="profile-container">
        <h1>Your Profile</h1>

        <!-- Display the user's previous inputs in a graph -->
        <h2>Your Stress Data</h2>
        <canvas id="userChart" width="400" height="200"></canvas>
    </div>

    <!-- Dynamically load Chart.js using JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // Data from PHP (encoded in JSON format)
        const heartRates = <?php echo json_encode($heartRates); ?>;
        const sleepHours = <?php echo json_encode($sleepHours); ?>;
        const activityLevels = <?php echo json_encode($activityLevels); ?>;
        const dates = <?php echo json_encode($dates); ?>;

        // Create the chart after Chart.js is loaded
        const ctx = document.getElementById('userChart').getContext('2d');
        const userChart = new Chart(ctx, {
            type: 'line', // Use a line chart
            data: {
                labels: dates, // Dates on the x-axis
                datasets: [{
                    label: 'Heart Rate (BPM)',
                    data: heartRates,
                    borderColor: 'rgb(255, 99, 132)',
                    fill: false
                },
                {
                    label: 'Sleep Hours',
                    data: sleepHours,
                    borderColor: 'rgb(54, 162, 235)',
                    fill: false
                },
                {
                    label: 'Activity Level (1-10)',
                    data: activityLevels,
                    borderColor: 'rgb(75, 192, 192)',
                    fill: false
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Values'
                        }
                    }
                }
            }
        });
    </script>
</section>

<p class="signup_2">
    Log out? <a href="logout.php">Yes</a>
</p>

<?php
include_once 'footer.php';
?>