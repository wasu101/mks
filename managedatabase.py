import sys //sys ตัวนี้มันเป็น library ที่จัดเตรียมฟังก์ชันและตัวแปรที่ใช้เพื่อจัดการกับส่วนต่างๆของ Python Runtime Environment เอาไว้ ช่วยให้เราเข้าถึงพารามิเตอร์และฟังก์ชันเฉพาะของระบบได้ง่าย
import os //คือคำสั่งนำเข้า module OS มาในโค้ดภาษา Python เพื่อทำงานกับระบบปฏิบัติ หรือ operating system
from PyQt5.QtCore import QUrl // คือคำสั่ง นำเข้า Module PyQt5 เพื่อแสดง UI ต่างๆ ในโปรแกรม
from PyQt5.QtGui import QFont // คือคำสั่ง นำเข้า Module PyQt5 เพื่อแสดง UI ต่างๆ ในโปรแกรม
from PyQt5.QtCore import Qt,QLibraryInfo // คือคำสั่ง นำเข้า Module PyQt5 เพื่อแสดง UI ต่างๆ ในโปรแกรม
from PyQt5.QtWebEngineWidgets import QWebEngineView  // คือคำสั่ง นำเข้า Module PyQt5 เพื่อแสดง UI ต่างๆ ในโปรแกรม
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QDialog, QLineEdit, QMessageBox, QHBoxLayout,QGraphicsOpacityEffect, QWidget,QProgressBar,QGridLayout // คือคำสั่ง นำเข้า Module PyQt5 เพื่อแสดง UI ต่างๆ ในโปรแกรม
from PyQt5.QtCore import Qt, QTimer,QSize // คือคำสั่ง นำเข้า Module PyQt5 เพื่อแสดง UI ต่างๆ ในโปรแกรม
from PyQt5.QtGui import QPixmap, QImage, QFont,QMovie // คือคำสั่ง นำเข้า Module PyQt5 เพื่อแสดง UI ต่างๆ ในโปรแกรม
import face_recognition // คือคำสั่งนำเข้า Module จดจำใบหน้า เป็น AI เพื่อใช้ตรวจสอบว่าเป็นใบหน้าของ คนไหม 
import cv2 //เป็น Module ที่เอาไว้ จัดการรูปภาพและกล้อง
import dlib //เป็น Module การตรวจจับใบหน้าด้วยไลบรารี่ Dlib (โดย Davis King) ซึ่งเป็น machine learning
from datetime import datetime // เป็นคำสั่งนำเข้า Module เวลา
import gspread //  เป็นคำสั่งนำเข้า Module ที่ใช้จัดการ Sheets ของ google
from oauth2client.service_account import ServiceAccountCredentials //  เป็นคำสั่งนำเข้า Module ที่ใช้จัดการ Account ของ google เพื่อเข้าไปทำอะไรสักอย่างตามคำสั่งที่เขียนใน โปรแกรม
import os.path //คือคำสั่งนำเข้า module OS มาในโค้ดภาษา Python เพื่อทำงานกับระบบปฏิบัติ หรือ operating system

from google.auth.transport.requests import Request //  เป็นคำสั่งนำเข้า Module ที่ใช้จัดการ Account ของ google เพื่อเข้าไปทำอะไรสักอย่างตามคำสั่งที่เขียนใน โปรแกรม

from google.oauth2.credentials import Credentials //  เป็นคำสั่งนำเข้า Module ที่ใช้จัดการ Account ของ google เพื่อเข้าไปทำอะไรสักอย่างตามคำสั่งที่เขียนใน โปรแกรม

from google_auth_oauthlib.flow import InstalledAppFlow //  เป็นคำสั่งนำเข้า Module ที่ใช้จัดการ Account ของ google เพื่อเข้าไปทำอะไรสักอย่างตามคำสั่งที่เขียนใน โปรแกรม

from googleapiclient.discovery import build //  เป็นคำสั่งนำเข้า Module ที่ใช้จัดการ Account ของ google เพื่อเข้าไปทำอะไรสักอย่างตามคำสั่งที่เขียนใน โปรแกรม

from googleapiclient.errors import HttpError //  เป็นคำสั่งนำเข้า Module ที่ใช้จัดการ Account ของ google เพื่อเข้าไปทำอะไรสักอย่างตามคำสั่งที่เขียนใน โปรแกรม

from google.oauth2 import service_account //  เป็นคำสั่งนำเข้า Module ที่ใช้จัดการ Account ของ google เพื่อเข้าไปทำอะไรสักอย่างตามคำสั่งที่เขียนใน โปรแกรม

