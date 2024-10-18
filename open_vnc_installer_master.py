from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, 
    QMessageBox, QSystemTrayIcon, QMenu, QProgressBar, QDialog, QTableWidget, 
    QTableWidgetItem, QLineEdit, QSpacerItem, QSizePolicy,QHeaderView
)
from PyQt6.QtGui import QAction, QIcon, QPixmap, QFont, QCursor
from PyQt6.QtCore import Qt, QSystemSemaphore, QTimer, QEvent, QSize, QThread, pyqtSignal, QSharedMemory

import os
import shutil
import subprocess
import sys
import logging
import signal
import socket
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests
import psutil
import time
import ctypes
import pandas as pd

# Ensure that there are no duplicate imports of the same modules/classes


VERSION = "1.2.5"
# Define a user-accessible directory for logs
log_directory = os.path.join(os.path.expanduser('~'), 'MKS Support Center Logs')

# Ensure the directory exists
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging
log_file = os.path.join(log_directory, 'log_mkssupportcenter.txt')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        computer_name = query_params.get('computer_name', [''])[0]

        if computer_name:
                vnc_path = r'C:\Program Files\TightVNC\tvnviewer.exe'
                response = self.check_computer_online(computer_name)
                
                if response:
                    subprocess.Popen([vnc_path, f"{computer_name}"], shell=True)
                    # Add your second command here if needed
                    # subprocess.Popen([second_command], shell=True)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'TightVNC Viewer opened and computer is online.')
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Error: Computer is offline or unreachable.')

        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error: Computer name not provided.')

    def check_computer_online(self, computer_name):
        try:
            output = subprocess.check_output(f"ping -n 1 {computer_name}", shell=True)
            return True
        except subprocess.CalledProcessError:
            return False



class ServerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server = None
        self.server_running = True

    def run(self):
        server_address = ('', 8080)
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

