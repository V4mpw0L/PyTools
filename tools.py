#!/usr/bin/env python3
_J='content-length'
_I='Enter the number of the stream to download: '
_H='Available Video Streams:'
_G='Enter your choice: '
_F='neofetch'
_E='mp4'
_D=False
_C='\n'
_B=None
_A=True
import os,subprocess,time,requests,socket,re
from pytube import YouTube,Playlist
from pytube.exceptions import AgeRestrictedError
from tqdm import tqdm
from alive_progress import alive_bar
from colorama import Fore,Style,Back
from slugify import slugify
import logging
class Colors:RED=Fore.RED;GREEN=Fore.GREEN;BLUE=Fore.BLUE;CYAN=Fore.CYAN;YELLOW=Fore.YELLOW;NORMAL=Style.RESET_ALL;BOLD=Style.BRIGHT;MAGENTA=Fore.MAGENTA
logging.basicConfig(filename='script.log',level=logging.DEBUG)
def draw_line():print(Colors.BLUE+'='*os.get_terminal_size().columns+Colors.NORMAL)
def print_box(message):draw_line();print(Colors.BLUE+Colors.BOLD+message+Colors.NORMAL);draw_line()
def progress_bar(total=15):
	A=total
	with alive_bar(A,bar='classic',spinner='dots_waves',title=f"{Colors.BOLD}{Colors.CYAN}Updating...{Colors.NORMAL}",length=40,enrich_print=_A,manual=_D)as B:
		for C in range(A):time.sleep(.1);B()
def commands_exist(commands):A=[A for A in commands if subprocess.call(['which',A],stdout=subprocess.PIPE,stderr=subprocess.PIPE)!=0];return not A
required_commands=['figlet','lolcat',_F]
if not commands_exist(required_commands):missing_commands_str=', '.join(required_commands);logging.error(f"One or more required commands not found: {missing_commands_str}. Please install them.");print(f"Error: One or more required commands not found: {missing_commands_str}. Please install them.");exit(1)
def update_system():
	B='Starting system update...'
	try:logging.info(B);print(B);print(Colors.BLUE+Colors.BOLD);os.system('figlet -f standard "UPDATING..." | lolcat');print(Colors.NORMAL);draw_line();run_command('sudo apt update -y','Updating package lists...');run_command('sudo apt upgrade -y','Upgrading installed packages...');run_command('sudo apt autoremove -y','Removing unused packages...');run_command('sudo apt autoclean -y','Cleaning up package cache...');print_box('Your system is up to date.')
	except Exception as A:logging.error(f"System update failed. Error: {A}");print(f"Error: {A}")
def run_command(command,message):
	A=command
	try:print_box(message);subprocess.run(A,shell=_A,check=_A);progress_bar()
	except subprocess.CalledProcessError as B:logging.error(f"Command '{A}' failed with error code {B.returncode}.");print(f"Error: System update failed. Please check the logs for details.")
def ping_site():
	try:
		A=input('Enter the website or IP to ping: ')
		if is_ip_address(A):D=resolve_ip(A);print(f"{Colors.BOLD}{Colors.RED}Website: {D}{Colors.NORMAL}")
		else:
			B=resolve_ip(A)
			if B:print(f"{Colors.BOLD}{Colors.RED}IP Address: {B}{Colors.NORMAL}");perform_ping(A)
			else:print(f"Unable to resolve IP address for {A}. Ping aborted.")
	except Exception as C:logging.error(f"Ping failed. Error: {C}");print(f"Error: {C}")
def is_ip_address(value):
	try:socket.inet_aton(value);return _A
	except socket.error:return _D
def resolve_ip(site_or_ip):
	A=site_or_ip
	try:
		if is_ip_address(A):return subprocess.getoutput(f"dig +short -x {A}")
		else:B=subprocess.getoutput(f"dig +short {A}");return B.strip()
	except Exception as C:logging.warning(f"Failed to resolve IP address. Error: {C}");return
def perform_ping(site_or_ip):
	try:os.system(f"ping -c 3 {site_or_ip}")
	except Exception as A:logging.error(f"Ping operation failed. Error: {A}");print(f"Error: {A}")
def geolocate_ip():
	try:
		C=input('Enter the IP to geolocate: ');A=get_geolocation(C)
		if A:display_geolocation_info(A)
		else:print('Unable to retrieve geolocation information.')
	except Exception as B:logging.error(f"Geolocation failed. Error: {B}");print(f"Error: {B}")
def get_geolocation(ip):
	try:
		A=requests.get(f"https://ipinfo.io/{ip}")
		if A.status_code==200:return A.json()
		else:logging.warning(f"Failed to retrieve geolocation. Status Code: {A.status_code}");return
	except requests.RequestException as B:logging.error(f"Geolocation request failed. Error: {B}");return
