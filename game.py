from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import asyncio

app = Ursina()

# Player & Sky
player = FirstPersonController()
Sky()   

# Blocks/World Generation
boxes = []
for i in range(20):
    for j in range(20):
        box = Button(
            color=color.white,
            model="cube",
            position=(j, 0, i),
            texture="grass.png",
            parent=scene,
            origin_y=0.5
        )
        boxes.append(box)

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

selected_block = "grass"            

def input(key):
    global selected_block

    if key == "e":
        shoot()

    if key == "m":
        selected_block = "stone"
        print("Selected block: Stone")

    if key == "g":
        selected_block = "grass"
        print("Selected block: Grass")    

    for box in boxes:
        if box.hovered:    
            if key == "right mouse down":
                if selected_block == "stone":
                 grass = Button(
                    color=color.white,
                    model="cube",
                    position=box.position + mouse.normal,
                    texture=f"{selected_block}.jpg",
                    parent=scene,
                    origin_y=0.5
                 )
                 boxes.append(grass)
                elif selected_block == "grass":
                    grass = Button(
                    color=color.white,
                    model="cube",
                    position=box.position + mouse.normal,
                    texture=f"{selected_block}.png",
                    parent=scene,
                    origin_y=0.5
                 )
                boxes.append(grass) 

            if key == "left mouse down":
                boxes.remove(box)
                destroy(box)

            #hey chatgpt make it so when i click m then i will select to place stone when i click right mouse button and wehen i click g it makes me select grass    
app.run()
