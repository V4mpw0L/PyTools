#!/usr/bin/env python3

import os
import subprocess
import time
import requests
from pytube import YouTube, Playlist
from pytube.exceptions import AgeRestrictedError
from tqdm import tqdm
from alive_progress import alive_bar
from colorama import Fore, Style
from slugify import slugify

# Define colors
class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    YELLOW = Fore.YELLOW
    NORMAL = Style.RESET_ALL
    BOLD = Style.BRIGHT

# Function to draw a line
def draw_line():
    print(Colors.BLUE + '=' * os.get_terminal_size().columns + Colors.NORMAL)

# Function to print a message with a box
def print_box(message):
    draw_line()
    print(Colors.BLUE + Colors.BOLD + message + Colors.NORMAL)
    draw_line()

# Function to draw a progress bar
def progress_bar():
    total = 20
    with alive_bar(total, bar='classic', spinner='dots_waves', title=f"{Colors.BOLD}{Colors.CYAN}Updating...{Colors.NORMAL}", length=40, enrich_print=True, manual=False) as bar:
        for _ in range(total):
            time.sleep(0.1)
            bar()

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
    print("Starting system update...")
    print(Colors.BLUE + Colors.BOLD)
    os.system('figlet -f standard "UPDATING..." | lolcat')
    print(Colors.NORMAL)
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
    try:
        ip = subprocess.getoutput(f'dig +short {site}')
        print(f"{Colors.BOLD}{Colors.RED}IP Address: {ip}{Colors.NORMAL}")
        os.system(f'ping -c 5 {site}')
    except Exception as e:
        print(f"Error: {e}")

# Function to geolocate an IP
def geolocate_ip():
    ip = input("Enter the IP to geolocate: ")
    geo = requests.get(f"https://ipinfo.io/{ip}").json()

    draw_line()
    print(f"{Colors.GREEN}{Colors.BOLD}Geolocation info:{Colors.NORMAL}")
    for key, value in geo.items():
        print(f"{Colors.YELLOW}{key}: {value}{Colors.NORMAL}")
    draw_line()

# Function to update the script from GitHub
def update_script():
    os.system('git pull origin main')
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

# Function to show system information
def system_information():
    print_box("System Information")
    os.system('neofetch')

# Function to show network information
def network_info():
    print_box("Network Information")
    output = subprocess.getoutput('ip addr')
    lines = output.split('\n')
    for line in lines:
        if 'inet' in line:
            print(Colors.GREEN + Colors.BOLD + line + Colors.NORMAL)
        else:
            print(line)

# Function to download video or mp3 from YouTube with progress bar
def download_youtube():
    url = input("Enter the YouTube video URL or playlist URL: ")
    print_box("Choose an option:")
    print(f"{Colors.BLUE}{Colors.BOLD}1.| Download Video{Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}2.| Download Audio (MP3){Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}3.| Cancel{Colors.NORMAL}")
    draw_line()
    choice = input("Enter your choice: ")
    selected_stream = None  # Initialize selected_stream here
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
            selected_stream -= 1  # Adjust for 0-based indexing
        for url in playlist.video_urls:
            download_video_or_audio(url, auto_download=True, choice=choice, selected_stream=selected_stream)
    else:
        download_video_or_audio(url, choice=choice, selected_stream=selected_stream)

def download_video_or_audio(url, auto_download=False, choice=None, selected_stream=None):
    yt = YouTube(url)
    print(f"{Colors.GREEN}{Colors.BOLD}Title: {yt.title}{Colors.NORMAL}")
    print(f"{Colors.GREEN}{Colors.BOLD}Duration: {yt.length // 60} minutes {yt.length % 60} seconds{Colors.NORMAL}")
    if choice == '1':
        if selected_stream is None:  # Only ask for user input if selected_stream is None
            print_box("Available Video Streams:")
            video_streams = yt.streams.filter(file_extension='mp4', progressive=True)
            for i, stream in enumerate(video_streams, start=1):
                print(f"{Colors.BLUE}{Colors.BOLD}{i}.| {stream.resolution} - {stream.filesize / 1024 / 1024:.2f} MB{Colors.NORMAL}")
            selected_stream = int(input("Enter the number of the stream to download: "))
            selected_stream -= 1  # Adjust for 0-based indexing
        download_video(yt, selected_stream)
    elif choice == '2':
        download_audio(yt)
    elif choice == '3':
        print("Download canceled.")
    else:
        print("Invalid option. Download canceled.")