def display_geolocation_info(geo_info):
	draw_line();print(f"{Colors.GREEN}{Colors.BOLD}Geolocation info:{Colors.NORMAL}")
	for(A,B)in geo_info.items():print(f"{Colors.YELLOW}{A}: {B}{Colors.NORMAL}")
	draw_line()
def update_script():
	try:os.system('git reset --hard origin/main');os.system('git clean -fdx');os.system('git pull origin main');print_box('Script updated successfully. Please restart the script.');logging.info('Script updated successfully.');exit()
	except Exception as A:logging.error(f"Script update failed. Error: {A}");print(f"Error: {A}")
def disk_usage():
	try:
		print_box('Disk Usage');G=subprocess.getoutput('df -h');B=G.split(_C);H=B[0];print(Colors.CYAN+Colors.BOLD+H+Colors.NORMAL)
		for I in B[1:]:A=I.split();J,K,L,M,C,N=A[0],A[1],A[2],A[3],A[4],A[5];O=f"{Colors.GREEN}{J: <15}{Colors.NORMAL}  {K: <10}  {L: <10}  {M: <10}  {Colors.YELLOW}{C: <6}{Colors.NORMAL}  {Colors.BLUE}{N}{Colors.NORMAL}";D=20;P=int(C.rstrip('%'));E=int(D*P/100);Q=D-E;R=f"{Colors.CYAN}[{'#'*E}{'-'*Q}]{Colors.NORMAL}";print(O);print(R)
	except Exception as F:logging.error(f"Failed to retrieve disk usage. Error: {F}");print(f"Error: {F}")
def memory_usage():
	try:print_box('Memory and Swap Usage');E=subprocess.check_output(['free','-h'],text=_A);B=E.split(_C);F=B[0];A=B[1].split();C=B[2].split();print(Colors.CYAN+Colors.BOLD+F+Colors.NORMAL);G=f"{Colors.GREEN}{A[0]:<10}{Colors.NORMAL}  {Colors.YELLOW}{A[1]:<10}{Colors.NORMAL}  {Colors.RED}{A[2]:<10}{Colors.NORMAL}  {Colors.BLUE}{A[3]:<10}{Colors.NORMAL}  {Colors.YELLOW}{A[4]:<10}{Colors.NORMAL}  {Colors.CYAN}{A[5]:<10}{Colors.NORMAL}";print(G);H=f"{Colors.GREEN}{C[0]:<10}{Colors.NORMAL}  {Colors.YELLOW}{C[1]:<10}{Colors.NORMAL}  {Colors.RED}{C[2]:<10}{Colors.NORMAL}";print(H)
	except Exception as D:logging.error(f"Failed to retrieve memory and swap usage. Error: {D}");print(f"Error: {D}")
def system_uptime():
	try:print_box('System Uptime');os.system('uptime')
	except Exception as A:logging.error(f"Failed to retrieve system uptime. Error: {A}");print(f"Error: {A}")
def list_processes():
	try:
		print_box('Running Processes');D=subprocess.getoutput('ps aux');B=D.split(_C);E=B[0];print(Colors.CYAN+Colors.BOLD+E+Colors.NORMAL)
		for F in B[1:]:A=F.split();G,H,I,J,K,L,M,N,O,P,Q=A[0],A[1],A[2],A[3],A[4],A[5],A[6],A[7],A[8],A[9],' '.join(A[10:]);R=f"{Colors.GREEN}{G}{Colors.NORMAL}  {Colors.YELLOW}{H}{Colors.NORMAL}  {I}  {J}  {K}  {L}  {Colors.BLUE}{M}{Colors.NORMAL}  {N}  {O}  {P}  {Colors.RED}{Q}{Colors.NORMAL}";print(R)
	except Exception as C:logging.error(f"Failed to list running processes. Error: {C}");print(f"Error: {C}")
def system_information():
	try:print_box('System Information');os.system(_F)
	except Exception as A:logging.error(f"Failed to retrieve system information. Error: {A}");print(f"Error: {A}")
def network_info():
	try:
		F={'lo':Colors.CYAN,'eth0':Colors.GREEN,'wlan0':Colors.YELLOW,'docker0':Colors.BLUE};print_box('Network Information');H=subprocess.getoutput('ip addr');I=H.split(_C);C=_B
		for D in I:
			A=D.split()
			for B in A:
				if':'in B and B[:-1]in F:C=B[:-1];break
			if C:
				print(f"{F[C]}{Colors.BOLD}{C}{Colors.NORMAL}")
				for(E,B)in enumerate(A):
					if'inet'in B and E+1<len(A)and'.'in A[E+1]:J=A[E+1];print(f"IP Address: {Colors.RED}{Colors.BOLD}{J}{Colors.NORMAL}");break
				else:print(D)
			else:print(D)
	except Exception as G:logging.error(f"Failed to retrieve network information. Error: {G}");print(f"Error: {G}")
