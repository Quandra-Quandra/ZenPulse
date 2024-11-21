1. Download visual studios at https://code.visualstudio.com/Download

2. On the left, click extensions. Search for and install Prettier by prettier.io 
for auto formatting and python

3. Install xampp at https://www.apachefriends.org

4. For Mac users, if there is a problem opening the application, go to settings -> privacy and security. Scroll where it says it's been blocked and click 'open anyway'

5. After launch, go to manage servers and start MySQL database and apache web server

6. You can minimize that window and go to the XAMPP folder, then xamppfiles and go to the htdocs folder. Delete the contents in there and drag the ZenPulse folder in there

7. Go back to visial studios and on the left, click explorer and then click open. Select the ZenPulse folder

8. go to http://localhost/phpmyadmin/ create a database called ZenPulse and then import the ZenPulse.sql file from the ZenPulse folder

9. If a box appears on the lower right hand corner about validation for php, you can click settings there OR go to settings -> type php -> click edit in settings.json where it says php validate executable path. It'll say "php.validate.executablePath":"". For mac users, paste /Applications/XAMPP/xamppfiles/bin/php-8.2.4 within the quotation marks (may have to change 8.2.4 to an updated version in the future).
For window users, go back to the xampp folder and find the php.exe file, copy the path and paste it in the quotation marks back in visual studios.
10. . venv/bin/activate  in terminal to activate virtual environment and shift command p to select python interpreter to make sure venv (virtual environment) is selected
11. In terminal run stress_detection.py first and then run app.py 
12. you can now proceed to website (XAMPP > manager-osx > go to application) and input your data 

*On macOS, to prevent interference try disabling the 'AirPlay Receiver' service from System Preferences -> General -> AirDrop & Handoff 
