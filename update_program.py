import os
import shutil
import subprocess
import logging
import requests
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.popup import Popup
import psutil  # Import psutil for process management

UPDATE_URL = "http://10.10.15.94:3000/version"
SOURCE_INSTALLER_PATH = r"I:\test\open_vnc_installer_master.exe"
DESTINATION_FOLDER = os.path.join(os.getenv('LOCALAPPDATA'), 'MKS Support Center')
DESTINATION_INSTALLER_PATH = os.path.join(DESTINATION_FOLDER, "open_vnc_installer_master.exe")
VERSION_FILE_PATH = os.path.join(DESTINATION_FOLDER, "version.txt")

logging.info(f"DESTINATION_FOLDER: {DESTINATION_FOLDER}")
class UpdateWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.status_label = Label(text='Status: Ready', font_size=20)
        self.progress_bar = ProgressBar(max=100)
        self.update_button = Button(text='Check for Updates', size_hint_y=None, height=40)
        self.update_button.bind(on_press=self.check_for_updates)

        self.add_widget(self.status_label)
        self.add_widget(self.progress_bar)
        self.add_widget(self.update_button)

        Clock.schedule_once(self.check_for_updates, 0)  # Check for updates on start

    def get_current_version(self):
        """Retrieve the current version from version.txt."""
        if os.path.isfile(VERSION_FILE_PATH):
            with open(VERSION_FILE_PATH, 'r') as file:
                return file.read().strip()
        return None

    def write_version_to_file(self, version):
        """Write the new version to version.txt."""
        with open(VERSION_FILE_PATH, 'w') as file:
            file.write(version)

    def check_for_updates(self, *args):
        try:
            # Check for latest version on server
            response = requests.get(UPDATE_URL)
            response.raise_for_status()
            latest_version = response.json().get('version', '').strip()

            # Read the current version from version.txt
            current_version = self.get_current_version()
            logging.info(f"Latest version: {latest_version}")
            logging.info(f"Current version: {current_version}")

            # Compare versions and update if needed
            if latest_version != current_version:
                self.perform_update(latest_version)
            else:
                logging.info("Current version is up-to-date. Launching installer.")
                self.launch_installer()

        except requests.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            self.show_error(f"HTTP error occurred: {http_err}")
        except requests.RequestException as req_err:
            logging.error(f"Request error occurred: {req_err}")
            self.show_error(f"Request error occurred: {req_err}")
        except Exception as e:
            logging.error(f"Error checking for updates: {e}")
            self.show_error(f"Error checking for updates: {e}")

    def terminate_running_installer(self):
        """Terminate any running instances of the installer."""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'open_vnc_installer_master.exe':
                logging.info(f"Terminating process {proc.info['pid']}")
                proc.terminate()
                proc.wait()  # Wait for the process to be terminated
                logging.info("Process terminated successfully.")

    def perform_update(self, new_version):
        try:
            # Terminate any running instances of the installer
            self.terminate_running_installer()

            # Check if destination folder exists, create it if not
            if not os.path.exists(DESTINATION_FOLDER):
                os.makedirs(DESTINATION_FOLDER)
                logging.info(f"Created destination folder: {DESTINATION_FOLDER}")

            # Copy installer files
            if os.path.isfile(SOURCE_INSTALLER_PATH):
                shutil.copy(SOURCE_INSTALLER_PATH, DESTINATION_INSTALLER_PATH)
                logging.info(f"Copied installer from {SOURCE_INSTALLER_PATH} to {DESTINATION_INSTALLER_PATH}")
                self.update_progress(50)  # Update progress after copying

            # Update version file
            self.write_version_to_file(new_version)

            # Execute installer
            if os.path.isfile(DESTINATION_INSTALLER_PATH):
                self.update_progress(100)  # Complete progress

                # Launch the installer
                Clock.schedule_once(lambda dt: self.launch_installer(), 0.5)  # Delay before launching
            else:
                logging.error(f"Installer file not found: {DESTINATION_INSTALLER_PATH}")

        except Exception as e:
            logging.error(f"Error performing update: {e}")
            self.show_error(f"Error performing update: {e}")

    def update_progress(self, value):
        self.progress_bar.value = value

    def launch_installer(self):
        try:
            if os.path.isfile(DESTINATION_INSTALLER_PATH):
                subprocess.Popen([DESTINATION_INSTALLER_PATH], shell=True)
                logging.info("Launcher: Executing installer.")
                App.get_running_app().stop()  # Close the application after launching the installer
            else:
                logging.error(f"Installer file not found for launching: {DESTINATION_INSTALLER_PATH}")

        except Exception as e:
            logging.error(f"Error launching installer: {e}")
            self.show_error(f"Error launching installer: {e}")

    def show_error(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        button = Button(text='Close', size_hint_y=None, height=40)
        content.add_widget(button)
        popup = Popup(title='Error', content=content, size_hint=(0.8, 0.4))
        button.bind(on_press=popup.dismiss)
        popup.open()

class UpdateApp(App):
    def build(self):
        return UpdateWindow()

def main():
    logging.basicConfig(filename='update.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    UpdateApp().run()

if __name__ == '__main__':
    main()
