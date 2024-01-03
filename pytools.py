#!/usr/bin/env python3

import os
import subprocess
import time
import datetime
import requests
import socket
import re
#import tkinter as tk
#FUTURE GUI UPDATE with tkinter
from pytube import YouTube, Playlist
from pytube.exceptions import AgeRestrictedError
from tqdm import tqdm
from alive_progress import alive_bar
from colorama import Fore, Style, Back
from slugify import slugify
import logging

# Determine the environment (Termux or other)
termux_environment = False
try:
    termux_environment = os.environ['PREFIX'] == '/data/data/com.termux/files/usr'
except KeyError:
    termux_environment = False

# Define colors
class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    YELLOW = Fore.YELLOW
    NORMAL = Style.RESET_ALL
    BOLD = Style.BRIGHT
    MAGENTA = Fore.MAGENTA

# Define the script version and credits
SCRIPT_VERSION = "v 1.0"
CREDITS = f"{Fore.RED}{Style.BRIGHT}V4mpw0L (2024){Style.RESET_ALL}"

# FUTURE UPDATE FOR GUI INTERFACE.
# def display_gui():
    #root = tk.Tk()
    #root.title("Your Tool")
    #label = tk.Label(root, text="Welcome to Your Tool!", font=("Helvetica", 16))
    #label.pack(pady=10) 

# Add function for input validation
def validate_menu_choice(choice):
    try:
        choice = int(choice)
        if 1 <= choice <= 15:
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 15.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

# Function to display credits
def display_credits():
    draw_line()
    print(f"{Colors.MAGENTA}{Colors.BOLD}{CREDITS}{Colors.NORMAL}")
    draw_line()

# Function to draw a line
def draw_line():
    print(Colors.BLUE + '=' * os.get_terminal_size().columns + Colors.NORMAL)

# Function to print a message with a box
def print_box(message):
    draw_line()
    print(Colors.BLUE + Colors.BOLD + message + Colors.NORMAL)
    draw_line()

# Function to draw a progress bar
def progress_bar(total=15):
    with alive_bar(total, bar='classic', spinner='dots_waves', title=f"{Colors.BOLD}{Colors.CYAN}Updating...{Colors.NORMAL}", length=40, enrich_print=True, manual=False) as bar:
        for _ in range(total):
            time.sleep(0.1)
            bar()

