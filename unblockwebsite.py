import os
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return False

def run_as_admin():
    """Restart the script with administrative privileges."""
    if is_admin():
        return True  # Already running as admin
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    except Exception as e:
        print(f"Error: {e}")
    return False

def remove_line_from_hosts(file_path, line_to_remove):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip() != line_to_remove:
                    file.write(line)

        print(f"Successfully removed line: '{line_to_remove}' from {file_path}")
    
    except Exception as e:
        print(f"Error: {e}")

# Check if running as admin, if not, restart as admin
if run_as_admin():
    # Specify path to the hosts file
    hosts_file_path = r"C:\Windows\System32\drivers\etc\hosts"
    # Specify the line to remove
    line_to_remove = "127.0.0.1 www.facebook.com"
    # Call the function
    remove_line_from_hosts(hosts_file_path, line_to_remove)