def download_youtube():
	try:
		A=input('Enter the YouTube video URL or playlist URL: ');print_box('Choose an option:');print(f"{Colors.BLUE}{Colors.BOLD}1.| Download Video{Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD}2.| Download Audio (MP3){Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD}3.| Cancel{Colors.NORMAL}");draw_line();C=input(_G);B=_B
		if'playlist'in A:
			D=Playlist(A);print(f"Downloading playlist: {D.title}")
			if C=='1':
				print_box(_H);G=YouTube(D.video_urls[0]);H=G.streams.filter(file_extension=_E,progressive=_A)
				for(I,E)in enumerate(H,start=1):print(f"{Colors.BLUE}{Colors.BOLD}{I}.| {E.resolution} - {E.filesize/1024/1024:.2f} MB{Colors.NORMAL}")
				B=int(input(_I));B-=1
			for A in D.video_urls:download_video_or_audio(A,auto_download=_A,choice=C,selected_stream=B)
		else:download_video_or_audio(A,choice=C,selected_stream=B)
	except Exception as F:logging.error(f"YouTube download failed. Error: {F}");print(f"Error: {F}")
def download_video_or_audio(url,auto_download=_D,choice=_B,selected_stream=_B):
	C=choice;B=selected_stream
	try:
		A=YouTube(url);print(f"{Colors.GREEN}{Colors.BOLD}Title: {A.title}{Colors.NORMAL}");print(f"{Colors.GREEN}{Colors.BOLD}Duration: {A.length//60} minutes {A.length%60} seconds{Colors.NORMAL}")
		if C=='1':
			if B is _B:
				print_box(_H);F=A.streams.filter(file_extension=_E,progressive=_A)
				for(G,D)in enumerate(F,start=1):print(f"{Colors.BLUE}{Colors.BOLD}{G}.| {D.resolution} - {D.filesize/1024/1024:.2f} MB{Colors.NORMAL}")
				B=int(input(_I));B-=1
			download_video(A,B)
		elif C=='2':download_audio(A)
		elif C=='3':print('Download canceled.')
		else:print('Invalid option. Download canceled.')
	except Exception as E:logging.error(f"Download failed. Error: {E}");print(f"Error: {E}")
def download_video(yt,selected_stream,max_retries=3):
	F=selected_stream;C=max_retries
	try:
		G=yt.streams.filter(file_extension=_E,progressive=_A)
		if F is not _B:B=G[F]
		else:B=G.first()
		print(f"{Colors.GREEN}{Colors.BOLD}Downloading: {B.resolution} - {B.filesize/1024/1024:.2f} MB{Colors.NORMAL}");H=os.path.join(os.getcwd(),'VideosDownloads');os.makedirs(H,exist_ok=_A);J=os.path.join(H,f"{slugify(yt.title)}_video.mp4");D=0
		while D<C:
			try:
				E=requests.get(B.url,stream=_A);E.raise_for_status();K=int(E.headers.get(_J,0))
				with tqdm(total=K,unit='b',unit_scale=_A,unit_divisor=1024)as L:
					with open(J,'wb')as M:
						for I in E.iter_content(chunk_size=1024):L.update(len(I));M.write(I)
				print_box(f"Video downloaded successfully as {slugify(yt.title)}_video.mp4 in the PlaylistVideos folder");return
			except requests.RequestException as A:logging.warning(f"Network request failed. Retrying... (Error: {A})");D+=1;time.sleep(2**D)
		logging.error(f"Video download failed after {C} retries. Error: {A}");print(f"Error: Unable to download the video after {C} retries.")
	except Exception as A:logging.error(f"Video download failed. Error: {A}");print(f"Error: {A}")
def download_audio(yt,max_retries=3):
	B=max_retries
	try:
		H=yt.streams.filter(only_audio=_A);C=H[0];print(f"{Colors.GREEN}{Colors.BOLD}Downloading audio: {C.abr} - {C.filesize/1024/1024:.2f} MB{Colors.NORMAL}");F=os.path.join(os.getcwd(),'AudiosDownloads');os.makedirs(F,exist_ok=_A);I=os.path.join(F,f"{slugify(yt.title)}_audio.mp3");D=0
		while D<B:
			try:
				E=requests.get(C.url,stream=_A);E.raise_for_status();J=int(E.headers.get(_J,0))
				with tqdm(total=J,unit='b',unit_scale=_A,unit_divisor=1024)as K:
					with open(I,'wb')as L:
						for G in E.iter_content(chunk_size=1024):K.update(len(G));L.write(G)
				print_box(f"Audio downloaded successfully as {slugify(yt.title)}_audio.mp3 in the AudioDownloads folder");return
			except requests.RequestException as A:logging.warning(f"Network request failed. Retrying... (Error: {A})");D+=1;time.sleep(2**D)
		logging.error(f"Audio download failed after {B} retries. Error: {A}");print(f"Error: Unable to download the audio after {B} retries.")
	except Exception as A:logging.error(f"Audio download failed. Error: {A}");print(f"Error: {A}")