import webbrowser //เป็นคำสั่งนำเข้า Module เพื่อเข้าถึง webbrowser
import qrcode //เป็นคำสั่งนำเข้า Module เพื่อสร้าง QRcode
from io import BytesIO //Stream คือ ทางไหลของ byte ข้อมูล (data ที่มีค่าเป็นไปได้ -128 ถึง 127 : primitive data type) หลายๆ ก้อนต่อกัน จากจุดหนึงไปสู่อีกจุดหนึ่ง
import subprocess // เป็น Module ที่ไว้ใช้เรียกคำสั่งเพิ่มจาก ตัวโปรแกรมที่ใช้ได้แค่ครั้ง ละ 1
from face_recognition import face_locations // เป็น Module ที่ไว้ใช้ตรวจจับตำแหน่งของใบหน้า
import time // เป็น Module นำเข้า เวลา
import atexit //library ที่ช่วยให้ Raspberry Pi กลายเป็น Web Server
import socket // โปรแกรม เชื่อมต่อระหว่าง server กับ client

def restart_program():
    try:
        subprocess.Popen([sys.executable, sys.argv[0]])
    except Exception as e:
        print("Error restarting program:", e)

def on_program_exit():
    restart_program()

# ลงทะเบียนฟังก์ชั่น on_program_exit() เพื่อให้ทำงานเมื่อโปรแกรมจบการทำงาน
atexit.register(on_program_exit)


    

os.environ["QT_QPA_PLATFORM"] = "eglfs"
#os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)
GPIO.setwarnings(False)
GPIO.cleanup()
relay_pin1 = 23 # กำหนดขา GPIO ที่ใช้งาน
relay_pin2 = 24 # กำหนดขา GPIO ที่ใช้งาน
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin1, GPIO.OUT)
GPIO.setup(relay_pin2, GPIO.OUT)
GPIO.output(relay_pin1, GPIO.LOW)
GPIO.output(relay_pin2, GPIO.LOW)

class QRCodeWindow(QDialog): #สร้าง QR Code เพื่อลงทะเบียนใน Google from
    def __init__(self):
        super().__init__()
        self.main_window = Main
        self.setWindowTitle("QR Code")
        self.showFullScreen()
        self.setFixedSize(720, 1280)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
    
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # กำหนดให้ส่วนหน้าต่างภายใน QVBoxLayout อยู่ตรงกลาง

        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.update_qr_code()
        layout.addWidget(self.qr_label, alignment=Qt.AlignCenter)  # กำหนดให้ QLabel อยู่ตรงกลางของ QVBoxLayout
        
        # เพิ่ม QLabel เพื่อแสดงข้อความ
        self.instruction_label = QLabel("Scan QR Code and Follow the Instructions.\nAfter completion, press the Next button.")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction_label)
        self.instruction_label.setFont(QFont("Thonburi", 12))  # กำหนดขนาดและรูปแบบตัวอักษร

        # สร้าง QHBoxLayout เพื่อจัดวางปุ่ม Next และ Back
        button_layout = QHBoxLayout()
        
        # เพิ่มปุ่ม Back
        self.back_button = QPushButton("Close")
        self.back_button.clicked.connect(self.close_application)
        self.back_button.setFont(QFont("Thonburi", 18))
        button_layout.addWidget(self.back_button)
        self.back_button.setToolTip("Click here to close program")

        # เพิ่มปุ่ม Next
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.go_to_login_window)
        self.next_button.setFont(QFont("Thonburi", 18)) 
        button_layout.addWidget(self.next_button)
        self.next_button.setToolTip("Click here to next step")

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.move_to_center()

    def move_to_center(self):
        # หาขนาดของหน้าจอ
        screen_geometry = QApplication.desktop().screenGeometry()

        # หาขนาดของหน้าต่าง
        window_geometry = self.frameGeometry()

        # คำนวณตำแหน่ง X และ Y ของหน้าต่าง
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # กำหนดตำแหน่งใหม่ให้กับหน้าต่าง
        self.move(x, y)

    def update_qr_code(self):
        qr_link = "https://docs.google.com/forms/d/174tO6HaUYInJJFME0YWUjMhtrGTue8pn3P5VZV7m2FY/edit?usp=drivesdk"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_byte_array = BytesIO()
        img.save(img_byte_array, format='PNG')
        pixmap = QPixmap()
        pixmap.loadFromData(img_byte_array.getvalue())
        
        # ปรับขนาด QR code เป็น 200x200 พิกเซล
        scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio)
        self.qr_label.setPixmap(scaled_pixmap)

        # ปรับขนาดของ QLabel เพื่อให้พอดีกับขนาดของ QR code
        self.qr_label.setFixedSize(500, 500)
    
    def close_application(self):
        loading_window = LoadingWindow()   
        loading_window.raise_()
        loading_window.show()

        loading_window.close()
        self.close()
        #self.main_window = Main()  # สร้างออบเจกต์ Main
        #self.main_window.show()  # เรียกเมธอด show() เพื่อแสดงวิดเจ็ต

    def go_to_login_window(self):

        loading_window = LoadingWindow()
        loading_window.show()

        loading_window.close()
    # Close current window and open login window
        self.close()
        login_window = LoginWindow()
        login_window.exec_()

