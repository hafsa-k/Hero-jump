# game data

from argparse import Action
from random import randint
from tkinter import ANCHOR
import pgzrun
from pgzhelper import *


WIDTH = 800
HEIGHT = 600

GROUND = 490
GRAVITY = 200

NUMBER_OF_BACKGROUND = 2
GAME_SPEED = 200
JUMP_SPEED = 200

# background initialisation

start_screen = Actor("start_game", anchor =["left", "top"])
game_over_screen = Actor("game_over", anchor =["left", "top"])

# hero initialisation

hero = Actor("chara_walking")
hero.pos = (64, GROUND)
hero.scale = 0.3
hero_speed = 3
hero.images = ["chara_walking", "chara_walking_1"]
hero.fps = 5

invincible = False
invincible_timer = 0


# enemies initialisations

BOX_APPARTION = (2, 5)
next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])
boxes = []

# dragon initialisation

dragon = Actor("frame-1")
dragon.pos = (400, 300)
dragon.scale = 0.15
dragon.images = ["frame-1", "frame-2", "frame-3", "frame-4"]
dragon.fps = 5

# background inititalisation

backgrounds_bottom = []
backgrounds_top = []

for n in range(NUMBER_OF_BACKGROUND):
    bg_b = Actor("bg_bottom", anchor=('left', 'top'))
    bg_b.pos = n * WIDTH, 0
    backgrounds_bottom.append(bg_b)

    bg_t = Actor("bg_top", anchor=('left', 'top'))
    bg_t.pos = n * (WIDTH+1), 0
    backgrounds_top.append(bg_t)

#init des variables ECRANS (start, pause, mort)

game_started = False
game_paused = False
game_over = False

# fonction pour déclancher les ECRANS (start, pause, game over)

def start_game():
    global game_started, game_paused, game_over, boxes, next_box_time
    game_started = True
    game_paused = False
    game_over = False
    boxes = []
    next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])

def pause():
    global game_paused
    game_paused = not game_paused

def end_game():
    global game_over
    game_over = True

# def restart_game():
#     global game_started, game_over
#     game_started = True
#     game_over = False

def draw():
    global game_paused, game_started, game_over
    screen.clear()

    # ECRAN START: ici mettre un ecran joli
    if not game_started:
        start_screen.draw()
        # screen.draw.text("Press ENTER to start the game", (WIDTH/5, HEIGHT/2), color="white", fontsize=60)

    # ECRAN DE PAUSE : mettre ici un ecran de pause joli (juste apres le if game_paused)
    elif game_paused:
        screen.draw.text("Pause", (WIDTH/2, HEIGHT/2), color="white", fontsize=60)

    # ECRAN GAME OVER: ici mettre un ecran joli
    elif game_over:
        game_over_screen.draw()
        # screen.draw.text("GAME OVER", (WIDTH/2, HEIGHT/2), color="white", fontsize=60)
    
    # ECRAN de jeu 
    else:
        screen.fill(color = "white")
        for bg in backgrounds_bottom:
            bg.draw()

        for bg in backgrounds_top:
            bg.draw()

        for box in boxes:
            box.draw()

        hero.draw()
        dragon.draw()

def update(dt):

    # enemies update
    # box

    global next_box_time, game_started, game_paused, game_over,invincible, invincible_timer
    
    if game_started and not game_over and not game_paused:

        next_box_time -= dt
        if next_box_time <= 0:
            box = Actor("obstacles")
            box.pos = WIDTH, GROUND
            box.scale = 0.5
            boxes.append(box)
            next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])

        for box in boxes:
            x, y = box.pos
            x -= GAME_SPEED * dt
            box.pos = x, y
            if box.colliderect(hero):
                end_game()
                invincible = True


        if boxes:
            if boxes[0].pos[0] <= - 32:
                boxes.pop(0)

        dragon.animate()

        # hero update

        global hero_speed

        if invincible :
            invincible_timer -= dt
            if invincible_timer <= 0:
                invincible = False
                
        hero_speed -= GRAVITY * dt
        x, y = hero.pos
        y -= hero_speed * dt

        if y > GROUND:
            y = GROUND
            hero_speed = 0

        hero.pos = x, y

        hero.animate()

        # bg update

        for bg in backgrounds_bottom:
            x, y = bg.pos
            x -= GAME_SPEED * dt
            bg.pos = x, y

        if backgrounds_bottom[0].pos[0] <= - WIDTH:
            bg = backgrounds_bottom.pop(0)
            bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
            backgrounds_bottom.append(bg)

        for bg in backgrounds_top:
            x, y = bg.pos
            x -= GAME_SPEED/3 * dt
            bg.pos = x, y

        if backgrounds_top[0].pos[0] <= - WIDTH:
            bg = backgrounds_top.pop(0)
            bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
            backgrounds_top.append(bg)


def on_key_down(key):
    global hero_speed, game_paused, game_started, game_over

    # start and pause the game
    if key == keys.RETURN:
        if not game_started or game_over:
            start_game()

    if key == keys.ESCAPE:
        if game_started:
            pause()

    # jump
    if key == keys.SPACE:
        if hero_speed <= 0:
            hero_speed = JUMP_SPEED

pgzrun.go()
