# PyTools 
  
  
 #### By V4mpw0L 
 
  * A Python script for Linux system management, written as part of my Python learning journey.


 #### 🖼️ Screenshot

    
 ![2332Screenshot_2024-01-02_15_42_53](https://github.com/V4mpw0L/PyTools/assets/125161567/008a8a2b-8034-4a41-9f56-4a3c7dc61696)

    
### ⚙️ Installation

##### Install Updates and Upgrades.

 - For Debian (Ubuntu, Kali-Linux,)
 - ```sudo apt update -y && sudo apt upgrade -y```

##### Install dependencies (git, python, figlet, neofetch, lolcat)

 - For Debian (Ubuntu, Kali-Linux,)
 - ```sudo apt install git figlet lolcat neofetch python3 python3-pip -y```

##### Clone this repository

 - ```git clone https://github.com/V4mpw0L/PyTools.git```

##### Enter the directory
 - ```cd Tools```

##### PIP install Requeriments

 - ```pip install -r requirements.txt```

##### Run the tool
 - ```python3 tools.py```

    ## 📝 Description

**PyTools** is a meticulously crafted script designed to optimize Linux system management tasks. Developed as a hands-on learning project, it serves the dual purpose of refining my Python skills and automating repetitive tasks efficiently.

### Key Features:

- **Update System**: 
  - Provides an all-in-one command to update, upgrade, autoremove, and autoclean the system.

- **Ping a Website**: 
  - Allows you to ping a website, retrieving its IP Address using PING -C.

- **Geolocate an IP**: 
  - Provides the capability to determine the geographical location of an IP Address using REQUESTS.GET.

- **Disk Usage**: 
  - Displays a comprehensive breakdown of disk usage, including its divisions with DF -H.

- **Memory Usage**: 
  - Offers insight into the computer's RAM usage with FREE -H.

- **System Uptime**: 
  - Shows the system's uptime, indicating how long it has been running with UPTIME.

- **List Running Processes**: 
  - Provides a detailed list of all running processes on the computer using PS AUX.

- **Network Information**: 
  - Presents valuable information about the connected network with IP ADDR.

- **System Information**: 
  - Displays an overview of system information with NEOFETCH.
    
- **Scan for Malware**:
  - Utilize the integrated antivirus tool (replace 'clamscan' with your actual command) to perform a deep scan for malware and viruses on your system. if no antivirus:
  - Run: ```sudo apt-get install clamav-daemon``` to install ClamAV.

- **Check Password Strength**:
  - Evaluate the strength of your passwords by entering them. The system categorizes the strength into Super Weak, Weak, Medium, Strong, or Super Strong, and provides an estimate of the time it would take to crack the password.

- **Perform Traceroute**:
  - Conduct a traceroute to a specified destination to visualize the route that packets take to reach the destination.

- **YouTube Video or MP3 Download**: 
  - Enables downloading of videos or MP3s from YouTube, including playlists by pasting the Playlist Link.

- **Update the Script**: 
  - Connects seamlessly with the GitHub branch to update the script using GIT PULL.

- **Exit**: 
  - Exits the script. Alternatively, use CTRL + C to halt the script abruptly.


   
 ## 🛠️ Technologies Used 
  
 * Python 🐍
   
 ## 🔗 Links 
  
 * https://github.com/V4mpw0L/PyTools.git
  
 ## 📜 License 
  
 This software is licensed under the MIT license. 
  
 Copyright (c) 2024 **V4mpw0L**
