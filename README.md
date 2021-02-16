# Upnext, a YouTube playlist builder by hbk Pancakes
BETA v0.1
twitter@hbkpancakes | hbkpancakes@protonmail.com


Upnext is a YouTube playlist builder, which will remove old
videos and add new videos to a specified playlist, based on 
channel subscription choices that you specify.

****** PLEASE NOTE ******
This is in very early stages, and while functional, error
handling is not yet complete. You may run into errors
that crash the script, or errors that look whacky. I'm expecting
this, and working on handling all errors in an efficient way.

Plans are to compile this into .exe so setup is far easier.

Current features include:
- Support for both Firefox and Chrome
- Firefox runs "headless", meaning it will not open a window,
  but run the process in the background. Chrome will open a window
- Ability to edit subscription choices, playlist link, 
  and default browser choices on the fly

# Requirements
- Python 3.x 
- Selenium package installed
- Up to date Firefox or Chrome browser downloaded and installed
  onto your computer.
- A custom browser profile for your respective browser that 
  is logged into your YouTube account, and has those credentials 
  saved. 
      + Both Firefox and Chrome have guides on how to do this, and
        it is recommended to check with your browsers documentation on how to 
        do this. This step is required, and failure to do this will make the 
        script not work. This is due to YouTube limitations (and to avoid typing your
        username and password into programs you download off the internet).
        This script will not ever see your username and password. 
        
# Setup and Instructions

1. Create a folder and place the script inside of it (name is your choice)

2. Create a folder called "configs"

3. Create a folder called "browsers", and inside of that folder,
   create a folder called "firefox" and a folder called "chrome"

4. Execute the script. Here you can either enter "1" and run right
   away, or go through each option and set up each separately. If you
   use option "1", you will be walked through the setup.

5. When you set up the browser settings, you will get asked to
   specify your driver file. This is an important file that allows
   your browser to run tasks on your behalf. Download this straight 
   from the source so you can be certain it is up to date *links below). 
   Next, create a folder called "browser", inside that folder create a 
   folder named either "firefox" or "chrome" (depending on which driver), 
   and place it inside.

   geckodriver (Firefox): https://github.com/mozilla/geckodriver/releases
   chromedriver (Chrome): https://chromedriver.chromium.org/downloads

   NOTE: Please ensure you are using the correct driver for the browser you
   specify. If you choose Firefox, make sure the file you are using is titled
   "geckodriver", if you chose Chrome, make sure the driver file is titled 
   "chromedriver".

   IMPORTANT: Once you specify the driver file location, do not move or delete 
   the file or folder, or else you will have to respecify the location next time
   you run the script.

6. After setting up the driver location, you will be asked to specify your browser
   profile location. This is different for each browser (Chrome and Firefox), and
   can be different by computer. The general location of your created profiles are:

   Firefox: C:\Users\user name\AppData\Roaming\Mozilla\Firefox\Profiles\somerandomstring.ProfileName
   Chrome: C:\Users\user name\AppData\Local\Google\Chrome\User Data\

   Point the program to these locations and then your Browser Profile settings will be 
   saved.

7. Next, you be asked to set up your subscription settings. Type each Channel Name one line 
   at a time, hitting enter after each specific channel name. You will want to ensure the 
   Channel Names are typed in EXACTLY as they are on Youtube, matching all spelling, spacing, 
   and capitalization. Failure to do this, will result in videos from that channel not being 
   added to your playlist. Type "/done" when you are finished.

8. Finally, you will be asked to enter in the direct link to the playlist the videos will
   be getting added to. Just naviagte to the playlist in YouTube, and copy and paste
   the link in the address bar. Please ensure the link has "https://wwww." in the address.

9. The script will then start to run. If you chose Chrome, you will see a new Chrome
   window pop up and start to remove any previous videos in the specified playlist
   (if any), and add new videos from the Channel Subscriptions you specified.
   If you chose Firefox, this will all happen in the background. There will be messages
   printed in the program to tell you exactly what step the program is on.
   
# License

Copyright (C) 2021 hbk Pancakes

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See https://www.gnu.org/licenses/ or the license file for more details.

# Contact Information
                
https://twitter.com/hbkpancakes
https://github.com/hbkpancakes
hbkpancakes@protonmail.com
