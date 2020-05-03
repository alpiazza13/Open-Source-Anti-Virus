# Open-Source-Anti-Virus

<img src="imgs/alert.png" height="40%" width="40%" > <img src="imgs/menu_bar.png" height="26%" width="26%" > 


Open Source Anti-Virus MAC OS menu-bar app. A different approach to virus checking - uses a hexadecimal comparison based algorithm that checks for hidden malware. 
We use a big list of know viruses to test whether a file is a virus or not. We also support zip files and directories. This is Open Source because you can contribute by adding malicious files in our separate repository to help improve the app.

If you have a known virus file that you'd like to add to our app, please go here and follow the instructions there:
https://github.com/samueljaval/List-of-viruses-for-Open-Source-Anti-Virus

 - This app only runs on macOS.
 - The UI is in the Mac Menu Bar at the top of the screen
 - A standalone macOS app is provided (download link at the botton of this README) 
 - You can test it by running main.py with python (you need to install the rumps and pync packages with pip) 
 - As it is, the main loop (excluding single file check) only works for downloads from chrome and safari but can be easily modified to cover more browsers (comments in the code can help know what to change)  
</br>

[CLICK HERE TO DOWNLOAD THE APP!](https://github.com/alpiazza13/Open-Source-Anti-Virus/releases/download/v1.0/Anti-Virus.zip) 

Please consider contributing to our project, or submitting a malware file to our database!
