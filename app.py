import sqlite3
from flask import Flask, jsonify
import subprocess
import platform
from datetime import datetime

app = Flask(__name__)

# Function to create a database connection
def create_connection():
    try:
        conn = sqlite3.connect(r'D:\Flask\databaseExcel.db')  # Ensure the path is correct
        print("Connection successful")
        return conn
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def check_table_exists():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='computers';")
        table = cursor.fetchone()
        if table:
            print("Table 'computers' exists.")
        else:
            print("Table 'computers' does not exist.")
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

check_table_exists()

# Function to ping a computer
def ping_computer(computer_name):
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        result = subprocess.run(['ping', param, '1', computer_name], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                text=True)
        
        print("Ping command output:", result.stdout)
        
        if platform.system().lower() == 'windows':
            return 'Online' if 'Reply from' in result.stdout else 'Offline'
        
        return 'Online' if result.returncode == 0 else 'Offline'
    except Exception as e:
        print("Ping error:", e)
        return 'Offline'

@app.route('/update_all_computer_statuses', methods=['GET'])
def update_all_computer_statuses():
    conn = create_connection()
    if conn is None:
        return jsonify({'status': 'error', 'message': 'Failed to connect to the database'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, computer_name FROM computers")
        computers = cursor.fetchall()

        statuses = []
        for computer_id, computer_name in computers:
            status = ping_computer(computer_name)
            cursor.execute("UPDATE computers SET status = ?, last_ping_time = ? WHERE id = ?", 
                           (status, datetime.now().strftime('%Y-%m-%d %H:%M'), computer_id))
            conn.commit()
            statuses.append({'id': computer_id, 'status': status})

        return jsonify(statuses)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/get_computer_status/<int:computer_id>', methods=['GET'])
def get_computer_status(computer_id):
    conn = create_connection()
    if conn is None:
        return jsonify({'status': 'error', 'message': 'Failed to connect to the database'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT computer_name FROM computers WHERE id = ?", (computer_id,))
        computer = cursor.fetchone()

        if not computer:
            return jsonify({'status': 'error', 'message': 'Computer not found'}), 404

        computer_name = computer[0]
        status = ping_computer(computer_name)
        last_ping_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        cursor.execute("UPDATE computers SET status = ?, last_ping_time = ? WHERE id = ?", 
                       (status, last_ping_time, computer_id))
        conn.commit()

        return jsonify({
            'id': computer_id, 
            'status': status, 
            'last_ping_time': last_ping_time
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