def download_video(yt, selected_stream):
    try:
        video_streams = yt.streams.filter(file_extension='mp4', progressive=True)
    except AgeRestrictedError:
        print(f"{Colors.RED}Age-restricted video: {yt.video_id}. This video can't be accessed without logging in.{Colors.NORMAL}")
        return
    if selected_stream is not None:
        video = video_streams[selected_stream]
    else:
        video = video_streams.first()
    print(f"{Colors.GREEN}{Colors.BOLD}Downloading: {video.resolution} - {video.filesize / 1024 / 1024:.2f} MB{Colors.NORMAL}")
    response = requests.get(video.url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    # Use tqdm to create a progress bar
    with tqdm(total=total_size, unit='b', unit_scale=True, unit_divisor=1024) as bar:
        folder_path = os.path.join(os.getcwd(), 'VideosDownloads')
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{slugify(yt.title)}_video.mp4")
        with open(file_path, 'wb') as f:
            for data in response.iter_content(chunk_size=1024):
                bar.update(len(data))
                f.write(data)
    print_box(f"Video downloaded successfully as {slugify(yt.title)}_video.mp4 in the PlaylistVideos folder")

def download_audio(yt):
    try:
        audio_streams = yt.streams.filter(only_audio=True)
    except AgeRestrictedError:
        print(f"{Colors.RED}Age-restricted video: {yt.video_id}. This video can't be accessed without logging in.{Colors.NORMAL}")
        return
    audio = audio_streams[0]
    print(f"{Colors.GREEN}{Colors.BOLD}Downloading audio: {audio.abr} - {audio.filesize / 1024 / 1024:.2f} MB{Colors.NORMAL}")
    response = requests.get(audio.url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    # Use tqdm to create a progress bar
    with tqdm(total=total_size, unit='b', unit_scale=True, unit_divisor=1024) as bar:
        folder_path = os.path.join(os.getcwd(), 'AudiosDownloads')
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{slugify(yt.title)}_audio.mp3")
        with open(file_path, 'wb') as f:
            for data in response.iter_content(chunk_size=1024):
                bar.update(len(data))
                f.write(data)
    print_box(f"Audio downloaded successfully as {slugify(yt.title)}_audio.mp3 in the AudioDownloads folder")

# Menu
while True:
    draw_line()
    print(Colors.CYAN + Colors.BOLD)
    os.system('figlet -f standard " M E N U " | lolcat')
    print(Colors.NORMAL)
    draw_line()
    print(f"{Colors.CYAN}{Colors.BOLD}1.| Update the system{Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}2.| Ping a website or IP{Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}3.| Geolocate an IP{Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}4.| Disk Usage{Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}5.| Memory Usage{Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}6.| System Uptime{Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}7.| List Running Processes{Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}8.| Network Information{Colors.NORMAL}")
    print(f"{Colors.BLUE}{Colors.BOLD}9.| System Information{Colors.NORMAL}")
    print(f"{Colors.GREEN}{Colors.BOLD}10.| Download YouTube Video or MP3{Colors.NORMAL}")
    print(f"{Colors.YELLOW}{Colors.BOLD}11.| Update the Script{Colors.NORMAL}")
    print(f"{Colors.RED}{Colors.BOLD}12.| Exit{Colors.NORMAL}")
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
        system_information()
    elif choice == '11':
        update_script()
    elif choice == '12':
        break
    elif choice == '10':
        download_youtube()
    else:
        print("Invalid option. Please try again.")