class LoginDialog(QDialog):
    login_successful = pyqtSignal()  # Signal to indicate successful login

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')

        # Create widgets
        self.username_label = QLabel('Username:', self)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Enter username')

        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.check_credentials)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == 'support' and password == 'cappuccino1*':
            self.login_successful.emit()  # Emit signal on successful login
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.latest_version = VERSION
        self.initUI()
        computer_name = socket.gethostname()
        self.login_dialog = None  # Initialize login_dialog attribute
        # Send status as "Connected" on initialization
        self.send_computer_status(computer_name, 'Connected')  # Send "Connected" status
        print(self.send_computer_status(computer_name, 'Connected') )

        if computer_name in ['W2403030NN', 'W231102AP']:
            self.server_thread = ServerThread()
            self.server_thread.start()

        self.block_websites_for_computer(computer_name)
        print(self.block_websites_for_computer(computer_name))


        icon_path = os.path.join(os.getenv('LOCALAPPDATA'), 'MKS Support Center', 'logo2.ico')
        self.tray_icon = SystemTrayIcon(QIcon(icon_path), self)
        self.tray_icon.show()
        self.tray_icon.hide()  # Initially hide the tray icon

        self.update_log = []  # Initialize update_log      
        self.open_browser()
    def update_status(self, status):
        self.status_label.setText(f'Status: {status}')

    def get_ip_address(self):
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            print(f"Failed to get IP address: {e}")
            return "Unknown IP"

    def initUI(self):
        self.setWindowTitle('MKS Support Center')
        computer_name = socket.gethostname()
        ip_address = self.get_ip_address()

        # Style for the labels
        label_style = "font-size: 14px; color: #333333;"

        welcome_label = QLabel('ยินดีต้อนรับสู่ MKS Support Center', self)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5a5a;")

        version_label = QLabel(f'Version: {VERSION}', self)
        version_label.setStyleSheet(label_style)

        computer_label = QLabel(f'Computer Name: {computer_name}', self)
        computer_label.setStyleSheet(label_style)

        ip_label = QLabel(f'IP Address: {ip_address}', self)
        ip_label.setStyleSheet(label_style)

        self.status_label = QLabel('Status: Online', self)
        self.status_label.setStyleSheet("font-size: 14px; color: #4CAF50;")  # Green color for Online status

        self.update_message_label = QLabel("Checking for updates...", self)
        self.update_message_label.setStyleSheet("font-size: 14px; color: #000000;")
        self.update_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.blocked_websites_table = QTableWidget()
        self.blocked_websites_table.setColumnCount(1)
        self.blocked_websites_table.setHorizontalHeaderLabels(['Website'])
        self.blocked_websites_table.horizontalHeader().setStretchLastSection(True)
        self.blocked_websites_table.setVisible(False)  # Initially hidden

        # Image label
        image_label = QLabel(self)
        image_path = os.path.join(os.getenv('LOCALAPPDATA'), 'MKS Support Center', 'images.jpeg')
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setFixedSize(400, 400)

        # Button
        button = QPushButton('เริ่มการทำงานของโปรแกรม', self)
        button.setStyleSheet("""
            font-size: 16px; 
            padding: 10px; 
            background-color: #4CAF50; 
            color: white; 
            border-radius: 10px;
            border: none;
        """)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.clicked.connect(self.open_browser)

        # Initialize layout
        layout = QVBoxLayout()
        spacer = QSpacerItem(20, 200, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)
        layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(computer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ip_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.update_message_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.blocked_websites_table, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.load_blocked_websites()

    def load_blocked_websites(self):
        """Load blocked websites from the file."""
        blocked_websites_path = os.path.join(os.getenv('LOCALAPPDATA'), 'MKS Support Center', 'block')
        try:
            if not os.path.exists(blocked_websites_path):
                QMessageBox.critical(self, 'Error', 'Blocked websites file not found.')
                return []  # Return an empty list if file is not found

            with open(blocked_websites_path, 'r') as file:
                websites = [line.strip() for line in file.readlines()]

            if not websites:
                QMessageBox.information(self, 'No Data', 'No blocked websites found.')
                return []  # Return an empty list if no websites are in the file

            self.blocked_websites_table.setRowCount(len(websites))
            for row, website in enumerate(websites):
                item = QTableWidgetItem(website)
                self.blocked_websites_table.setItem(row, 0, item)
            return websites

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load blocked websites: {e}')
            return []




    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange and self.windowState() & Qt.WindowState.WindowMinimized:
            self.minimizedEvent(event)

    def minimizedEvent(self, event):
        reply = QMessageBox.question(self, 'เก็บไว้ในพื้นหลัง',
                                     'ต้องการเก็บโปรแกรมไว้ในพื้นหลังหรือไม่?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.hide()
            event.ignore()
        else:
            event.ignore()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'ออกจากโปรแกรม',
                                    'Are you sure you want to quit?\nคุณแน่ใจใช่ไหมที่ต้องการจะออกจากโปรแกรม?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.send_computer_status(socket.gethostname(), 'Disconnected')  # Send "Disconnected" status
            if hasattr(self, 'server_thread'):
                self.server_thread.stop()  # Ensure server thread stops if it exists
            event.accept()
        else:
            event.ignore()

    def open_browser(self):
        import webbrowser
        webbrowser.open("http:10.10.15.94:3000")
        print(f"Open{webbrowser}")

    def close_application(self):
        print("Closing application.")
        QApplication.quit()


    def send_computer_status(self, computer_name, status):
        try:
            url = "http://10.10.15.94:3000/update_status_wall_to_wall"
            data = {'computer_name': computer_name, 'status': status}
            print(f"Sending data: {data}")
            response = requests.post(url, data=data)

            if response.status_code == 200:
                print(f"Successfully updated status for {computer_name}.")
            else:
                print(f"Failed to update status for {computer_name}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending status update: {e}")

    def show_update_button(self):
        # Initialize the update button if it does not exist
        if not hasattr(self, 'update_button') or self.update_button is None:
            self.update_button = QPushButton('Update Now', self)
            self.update_button.setStyleSheet("""
                font-size: 14px; 
                padding: 10px; 
                background-color: #FF5722; 
                color: white; 
                border-radius: 5px;
                border: none;
            """)
            self.update_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.update_button.clicked.connect(self.update_clicked)
            
            # Add button to the layout
            self.layout.addWidget(self.update_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.update_button.setVisible(True)
    
        self.timestamp_file_path = "I:\\test\\block\\timestamp.txt"

    def get_last_modified_time(self, file_path):
        """Get the last modified time of the file."""
        try:
            return os.path.getmtime(file_path)
        except FileNotFoundError:
            return None
    def get_ip_address(self):
            try:
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                return ip_address
            except Exception as e:
                print(f"Failed to get IP address: {e}")
                return "Unknown IP"
    
    def update_timestamp_file(self, file_path):
        """Update the timestamp file with the current time."""
        with open(self.timestamp_file_path, 'w') as timestamp_file:
            timestamp_file.write(str(os.path.getmtime(file_path)))

    def read_last_timestamp(self):
        """Read the last known timestamp from the timestamp file."""
        if os.path.exists(self.timestamp_file_path):
            with open(self.timestamp_file_path, 'r') as timestamp_file:
                return float(timestamp_file.read().strip())
        return None



    def block_websites_for_computer(self, computer_name):
        url = "http://10.10.15.94:3000/blocked_websites"
        data = {'computer_name': computer_name}

        try:
            response = requests.post(url, data=data)
            logging.info(f"Your computername is: {data}")
            print(f"Your computername is: {data}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            logging.info(f"Response Status Code: {response.status_code}")
            logging.info(f"Response Text: {response.text}")

            if response.status_code == 200:
                result = response.json()
                print(result.get("message", "Success"))
                logging.info(result.get("message", "Success"))

                # Define file paths
                original_file_path = rf"\\10.10.10.11\Departments\test\block\{computer_name}.txt"
                new_folder_path = os.path.join(os.getenv('LOCALAPPDATA'), 'MKS Support Center', 'block')
                new_file_path = os.path.join(new_folder_path, f"{computer_name}.txt")
                hosts_file_path = r"C:\Windows\System32\drivers\etc\hosts"
                logging.info(original_file_path)
                logging.info(new_folder_path)
                logging.info(new_file_path)
                logging.info(hosts_file_path)
                # Check accessibility of hosts file
                if not self.is_accessible(hosts_file_path):
                    print(f"Hosts file {hosts_file_path} is not accessible.")
                    logging.error(f"Hosts file {hosts_file_path} is not accessible.")
                    return

                # Create the new directory if it does not exist
                if not os.path.exists(new_folder_path):
                    try:
                        os.makedirs(new_folder_path)
                        print(f"Created directory: {new_folder_path}")
                        logging.info(f"Created directory: {new_folder_path}")
                    except IOError as e:
                        print(f"Error creating directory {new_folder_path}: {e}")
                        logging.error(f"Error creating directory {new_folder_path}: {e}")
                        return

                # Check if the original file exists before copying
                if os.path.exists(original_file_path):
                    try:
                        shutil.copy(original_file_path, new_file_path)
                        print(f"File copied to {new_file_path}")
                        logging.info(f"File copied to {new_file_path}")
                    except IOError as e:
                        print(f"Error copying file {original_file_path} to {new_file_path}: {e}")
                        logging.error(f"Error copying file {original_file_path} to {new_file_path}: {e}")
                        return
                else:
                    print(f"File {original_file_path} does not exist.")
                    logging.error(f"File {original_file_path} does not exist.")
                    return

                # Process the copied file
                existing_lines = self.read_hosts_file(hosts_file_path)
                blocked_domains = set(line.split()[1] for line in existing_lines if line.startswith('127.0.0.1 '))

                if os.path.exists(new_file_path):
                    print(f"Reading from file: {new_file_path}")
                    logging.debug(f"Reading from file: {new_file_path}")
                    try:
                        with open(new_file_path, 'r') as file:
                            websites = file.readlines()

                        print(f"Websites found in file: {websites}")
                        logging.debug(f"Websites found in file: {websites}")

                        if websites:
                            new_lines = [f"127.0.0.1 {website.strip()}\n" for website in websites if website.strip() not in blocked_domains]
                            if new_lines:
                                self.write_hosts_file(hosts_file_path, existing_lines + new_lines)
                                print(f"Blocked domains: {', '.join(website.strip() for website in websites)}")
                                logging.info(f"Blocked domains: {', '.join(website.strip() for website in websites)}")
                        else:
                            new_lines = [line for line in existing_lines if not line.startswith('127.0.0.1 ')]
                            self.write_hosts_file(hosts_file_path, new_lines)
                            print("All previously blocked domains have been removed.")
                            logging.info("All previously blocked domains have been removed.")

                        self.update_timestamp_file(new_file_path)

                    except IOError as e:
                        print(f"Error reading file {new_file_path}: {e}")
                        logging.error(f"Error reading file {new_file_path}: {e}")

                else:
                    new_lines = [line for line in existing_lines if not line.startswith('127.0.0.1 ')]
                    self.write_hosts_file(hosts_file_path, new_lines)
                    print("All previously blocked domains have been removed. (File not found)")
                    logging.info("All previously blocked domains have been removed. (File not found)")

            else:
                result = response.json()
                print(f"Failed to get blocked websites. Error: {result.get('error', 'Unknown error')}")
                logging.error(f"Failed to get blocked websites. Error: {result.get('error', 'Unknown error')}")

        except requests.RequestException as e:
            print(f"Error contacting server: {e}")
            logging.error(f"Error contacting server: {e}")

    def is_accessible(self, file_path):
        """Check if a file is accessible."""
        return os.access(file_path, os.R_OK | os.W_OK)

    def read_hosts_file(self, hosts_file_path):
        """Read the contents of the hosts file."""
        with open(hosts_file_path, 'r') as file:
            return file.readlines()

    def write_hosts_file(self, hosts_file_path, lines):
        """Write lines to the hosts file."""
        with open(hosts_file_path, 'w') as file:
            file.writelines(lines)

    def update_timestamp_file(self, file_path):
        from time import datetime
        """Update a timestamp file after changes."""
        timestamp_file_path = file_path + '.timestamp'
        with open(timestamp_file_path, 'w') as file:
            file.write('Updated at: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


    def is_accessible(self, path):
        """Check if the file or directory at the given path is accessible."""
        try:
            if os.path.exists(path):
                if os.path.isfile(path):
                    with open(path, 'r'):
                        pass
                elif os.path.isdir(path):
                    return True
                return True
        except IOError as e:
            print(f"IOError while checking access for {path}: {e}")
            logging.error(f"IOError while checking access for {path}: {e}")
        return False

    def update_timestamp_file(self, file_path):
        timestamp_file_path = f"{file_path}.timestamp"
        if self.is_accessible(file_path):
            try:
                with open(timestamp_file_path, 'w') as timestamp_file:
                    timestamp_file.write(f"Timestamp: {pd.Timestamp.now()}")
                print(f"Timestamp file updated: {timestamp_file_path}")
                logging.info(f"Timestamp file updated: {timestamp_file_path}")
            except IOError as e:
                print(f"Error updating timestamp file: {e}")
                logging.error(f"Error updating timestamp file: {e}")
        else:
            print(f"File path {file_path} is not accessible for timestamp update.")
            logging.error(f"File path {file_path} is not accessible for timestamp update.")

    def update_hosts_file(self, computer_name):
        file_path = r"\\10.10.10.11\Departments\test\block\{}".format(f"{computer_name}.txt")
        hosts_file_path = r"C:\Windows\System32\drivers\etc\hosts"

        if not self.is_accessible(file_path):
            print(f"File {file_path} is not accessible.")
            logging.error(f"File {file_path} is not accessible.")
            return

        if not self.is_accessible(hosts_file_path):
            print(f"Hosts file {hosts_file_path} is not accessible.")
            logging.error(f"Hosts file {hosts_file_path} is not accessible.")
            return

        existing_lines = self.read_hosts_file(hosts_file_path)
        blocked_domains = set(line.split()[1] for line in existing_lines if line.startswith('127.0.0.1 '))

        try:
            with open(file_path, 'r') as file:
                websites = file.readlines()

            new_lines = [f"127.0.0.1 {website.strip()}\n" for website in websites if website.strip() not in blocked_domains]
            if new_lines:
                self.write_hosts_file(hosts_file_path, existing_lines + new_lines)
                print(f"Blocked domains: {', '.join(website.strip() for website in websites)}")

        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            logging.error(f"Error reading file {file_path}: {e}")

    def read_hosts_file(self, hosts_file_path):
        try:
            with open(hosts_file_path, 'r') as file:
                return file.readlines()
        except IOError as e:
            print(f"Error reading hosts file {hosts_file_path}: {e}")
            logging.error(f"Error reading hosts file {hosts_file_path}: {e}")
            return []

    def write_hosts_file(self, hosts_file_path, lines):
        try:
            with open(hosts_file_path, 'w') as file:
                file.writelines(lines)
        except IOError as e:
            print(f"Error writing to hosts file {hosts_file_path}: {e}")
            logging.error(f"Error writing to hosts file {hosts_file_path}: {e}")


    def load_blocked_websites(self):
        blocked_websites = self.read_blocked_websites()
        self.blocked_websites_table.setRowCount(len(blocked_websites))
        self.blocked_websites_table.setColumnCount(2)
        self.blocked_websites_table.setHorizontalHeaderLabels(['Website', 'Unblock'])

        for i, website in enumerate(blocked_websites):
            website_item = QTableWidgetItem(website)
            unblock_button = QPushButton('Unblock')
            unblock_button.clicked.connect(lambda _, w=website: self.unblock_website(w))
            self.blocked_websites_table.setItem(i, 0, website_item)
            self.blocked_websites_table.setCellWidget(i, 1, unblock_button)

    def read_blocked_websites(self):
        blocked_websites_file_path = r'C:\Program Files (x86)\MKS Support Center\blocked_websites.txt'
        if os.path.exists(blocked_websites_file_path):
            with open(blocked_websites_file_path, 'r') as file:
                return file.read().splitlines()
        return []
    def read_hosts_file(self, hosts_file_path):
        with open(hosts_file_path, 'r') as file:
            return file.readlines()

    def write_hosts_file(self, hosts_file_path, lines):
        with open(hosts_file_path, 'w') as file:
            file.writelines(lines)
    def unblock_website(self, website):
        blocked_websites_file_path = r'C:\Program Files (x86)\MKS Support Center\blocked_websites.txt'
        with open(blocked_websites_file_path, 'r') as file:
            lines = file.readlines()
        with open(blocked_websites_file_path, 'w') as file:
            for line in lines:
                if line.strip() != website:
                    file.write(line)
        self.load_blocked_websites()

    def unblock_selected_websites(self):
        selected_rows = set(index.row() for index in self.blocked_websites_table.selectedIndexes())
        for row in selected_rows:
            website_item = self.blocked_websites_table.item(row, 0)
            if website_item:
                website = website_item.text()
                self.unblock_website(website)

def block_websites(file_path):
    """Block websites listed in the given file."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        logging.warning(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as file:
        ip_addresses = file.readlines()

    for ip in ip_addresses:
        ip = ip.strip()
        if ip:
            # Create firewall rule to block the IP address
            command = f"netsh advfirewall firewall add rule name=\"Block {ip}\" dir=out action=block remoteip={ip}"
            print(f"Blocking IP: {ip}")
            logging.info(f"Blocking IP: {ip}")
            subprocess.run(command, shell=True)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None, send_status_callback=None):
        super().__init__(icon, parent)
        self.parent = parent
        self.send_computer_status = send_status_callback
        self.setToolTip('MKS Support Center')

        menu = QMenu(parent)
        open_action = QAction("เปิดโปรแกรม", self)
        open_action.triggered.connect(self.show_main_window)
        quit_action = QAction("ออกจากโปรแกรม", self)
        quit_action.triggered.connect(self.quit_application)

        menu.addAction(open_action)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

        # Connect the double-click event to show the main window
        self.activated.connect(self.on_icon_activated)

    def show_main_window(self):
        if self.parent:
            self.parent.show()
            self.parent.activateWindow()  # Bring the main window to the front
            print("Main window should be visible now")  # Debug statement

    def quit_application(self):
        if self.parent:
            # Optionally send a status update
            if self.send_computer_status:
                self.send_computer_status(socket.gethostname(), 'Disconnected')  # Send "Disconnected" status

            # Optionally stop any server thread or background tasks
            if hasattr(self.parent, 'server_thread') and self.parent.server_thread:
                self.send_computer_status(socket.gethostname(), 'Disconnected')
                self.parent.server_thread.stop()
                        
            # Close the application
            sys.exit(1)
            QApplication.quit()

    def on_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_main_window()


def show_warning_message(parent):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle('กำลังเปิดโปรแกรม')
    msg_box.setText('กำลังเปิดโปรแกรม.')
    
    # Set up a QTimer to close the message box after 3 seconds
    QTimer.singleShot(3000, msg_box.close)
    
    msg_box.exec()



def is_installer_running():
    target_process_name = 'open_vnc_installer_master.exe'.lower()
    
    for process in psutil.process_iter(['name', 'pid']):
        try:
            if process.info['name'].lower() == target_process_name:
                print(f"Found {target_process_name} running with PID: {process.info['pid']}")
                logging.info(f"Found {target_process_name} running with PID: {process.info['pid']}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
            
    return False

def is_application_running(window_title):
    """
    Check if there is a window with the given title.
    """
    def enum_windows_callback(hwnd, titles):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            title = ctypes.create_string_buffer(256)
            ctypes.windll.user32.GetWindowTextA(hwnd, title, 256)
            titles.append(title.value.decode('utf-8'))
    
    titles = []
    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(enum_windows_callback), ctypes.pointer(titles))
    
    for title in titles:
        if window_title.lower() in title.lower():
            print(f"Found window with title: {title}")
            logging.info(f"Found window with title: {title}")
            return True
    
    return False

def run_installer():
    # Your code to start the installer goes here
    print("Starting installer...")
    # Example to start the installer
    # subprocess.Popen(['path_to_installer.exe'])

def handle_signal(signal, frame):
    """Handle signals to send 'Offline' status before exiting."""
    print("Signal received, sending offline status.")
    logging.info("Signal received, sending offline status.")
    if hasattr(main_window, 'send_computer_status'):
        main_window.send_computer_status(socket.gethostname(), 'Offline')
    sys.exit(0)

def main():

    semaphore_name = 'my_unique_semaphore_key'
    shared_memory_key = 'my_shared_memory_key'

    # Create shared memory and semaphore
    shared_memory = QSharedMemory(shared_memory_key)
    semaphore = QSystemSemaphore(semaphore_name, 1)

    # Try to attach to existing shared memory
    if shared_memory.attach():
        print("Another instance is already running.")
        logging.warning("Another instance detected.")
        url = "http://10.10.15.94:3000"
        webbrowser.open(url)
        sys.exit()

    # Create the shared memory
    shared_memory.create(1)

    # Try to acquire the semaphore
    semaphore.acquire()
    try:
        # Log the current working directory
        logging.info(f"Current working directory: {os.getcwd()}")
        print(f"Current working directory: {os.getcwd()}")

        # Register signal handlers for termination signals
        signal.signal(signal.SIGTERM, handle_signal)
        signal.signal(signal.SIGINT, handle_signal)

        # Create and initialize the application
        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        # Load icon image
        icon_path = os.path.join(os.getenv('LOCALAPPDATA'), 'MKS Support Center', 'logo2.ico')
        if not os.path.isfile(icon_path):
            print(f"Icon file not found at {icon_path}.")
            logging.error(f"Icon file not found at {icon_path}.")
            pass

        # Create the main window but do not show it immediately
        global main_window
        main_window = MainWindow()
        main_window.setWindowIcon(QIcon(icon_path))

        # Create and show system tray icon
        tray_icon = SystemTrayIcon(QIcon(icon_path), main_window)
        tray_icon.show()

        # Start the application event loop
        sys.exit(app.exec())
    finally:
        # Release the semaphore and detach the shared memory
        semaphore.release()
        shared_memory.detach()


if __name__ == '__main__':
    main()

