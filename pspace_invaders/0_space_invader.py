#-----------------SPACE INVADERS-----------------
import turtle
import os
import math
import random
import platform

# use winsound in Wins
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound module not available.") 


# set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invanders")
wn.bgpic("img/space_bg.gif")
wn.tracer(0)

# register the shapes 
wn.register_shape("img/player.gif")
wn.register_shape("img/eli.gif")
wn.register_shape("img/bullet.gif")

# draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("DarkGray")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# set score to 0
score = 0

# draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring =  "Score: {}" .format(score)
score_pen.write(scorestring, False, align = "left", font = ("Impact", 12, "normal"))
score_pen.hideturtle()

# create the player turtle
player = turtle.Turtle()
# player.color("Blue")
player.shape("img/player.gif")
player.penup()
player.speed(0) # method comes first
player.setposition(0,-250)
player.setheading(90) # variable


player.speed = 0  # was playspeed before


# choose number of elis
number_eli =  30
# create an empty list of elis
elis = []

# add elis to the list
for i in range(number_eli):
    # create eli
    elis.append(turtle.Turtle())

eli_start_x = -225
eli_start_y = 225
eli_number = 0

for eli in elis:
    #eli.color("red")
    eli.shape("img/eli.gif")
    eli.penup()
    eli.speed(0)
    x = eli_start_x + (50 * eli_number)
    y = eli_start_y
    eli.setposition(x, y)
    # update the eli number
    eli_number += 1
    if eli_number == 10:
        eli_start_y -= 50
        eli_number = 0

    elispeed = 0.02


# create player's bullet
bullet = turtle.Turtle()
# bullet.color("yellow")
bullet.shape("img/bullet.gif")
bullet.penup()
bullet.speed(0)
# bullet.setheading(90)
# bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 1

# define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"

# move the player left and right
def move_left():
    player.speed = -0.2

def move_right():
    player.speed = 0.2

def move_player():
        x = player.xcor()
        x += player.speed
        if x <-280:
            x = -280
        player.setx(x)

        if x > 280:
            x = 280
        player.setx(x)


def fire_bullet():
    # declare bulletstate as a global if it needs to be changed
    # global why? Any change in this function's bulletstate will be reflected above
    global bulletstate 
    if bulletstate == "ready":
        PlaySound("sounds/fireball.wav")
        bulletstate = "fire"
        # move the bullet just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1, t2):
    dist = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if dist < 15:
        return True 
    else:
        return False
    
def PlaySound(sound_file, time = 0):
    # Windows
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC) 
    
    # Linux
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    
    # Mac
    else:
        os.system("afplay {}&".format(sound_file))



# create keyboard bindings 
wn.listen()

wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# main game loop
while True:
    wn.update()
    move_player()

    for eli in elis:

        # move eli 
        x = eli.xcor()
        x += elispeed
        eli.setx(x)

        # move eli back and down
        if eli.xcor() > 280:
            # move all elis down
            for e in elis:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # change eli direction
            elispeed *= -1

        if eli.xcor() < -280:
            # move all elis down
            for e in elis:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # change eli direction
            elispeed *= -1

        # chk for a collisions btw the bullet and eli :(
        if isCollision(bullet, eli):
            PlaySound("sounds/explosion.wav")
            # reset bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # revive eli :)
            eli.setposition(0, 10000)
            # update score
            score += 10
            scorestring = "Score: {}" .format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align = "left", font = ("Impact", 12, "normal"))


        if isCollision(eli, player):
            PlaySound("sounds/explosion.wav")
            player.hideturtle()
            eli.hideturtle()
            print("Game Over")
            break

    
    # move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # chk to see if the bullet has reached top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    



