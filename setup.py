from cx_Freeze import setup, Executable
import os
import shutil
from win32com.client import Dispatch

# Define the path to the icon file if you have one
icon_path = 'D:\\Flask\\templates\\logo2.ico'

# Define paths dynamically
local_app_data = os.getenv('LOCALAPPDATA')
block_directory = os.path.join(local_app_data, 'MKS Support Center', 'block')

# Define any additional files you want to include
files = [
    ('D:\\Flask\\static\\images\\images.jpeg', 'images.jpeg'),
    (block_directory, 'block')  # Ensure 'block' is a directory
]

# Add the manifest for admin privileges
manifest = 'D:\\Flask\\templates\\manifest.xml'


# Post build script to add to autostart and create desktop shortcut
def post_build():
    # Create a shortcut on Desktop
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    shortcut_path = os.path.join(desktop, 'MKS Support Center.lnk')
    exe_path = os.path.join(os.environ['PROGRAMFILES'], 'MKS Support Center', 'MKS_Support_Center.exe')
    
    # Check if the shortcut already exists
    if not os.path.exists(shortcut_path):
        # Create a shortcut if it doesn't exist
        try:
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = exe_path
            shortcut.WorkingDirectory = os.path.dirname(exe_path)
            shortcut.IconLocation = exe_path
            shortcut.save()
            print(f"Shortcut created: {shortcut_path}")
        except Exception as e:
            print(f"Error creating shortcut: {e}")
            return

    # Add to autostart
    autostart_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'MKS Support Center.lnk')
    
    # Copy the shortcut to autostart
    try:
        shutil.copy(shortcut_path, autostart_path)
        print(f"Shortcut copied to startup: {autostart_path}")
    except FileNotFoundError:
        print(f"Shortcut not found: {shortcut_path}")
    except IOError as e:
        print(f"Error copying shortcut: {e}")

setup(
    name="MKS Support Center",
    version="1.2.5",
    description="MKS Support Center Application",
    executables=[
        Executable(
            script="D:\\Flask\\templates\\update.py",  # Your launcher script
            base="Win32GUI",  # Use "Console" for console apps, "Win32GUI" for GUI
            icon=icon_path,   # Use the icon file
            target_name="MKS_Support_Center.exe",  # Launcher executable
            manifest=manifest  # Include the manifest file
        ),
        Executable(
            script="D:\\Flask\\templates\\open_vnc_installer_master.py",  # Main application script
            base="Win32GUI",  # Use "Console" for console apps, "Win32GUI" for GUI
            icon=icon_path,   # Use the icon file
            target_name="MKS_Support_Center_main.exe",  # Main executable
            manifest=manifest  # Include the manifest file
        )
    ],
    options={
        'build_exe': {
            'packages': [
                'requests', 'socket', 'PyQt6', 'os', 'shutil', 'logging',
                'signal', 'threading', 'webbrowser', 'http', 'urllib', 'psutil',
                'ctypes', 'pandas'
            ],
            'include_files': files,
            'include_msvcr': True,  # Include Microsoft Visual C++ runtime
            'build_exe': os.path.join('D:', 'Flask', 'templates', 'build', 'mks_support_centerX64_3.11')
        }
    }
)

# Run the post-build steps
post_build()

