import math

from ursina import *
import random

app = Ursina()

camera.position = (0, 15 , -7)
camera.look_at((0, 0, 3))
stop = False
spiller = Entity(model='test.glb',
                 scale=(1, 1, 1),
                 position=(0, 0, 0),
                 collider='box',
                 shader='basic_lighting_shader'
                 )

shield = Entity(
    model='sphere',
    color=color.cyan,
    scale=2,  # Bigger than player
    position=spiller.position,
    alpha=0.3,  # Makes it transparent! (0=invisible, 1=solid)
    enabled=False  # Hidden at start
)

modstander = []
tid_modstander = 3
tid_bonus = 0

score_text = Text(text='Score: 0', position=(0, 0.45), scale=2, origin=(0,0))
game_over_text = Text(text='Game over', 
                      position=(0, 0), 
                      scale=3, 
                      color=color.red, 
                      origin=(0,0),
                      enabled=False)
langsom_text = Text(text='Langsom tid: 0', 
                    position=(0.45, 0.45),
                    scale=1,
                    color=color.black,
                    origin=(0, 0))
score = 0
speed = 0
bonus = None
genstart_knap = None
langsom_tid = 0
score_lyd = Audio('score.mp3', autoplay=False)

Entity(model='plane',
        color=color.gray,
        scale=(10, 1, 15),
        position=(0, -0.5, 0),
        shader='basic_lighting_shader')

Entity(model='plane',
       color=color.gray,
       scale=(2, 1, 15),
       position=(-5, 0, 0),
       world_rotation_z=90,
       shader='basic_lighting_shader')

def opdatere_langsom_text():
    global langsom_tid, langsom_text
    langsom_text.text = f'Langsom tid: {round(langsom_tid)}'
        

def genstart():
    global game_over_text, speed, langsom_tid, modstander, spiller, score, tid_modstander, score_text, genstart_knap, shield
    for modstand in modstander:
        destroy(modstand)
    modstander = []
    spiller.x = 0
    score = 0
    score_text.text = f'Score: {score}'
    tid_modstander = 8
    speed = 0
    langsom_tid = 0
    game_over_text.enabled = False
    shield.enabled = False
    if genstart_knap != None:
        destroy(genstart_knap)
        genstart_knap = None


def spawn_modstand(farve, speed_factor, storelse):
    """Lav en modstander med forskellige egenskaber"""
    ny_modstand = Entity(
        model='sphere',
        color=farve,
        scale=(storelse, storelse, storelse),
        position=(random.uniform(-4, 4), 0, 8),
        collider='sphere',
        shader='basic_lighting_shader'
    )
    ny_modstand.speed_factor = speed_factor
    return ny_modstand


def spawn_bonus(farve, storelse):
    """Lav en bonus med forskellige egenskaber"""
    ny_bonus = Entity(
        model='sphere',
        color=farve,
        scale=(storelse, storelse, storelse),
        position=(random.uniform(-4, 4), 0, 8),
        collider='sphere',
        shader='basic_lighting_shader'
    )
    return ny_bonus

def update():
    global stop, score, score_text, modstander, tid_modstander, game_over_text, speed, tid_bonus, bonus, langsom_tid
    global genstart_knap, score_lyd, shield
    if game_over_text.enabled:
        return

    if held_keys['left arrow'] and spiller.x > -3:
        spiller.x -= 8 * time.dt
    if held_keys['right arrow'] and spiller.x < 3:
        spiller.x += 8 * time.dt

    for modstand in modstander:
        if spiller.intersects(modstand).hit:
            if shield.enabled:
                shield.enabled = False
                destroy(modstand)
                modstander.remove(modstand)
            else:
                game_over_text.enabled = True
                genstart_knap = Button('Genstart spil', 
                                    origin=(0.0, 0.5), 
                                    scale_x = 0.2, 
                                    scale_y=0.15)
                genstart_knap.on_click = genstart

    if tid_modstander > 10:
        # Spawn different types randomly!
        if random.random() < 0.3:
            ny_modstand = spawn_modstand(farve=color.orange, speed_factor=0.70, storelse=1.5)  # Slow big one
        else:
            ny_modstand = spawn_modstand(farve=color.red, speed_factor=1.20, storelse=1)  # Fast small one
        modstander.append(ny_modstand)
        tid_modstander = 0
        speed += 0.01

    if tid_bonus > 12:
        if random.random() < 0.5:
            bonus = spawn_bonus(farve=color.green, storelse=1)
        else:
            bonus = spawn_bonus(farve=color.blue, storelse=0.5)
        tid_bonus = 0

    langsom = 1
    if held_keys['space'] and langsom_tid > 0:
        langsom = 0.5
        langsom_tid -= time.dt

    for modstand in modstander:
        modstand.z -= (time.dt * 2 + (speed * langsom * modstand.speed_factor))
        if modstand.z < -4:
            modstand.z = 8
            modstand.x = random.uniform(-4, 4)
            score_lyd.play()
            score += 1
            score_text.text = f'Score: {score}'

    if bonus != None:        
        bonus.z -= time.dt * 3
        if spiller.intersects(bonus).hit:
            if bonus.color == color.green:
                langsom_tid += 10
            elif bonus.color == color.blue:
                shield.enabled = True
            destroy(bonus)
            bonus = None
    if shield.enabled:
        shield.position = spiller.position
        shield.scale = 2 + math.sin(time.time() * 5) * 0.2

    tid_modstander += time.dt
    tid_bonus += time.dt
    opdatere_langsom_text()

app.run()