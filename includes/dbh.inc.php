<?php

$serverName = "localhost";
$dbUserName = "root";
$dbPassword = "";

// change to whatever the database name is
$dbName = "ZenPulse";

$conn = mysqli_connect($serverName, $dbUserName, $dbPassword, $dbName);

if (!$conn) {
    die("Connection Failed:  " . mysqli_connect_error());
}
