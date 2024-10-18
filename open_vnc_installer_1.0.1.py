import sys
import subprocess
import urllib.parse
import urllib.request
import socket
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel
from PyQt5.QtGui import QPixmap
import ctypes
import shutil  # Import shutil for file operations

VERSION = "1.0.1"  # Define the current version

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
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        # Version label
        version_label = QLabel(f'Version: {VERSION}', self)
        version_label.setStyleSheet("font-size: 14px;")
        
        # Computer name label
        computer_label = QLabel(f'Computer Name: {computer_name}', self)
        computer_label.setStyleSheet("font-size: 14px;")
        
        # IP address label
        ip_label = QLabel(f'IP Address: {ip_address}', self)
        ip_label.setStyleSheet("font-size: 14px;")
        
        # Image label
        image_label = QLabel(self)
        pixmap = QPixmap('D:\Flask\static\images\logo1')  # Specify the path to your image file
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)  # Scale image to fit the label
        image_label.setFixedSize(pixmap.size())  # Set the size of the label to the size of the image
        
        # Button to start the program
        button = QPushButton('เริ่มการทำงานของโปรแกรม')
        button.clicked.connect(self.open_browser)
        
        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(image_label)  # Add the image label to the layout
        layout.addWidget(welcome_label)
        layout.addWidget(computer_label)
        layout.addWidget(ip_label) 
        layout.addWidget(version_label)
        layout.addWidget(button)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        self.setFixedSize(600, 800)  # Set fixed window size
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
        
        try:
            # Copy the installer from the local path to the destination
            print(f"Copying update from {download_url} to {installer_path}...")
            shutil.copy(download_url, installer_path)
            
            # Run the installer
            print(f"Installing update from {installer_path}...")
            subprocess.Popen([installer_path], shell=True)
            
            # Close the application
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update: {e}")

if __name__ == '__main__':
    # Hide the console window on Windows
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW("VNC Server")
        
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
