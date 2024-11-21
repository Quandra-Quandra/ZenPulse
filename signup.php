<?php
include_once 'header.php';
?>


<section class="signup-form">
    <h2 class="signup">Sign Up</h2>
    <p class="signup_1">
        Already have an account?
        <a href="login.php"> Sign in</a>
    </p>

    <div class="signup-form-form">

        <form action="includes/signup.inc.php" method="post">
            <input type="text" name="name" placeholder="Full name...">
            <input type="text" name="email" placeholder="Email...">
            <input type="text" name="uid" placeholder="username...">
            <input type="password" name="pwd" placeholder="password...">
            <input type="password" name="pwdrepeat" placeholder="Repeat Password...">
            <button type="submit" name="submit">Sign Up</button>
        </form>
    </div>

    <?php

    if (isset($_GET["error"])) {
        if ($_GET["error"] == "emptyinput") {
            echo "<p>Fill in all fields!</p>";
        } else if ($_GET["error"] == "invaliduid") {
            echo "<p>Choose a proper username!</p>";
        } else if ($_GET["error"] == "invalidemail") {
            echo "<p>Choose a proper email!</p>";
        } else if ($_GET["error"] == "passwordsdontmatch") {
            echo "<p>Passwords doesn't match!</p>";
        } else if ($_GET["error"] == "stmtfailed") {
            echo "<p>Something went wrong!</p>";
        } else if ($_GET["error"] == "usernametaken") {
            echo "<p>Username already taken!</p>";
        } else if ($_GET["error"] == "none") {
            echo "<p>You have signed up!</p>";
        }
    }
    ?>
</section>



<?php
include_once 'footer.php';
?>