# Function to check if commands are available
def commands_exist(commands):
    missing_commands = [command for command in commands if subprocess.call(['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0]
    return not missing_commands

# Dependency check
required_dependencies = ['requests', 'pytube', 'alive-progress', 'colorama', 'slugify']

# List of required commands
required_commands = ['figlet', 'lolcat', 'neofetch']
# Check if all required commands are available
if not termux_environment and not commands_exist(required_commands):
    missing_commands_str = ', '.join(required_commands)
    logging.error(f"One or more required commands not found: {missing_commands_str}. Please install them.")
    print(f"Error: One or more required commands not found: {missing_commands_str}. Please install them.")
    exit(1)

# Configure logging with a file handler and set the logging level
logging.basicConfig(filename='script.log', level=logging.DEBUG)

# Modify log entries to include timestamps
def log_message(message, level='info'):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - [{level.upper()}] - {message}"
    print(log_entry)
    with open('script.log', 'a') as log_file:
        log_file.write(log_entry + '\n')

# Clear console (works for Unix-based systems, replace with 'os.system('cls')' for Windows)
def clear_console():
    if termux_environment:
        os.system('clear')
    else:
        os.system('cls')


# Function to update the system
def update_system():
    try:
        logging.info("Starting system update...")
        print("Starting system update...")
        clear_console()
        os.system('figlet -f standard "UPDATING..." | lolcat')
        print(Colors.NORMAL)
        run_command('sudo apt update -y' if not termux_environment else 'pkg update -y', "Updating package lists...")
        run_command('sudo apt upgrade -y' if not termux_environment else 'pkg upgrade -y', "Upgrading installed packages...")
        run_command('sudo apt autoremove -y' if not termux_environment else 'pkg autoremove -y', "Removing unused packages...")
        run_command('sudo apt autoclean -y' if not termux_environment else 'pkg autoclean', "Cleaning up package cache...")
        print_box("Your system is up to date.")
    except Exception as e:
        logging.error(f"System update failed. Error: {e}")
        print(f"Error: {e}")
def run_command(command, message):
    try:
        print_box(message)
        subprocess.run(command, shell=True, check=True)
        progress_bar()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{command}' failed with error code {e.returncode}.")
        print(f"Error: System update failed. Please check the logs for details.")

# Function to ping a website or IP
def ping_site():
    try:
        user_input = input("Enter the website or IP to ping: ")
        if is_ip_address(user_input):
            website = resolve_ip(user_input)
            print(f"{Colors.BOLD}{Colors.RED}Website: {website}{Colors.NORMAL}")
        else:
            ip = resolve_ip(user_input)
            if ip:
                print(f"{Colors.BOLD}{Colors.RED}IP Address: {ip}{Colors.NORMAL}")
                perform_ping(user_input)
            else:
                print(f"Unable to resolve IP address for {user_input}. Ping aborted.")
    except Exception as e:
        logging.error(f"Ping failed. Error: {e}")
        print(f"Error: {e}")
def is_ip_address(value):
    try:
        socket.inet_aton(value)
        return True
    except socket.error:
        return False
def resolve_ip(site_or_ip):
    try:
        if is_ip_address(site_or_ip):
            return subprocess.getoutput(f'dig +short -x {site_or_ip}')
        else:
            result = subprocess.getoutput(f'dig +short {site_or_ip}')
            return result.strip()
    except Exception as e:
        logging.warning(f"Failed to resolve IP address. Error: {e}")
        return None
def perform_ping(site_or_ip):
    try:
        os.system(f'ping -c 3 {site_or_ip}')
    except Exception as e:
        logging.error(f"Ping operation failed. Error: {e}")
        print(f"Error: {e}")


# Function to geolocate an IP
def geolocate_ip():
    try:
        ip = input("Enter the IP to geolocate: ")
        geo_info = get_geolocation(ip)
        if geo_info:
            display_geolocation_info(geo_info)
        else:
            print("Unable to retrieve geolocation information.")
    except Exception as e:
        logging.error(f"Geolocation failed. Error: {e}")
        print(f"Error: {e}")
def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}")
        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"Failed to retrieve geolocation. Status Code: {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"Geolocation request failed. Error: {e}")
        return None
def display_geolocation_info(geo_info):
    draw_line()
    print(f"{Colors.GREEN}{Colors.BOLD}Geolocation info:{Colors.NORMAL}")
    for key, value in geo_info.items():
        print(f"{Colors.YELLOW}{key}: {value}{Colors.NORMAL}")
    draw_line()


# Function to update the script from GitHub
def update_script():
    try:
        # Discard all local changes and switch to the main branch
        os.system('git reset --hard origin/main')
        # Clean untracked files and directories
        os.system('git clean -fdx')
        # Pull changes from the remote repository
        os.system('git pull origin main')
        print_box("Script updated successfully. Please restart the script.")
        logging.info("Script updated successfully.")
        exit()
    except Exception as e:
        logging.error(f"Script update failed. Error: {e}")
        print(f"Error: {e}")

# Function to show disk usage
def disk_usage():
    try:
        print_box("Disk Usage")
        df_output = subprocess.getoutput('df -h')
        df_lines = df_output.split('\n')
        header = df_lines[0]
        print(Colors.CYAN + Colors.BOLD + header + Colors.NORMAL)
        for fs in df_lines[1:]:
            fields = fs.split()
            filesystem, size, used, available, percent, mountpoint = fields[0], fields[1], fields[2], fields[3], fields[4], fields[5]
            formatted_fs = f"{Colors.GREEN}{filesystem: <15}{Colors.NORMAL}  {size: <10}  {used: <10}  {available: <10}  {Colors.YELLOW}{percent: <6}{Colors.NORMAL}  {Colors.BLUE}{mountpoint}{Colors.NORMAL}"
            bar_length = 20
            used_percentage = int(percent.rstrip('%'))
            used_blocks = int(bar_length * used_percentage / 100)
            free_blocks = bar_length - used_blocks
            visual_bar = f"{Colors.CYAN}[{'#' * used_blocks}{'-' * free_blocks}]{Colors.NORMAL}"
            print(formatted_fs)
            print(visual_bar)
    except Exception as e:
        logging.error(f"Failed to retrieve disk usage. Error: {e}")
        print(f"Error: {e}")

# Function to show memory and swap usage
def memory_usage():
    try:
        print_box("Memory and Swap Usage")
        output = subprocess.check_output(['free', '-h'], text=True)
        lines = output.split('\n')
        header = lines[0]
        memory_info = lines[1].split()
        swap_info = lines[2].split()
        print(Colors.CYAN + Colors.BOLD + header + Colors.NORMAL)
        formatted_memory_info = f"{Colors.GREEN}{memory_info[0]:<10}{Colors.NORMAL}  {Colors.YELLOW}{memory_info[1]:<10}{Colors.NORMAL}  {Colors.RED}{memory_info[2]:<10}{Colors.NORMAL}  {Colors.BLUE}{memory_info[3]:<10}{Colors.NORMAL}  {Colors.YELLOW}{memory_info[4]:<10}{Colors.NORMAL}  {Colors.CYAN}{memory_info[5]:<10}{Colors.NORMAL}"
        print(formatted_memory_info)
        formatted_swap_info = f"{Colors.GREEN}{swap_info[0]:<10}{Colors.NORMAL}  {Colors.YELLOW}{swap_info[1]:<10}{Colors.NORMAL}  {Colors.RED}{swap_info[2]:<10}{Colors.NORMAL}"
        print(formatted_swap_info)
    except Exception as e:
        logging.error(f"Failed to retrieve memory and swap usage. Error: {e}")
        print(f"Error: {e}")

# Function to show system uptime
def system_uptime():
    try:
        print_box("System Uptime")
        os.system('uptime')
    except Exception as e:
        logging.error(f"Failed to retrieve system uptime. Error: {e}")
        print(f"Error: {e}")

# Function to list running processes
def list_processes():
    try:
        print_box("Running Processes")
        process_output = subprocess.getoutput('ps aux')
        processes = process_output.split('\n')
        header = processes[0]
        print(Colors.CYAN + Colors.BOLD + header + Colors.NORMAL)
        for process in processes[1:]:
            fields = process.split()
            pid, user, cpu, mem, vsz, rss, tty, stat, start, time, command = fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8], fields[9], ' '.join(fields[10:])
            formatted_process = f"{Colors.GREEN}{pid}{Colors.NORMAL}  {Colors.YELLOW}{user}{Colors.NORMAL}  {cpu}  {mem}  {vsz}  {rss}  {Colors.BLUE}{tty}{Colors.NORMAL}  {stat}  {start}  {time}  {Colors.RED}{command}{Colors.NORMAL}"
            print(formatted_process)
    except Exception as e:
        logging.error(f"Failed to list running processes. Error: {e}")
        print(f"Error: {e}")

# Function to show system information
def system_information():
    try:
        print_box("System Information")
        os.system('neofetch')
    except Exception as e:
        logging.error(f"Failed to retrieve system information. Error: {e}")
        print(f"Error: {e}")

# Function to show network information
def network_info():
    try:
        interface_colors = {
            'lo': Colors.CYAN,
            'eth0': Colors.GREEN,
            'wlan0': Colors.YELLOW,
            'docker0': Colors.BLUE
        }
        print_box("Network Information")
        output = subprocess.getoutput('ip addr')
        lines = output.split('\n')
        current_interface = None
        for line in lines:
            words = line.split()
            for word in words:
                if ':' in word and word[:-1] in interface_colors:
                    current_interface = word[:-1]
                    break
            if current_interface:
                print(f"{interface_colors[current_interface]}{Colors.BOLD}{current_interface}{Colors.NORMAL}")
                for i, word in enumerate(words):
                    if 'inet' in word and i + 1 < len(words) and '.' in words[i + 1]:
                        ip_address = words[i + 1]
                        print(f"IP Address: {Colors.RED}{Colors.BOLD}{ip_address}{Colors.NORMAL}")
                        break
                else:
                    print(line)
            else:
                print(line)
    except Exception as e:
        logging.error(f"Failed to retrieve network information. Error: {e}")
        print(f"Error: {e}")

# Function to download video or mp3 from YouTube with progress bar
def download_youtube():
    try:
        url = input("Enter the YouTube video URL or playlist URL: ")
        print_box("Choose an option:")
        print(f"{Colors.BLUE}{Colors.BOLD}1.| Download Video{Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD}2.| Download Audio (MP3){Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD}3.| Cancel{Colors.NORMAL}")
        draw_line()
        choice = input("Enter your choice: ")
        selected_stream = None
        if 'playlist' in url:
            playlist = Playlist(url)
            print(f"Downloading playlist: {playlist.title}")
            if choice == '1':
                print_box("Available Video Streams:")
                yt = YouTube(playlist.video_urls[0])
                video_streams = yt.streams.filter(file_extension='mp4', progressive=True)
                for i, stream in enumerate(video_streams, start=1):
                    print(f"{Colors.BLUE}{Colors.BOLD}{i}.| {stream.resolution} - {stream.filesize / 1024 / 1024:.2f} MB{Colors.NORMAL}")
                selected_stream = int(input("Enter the number of the stream to download: "))
                selected_stream -= 1
            for url in playlist.video_urls:
                download_video_or_audio(url, auto_download=True, choice=choice, selected_stream=selected_stream)
        else:
            download_video_or_audio(url, choice=choice, selected_stream=selected_stream)
    except Exception as e:
        logging.error(f"YouTube download failed. Error: {e}")
        print(f"Error: {e}")

def download_video_or_audio(url, auto_download=False, choice=None, selected_stream=None):
    try:
        yt = YouTube(url)
        print(f"{Colors.GREEN}{Colors.BOLD}Title: {yt.title}{Colors.NORMAL}")
        print(f"{Colors.GREEN}{Colors.BOLD}Duration: {yt.length // 60} minutes {yt.length % 60} seconds{Colors.NORMAL}")
        if choice == '1':
            if selected_stream is None:
                print_box("Available Video Streams:")
                video_streams = yt.streams.filter(file_extension='mp4', progressive=True)
                for i, stream in enumerate(video_streams, start=1):
                    print(f"{Colors.BLUE}{Colors.BOLD}{i}.| {stream.resolution} - {stream.filesize / 1024 / 1024:.2f} MB{Colors.NORMAL}")
                selected_stream = int(input("Enter the number of the stream to download: "))
                selected_stream -= 1
            download_video(yt, selected_stream)
        elif choice == '2':
            download_audio(yt)
        elif choice == '3':
            print("Download canceled.")
        else:
            print("Invalid option. Download canceled.")
    except Exception as e:
        logging.error(f"Download failed. Error: {e}")
        print(f"Error: {e}")

def slugify_title(title):
    return re.sub(r'[^a-zA-Z0-9]', '_', title)

def download_video(yt, selected_stream, max_retries=3):
    try:
        video_streams = yt.streams.filter(file_extension='mp4', progressive=True)
        if selected_stream is not None:
            video = video_streams[selected_stream]
        else:
            video = video_streams.first()
        
        video_title = slugify_title(yt.title)

        folder_path = os.path.join(os.getcwd(), 'VideosDownloads')
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{slugify_title(video_title)}_video.mp4")
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.get(video.url, stream=True)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                # Use tqdm to create a progress bar
                with tqdm(total=total_size, unit='b', unit_scale=True, unit_divisor=1024) as bar:
                    with open(file_path, 'wb') as f:
                        for data in response.iter_content(chunk_size=1024):
                            bar.update(len(data))
                            f.write(data)
                print_box(f"Video downloaded successfully as {slugify(video_title)}_video.mp4 in the PlaylistVideos folder")
                return
            except requests.RequestException as e:
                logging.warning(f"Network request failed. Retrying... (Error: {e})")
                retry_count += 1
                time.sleep(2 ** retry_count)
        logging.error(f"Video download failed after {max_retries} retries. Error: {e}")
        print(f"Error: Unable to download the video after {max_retries} retries.")
    except Exception as e:
        logging.error(f"Video download failed. Error: {e}")
        print(f"Error: {e}")


def download_audio(yt, max_retries=3):
    try:
        audio_streams = yt.streams.filter(only_audio=True)
        audio = audio_streams[0]
        audio_title = slugify_title(yt.title)

        folder_path = os.path.join(os.getcwd(), 'AudiosDownloads')
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{slugify_title(audio_title)}_audio.mp3")
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.get(audio.url, stream=True)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                # Use tqdm to create a progress bar
                with tqdm(total=total_size, unit='b', unit_scale=True, unit_divisor=1024) as bar:
                    with open(file_path, 'wb') as f:
                        for data in response.iter_content(chunk_size=1024):
                            bar.update(len(data))
                            f.write(data)
                print_box(f"Audio downloaded successfully as {slugify(audio_title)}_audio.mp3 in the AudiosDownloads folder")
                return
            except requests.RequestException as e:
                logging.warning(f"Network request failed. Retrying... (Error: {e})")
                retry_count += 1
                time.sleep(2 ** retry_count)
        logging.error(f"Audio download failed after {max_retries} retries. Error: {e}")
        print(f"Error: Unable to download the audio after {max_retries} retries.")
    except Exception as e:
        logging.error(f"Audio download failed. Error: {e}")
        print(f"Error: {e}")

# Function to scan for malware or viruses on the system
def scan_for_malware():
    try:
        # Try using clamscan
        run_command('clamscan --infected --recursive --suppress-ok-results', "Scanning for malware or viruses...")
        print_box("Malware scan completed.")
    except FileNotFoundError:
        # List of popular antivirus tools to try
        alternative_tools = ['sophos', 'avgscan', 'chkrootkit', 'rkhunter', 'bitdefender', 'f-prot', 'eset', 'sophos-av', 'kaspersky', 'avast']
        for tool in alternative_tools:
            try:
                run_command(f'{tool} --options', f"Scanning for malware or viruses with {tool}...")
                print_box(f"Malware scan completed using {tool}.")
                return
            except FileNotFoundError:
                continue
        logging.error("No antivirus tool found on the system.")
        print("Error: No antivirus tool found on the system. Please install an antivirus tool.")
    except Exception as e:
        logging.error(f"Malware scan failed. Error: {e}")
        print(f"Error: {e}")


# Function to check the strength of user passwords
def check_password_strength():
    try:
        print_box("Checking password strength...")
        user_password = input("Enter the password to check its strength: ")
        strength_message, color = get_password_strength(user_password)
        print_colored_box(strength_message, color)
    except Exception as e:
        logging.error(f"Password strength check failed. Error: {e}")
        print(f"Error: {e}")
def get_password_strength(password):
    if len(password) >= 16 and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password strength: Super Strong", Fore.GREEN
    elif len(password) >= 12 and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\d', password):
        return "Password strength: Strong", Fore.CYAN
    elif len(password) >= 8 and re.search(r'[A-Za-z]', password) and re.search(r'\d', password):
        return "Password strength: Medium", Fore.YELLOW
    elif len(password) >= 6:
        return "Password strength: Weak", Fore.RED
    else:
        return "Password strength: Super Weak", Fore.MAGENTA
def print_colored_box(message, color):
    draw_line()
    print(color + Style.BRIGHT + message + Style.RESET_ALL)
    draw_line()

# Function to perform a traceroute to a specified destination
def perform_traceroute():
    try:
        print_box("Performing traceroute...")
        destination = input("Enter the destination for traceroute: ")
        run_command(f'traceroute {destination}', "Performing traceroute...")
    except Exception as e:
        logging.error(f"Traceroute failed. Error: {e}")
        print(f"Error: {e}")

#Menu
def menu():
    while True:
        draw_line()
        os.system('figlet -f standard "Py Tools" | lolcat')
        os.system(f'figlet -f mini "{SCRIPT_VERSION}" | lolcat')
        draw_line()
        print(f"{Colors.CYAN}{Colors.BOLD} 1.| {Colors.CYAN}Update the system{Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD} 2.| {Colors.BLUE}Ping a website or IP{Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD} 3.| {Colors.BLUE}Geolocate an IP{Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD} 4.| {Colors.BLUE}Disk Usage{Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD} 5.| {Colors.BLUE}Memory Usage{Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD} 6.| {Colors.BLUE}System Uptime{Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD} 7.| {Colors.BLUE}List Running Processes{Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD} 8.| {Colors.BLUE}Network Information{Colors.NORMAL}")
        print(f"{Colors.BLUE}{Colors.BOLD} 9.| {Colors.BLUE}System Information{Colors.NORMAL}")
        print(f"{Colors.YELLOW}{Colors.BOLD}10.| {Colors.YELLOW}Scan for Malware{Colors.NORMAL}")
        print(f"{Colors.YELLOW}{Colors.BOLD}11.| {Colors.YELLOW}Check Password Strength{Colors.NORMAL}")
        print(f"{Colors.YELLOW}{Colors.BOLD}12.| {Colors.YELLOW}Perform Traceroute{Colors.NORMAL}")
        print(f"{Colors.GREEN}{Colors.BOLD}13.| {Colors.GREEN}Download YouTube Video or MP3{Colors.NORMAL}")
        print(f"{Colors.GREEN}{Colors.BOLD}14.| {Colors.GREEN}Update the Script{Colors.NORMAL}")
        print(f"{Colors.RED}{Colors.BOLD}15.| {Colors.RED}Exit{Colors.NORMAL}")
        display_credits()
        try:
            choice = input("Enter your choice: ")
            validated_choice = validate_menu_choice(choice)
            if validated_choice is not None:
                if validated_choice == 1:
                    update_system()
                elif validated_choice == 2:
                    ping_site()
                elif validated_choice == 3:
                    geolocate_ip()
                elif validated_choice == 4:
                    disk_usage()
                elif validated_choice == 5:
                    memory_usage()
                elif validated_choice == 6:
                    system_uptime()
                elif validated_choice == 7:
                    list_processes()
                elif validated_choice == 8:
                    network_info()
                elif validated_choice == 9:
                    system_information()
                elif validated_choice == 10:
                    scan_for_malware()
                elif validated_choice == 11:
                    check_password_strength()
                elif validated_choice == 12:
                    perform_traceroute()
                elif validated_choice == 13:
                    download_youtube()
                elif validated_choice == 14:
                    update_script()
                elif validated_choice == 15:
                    break
        except ValueError as ve:
            logging.error(f"ValueError in menu: {ve}")
            print(f"Error: {ve}")
        except Exception as e:
            logging.error(f"Exception in menu: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    menu()
