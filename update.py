import os
import requests
import shutil
import socket
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import ctypes
import time
import tkinter.font as tkFont  # Import the font module
import threading
import winreg

import subprocess
from datetime import datetime, timedelta


local_app_path = os.path.join(os.getenv('LOCALAPPDATA'), 'MKS Support Center')
update_source_path = r'\\10.10.10.11\Departments\test\update\path'
local_exe_path = os.path.join(local_app_path, 'MKS_Support_Center_main.exe')
version_url = 'http://10.10.15.94:3000/version'
local_version_file = os.path.join(local_app_path, 'version.txt')
block_source_path = r'\\10.10.10.11\Departments\test\block'
block_destination_path = os.path.join(local_app_path, 'block')
blocked_websites_url = 'http://10.10.15.94:3000/blocked_websites'
app1_path = os.path.join(local_app_path, 'MKS_Support_Center.exe')
app2_path = os.path.join(local_app_path, 'MKS_Support_Center_main.exe')


print(f"Local EXE Path: {local_exe_path}")
print(f"App1 Path: {app1_path}")
print(f"App2 Path: {app2_path}")


# Function to create a scheduled task
def create_scheduled_task(app_path):
    task_name = "MKS_Support_Center"
    start_time = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
    
    # Check if the application path exists
    if not os.path.isfile(app_path):
        print_to_gui(f"Application path does not exist: {app_path}")
        return False
    
    # Prepare the command to create the scheduled task
    task_command = f'SchTasks /Create /TN "{task_name}" /TR "{app_path}" /SC ONCE /ST {start_time} /RL HIGHEST /F'
    print(f"Task command: {task_command}")  # Print the command

    
    try:
        # Run the command to create the scheduled task
        result = subprocess.run(task_command, shell=True, check=True, capture_output=True, text=True)
        print_to_gui(f"Scheduled task '{task_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else "No error message available."
        print_to_gui(f"Failed to create scheduled task: {error_message}")
        return False
    
    return True

def run_scheduled_task(task_name):
    try:
        subprocess.run(f'SchTasks /Run /TN "{task_name}"', shell=True, check=True)
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else f"Error code: {e.returncode}"
        print_to_gui(f"Failed to run scheduled task: {error_message}")



def disable_uac_for_app(app_path):
    try:
        key_path = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, os.path.basename(app_path), 0, winreg.REG_SZ, 'RUNASINVOKER')
        return f"UAC disabled for: {app_path}"
    except Exception as e:
        return f"Failed to disable UAC for {app_path}: {e}"

# กำหนดเส้นทางของแอปพลิเคชัน



# ปิด UAC สำหรับแอปทั้งสอง
disable_uac_for_app(app1_path)
disable_uac_for_app(app2_path)

# กำหนดเส้นทาง



root = tk.Tk()
root.title("MKS Support Center Updater")
root.geometry("550x450")
root.configure(bg="#f1f1f1")  # Soft gray background for the app window

# Set the window icon (ensure you have the .ico file at the specified path)
root.iconbitmap = os.path.join(local_app_path,'logo2.ico')  # Replace with your icon file path

# Remove window decorations (minimize, maximize, close buttons)
root.overrideredirect(True)

# Disable resizing
root.resizable(False, False)

# Center the window on the screen
window_width = 550
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates to center the window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the new geometry
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Apply styles using ttk.Style
style = ttk.Style()
style.theme_use("clam")  # Choose a built-in theme ('clam', 'alt', 'default', 'classic')

# Set global font for the app
root.option_add("*Font", "TkDefaultFont")

# Customize the progress bar to have a modern look
style.configure("TProgressbar",
                thickness=20,
                troughcolor='#e0e0e0',  # Light gray trough to match Windows 11's subtle background
                background='#0a84ff',  # Windows 11 blue color for progress bar
                borderwidth=1,
                troughrelief='flat')

