import turtle
import os
import math
import random
import platform
import tkinter as tk
from tkinter import font

# Set up sound
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound module not available.")

def play_sound(sound_file, time=0):
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    elif platform.system() == "Linux":
        os.system(f"aplay -q {sound_file}&")
    else:
        os.system(f"afplay {sound_file}&")

# Screen setup
def setup_screen():
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Space Invaders")
    screen.bgpic("img/space_bg.gif")
    screen.tracer(0)
    screen.register_shape("img/player.gif")
    screen.register_shape("img/eli.gif")
    screen.register_shape("img/bullet.gif")
    return screen

# Draw border
def draw_border():
    border_pen = turtle.Turtle()
    border_pen.speed(0)
    border_pen.color("white")
    border_pen.penup()
    border_pen.setposition(-300, -300)
    border_pen.pendown()
    border_pen.pensize(3)
    for _ in range(4):
        border_pen.fd(600)
        border_pen.lt(90)
    border_pen.hideturtle()

# Create player
def create_player():
    player = turtle.Turtle()
    player.shape("img/player.gif")
    player.penup()
    player.speed(0)
    player.setposition(0, -250)
    player.setheading(90)
    player.speed = 0
    return player

# Create elis
def create_elis(number_eli):
    elis = []
    eli_start_x, eli_start_y = -225, 225
    eli_number = 0
    for _ in range(number_eli):
        eli = turtle.Turtle()
        eli.shape("img/eli.gif")
        eli.penup()
        eli.speed(0)
        x = eli_start_x + (50 * eli_number)
        y = eli_start_y
        eli.setposition(x, y)
        eli_number += 1
        if eli_number == 10:
            eli_start_y -= 50
            eli_number = 0
        elis.append(eli)
    return elis

# Create bullet
def create_bullet():
    bullet = turtle.Turtle()
    bullet.shape("img/bullet.gif")
    bullet.penup()
    bullet.speed(0)
    bullet.hideturtle()
    bullet.setposition(0, -400)
    return bullet

# Create UI elements
def create_ui_elements():
    score_pen = turtle.Turtle()
    score_pen.speed(0)
    score_pen.color("white")
    score_pen.penup()
    score_pen.setposition(-290, 280)
    score_pen.hideturtle()

    game_over_text = turtle.Turtle()
    game_over_text.hideturtle()
    game_over_text.color("#228B22")
    game_over_text.penup()
    game_over_text.goto(0, 50)

    high_score_display = turtle.Turtle()
    high_score_display.hideturtle()
    high_score_display.color("white")
    high_score_display.penup()
    high_score_display.goto(0, 200)

    return score_pen, game_over_text, high_score_display

# Game logic functions
def move_left():
    global player
    if game_state == "playing":
        player.speed = -0.35

def move_right():
    global player
    if game_state == "playing":
        player.speed = 0.35

def move_player():
    global player
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    global bulletstate, bullet, player
    if game_state == "playing" and bulletstate == "ready":
        play_sound("sounds/fireball.wav")
        bulletstate = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    return distance < 15

def start_game():
    global game_state, first_play
    game_state = "playing"
    play_button.place_forget()
    game_over_text.clear()
    high_score_display.clear()
    wn.bgcolor("black")
    reset_game()
    if first_play:
        first_play = False
        play_button.config(text="leZz GO! again")

def reset_game():
    global score, elis, player
    score = 0
    update_score(0)
    player.showturtle()
    player.goto(0, -250)
    
    eli_start_x, eli_start_y = -225, 225
    eli_number = 0
    for eli in elis:
        eli.showturtle()
        x = eli_start_x + (50 * eli_number)
        y = eli_start_y
        eli.setposition(x, y)
        eli_number += 1
        if eli_number == 10:
            eli_start_y -= 50
            eli_number = 0

def end_game():
    global game_state, high_score
    game_state = "over"
    if score > high_score:
        high_score = score
    wn.bgcolor("gray10")
    player.hideturtle()
    for eli in elis:
        eli.hideturtle()
    play_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    high_score_display.clear()
    high_score_display.write(f"High Score: {high_score}", align="center", font=("Impact", 14, "normal"))
    blink_game_over()

def blink_game_over():
    if game_state == "over":
        game_over_text.clear()
        game_over_text.write("   GAME OVER   ", align="center", font=("Press Start 2P", 30, "normal"))
        wn.ontimer(game_over_text.clear, 1000)
        wn.ontimer(blink_game_over, 2000)

def update_score(points):
    global score
    score += points
    score_pen.clear()
    score_pen.write(f"Score: {score}", False, align="left", font=("Impact", 12, "normal"))

def update_elis():
    global elispeed, game_state, bullet, bulletstate
    for eli in elis:
        if eli.isvisible():
            x = eli.xcor()
            x += elispeed
            eli.setx(x)

            if eli.xcor() > 280 or eli.xcor() < -280:
                for e in elis:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                elispeed *= -1

            if is_collision(bullet, eli):
                play_sound("sounds/explosion.wav")
                bullet.hideturtle()
                bulletstate = "ready"
                bullet.setposition(0, -400)
                eli.hideturtle()
                update_score(10)

            if is_collision(eli, player) or eli.ycor() < player.ycor() + 20:
                play_sound("sounds/explosion.wav")
                end_game()
                return

def update_bullet():
    global bulletstate, bullet, bulletspeed
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

# Main game setup
wn = setup_screen()
draw_border()

score = 0
high_score = 0
game_state = "start"
first_play = True

player = create_player()
elis = create_elis(30)
bullet = create_bullet()
score_pen, game_over_text, high_score_display = create_ui_elements()

elispeed = 0.05
bulletspeed = 1.3
bulletstate = "ready"

# Create Tkinter button
root = tk.Tk()
root.withdraw()  # Hide the main Tkinter window

# Load the custom font
font_path = os.path.join("fonts", "PressStart2P-Regular.ttf")
custom_font = font.Font(family="Press Start 2P", size=20)

if os.path.exists(font_path):
    custom_font = font.Font(font=font.Font(family="TkDefaultFont").actual()["family"], size=20)
    custom_font.configure(family="Press Start 2P")
    root.tk.call("font", "configure", custom_font.name, "-file", font_path)

play_button = tk.Button(
    wn.getcanvas().master,
    text="leZz GO!",
    font=custom_font,
    fg="white",
    bg="dark blue",
    command=start_game
)
play_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Keyboard bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Main game loop
while True:
    wn.update()
    
    if game_state == "playing":
        move_player()
        update_elis()
        update_bullet()

    root.update()  # Update Tkinter elements