class VirtualKeyboard(QWidget):
    def __init__(self, username_entry, password_entry):
        super().__init__()
        self.username_entry = username_entry
        self.password_entry = password_entry
        self.current_target = self.username_entry  # เริ่มต้นให้เป็นช่อง username

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Virtual Keyboard")
        grid_layout = QGridLayout()
        keys =[ 
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Clear',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', '','Username','Password'
        ]
        positions = [(i, j) for i in range(3) for j in range(10)]
        for position, key in zip(positions, keys):
            row, col = position
            button = QPushButton(key)
            if key in ['Username', 'Password','Clear']:
                button.setFixedSize(60, 60)  # ปรับขนาดของปุ่ม Username และ Password เป็น 55x55 พิกเซล
                button.setFont(QFont("Arial", 14))  # ตั้งค่าขนาดตัวอักษรเป็น 14 พิกเซล
            else:
                button.setFixedSize(60, 60)  # ปรับขนาดของปุ่มอื่นเป็น 50x50 พิกเซล
            button.clicked.connect(lambda _, t=key: self.key_pressed(t))
            grid_layout.addWidget(button, row, col)

        self.setLayout(grid_layout)

    def key_pressed(self, key):
            if key == 'Clear':
                self.current_target.clear()
            elif key == 'Username':
                 # สลับการป้อนข้อมูลระหว่างช่อง username และ password
                if self.current_target == self.username_entry:
                    self.current_target = self.username_entry
                else:
                    self.current_target = self.username_entry
            elif key == 'Space':
                self.current_target.insert(' ')
            elif key == 'Password':
                # สลับการป้อนข้อมูลระหว่างช่อง username และ password
                if self.current_target == self.password_entry:
                    self.current_target = self.password_entry
                else:
                    self.current_target = self.password_entry
            else:
                self.current_target.insert(key)

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.login_attempts = 0
        self.setWindowTitle("Login")
        self.setFixedSize(720, 1280)
        self.showFullScreen()
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel("Admin User Login", self)
        self.text_label.setFont(QFont("Thonburi", 25))
        layout.addWidget(self.text_label, alignment=Qt.AlignCenter)

        self.username_label = QLabel("Username:", self)
        self.username_label.setFont(QFont("Thonburi", 15))
        layout.addWidget(self.username_label, alignment=Qt.AlignCenter)

        self.username_entry = QLineEdit(self)
        self.username_entry.setFont(QFont("Thonburi", 15))
        self.username_entry.setFixedWidth(300)  # ปรับขนาดความกว้างของช่องใส่ข้อความ
        layout.addWidget(self.username_entry, alignment=Qt.AlignCenter)

        self.password_label = QLabel("Password:", self)
        self.password_label.setFont(QFont("Thonburi", 15))
        layout.addWidget(self.password_label, alignment=Qt.AlignCenter)

        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setFont(QFont("Thonburi", 15))
        self.password_entry.setFixedWidth(300)  # ปรับขนาดความกว้างของช่องใส่ข้อความ
        layout.addWidget(self.password_entry, alignment=Qt.AlignCenter)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        self.login_button.setFont(QFont("Thonburi", 15))
        self.login_button.setFixedWidth(150)  # ปรับขนาดความกว้างของปุ่ม
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        self.virtual_keyboard = VirtualKeyboard(self.username_entry, self.password_entry)
        layout.addWidget(self.virtual_keyboard)  # เพิ่ม VirtualKeyboard เข้าไปใน layout

        self.setLayout(layout)

    def login(self):
        entered_username = self.username_entry.text()
        entered_password = self.password_entry.text()

        if entered_username == "ROOT" and entered_password == "ADMIN":
            loading_window = LoadingWindow()
            loading_window.show()
                                        # Simulate loading progress (0% to 100%)
            for progress in range(101):
                loading_window.set_progress(progress)
                QApplication.processEvents()  # Update the GUI to show the progress
                time.sleep(0.05)  # Simulate some processing time            
            self.close()
            self.main_window = MainWindow() # หน้าต่างลงทะเบียน
            self.main_window.show()
            self.main_window.raise_()
            loading_window.raise_()
            loading_window.close()
        else:
            self.login_attempts += 1
            attempts_left = 3 - self.login_attempts
            if attempts_left <= 0:
                error_message = QMessageBox(self)
                error_message.setFixedSize(600, 200)  # ปรับขนาดของ QMessageBox
                #error_message.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
                error_message.setWindowTitle("Login Failed")
                error_message.setText("Login Failed \nYou have exceeded the maximum number of login attempts.")
                #error_message.setStyleSheet("QMessageBox { border: 1px solid black; }")  
                error_message.exec_()
                # Close the current dialog and open the main window again
                self.close()

            else:
                error_message = QMessageBox(self)
                #error_message.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
                error_message.setFixedSize(600, 200)  # ปรับขนาดของ QMessageBox
                error_message.setWindowTitle("Login Failed")
                error_message.setText(f"Invalid username or password. Please try again. {attempts_left} attempts left.")
                #error_message.setStyleSheet("QMessageBox { border: 1px solid black; }")  
                error_message.exec_()
           

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        # Initialize UI components and setup camera
        self.init_ui()
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.update_camera()
        self.setWindowTitle("Capture Image")
        self.setFixedSize(720, 1280)
        self.showFullScreen()
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint) 

    def init_ui(self):
        # Initialize UI components
        self.setWindowTitle("Capture_Image")
        #self.setFixedSize(720, 480)
        self.showFullScreen()
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint) 

        self.label = QLabel("Enter your ID:", self)
        self.label.setGeometry(280, 20, 200, 60)
        self.label.setFont(QFont("Thonburi",15))

        self.entry = QLineEdit(self)
        self.entry.setGeometry(110, 80, 500, 60)
        self.entry.setFont(QFont("Thonburi",30))

        self.camera_label = QLabel(self)
        self.camera_label.setGeometry(110, 160, 500,500)
        self.camera_label.setStyleSheet("border: 2px solid black;")

        self.capture_button = QPushButton("Save", self)
        self.capture_button.setGeometry(220, 970, 90, 90)
        self.capture_button.setFont(QFont("Thonburi",25))
        self.capture_button.clicked.connect(self.capture_image)
        
        self.cancel_button = QPushButton("Cancel", self)  # เพิ่มปุ่ม Cancel
        self.cancel_button.setGeometry(220, 1070, 290, 50)  # กำหนดตำแหน่งและขนาดของปุ่ม Cancel
        self.cancel_button.setFont(QFont("Thonburi",20))  # กำหนดขนาดตัวอักษรสำหรับปุ่ม Cancel
        self.cancel_button.clicked.connect(self.cancel_capture)  # เชื่อมต่อฟังก์ชัน cancel_capture กับปุ่ม Cancel

        # Create numeric buttons
        numeric_buttons = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [None, 0, "Delete"]  # ใช้ None แทนเว้นวรรคและใส่ชื่อปุ่ม Delete
        ]

        x_position = 220
        y_position = 670
        for row in numeric_buttons:
            for digit in row:
                if digit is not None:
                    button_text = str(digit) if digit != "Delete" else "Del"
                    button = QPushButton(button_text, self)
                    button.setGeometry(x_position, y_position, 90, 90)
                    button.setFont(QFont("Thonburi",25))
                    if digit != "Delete":
                        button.clicked.connect(lambda _, d=digit: self.add_digit(d))
                    else:
                        button.clicked.connect(self.delete_digit)
                x_position += 100
            x_position = 220
            y_position += 100

    def add_digit(self, digit):
        current_text = self.entry.text()
        self.entry.setText(current_text + str(digit))

    def delete_digit(self):
        current_text = self.entry.text()
        self.entry.setText(current_text[:-1])

    def update_camera(self):
        # Update camera feed
        ret, frame = self.cap.read()
        if ret:
            # Detect faces in the frame
            faces = self.detector(frame, 1)
            if faces is not None:
                # Draw rectangles around the faces
                for face in faces:
                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Convert frame to RGB for displaying in Qt
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)

            # Display the camera feed
            pixmap_resized = pixmap.scaled(500, 500, Qt.KeepAspectRatio)
            self.camera_label.setPixmap(pixmap_resized)

        QTimer.singleShot(10, self.update_camera)

    def cancel_capture(self):
        # ฟังก์ชันสำหรับการยกเลิกการจับภาพ
        self.cap.release()  # ปิดการใช้งานกล้อง
        self.close()  # ปิดหน้าต่างการจับภาพ
              
    def capture_image(self):
        user_id = self.entry.text()
        _, frame = self.cap.read()

        folderA_path = '/home/project/Desktop/Project/image'
        try:
            if not os.path.exists(folderA_path):
                os.makedirs(folderA_path)

        # Check if user_id is empty or already exists
            if not user_id.strip():
                QMessageBox.critical(self, "Error", "Please enter a valid ID")
                return

            image_path = f'{folderA_path}/{user_id}.jpg'

            if os.path.exists(image_path):
                QMessageBox.critical(self, "Error", "This ID already exists. Please use a different one.")
                return

        # Check if there are faces in the frame
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) == 0:
                QMessageBox.critical(self, "Error", "No face detected in the image. Please try again.")
                return

            cv2.imwrite(image_path, frame)

            QMessageBox.information(self, "Success", f"Image saved as {image_path}")
            self.confirm_save_image()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.confirm_save_image()
            
    def confirm_save_image(self):
        # Ask user if they want to save the ID
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText("Do you want to save ID More?")
        confirm_dialog.setWindowTitle("Pleas wait..")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_dialog.setDefaultButton(QMessageBox.Yes)
        response = confirm_dialog.exec_()

        if response == QMessageBox.Yes:
            return MainWindow()
            self.entry.clear() 
        else:
            QMessageBox.information(self, "Info", "Redirecting to face scanning system")
            self.cap.release()
            self.close()  # ปิดหน้าต่างปัจจุบัน   
            scan_window = ScanWindow()  # สร้างอ็อบเจ็กต์ของ ScanWindow
            scan_window.raise_()  # แสดงหน้าต่าง ScanWindow
 

class ScanWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition")
        self.setFixedSize(720, 1280)
        self.showFullScreen()  
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint) 

        self.central_widget = QLabel(self)
        self.central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.central_widget)

        self.camera_label = QLabel(self)
        self.camera_label.setGeometry(50, 160, 600,600)

        self.timename_label = QLabel(self)
        self.timename_label.setGeometry(70, 30, 550, 60)
        self.timename_label.setAlignment(Qt.AlignCenter)
        self.timename_label.setFont(QFont("Thonburi", 20))
        self.timename_label.setStyleSheet("color: Black; font-weight: bold;")

        self.ipname_label = QLabel(self)
        self.ipname_label.setGeometry(1, 10, 550, 60)
        self.ipname_label.setFont(QFont("Thonburi", 7))
        self.ipname_label.setStyleSheet("color: Gray; font-weight: bold;")

        self.filename_label = QLabel(self)
        self.filename_label.setGeometry(90, 700, 550, 60)
        self.filename_label.setAlignment(Qt.AlignCenter)
        self.filename_label.setFont(QFont("Thonburi", 18))
        self.filename_label.setStyleSheet("font-weight: bold;")

        self.title_label = QLabel(self)
        self.title_label.setGeometry(90, 780, 550, 60)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Thonburi", 15))

        self.register_button = QPushButton("Register", self)
        self.register_button.setGeometry(110, 1030, 500, 60)
        self.register_button.setFont(QFont("Thonburi", 20))
        self.register_button.clicked.connect(self.register)

        self.cap = cv2.VideoCapture(0)
        self.known_faces_path = '/home/project/Desktop/Project/image'
        self.scanning_face = False
        self.face_recognizer = dlib.face_recognition_model_v1("/home/project/Desktop/Project/dlib_face_recognition_resnet_model_v1.dat")
        #self.landmark_predictor = dlib.shape_predictor("/home/project/Desktop/Project/shape_predictor_68_face_landmarks.dat")
        self.face_detector = dlib.get_frontal_face_detector()
        self.scan_and_open_door()
        self.update_camera_frame()
        self.update_time()          
    
    def get_ip_address(self):
        hostname = socket.gethostname()    
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def update_camera_frame(self):
        _, frame = self.cap.read()

        if frame is not None:
            # Get the dimensions of the frame
            height, width, _ = frame.shape

            # Calculate the center coordinates
            center_x = width // 2
            center_y = height // 2

            # Define the size of the fixed rectangle
            rect_width = int(width * 0.7)
            rect_height = int(height *0.7)

            # Define the coordinates of the top-left corner of the rectangle
            rect_top_left_x = int(center_x - rect_width //2)
            rect_top_left_y = int(center_y - rect_height * 0.5)

            # Draw the fixed rectangle on the frame
            cv2.rectangle(frame, (rect_top_left_x, rect_top_left_y), 
                        (rect_top_left_x + rect_width, rect_top_left_y + rect_height), 
                        (255, 0, 0), 2)

            # Extract the region of interest (ROI) within the fixed rectangle
            roi_frame = frame[rect_top_left_y:rect_top_left_y + rect_height, 
                            rect_top_left_x:rect_top_left_x + rect_width]

            # Detect faces within the ROI
            faces = self.face_detector(roi_frame, 1)

            for face in faces:
    # Get the coordinates and size of the rectangle
                x = face.left()
                y = face.top()
                w = face.right() - x
                h = face.bottom() - y
                
                # Adjust the coordinates to the original frame
                x += rect_top_left_x
                y += rect_top_left_y

                # Draw the rectangle around the face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                self.filename_label.setText("Searching for faces")
                self.title_label.setText("Please stay in the designated area.")
                QTimer.singleShot(1000, self.scan_and_open_door)

            # Convert the frame to RGB format
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            pixmap_resized = pixmap.scaled(600, 600, Qt.KeepAspectRatio)
            self.camera_label.setPixmap(pixmap_resized)

        # Schedule the next frame update
        QTimer.singleShot(10, self.update_camera_frame)

    def scan_and_open_door(self):
        #self.update_camera_frame                    
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        known_face_encodings = []
        known_face_names = []
        #self.filename_label.setText("Welcome To Faces Scan")
        #self.title_label.setText("Please Put your face in to the area")
        
        known_faces = []
        known_face_names = [] 
        
        if self.scanning_face:
            self.scanning_face = False
            return
        self.scanning_face = True  

        for file_name in os.listdir(self.known_faces_path):
            if file_name.endswith('.jpg'):
                name = os.path.splitext(file_name)[0]
                known_face_names.append(name)

                image_path = os.path.join(self.known_faces_path, file_name)
                face_image = face_recognition.load_image_file(image_path)

                face_encodings = face_recognition.face_encodings(face_image)

                if face_encodings:
                    face_encoding = face_encodings[0]
                    known_face_encodings.append(face_encoding)

        _, frame = self.cap.read()

        if frame is not None:
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            match_found = False
            match_image_path = None
            if len(face_locations) > 1:  # ตรวจสอบว่ามีใบหน้ามากกว่า 1 ในเฟรมหรือไม่
                self.filename_label.setText("Multiple faces detected.")
                print(f" {current_time} Multiple faces detected.")
                self.title_label.setText("Please ensure only one face is in the frame.")
                QTimer.singleShot(3000, self.scan_and_open_door)
            else:
                if len(face_locations) == 1:            

                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        threshold = 0.4  # ค่า threshold สำหรับการตรวจสอบความเท่ากันของใบหน้า
                # ตรวจสอบความเท่ากันของใบหน้าในภาพกับใบหน้าในฐานข้อมูล   
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        matches = list(face_distances <= threshold)

                        if True in matches:
                                first_match_index = matches.index(True)
                                name = known_face_names[first_match_index]
                                match_found = True
                                match_image_path = os.path.join(self.known_faces_path, f"{name}.jpg")
                    
                    # Calculate the confidence level (1 - face_distance) * 100
                                confidence_level = (1 - face_distances[first_match_index]) * 100
                                print(f" Image {name} confidence= {confidence_level:.2f}% ")
                    
                    # Check if confidence level is above 60% to open the door
                                if confidence_level >= 60:
                                    print(f"{name} Passed At {current_time} with {confidence_level:.2f}%")
                                    self.filename_label.setText((f"{name} Passed At {current_time} \nwith {confidence_level:.2f}%"))
                                    self.title_label.setText("Please Get in the gate")
                                    data_to_send = [name, current_time]
                                    self.send_to_google_sheets(data_to_send)
                                    self.close_camera()
                                    QTimer.singleShot(3000, self.open_camera)
                                else:
                                    print(f" {current_time} Not Passed")
                                    self.filename_label.setText(f" {confidence_level:.2f}% Not Found Your Face In Data")
                                    self.title_label.setText("Please Contact your admin For Register")
                    
                                if confidence_level >= 60:
                                    if match_image_path is not None:
                                        self.show_matched_image(match_image_path)
                        if not match_found:
                            print(f" {current_time} No matching face found.")
                            self.filename_label.setText("No matching face found.")
                            self.title_label.setText("Please try again or contact admin.")
                            QTimer.singleShot(2000, self.scan_and_open_door)
                elif len(face_locations) == 0:
                        self.filename_label.setText("Welcome To Faces Scan")
                        self.title_label.setText("Please Put your face in to the area")                           
            
        else:
            QTimer.singleShot(2000, self.scan_and_open_door)  # เรียก scan_and_open_door ใหม่หลังจาก 5 วินาที

    
    def close_camera(self):
        self.cap.release()
        GPIO.output(relay_pin1, GPIO.HIGH)
        GPIO.output(relay_pin2, GPIO.HIGH) 
        print("Turning off relay...")
        print("Camera closed.")

    def open_camera(self):
        self.cap.open(0)
        self.update_camera_frame()
        GPIO.output(relay_pin1, GPIO.LOW)
        GPIO.output(relay_pin2, GPIO.LOW) 
        print("Turning on relay...")
        print("Camera opened.")
        self.filename_label.setText("Welcome To Faces Scan")
        self.title_label.setText("Please Put your face in to the area")                           
            
        
    def send_to_google_sheets(self, data_to_send):
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets']
            credentials = service_account.Credentials.from_service_account_file('/home/project/Desktop/Project/uploadlog.json', scopes=scope)
            gc = gspread.authorize(credentials)
            spreadsheet_key = '1BBYFhgDdp6J1AKoD6zzRl_q8BCFpKfIPy2eJImnugFw'
            sheet = gc.open_by_key(spreadsheet_key).sheet1
            sheet.append_row(data_to_send)
            print(" Data sent to Google Sheets successfully.")
        except Exception as e:
            print(" Error sending data to Google Sheets:", e)
    
    def show_matched_image(self, image_path):
        match_window = QDialog(self)
        match_window.setWindowTitle("Welcome")
        match_window_layout = QVBoxLayout(match_window)
        
        match_image_pixmap = QPixmap(image_path)
        match_image_label = QLabel()
        match_image_label.setPixmap(match_image_pixmap.scaled(500, 500, Qt.KeepAspectRatio))
        match_window_layout.addWidget(match_image_label)

        QTimer.singleShot(3000, match_window.close)

        match_window.exec_()
    def get_rvnc_ip_address(self):
        command = "netstat -tn | grep :5900"  # เชื่อมต่อผ่านพอร์ต 5900 สำหรับ RealVNC
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        lines = stdout.decode().splitlines()
    
        for line in lines:
            if "ESTABLISHED" in line:  # หากการเชื่อมต่อถูกต้อง
                parts = line.split()
                address = parts[3]
                ip_address = address.split(":")[0]
                return ip_address
    
    def update_time(self):
        ip_address = self.get_rvnc_ip_address()    
        self.timename_label.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        QTimer.singleShot(1000, self.update_time)
        self.ipname_label.setText(f"IP Address:{ip_address}")

    def register(self):
        self.cap.release()
        loading_window = LoadingWindow()
        loading_window.show()

# Simulate loading progress (0% to 100%)
        for progress in range(101):
            loading_window.set_progress(progress)
            QApplication.processEvents()  # Update the GUI to show the progress
            time.sleep(0.05) 
        loading_window.raise_()
        loading_window.close()
        self.register_window = QRCodeWindow()
        self.register_window.show()
        self.close()

    def closeEvent(self, event):
        self.cap.release()
        GPIO.output(relay_pin1, GPIO.LOW)  # หยุดจ่ายไฟที่ขา GPIO
        GPIO.output(relay_pin2, GPIO.LOW)  # หยุดจ่ายไฟที่ขา GPIO
        super().closeEvent(event)         

class ConfirmationWindow(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmation")
        self.setFixedSize(720, 1280)
        self.showFullScreen()
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter) 

        message_label = QLabel(message, self)
        layout.addWidget(message_label)

        confirm_button = QPushButton("Confirm", self)
        confirm_button.clicked.connect(self.accept)
        layout.addWidget(confirm_button)
        confirm_button.setFont(QFont("Thonburi", 20))

        self.setLayout(layout)
        self.move_to_center()

    def move_to_center(self):
        # หาขนาดของหน้าจอ
        screen_geometry = QApplication.desktop().screenGeometry()

        # หาขนาดของหน้าต่าง
        window_geometry = self.frameGeometry()

        # คำนวณตำแหน่ง X และ Y ของหน้าต่าง
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # กำหนดตำแหน่งใหม่ให้กับหน้าต่าง
        self.move(x, y)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Main Menu")
        self.setFixedSize(720, 1280)
        self.showFullScreen()

        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.central_widget = QLabel(self)
        self.central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.central_widget)

        welcome_text = "Face Recognition Door"
        self.welcome_label = QLabel(welcome_text, self)
        welcome_font = QFont(self.welcome_label.font().family(), 40)
        self.welcome_label.setFont(welcome_font)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        instruction_text = "Please choose button below for the next step"
        self.instruction_label = QLabel(instruction_text, self)
        instruction_font = QFont(self.instruction_label.font().family(), 20)
        self.instruction_label.setFont(instruction_font)
        self.instruction_label.setAlignment(Qt.AlignCenter)

        self.register_button = QPushButton("Register", self)
        self.register_button.setFont(QFont(self.register_button.font().family(), 25))
        self.register_button.clicked.connect(self.register)

        self.main_menu_button = QPushButton("Main Menu", self)
        self.main_menu_button.setFont(QFont(self.main_menu_button.font().family(), 25))
        self.main_menu_button.clicked.connect(self.mainmenu)

        self.login_window = None

        self.resizeEvent(None)

        self.welcome_label.setGeometry(100, 150,550, 100)
        self.instruction_label.setGeometry(100, 280,550, 100)

        self.register_button.setGeometry(100,500,200,70)
        self.main_menu_button.setGeometry(400,500,200,70)
        self.move_to_center()

    def move_to_center(self):
        # หาขนาดของหน้าจอ
        screen_geometry = QApplication.desktop().screenGeometry()

        # หาขนาดของหน้าต่าง
        window_geometry = self.frameGeometry()

        # คำนวณตำแหน่ง X และ Y ของหน้าต่าง
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # กำหนดตำแหน่งใหม่ให้กับหน้าต่าง
        self.move(x, y)

    def mainmenu(self):
        

        confirmation_window = ConfirmationWindow("Are you sure you want to go to the Face Recognition?")
        confirmation_window.setFont(QFont("Thonburi", 20))

        if confirmation_window.exec_() == QDialog.Accepted:
             
            loading_window = LoadingWindow()
            loading_window.show()

