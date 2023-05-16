# game data

from argparse import Action
from random import randint
from tkinter import ANCHOR
import pgzrun


WIDTH = 800
HEIGHT = 600

GROUND = 458
GRAVITY = 200

NUMBER_OF_BACKGROUND = 2
GAME_SPEED = 100
JUMP_SPEED = 200

# hero initialisation

hero = Actor("hero", anchor=('middle', 'bottom'))
hero.pos = (64, GROUND)
hero_speed = 0

# life initialisation

lives = []
coeurs = 3

for i in range(coeurs):
    life = Actor("heart_on")
    life.pos = (90*(i+1),50)
    lives.append(life)

# enemies initialisations

BOX_APPARTION = (2, 5)
next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])
boxes = []

# background inititalisation

backgrounds_bottom = []
backgrounds_top = []

for n in range(NUMBER_OF_BACKGROUND):
    bg_b = Actor("bg_1", anchor=('left', 'top'))
    bg_b.pos = n * WIDTH, 0
    backgrounds_bottom.append(bg_b)

    bg_t = Actor("bg_2", anchor=('left', 'top'))
    bg_t.pos = n * WIDTH, 0
    backgrounds_top.append(bg_t)

#init des variables ECRANS (start, pause, mort)

game_started = False
game_paused = False
game_over = False

# fonction pour déclancher les ECRANS (start, pause, game over)
def start_game():
    global game_started
    game_started = True

def pause():
    global game_paused
    game_paused = not game_paused

def lost_game():
    global game_over
    game_over = not game_over

def draw():
    global game_paused, game_started, game_over
    screen.clear()

    if not game_over:
        if game_started:
            # ECRAN DE PAUSE : mettre ici un ecran de pause joli (juste apres le if game_paused)
            if game_paused:
                screen.draw.text("Pause", (WIDTH/2, HEIGHT/2), color="white", fontsize=60)

            # ECRAN de jeu 
            else:
                for bg in backgrounds_bottom:
                    bg.draw()

                for bg in backgrounds_top:
                    bg.draw()

                for box in boxes:
                    box.draw()

                hero.draw()
                
                for coeur in lives:
                    coeur.draw()

        # ECRAN START: ici mettre un ecran joli
        else:
            screen.draw.text("Press ENTER to start the game", (WIDTH/5, HEIGHT/2), color="white", fontsize=60)

    # ECRAN GAME OVER: ici mettre un ecran joli
    else:
        screen.draw.text("GAME OVER", (WIDTH/2, HEIGHT/2), color="white", fontsize=60)


def update(dt):

    # enemies update
    # box
    global next_box_time, game_paused, game_over,coeurs
    
    
    if not game_over and not game_paused:

        next_box_time -= dt
        if next_box_time <= 0:
            box = Actor("box", anchor=('left', 'bottom'))
            box.pos = WIDTH, GROUND
            boxes.append(box)
            next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])

        for box in boxes:
            x, y = box.pos
            x -= GAME_SPEED * dt
            box.pos = x, y
            if box.colliderect(hero):
                coeurs -= 1
                if coeurs == 0:
                    lost_game()
                # perd 1 life direct + invincible 2 secondes check asteroid


        if boxes:
            if boxes[0].pos[0] <= - 32:
                boxes.pop(0)

        
        # hero update

        global hero_speed

        hero_speed -= GRAVITY * dt
        x, y = hero.pos
        y -= hero_speed * dt

        if y > GROUND:
            y = GROUND
            hero_speed = 0

        hero.pos = x, y

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
    global hero_speed, game_paused, game_started

    # start and pause the game
    if key == keys.RETURN:
        start_game()

    if key == keys.ESCAPE:
        pause()

    # jump
    if key == keys.SPACE:
        if hero_speed <= 0:
            hero_speed = JUMP_SPEED

pgzrun.go()
