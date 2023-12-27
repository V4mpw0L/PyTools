#!/usr/bin/env python3

import os
import subprocess
import time
import requests

# Define colors and testing the update
class colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    YELLOW = '\033[33m'
    NORMAL = '\033[0m'
    BOLD = '\033[1m'

# Function to draw a line
def draw_line():
    print(colors.CYAN + '#' * os.get_terminal_size().columns + colors.NORMAL)

# Function to print a message with a box
def print_box(message):
    draw_line()
    print(colors.BLUE + colors.BOLD + message + colors.NORMAL)
    draw_line()

# Function to draw a progress bar
def progress_bar():
    total = 30
    for i in range(total + 1):
        time.sleep(0.1)
        percent = i * 100 // total
        filled = i * 73 // total
        empty = 73 - filled

        print(f"{colors.CYAN}{percent}%{colors.NORMAL} [{colors.CYAN}{'=' * filled}{colors.NORMAL}{' ' * empty}]", end='\r')
    print()

# Function to check if a command is available
def command_exists(command):
    return subprocess.call('type ' + command, shell=True, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

# Check if figlet is available
if not command_exists("figlet"):
    print("Error: 'figlet' command not found. Please install it.")
    exit(1)

# Function to update the system
def update_system():
    # Print System Update message
    print("Starting system update...")
    print(colors.BLUE + colors.BOLD)
    os.system('figlet -c -f big "UPDATING..."')
    print(colors.NORMAL)
    draw_line()

    os.system('sudo apt update -y')
    progress_bar()

    os.system('sudo apt upgrade -y')
    progress_bar()

    os.system('sudo apt autoremove -y')
    progress_bar()

    os.system('sudo apt autoclean -y')
    progress_bar()

    print_box("Your system is up to date.")

# Function to ping a website or IP
def ping_site():
    site = input("Enter the website or IP to ping: ")
    ip = subprocess.getoutput(f'dig +short {site}')

    print(f"{colors.BOLD}{colors.RED}IP Address: {ip}{colors.NORMAL}")
    os.system(f'ping -c 5 {site}')

# Function to geolocate an IP
def geolocate_ip():
    ip = input("Enter the IP to geolocate: ")
    geo = requests.get(f"https://ipinfo.io/{ip}").json()

    draw_line()
    print(f"{colors.GREEN}{colors.BOLD}Geolocation info:{colors.NORMAL}")
    for key, value in geo.items():
        print(f"{colors.GREEN}{key}: {value}{colors.NORMAL}")
    draw_line()

# Function to update the script from GitHub
def update_script():
    os.system('git pull origin main')  # Assuming your default branch is 'main'
    print_box("Script updated successfully. Please restart the script.")
    exit()

# Function to show disk usage
def disk_usage():
    print_box("Disk Usage")
    os.system('df -h')

# Function to show memory usage
def memory_usage():
    print_box("Memory Usage")
    os.system('free -h')

# Function to show system uptime
def system_uptime():
    print_box("System Uptime")
    os.system('uptime')

# Function to list running processes
def list_processes():
    print_box("Running Processes")
    os.system('ps aux')

# Function to show network information
def network_info():
    print_box("Network Information")
    output = subprocess.getoutput('ip addr')
    lines = output.split('\n')
    for line in lines:
        if 'inet' in line:
            print(colors.GREEN + colors.BOLD + line + colors.NORMAL)
        else:
            print(line)

# Menu
while True:
    draw_line()
    print(colors.BLUE + colors.BOLD)
    os.system('figlet -c -f big " M E N U "')
    print(colors.NORMAL)
    draw_line()
    print(f"{colors.BLUE}{colors.BOLD}1.| Update the system{colors.NORMAL}")
    print(f"{colors.BLUE}{colors.BOLD}2.| Ping a website or IP{colors.NORMAL}")
    print(f"{colors.BLUE}{colors.BOLD}3.| Geolocate an IP{colors.NORMAL}")
    print(f"{colors.BLUE}{colors.BOLD}4.| Disk Usage{colors.NORMAL}")
    print(f"{colors.BLUE}{colors.BOLD}5.| Memory Usage{colors.NORMAL}")
    print(f"{colors.BLUE}{colors.BOLD}6.| System Uptime{colors.NORMAL}")
    print(f"{colors.BLUE}{colors.BOLD}7.| List Running Processes{colors.NORMAL}")
    print(f"{colors.BLUE}{colors.BOLD}8.| Network Information{colors.NORMAL}")
    print(f"{colors.BLUE}{colors.BOLD}9.| Exit{colors.NORMAL}")
    print(f"{colors.BLUE}{colors.BOLD}10.| Update the script{colors.NORMAL}")
    draw_line()

    choice = input("Enter your choice: ")

    if choice == '1':
        update_system()
    elif choice == '2':
        ping_site()
    elif choice == '3':
        geolocate_ip()
    elif choice == '4':
        disk_usage()
    elif choice == '5':
        memory_usage()
    elif choice == '6':
        system_uptime()
    elif choice == '7':
        list_processes()
    elif choice == '8':
        network_info()
    elif choice == '9':
        break
    elif choice == '10':
        update_script()
    else:
        print("Invalid option. Please try again.")
