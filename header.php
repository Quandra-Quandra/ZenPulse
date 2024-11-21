<?php
session_start();
?>



<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewpoint" content="width=device-width, initial-scale=1.0" />
  <title>Zen Pulse</title>
  <!-- title font -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="style.css" />
</head>


<!-- next line is to measure the content of the page -->
<div id="container">
  <!-- next line is for everything on the webpage, code should be in here -->
  <div id="main">
    <section class="header">
      <nav>
        <a href="index.php"><img src="images/iP9EB.png" /></a>
        <h1 class="cinzel-font">ZenPulse</h1>

        <div class="nav_links">
          <ul>
            <!-- Navigation links -->
            <li><a href="index.php">Home</a></li>
            <li><a href="stressprediction.php">Stress Prediction</a></li>
            <li><a href="stressdetection.php">Stress Detection</a></li>
            <li><a href="resources.php">Resources</a></li>
            <li><a href="community.php">Community</a></li>
          </ul>
        </div>
        <!-- cart -->

        <!-- user icon -->
        <div class="user_icon">
          <ul>
            <?php
            if (isset($_SESSION["useruid"])) {
              echo "<li><a href='profile_page.php'>Profile Page</a></li>";
            } else {
              echo "<li><a href='signup.php'>Log in/Sign in</a></li>";
            }
            ?>
            <ul>
              <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z" clip-rule="evenodd" />
              </svg>
        </div>
      </nav>
    </section>
  </div>
</div>
