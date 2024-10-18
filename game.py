from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# สร้างแอปพลิเคชัน
app = Ursina()

# สร้างพื้นดิน
ground = Entity(
    model='plane',
    texture='grass_texture',  # เปลี่ยนเป็นเท็กซ์เจอร์หญ้าที่มีรายละเอียด
    collider='box',
    scale=(100, 1, 100)
)

# สร้างภูเขา
mountain = Entity(
    model='cube',
    texture='mountain_texture',  # เปลี่ยนเป็นเท็กซ์เจอร์ภูเขาที่มีรายละเอียด
    color=color.brown,
    scale=(10, 10, 10),
    position=(20, 5, 20),
    collider='box'
)

# สร้างน้ำ
water = Entity(
    model='plane',
    texture='water_texture',  # เปลี่ยนเป็นเท็กซ์เจอร์น้ำที่สมจริง
    scale=(30, 1, 30),
    position=(-10, 0.5, -10),
    collider='box'
)

# สร้างกำแพงบางส่วน
wall_1 = Entity(
    model='cube',
    texture='wall_texture',  # เปลี่ยนเป็นเท็กซ์เจอร์กำแพงที่สมจริง
    color=color.gray,
    scale=(10, 5, 1),
    position=(0, 2.5, 5),
    collider='box'
)

# สร้าง enemy
enemy_health = 100
enemy = Entity(
    model='cube',
    color=color.red,
    scale=(1, 2, 1),
    position=(5, 1, 10),
    collider='box'
)

# สร้างปืน
gun = Entity(
    model='cube',
    color=color.black,
    scale=(0.2, 0.1, 1),
    position=(0.5, -0.4, 1.5),
    parent=camera.ui
)

# สร้างตัวละครของผู้เล่น
player = FirstPersonController()

# สร้างโมเดลให้กับตัวละครผู้เล่น
player_model = Entity(
    model='cube',
    color=color.orange,
    scale=(1, 2, 1),
    position=player.position,
    parent=player
)

# เพิ่มแสงสว่าง
light = DirectionalLight(y=10, rotation=(45, -45, 45))

# เพิ่มแสงและเงา
ambient_light = AmbientLight(color=color.white * 0.3)

# กระสุนและจำนวนกระสุน
bullet_count = 10
max_bullets = 10

# แสดงผลจำนวนกระสุนบนหน้าจอ
bullet_text = Text(text=f'Bullets: {bullet_count}', position=(-0.85, 0.45), scale=1.5, background=True)

# ฟังก์ชันการยิงปืน
def shoot():
    global bullet_count, enemy_health

    # เช็คจำนวนกระสุน
    if bullet_count > 0:
        bullet_count -= 1
        bullet_text.text = f'Bullets: {bullet_count}'

        bullet = Entity(
            model='sphere',
            color=color.yellow,
            scale=0.1,
            position=player.position + Vec3(0, 1, 0) + camera.forward * 2,
            collider='box'
        )
        bullet.animate_position(bullet.position + camera.forward * 10, duration=0.5)

        # ตรวจสอบว่ากระสุนชนกับ enemy หรือไม่
        def check_collision():
            global enemy_health

            if not bullet or not enemy:
                return

            if bullet.intersects(enemy).hit:
                if abs(bullet.position.y - enemy.position.y) < 1:  # ยิงที่หัว
                    enemy_health -= 100
                else:  # ยิงที่ตัว
                    enemy_health -= 30
                print(f'Enemy Health: {enemy_health}')
                if enemy_health <= 0:
                    destroy(enemy)
            if bullet:
                destroy(bullet)

        invoke(check_collision, delay=0.5)

# ฟังก์ชันการ reload ปืน
def reload():
    global bullet_count
    bullet_count = max_bullets
    bullet_text.text = f'Bullets: {bullet_count}'

# ตั้งค่าให้ยิงเมื่อคลิกเมาส์ซ้าย
def input(key):
    if key == 'left mouse down':
        shoot()
    elif key == 'r':
        reload()

# เพิ่มการเคลื่อนไหวของตัวละคร
def update():
    if held_keys['w']:
        player.position += player.forward * time.dt * 5
    if held_keys['s']:
        player.position -= player.forward * time.dt * 5
    if held_keys['a']:
        player.position -= player.right * time.dt * 5
    if held_keys['d']:
        player.position += player.right * time.dt * 5

# เริ่มแอปพลิเคชัน
app.run()
