<?php
include_once 'header.php'
?>

<body>
    <div class="bg_s">  
        <div class="community-section">
            <h2 style="color: black; text-align: center;">Community Tab</h2>
            
            <div class="post-form">
                <h3>Share Your Thoughts</h3>
                <textarea placeholder="What's on your mind?" disabled></textarea>
                <button disabled>Post</button>
                <p class="note">* This is a demo. Posting is disabled.</p>
            </div>

            <div class="posts">
                <h3>Recent Posts</h3>

                <div class="post">
                    <p>"I found some great techniques to manage stress. Meditation really helps!"</p>
                    <span class="author">- User123</span>
                </div>

                <div class="post">
                    <p>"Feeling overwhelmed lately. Anyone have tips?"</p>
                    <span class="author">- User456</span>
                </div>

                <div class="post">
                    <p>"Remember to take breaks during work. Your mental health matters!"</p>
                    <span class="author">- User789</span>
                </div>
            </div>
        </div>
    </div>
</body>




<?php
include_once 'footer.php'
?>