def scan_for_malware():
	try:run_command('clamscan --infected --recursive --suppress-ok-results','Scanning for malware or viruses...');print_box('Malware scan completed.')
	except Exception as A:logging.error(f"Malware scan failed. Error: {A}");print(f"Error: {A}")
def check_password_strength():
	try:print_box('Checking password strength...');B=input('Enter the password to check its strength: ');C,D=get_password_strength(B);print_colored_box(C,D)
	except Exception as A:logging.error(f"Password strength check failed. Error: {A}");print(f"Error: {A}")
def get_password_strength(password):
	D='[a-z]';C='[A-Z]';B='\\d';A=password
	if len(A)>=16 and re.search(C,A)and re.search(D,A)and re.search(B,A)and re.search('[!@#$%^&*(),.?":{}|<>]',A):return'Password strength: Super Strong',Fore.GREEN
	elif len(A)>=12 and re.search(C,A)and re.search(D,A)and re.search(B,A):return'Password strength: Strong',Fore.CYAN
	elif len(A)>=8 and re.search('[A-Za-z]',A)and re.search(B,A):return'Password strength: Medium',Fore.YELLOW
	elif len(A)>=6:return'Password strength: Weak',Fore.RED
	else:return'Password strength: Super Weak',Fore.MAGENTA
def print_colored_box(message,color):draw_line();print(color+Style.BRIGHT+message+Style.RESET_ALL);draw_line()
def perform_traceroute():
	B='Performing traceroute...'
	try:print_box(B);C=input('Enter the destination for traceroute: ');run_command(f"traceroute {C}",B)
	except Exception as A:logging.error(f"Traceroute failed. Error: {A}");print(f"Error: {A}")
def menu():
	while _A:
		draw_line();print(f"{Colors.CYAN}{Colors.BOLD}");os.system('figlet -f standard " M e n u " | lolcat');print(Colors.NORMAL);draw_line();print(f"{Colors.CYAN}{Colors.BOLD} 1.| {Colors.CYAN}Update the system{Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD} 2.| {Colors.BLUE}Ping a website or IP{Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD} 3.| {Colors.BLUE}Geolocate an IP{Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD} 4.| {Colors.BLUE}Disk Usage{Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD} 5.| {Colors.BLUE}Memory Usage{Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD} 6.| {Colors.BLUE}System Uptime{Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD} 7.| {Colors.BLUE}List Running Processes{Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD} 8.| {Colors.BLUE}Network Information{Colors.NORMAL}");print(f"{Colors.BLUE}{Colors.BOLD} 9.| {Colors.BLUE}System Information{Colors.NORMAL}");print(f"{Colors.YELLOW}{Colors.BOLD}10.| {Colors.YELLOW}Scan for Malware{Colors.NORMAL}");print(f"{Colors.YELLOW}{Colors.BOLD}11.| {Colors.YELLOW}Check Password Strength{Colors.NORMAL}");print(f"{Colors.YELLOW}{Colors.BOLD}12.| {Colors.YELLOW}Perform Traceroute{Colors.NORMAL}");print(f"{Colors.GREEN}{Colors.BOLD}13.| {Colors.GREEN}Download YouTube Video or MP3{Colors.NORMAL}");print(f"{Colors.GREEN}{Colors.BOLD}14.| {Colors.GREEN}Update the Script{Colors.NORMAL}");print(f"{Colors.RED}{Colors.BOLD}15.| {Colors.RED}Exit{Colors.NORMAL}");draw_line()
		try:
			A=int(input(_G))
			if A==1:update_system()
			elif A==2:ping_site()
			elif A==3:geolocate_ip()
			elif A==4:disk_usage()
			elif A==5:memory_usage()
			elif A==6:system_uptime()
			elif A==7:list_processes()
			elif A==8:network_info()
			elif A==9:system_information()
			elif A==10:scan_for_malware()
			elif A==11:check_password_strength()
			elif A==12:perform_traceroute()
			elif A==13:download_youtube()
			elif A==14:update_script()
			elif A==15:break
			else:print('Invalid option. Please try again.')
		except ValueError:print('Invalid input. Please enter a number.')
if __name__=='__main__':menu()
