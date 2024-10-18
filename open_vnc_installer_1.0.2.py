from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import shutil
import subprocess
import sys
import ctypes
import socket
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

VERSION = "1.0.2"  # Define the current version

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        computer_name = query_params.get('computer_name', [''])[0]
        
        if computer_name:
            # Path to TightVNC executable
            vnc_path = r'C:\Program Files\TightVNC\tvnviewer.exe'
            
            # Run TightVNC Viewer with the specified computer name
            subprocess.Popen([vnc_path, f"{computer_name}"], shell=True)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'TightVNC Viewer opened.')
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error: Computer name not provided.')

class ServerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server = None
        self.server_running = True

    def run(self):
        server_address = ('', 8080)  # Port 8080
        self.server = HTTPServer(server_address, RequestHandler)
        print('Running server on port 8080...')
        
        while self.server_running:
            try:
                self.server.handle_request()
            except Exception as e:
                print(f"Error handling request: {e}")

    def stop(self):
        if self.server:
            print('Stopping server...')
            self.server_running = False
            self.server.server_close()
            print('Server stopped.')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Start the HTTP server in a separate thread
        self.server_thread = ServerThread()
        self.server_thread.start()
        
        self.initUI()
        
        # Check for updates when the application starts
        self.check_for_updates()
        
    def get_ip_address(self):
        """Retrieve the local IP address of the machine."""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            print(f"Failed to get IP address: {e}")
            return "Unknown IP"

    def initUI(self):
        # Get the computer name and IP address
        computer_name = socket.gethostname()
        ip_address = self.get_ip_address()
        
        # Welcome message label
        welcome_label = QLabel('ยินดีต้อนรับสู่ MKS Support Center', self)
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333333;")
        
        # Version label
        version_label = QLabel(f'Version: {VERSION}', self)
        version_label.setStyleSheet("font-size: 12px; color: #555555;")
        
        # Computer name label
        computer_label = QLabel(f'Computer Name: {computer_name}', self)
        computer_label.setStyleSheet("font-size: 12px; color: #555555;")
        
        # IP address label
        ip_label = QLabel(f'IP Address: {ip_address}', self)
        ip_label.setStyleSheet("font-size: 12px; color: #555555;")
        
        # Image label
        image_label = QLabel(self)
        pixmap = QPixmap('D:\\Flask\\static\\images\\logo1')  # Specify the path to your image file
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)  # Scale image to fit the label
        image_label.setFixedSize(200, 100)  # Set the size of the label for better fit
        
        # Button to start the program
        button = QPushButton('เริ่มการทำงานของโปรแกรม')
        button.setStyleSheet("font-size: 14px; padding: 10px; background-color: #0078d4; color: white; border-radius: 5px;")
        button.clicked.connect(self.open_browser)
        
        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("height: 20px;")
        
        # Layout setup
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Add margins around the layout
        layout.setSpacing(10)  # Set spacing between widgets
        layout.addWidget(image_label, alignment=Qt.AlignCenter)  # Center the image
        layout.addWidget(welcome_label, alignment=Qt.AlignCenter)
        layout.addWidget(computer_label, alignment=Qt.AlignCenter)
        layout.addWidget(ip_label, alignment=Qt.AlignCenter)
        layout.addWidget(version_label, alignment=Qt.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignCenter)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)  # Add progress bar to the layout
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        self.setFixedSize(600, 400)  # Adjusted window size for better fit
        self.setWindowTitle('MKS Support Center')
        self.show()

    def open_browser(self):
        # Open the specified URL in the default web browser
        url = "http://10.10.15.94:3000"
        webbrowser.open(url)
        print(f"Opened browser to {url}")

    def check_for_updates(self):
        # Path to check for the latest version
        version_check_path = r"D:\Flask\version.txt"  # Use raw string for Windows paths
        try:
            # Read the latest version from the local file
            with open(version_check_path, 'r') as file:
                latest_version = file.read().strip()
                if latest_version != VERSION:
                    self.prompt_update(latest_version)
        except Exception as e:
            print(f"Failed to check for updates: {e}")

    def prompt_update(self, latest_version):
        # Prompt the user to update to the latest version
        reply = QMessageBox.question(self, 'Update Available',
                                     f"A new version ({latest_version}) is available. Do you want to update?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.download_and_install_update(latest_version)

    def download_and_install_update(self, latest_version):
        # Local file path to the installer
        download_url = f"I:\\it share\\test\\update\\open_vnc_installer_{latest_version}.exe"
        installer_path = f"C:\\MKS Support Center\\open_vnc_installer_{latest_version}.exe"
        old_installer_path = f"C:\\MKS Support Center\\open_vnc_installer_{VERSION}.exe"
        
        try:
            # Copy the installer from the local path to the destination
            self.progress_bar.setValue(10)  # Set initial progress
            print(f"Copying update from {download_url} to {installer_path}...")
            shutil.copy(download_url, installer_path)
            self.progress_bar.setValue(40)  # Update progress
            
            # Run the installer with hidden CMD window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            print(f"Installing update from {installer_path}...")
            self.progress_bar.setValue(60)  # Update progress
            subprocess.Popen([installer_path], startupinfo=startupinfo, shell=True)
            
            # Delete the old installer
            if os.path.isfile(old_installer_path):
                print(f"Deleting old installer at {old_installer_path}...")
                os.remove(old_installer_path)
            
            self.progress_bar.setValue(100)  # Complete progress
            print("Update installation process started.")
        except Exception as e:
            self.progress_bar.setValue(0)  # Reset progress on error
            print(f"Failed to download or install update: {e}")
            QMessageBox.critical(self, 'Update Error', 'Failed to download or install the update.')

    def closeEvent(self, event):
        self.server_thread.stop()
        event.accept()

if __name__ == '__main__':
    # Hide the console window on Windows
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW("VNC Server")
        
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