# Simulate loading progress (0% to 100%)
            for progress in range(101):
                loading_window.set_progress(progress)
                QApplication.processEvents()  # Update the GUI to show the progress
                time.sleep(0.05)  # Simulate some processing time

             
            self.mainmenu = ScanWindow() 
            self.mainmenu.show()
            self.mainmenu.raise_()  
            loading_window.raise_()
            loading_window.close()   
            
    def register(self):


        confirmation_window = ConfirmationWindow("Are you sure you want to Register?")
        confirmation_window.setFont(QFont("Thonburi", 20))

        if confirmation_window.exec_() == QDialog.Accepted:
            loading_window = LoadingWindow()
            loading_window.show()

# Simulate loading progress (0% to 100%)
            for progress in range(101):
                loading_window.set_progress(progress)
                QApplication.processEvents()  # Update the GUI to show the progress
                time.sleep(0.05)  # Simulate some processing time

            loading_window.raise_()

            loading_window.close()
            qr_window = QRCodeWindow()
            qr_window.raise_()
            qr_window.exec_()

class LoadingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading...")
        self.setFixedSize(720, 1280)
        self.showFullScreen()

        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter) 

        # Load the GIF
        movie = QMovie("/home/project/Desktop/Project/loading.gif")
        movie.setScaledSize(QSize(100, 100))

        # Create and configure the QLabel for displaying the GIF
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)

        # Create and configure the QLabel for displaying the text
        self.loading_label = QLabel("Loading...\nPlease wait...", self)
        self.loading_label.setFont(QFont("Thonburi", 20))
        self.loading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loading_label)

        # Create a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setBaseSize(QSize(100, 100))
        self.progress_bar.setRange(0, 100)  # Set the range from 0 to 100%
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.move_to_center()

    def set_progress(self, value):
        self.progress_bar.setValue(value)

    def move_to_center(self):
        # หาขนาดของหน้าจอ
        screen_geometry = QApplication.desktop().screenGeometry()

        # หาขนาดของหน้าต่าง
        window_geometry = self.frameGeometry()

        # คำนวณตำแหน่ง X และ Y ของหน้าต่าง
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # กำหนดตำแหน่งใหม่ให้กับหน้าต่าง
        self.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loading_window = LoadingWindow()
    loading_window.show()

# Simulate loading progress (0% to 100%)
    for progress in range(101):
        loading_window.set_progress(progress)
        QApplication.processEvents()  # Update the GUI to show the progress
        time.sleep(0.05)  # Simulate some processing time

    loading_window.raise_()

    loading_window.close()
    login_window = Main()
    login_window.show()
    login_window.raise_()
    sys.exit(app.exec_())
