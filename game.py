
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import asyncio

app = Ursina()

# Player & Sky
player = FirstPersonController()
Sky()

# Enemy Class with Health
class Enemy(Entity):
    def __init__(self, position=(0, 0, 5), health=100, **kwargs):
        super().__init__(
            model='cube',
            color=color.red,
            position=position,
            scale=(1, 3, 1),  # Taller enemies
            tag='enemy',
            collider='box',   # Ensures hit detection
            **kwargs
        )
        self.health = health
        self.health_bar = Entity(
            parent=self,
            model='quad',
            color=color.green,
            position=(0, 1.7, 0),
            scale=(1, 0.1, 1)
        )

    def take_damage(self, damage):
        self.health -= damage
        self.health_bar.scale_x = self.health / 100
        if self.health <= 0:
            self.explode()

    def explode(self):
        explosion = Entity(
            model='sphere',
            color=color.orange,
            scale=1.5,
            position=self.position,
            texture='white_cube'
        )
        destroy(self, delay=0.1)
        destroy(explosion, delay=0.5)

# Weapon (Placeholder)
weapon = Entity(
    model='cube',
    color=color.gray,
    scale=(0.3, 0.2, 1),
    position=(0.5, -0.3, 1),
    parent=camera.ui
)

# Blocks/World Generation
boxes = []
for i in range(1):
    for j in range(1):
        box = Button(
            color=color.white,
            model="cube",
            position=(j, 0, i),
            texture="grass.png",
            parent=scene,
            origin_y=0.5
        )
        boxes.append(box)

# Shoot Bullet towards Mouse position
def shoot():
    # Ensure the player is shooting in the direction of the camera's view
    direction = camera.forward  # This uses the camera's forward direction (relative to player)

    bullet = Entity(
        model='sphere',
        color=color.yellow,
        scale=0.2,
        position=player.position + Vec3(0, 1.5, 0),  # Position it near the player
        speed=15
    )

    def update_bullet():
        bullet.position += direction * bullet.speed * time.dt  # Move bullet in the camera's direction

        hit_info = bullet.intersects()
        if hit_info.hit:
            if hit_info.entity and hit_info.entity.tag == 'enemy':
                hit_info.entity.take_damage(34)  # Correct damage application
            elif hit_info.entity in boxes:
                boxes.remove(hit_info.entity)
                destroy(hit_info.entity)
            destroy(bullet)
            return

        if distance(bullet.position, player.position) > 50:  # Bullet distance check
            destroy(bullet)

    bullet.update = update_bullet

# Input function to detect keypress
def input(key):
    if key == "e":  # When 'E' is pressed, shoot a bullet
        shoot()

    for box in boxes:
        if box.hovered:
            if key == "left mouse down":
                boxes.remove(box)
                destroy(box)
            if key == "right mouse down":
                new_box = Button(
                    color=color.white,
                    model="cube",
                    position=box.position + mouse.normal,
                    texture="grass.png",
                    parent=scene,
                    origin_y=0.5
                )
                boxes.append(new_box)

# Create enemies
enemies = [Enemy(position=(3, 0, 3)), Enemy(position=(-4, 0, 8)), Enemy(position=(6, 0, -2))]

def run_ursina():
   app.run()

async def main():   
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, run_ursina)  # Non-blocking Ursina app
    print("Ursina is running — now continuing the rest of the script!")

    # Example of background logic that runs while the game continues
    while True:
        await asyncio.sleep(1)  # Simulating a background task
        print("This is running alongside Ursina")