# Rounded progress bar edges (simulated through padding)
style.layout("TProgressbar",
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'})])

# Customize the label styles
style.configure("TLabel",
                font=("TkDefaultFont", 12),
                background="#f1f1f1",  # Match background color for seamless look
                foreground='#333333')  # Dark gray text

# Customize buttons (if needed)
style.configure("TButton",
                font=("TkDefaultFont", 10, "bold"),
                background='#0a84ff',  # Windows 11 blue for buttons
                foreground='white',
                borderwidth=0,
                padding=(5, 5))  # Some padding for a nice feel
style.map("TButton", background=[("active", "#005b99")])  # Darker blue on hover

# Add a scrolled text widget for displaying logs
text_area = tk.Text(root, wrap=tk.WORD, width=70, height=15, bg="#ffffff", fg="#333333", 
                    relief="flat", padx=10, pady=10, highlightbackground="#e0e0e0", highlightthickness=1)
text_area.pack(pady=10)

# Add a progress bar
progress_label = ttk.Label(root, text="Update Progress:")
progress_label.pack(pady=5)
progress_percent_label = ttk.Label(root, text="0%")
progress_percent_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate", style="TProgressbar")
progress_bar.pack(pady=10)

# Add a time estimate label
time_label = ttk.Label(root, text="Estimated Time Remaining: 00:00")
time_label.pack(pady=5)
def print_to_gui(message):
    """Function to print messages to the GUI."""
    if isinstance(message, bool):
        message = str(message)  # Convert boolean to string
    text_area.insert(tk.END, message + "\n")
    text_area.see(tk.END)
    root.update()


# Function to get the local version
def get_local_version():
    if os.path.exists(local_version_file):
        with open(local_version_file, 'r') as f:
            return f.read().strip()
    return None

# Function to get the remote version
def get_remote_version():
    try:
        response = requests.get(version_url)
        if response.status_code == 200:
            return response.json().get('version')
        else:
            print_to_gui(f"Failed to get version from server. Status code: {response.status_code}")
            return None
    except Exception as e:
        print_to_gui(f"Error fetching remote version: {e}")
        return None

def copy_update_files():
    total_files = sum([len(files) for _, _, files in os.walk(update_source_path)])
    processed_files = 0

    start_time = time.time()

    if os.path.exists(update_source_path):
        for root_dir, dirs, files in os.walk(update_source_path):
            for file in files:
                try:
                    source_file = os.path.join(root_dir, file)
                    destination_file = os.path.join(local_app_path, os.path.relpath(source_file, update_source_path))
                    os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                    shutil.copy2(source_file, destination_file)

                    processed_files += 1
                    progress = (processed_files / total_files) * 100
                    progress_bar['value'] = progress
                    progress_percent_label.config(text=f"{progress:.2f}%")  # Update the percent label

                    # Calculate time estimate
                    elapsed_time = time.time() - start_time
                    estimated_total_time = (elapsed_time / processed_files) * total_files
                    remaining_time = estimated_total_time - elapsed_time
                    remaining_minutes, remaining_seconds = divmod(remaining_time, 60)
                    time_label.config(text=f"Estimated Time Remaining: {int(remaining_minutes):02}:{int(remaining_seconds):02}")

                    print_to_gui(f"Installing {file}: {progress:.2f}% Done.")
                    root.update_idletasks()  # Update the GUI

                except Exception as e:
                    print_to_gui(f"Error copying {file}: {e}")
                    
        progress_bar['value'] = 100
        progress_percent_label.config(text="100%")  # Set progress label to 100% when done
        print_to_gui("Update files copied successfully.")
    else:
        print_to_gui(f"Update source path {update_source_path} does not exist. Creating the directory...")
        os.makedirs(update_source_path, exist_ok=True)

# Function to run copy in a separate thread
def run_copy_update_files():
    threading.Thread(target=copy_update_files).start()

def task_exists(task_name):
    try:
        subprocess.run(f'SchTasks /Query /TN "{task_name}"', shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# In the main function
if not task_exists("MKS_Support_Center"):
    print_to_gui("Scheduled task does not exist. Cannot run the task.")
else:
    run_scheduled_task("MKS_Support_Center")
# Function to copy the block file named after the computer name
def copy_block_file():
    computer_name = socket.gethostname() + '.txt'
    source_block_file = os.path.join(block_source_path, computer_name)
    destination_block_file = os.path.join(block_destination_path, computer_name)
    
    if os.path.exists(source_block_file):
        os.makedirs(block_destination_path, exist_ok=True)
        shutil.copy2(source_block_file, destination_block_file)
        print_to_gui(f"Block file '{computer_name}' copied successfully.")
    else:
        print_to_gui(f"Block file '{computer_name}' does not exist in the source path. Creating the file...")
        create_file(source_block_file)
        notify_server_blocked_websites(computer_name)

# Function to create a file if it does not exist
def create_file(file_path):
    try:
        open(file_path, 'w').close()
        print_to_gui(f"Created empty file: {file_path}")
    except IOError as e:
        print_to_gui(f"Error creating file {file_path}: {e}")

# Function to send computer name to the server
def notify_server_blocked_websites(computer_name):
    try:
        response = requests.post(blocked_websites_url, data={'computer_name': computer_name})
        if response.status_code == 200:
            print_to_gui(f"Computer name '{computer_name}' sent to server successfully.")
        else:
            print_to_gui(f"Failed to send computer name to server. Status code: {response.status_code}")
    except Exception as e:
        print_to_gui(f"Error sending computer name to server: {e}")

# Function to run the EXE file with elevated permissions
def run_as_admin(executable):
    try:
        # Use ctypes to request elevation
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, None, None, 1)
    except Exception as e:
        print_to_gui(f"Failed to run application as admin: {e}")

# Main function
def check_access_and_list_files(path):
    """Function to check access to a directory and list files within it."""
    if os.path.exists(path):
        if os.path.isdir(path):
            print_to_gui(f"Access to directory {path} is available.")
            files = os.listdir(path)
            if files:
                print_to_gui(f"Files found in {path}:")
                for file in files:
                    print_to_gui(file)
            else:
                print_to_gui(f"No files found in {path}.")
        else:
            print_to_gui(f"The path {path} is not a directory.")
    else:
        print_to_gui(f"The path {path} does not exist. Creating the directory...")
        os.makedirs(path, exist_ok=True)

# Function to check access and list files in the update source path and block source path
def check_paths():
    print_to_gui("Checking access and listing files...")
    check_access_and_list_files(update_source_path)
    check_access_and_list_files(block_source_path)

# Main function
# At the start of your script, define app_path
app_path = app1_path  # Or app2_path, depending on which you want to use

def main():
    local_version = get_local_version()
    remote_version = get_remote_version()

    print_to_gui(f"Local version: {local_version}")
    print_to_gui(f"Remote version: {remote_version}")
    
    # Create the scheduled task and capture the result
    create_task_result = create_scheduled_task(app_path)
    
    if create_task_result:
        print_to_gui("Scheduled task created successfully.")
    else:
        print_to_gui("Failed to create scheduled task.")

    # Run the scheduled task
    run_scheduled_task("MKS_Support_Center")

    # Check file access before performing updates
    check_paths()

    if remote_version and local_version != remote_version:
        print_to_gui("Versions do not match. Updating files...")
        copy_update_files()
        
        # Update the local version file
        with open(local_version_file, 'w') as f:
            f.write(remote_version)
        
        print_to_gui("Update complete.")
    
    # Copy block file regardless of update status
    copy_block_file()

    # Disable UAC for both applications
    uac_result1 = disable_uac_for_app(app1_path)
    uac_result2 = disable_uac_for_app(app2_path)
    print_to_gui(f"{uac_result1}, and {uac_result2}")

    # Launch the application with admin privileges
    print_to_gui("Launching the application...")
    run_as_admin(local_exe_path)

    root.after(3000, root.destroy())

# Run the update in the tkinter main loop
def run_update():
    main()

root.after(1000, run_update)  # Starts update process after 1 second delay
root.mainloop()
