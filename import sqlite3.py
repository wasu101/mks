@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'current_user' not in session:
            return jsonify({"success": False, "error": "User not logged in"}), 401

        image_data = request.form.get('imageData')
        if not image_data:
            return jsonify({'success': False, 'error': 'Image data not found in request'}), 400

        # Decode base64 image data
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image_file = BytesIO(image_bytes)

        # Generate a unique filename
        filename = str(uuid.uuid4()) + '.png'
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the image file
        with open(image_path, 'wb') as f:
            f.write(image_file.getvalue())

        # Insert image data into the database
        conn = get_db_connection()
        ticket_id = request.form.get('ticket_id')
        message = request.form.get('message')
        current_user_id = session['current_user']
        current_user = conn.execute('SELECT * FROM users WHERE id = ?', (current_user_id,)).fetchone()

        if current_user is None:
            conn.close()
            return jsonify({"success": False, "error": "User not found"}), 404

        sender = current_user['username']
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        conn.execute(
            'INSERT INTO chat_messages (ticket_id, message, image_path, sender, timestamp) VALUES (?, ?, ?, ?, ?)',
            (ticket_id, message, image_path, sender, timestamp)
        )
        conn.commit()
        conn.close()

        image_url = f'/static/uploads/{filename}'
        return jsonify({'success': True, 'imageUrl': image_url}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    








       function sendChat(ticketId) {
        var textarea = document.getElementById('chat_' + ticketId);
        var message = textarea.value;
        var fileInput = document.getElementById('imageUpload_' + ticketId);
        var file = fileInput.files[0];
        const username = "{{ current_user.displayname }}";

        var formData = new FormData();
        formData.append('ticket_id', ticketId);
        formData.append('message', message);
        formData.append("sender", username);
        if (file) {
            formData.append('image', file);
        }

        fetch('/send_chat', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Failed to send message.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }


@app.route('/send_chat', methods=['POST'])
def send_chat():
    # ตรวจสอบว่ามีการล็อกอินอยู่หรือไม่
    if 'current_user' not in session:
        return jsonify({"success": False, "error": "User not logged in"}), 401

    # รับข้อมูลจากแบบฟอร์ม
    ticket_id = request.form.get('ticket_id')
    message = request.form.get('message')
    image = request.files.get('image')

    # ตรวจสอบว่ามีไฟล์รูปภาพถูกส่งมาหรือไม่
    if image:
        # บันทึกภาพลงในโฟลเดอร์ที่กำหนด
        filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
    else:
        image_path = None

    # ดึงข้อมูลผู้ใช้ปัจจุบันจากเซสชัน
    current_user_id = session['current_user']

    # ตรวจสอบว่าผู้ใช้ปัจจุบันมีอยู่ในฐานข้อมูลหรือไม่
    conn = get_db_connection()
    current_user = conn.execute('SELECT * FROM users WHERE id = ?', (current_user_id,)).fetchone()
    if current_user is None:
        conn.close()
        return jsonify({"success": False, "error": "User not found"}), 404

    # ใช้ข้อมูลจากผู้ใช้ปัจจุบันเพื่อเป็นผู้ส่งข้อความ
    sender = f"{current_user['displayname']} ({current_user['username']})"

    # เวลาปัจจุบัน
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    # แทรกข้อความแชทลงในฐานข้อมูล
    conn.execute(
        'INSERT INTO chat_messages (ticket_id, message, image_path, sender, timestamp) VALUES (?, ?, ?, ?, ?)',
        (ticket_id, message, image_path, sender, timestamp)
    )
    conn.commit()
    conn.close()

    return jsonify({'success': True})


@app.route('/delete_image', methods=['POST'])
def delete_image():
    data = request.json
    image_path = data.get('image_path')
    image_filename = image_path.split('/')[-1]  # ดึงชื่อไฟล์ภาพจากเส้นทางที่กำหนด

    if image_path:
        try:
            # ลบไฟล์ภาพในระบบไฟล์
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            
            # ลบรายการของภาพออกจากฐานข้อมูล
            conn = get_db_connection()
            conn.execute('DELETE FROM chat_messages WHERE image_path = ?', (image_path,))
            conn.commit()
            conn.close()
            flash(f"Delete Image {image_filename}", "error")
            return jsonify({'success': True}), 200
        except Exception as e:
            logging.error(f"Error deleting image: {e}")
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    else:
        return jsonify({'success': False, 'error': 'Missing image_path'}), 400