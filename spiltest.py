import math

from ursina import *
from ursina.shaders import lit_with_shadows_shader
import random

app = Ursina()

camera.position = (0, 5 , -10)
camera.look_at((0, 0, 0))
stop = False
Entity.default_shader = lit_with_shadows_shader
spiller = Entity(model='cube',
                 color=color.green,
                 scale=(1, 1, 1),
                 position=(0, 0, 0),
                 collider='box')

modstander = []
tid_modstander = 0
tid_bonus = 0

score_text = Text(text='Score: 0', position=(0, 0.45), scale=2, origin=(0,0))
game_over_text = Text(text='Game over', 
                      position=(0, 0.1), 
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
langsom_tid = 0
genstart_knap = None
score_lyd = Audio(sound_file_name='score.mp3', autoplay=False)


Entity(model='plane',
        color=color.gray,
        scale=(10, 1, 15),
        position=(0, -0.5, 0))

Entity(model='plane',
       color=color.gray,
       scale=(2, 1, 15),
       position=(-5, 0, 0),
       world_rotation_z=90)

def opdatere_langsom_text():
    global langsom_tid, langsom_text
    langsom_text.text = f'Langsom tid: {round(langsom_tid)}'


def input(key):
    global game_over_text
    if key == 'space' and game_over_text.enabled == True:
        genstart()

def genstart():
    global modstander, spiller, score, tid_modstander, score_text, speed, genstart_knap
    for modstand in modstander:
        destroy(modstand)
    modstander = []
    spiller.x = 0
    score = 0
    score_text.text = f'Score: {score}'
    tid_modstander = 8
    speed = 0
    game_over_text.enabled = False
    destroy(genstart_knap)


def update():
    global stop, score, score_text, modstander, tid_modstander, game_over_text, speed, tid_bonus, bonus, langsom_tid
    global genstart_knap, score_lyd
    if game_over_text.enabled:
        return

    if held_keys['left arrow'] and spiller.x > -3:
        spiller.x -= 8 * time.dt
    if held_keys['right arrow'] and spiller.x < 3:
        spiller.x += 8 * time.dt

    for modstand in modstander:
        if spiller.intersects(modstand).hit:
            game_over_text.enabled = True
            genstart_knap = Button(text='Restart', scale=0.2, scale_y=0.1, origin=(0, 0.5), disabled=True)
            genstart_knap.on_click = genstart

    if tid_modstander > 10:
        modstander.append(Entity(model='sphere',
                    color=color.red,
                    scale=(1, 1, 1),
                    position=(0, 0, 8),
                    collider='sphere',
                    shader='basic_lighting_shader'))
        tid_modstander = 0
        speed += 0.01

    if tid_bonus > 25:
        # global tid_bonus, bonus, tid_bonus = 0, bonus = None 
        bonus = Entity(model='sphere',
                    color=color.green,
                    scale=(1, 1, 1),
                    position=(0, 0, 8),
                    collider='sphere',
                    shader='basic_lighting_shader')
        tid_bonus = 0

    langsom = 1
    if held_keys['space'] and langsom_tid > 0:
        langsom = 0.5
        langsom_tid -= time.dt

    for modstand in modstander:
        modstand.z -= (time.dt * 2 + speed) * langsom
        if modstand.z < -4:
            modstand.z = 8
            modstand.x = random.uniform(-4, 4)
            score += 1
            score_text.text = f'Score: {score}'
            score_lyd.play()

    if bonus != None:        
        bonus.z -= time.dt * 3
        if spiller.intersects(bonus).hit:
            langsom_tid += 10
            destroy(bonus)
            bonus = None

    tid_modstander += time.dt
    tid_bonus += time.dt

app.run()