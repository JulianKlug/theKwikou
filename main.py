# Implementation of Kwikou2.0
# By MonsieurWave
#           ~                  ~
#     *                   *                *       *
#                  *               *
#  ~       *                *         ~    *
#              *       ~        *              *   ~
#                  )         (         )              *
#    *    ~     ) (_)   (   (_)   )   (_) (  *
#           *  (_) # ) (_) ) # ( (_) ( # (_)       *
#              _#.-#(_)-#-(_)#(_)-#-(_)#-.#_
#  *         .' #  # #  #  # # #  #  # #  # `.   ~     *
#           :   #    #  #  #   #  #  #    #   :
#    ~      :.       #     #   #     #       .:      *
#        *  | `-.__                     __.-' | *
#           |      `````"""""""""""`````      |         *
#     *     |         | ||\ |~)|~)\ /         |
#           |         |~||~\|~ |~  |          |       ~
#   ~   *   |                                 | *
#           |      |~)||~)~|~| ||~\|\ \ /     |         *
#   *    _.-|      |~)||~\ | |~|| /|~\ |      |-._
#      .'   '.      ~            ~           .'   `.  *
#      :      `-.__                     __.-'      :
#       `.         `````"""""""""""`````         .'
#         `-.._                             _..-
#


# DON'T MODIFY ANYTHING BELOW UNLESS YOU KNOW WHAT YOU'RE DOING


import simpleguitk as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
countdown = 0
started = False
doge = False
bonus = 0
quer = 0
mode = "Normal"

color_list = ["Navy", "Purple", "Tomato"]
color = "White"
message_list = ["L0L", "42", "Apocalyptus", "Much WOW", "Essaie avec une pelle!", "Pika!", "Have u seen da D?"]
message = ""


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False, N_images=None, decay=1):
        self.center = center
        self.size = size
        self.radius = radius
        self.decay = decay
        if N_images:
            self.length = N_images
        else:
            self.length = lifespan
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_length(self):
        return self.length

    def get_decay(self):
        return self.decay

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# Clouds
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("./static/clouds1.png")

# Background
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("./static/blueBG.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("./static/splash2.png")

# kri image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("./static/kri-sheet1-lowres black.png")

# twitch image
twitch_info = ImageInfo([90, 90], [180, 180], 35)
twitch_image = simplegui.load_image("./static/twitch_sheet copy.png")

# no pants kri image
nopantskri_info = ImageInfo([45, 45], [90, 90], 45)
nopantskri_image = simplegui.load_image("./static/kri-sheet2-lowres copy.png")

# dick image
dick_info = ImageInfo([90, 90], [180, 180], 30)
dick_image = simplegui.load_image("./static/dick_sheet copy.png")

# quer images
quer_info = ImageInfo([64, 64], [128, 128], 64, None, True, 5, 10)
quer_image = simplegui.load_image("./static/quer_sprites copy.png")

# falling
falling_image = simplegui.load_image("./static/falling_sheet copy.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 55)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images = vanilla ice cream
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("./static/mob_spritesheet.png")

# minion images
minion_info = ImageInfo([45, 45], [90, 90], 35)
minion_image = simplegui.load_image("./static/minion.png")

# bonus image
bonus_image = simplegui.load_image("./static/bonus_sheet copy.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)

explosion_image1 = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image2 = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
# explosion_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")
# explosion_image4 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")
explosion_list = [explosion_image1, explosion_image1, explosion_image2, explosion_image2]

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("./static/Sprite Creation.mp3")
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(.2)


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]],
                              self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1

        self.vel[0] *= .99
        self.vel[1] *= .99

        # gravity
        if gravity == "Inverse":
            self.vel[1] -= 0.05
        if gravity:
            self.vel[1] += 0.005

        # bounce off walls
        if self.pos[1] <= self.radius:
            self.vel[1] = -1 * self.vel[1]

        if self.pos[1] > (HEIGHT - 1 - self.radius):
            self.vel[1] = -1 * self.vel[1]

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def increment_angle_vel(self):
        self.angle_vel += .05

    def decrement_angle_vel(self):
        self.angle_vel -= .05

    def relook(self, newlook, info):
        # change the image of your ship/hero
        self.image = newlook
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None, bounce=True):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.image_length = info.get_length()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.bounce = bounce
        self.age = 0
        self.decay = info.get_decay()
        self.k = 1
        if sound:
            sound.rewind()
            sound.play()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_object):
        p = other_object.get_pos()
        r = other_object.get_radius()
        d = dist(self.get_pos(), p)
        return d < (self.get_radius() + r)

    def draw(self, canvas):
        if self.animated == False:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            self.image_center[0] = (64 + (self.age * self.image_size[0])) % (self.image_size[0] * self.image_length)
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        if self.k == self.decay:
            self.age += 1
            self.k = 1
        else:
            self.k += 1

        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # bounce off walls
        if self.bounce:
            if self.pos[1] <= self.radius:
                self.vel[1] = -1 * self.vel[1]

            if self.pos[1] > (HEIGHT - 1 - self.radius):
                self.vel[1] = -1 * self.vel[1]

        return self.age > self.lifespan


# key handlers to control ship
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()


def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)


# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, gravity
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        gravity = True
        lives = 3
        score = 0
        my_ship.relook(ship_image, ship_info)
        soundtrack.play()


def process_sprite_group(canvas, set):
    l = list(set)
    for i in range(0, len(l)):
        l[i].draw(canvas)
        l[i].update()
        if l[i].update():
            set.remove(l[i])


def newgame():
    global time, started, lives, score, rock_group, quer_group, falling_group, bonus_group, doge, gravity
    started = False
    doge = False
    gravity = False
    rock_group = set([])
    quer_group = set([])
    falling_group = set([])
    bonus_group = set([])
    soundtrack.pause()
    soundtrack.rewind()


def draw(canvas):
    global time, started, lives, score, rock_group, quer_group, a_quer, falling_group, a_falling, bonus_group, doge, countdown, message, gravity
    # new game and stuff
    if lives < 1:
        newgame()

    # animiate background
    time += 1
    htime = (time / 4) % HEIGHT
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (WIDTH / 2, htime - HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (WIDTH / 2, htime + HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 25, "Black")
    canvas.draw_text("Score", [680, 50], 25, "Black")
    canvas.draw_text(str(lives), [50, 80], 25, "Black")
    canvas.draw_text(str(score), [680, 80], 25, "Black")

    # draw messages

    if doge:
        color = color_list[random.randint(0, len(color_list) - 1)]
        canvas.draw_text(message, [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)], 60, color)
        if time > countdown + 120:
            doge = False

    if score == 69:
        canvas.draw_text("69", [WIDTH / 2, HEIGHT / 2], 40, "Purple")
        canvas.draw_text("Zelephant!", [WIDTH / 2, HEIGHT / 2 + 40], 40, "Purple")

    # gravity modulation
    if gravity == "Inverse" and started == True:
        canvas.draw_text("Inversed gravity !", [WIDTH / 2, HEIGHT / 2], 40, "Purple")
        if time > countdown + 360:
            gravity = True

    # draw ship and sprites
    my_ship.draw(canvas)

    # update ship and sprites
    my_ship.update()

    # draw and update sprite sets
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    process_sprite_group(canvas, quer_group)
    process_sprite_group(canvas, bonus_group)
    process_sprite_group(canvas, falling_group)

    # collisions
    collisions()

    # relook
    if score > 68:
        my_ship.relook(nopantskri_image, nopantskri_info)
        if score > 130:
            my_ship.relook(twitch_image, twitch_info)
            if score > 180:
                my_ship.relook(dick_image, dick_info)

    # quer
    if score % 10 == 0 and len(quer_group) < 1 and score > 1:
        quer_pos = [random.randrange(-3, 0), random.randrange(5, HEIGHT - 5)]
        d = dist(quer_pos, my_ship.get_pos())
        quer = random.randint(0, 2)
        quer_info = ImageInfo([64, 64 + 128 * quer], [128, 128], 64, None, True, 5, 10)

        if (d > (quer_info.get_radius() + my_ship.get_radius() + 10)):
            quer_vel = [1, 0]
            quer_avel = 0
            a_quer = Sprite(quer_pos, quer_vel, 0, quer_avel, quer_image, quer_info)
            quer_group.add(a_quer)

            # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())


def collisions():
    global rock_group, quer_group, a_quer, a_falling, bonus_group, falling_group, doge, countdown, message, gravity, lives, score, bonus
    # collisions consequences
    if mode == "Antoine":
        if group_collide(rock_group, my_ship) or group_collide(falling_group, my_ship):
            lives -= 1
        if group_collide(quer_group, my_ship):
            score -= 1

    else:
        if group_collide(rock_group, my_ship) or group_collide(quer_group, my_ship) or group_collide(falling_group,
                                                                                                     my_ship):
            lives -= 1
    if group_collide(bonus_group, my_ship):
        score += 5
        if bonus == 0:
            message = message_list[random.randint(0, len(message_list) - 1)]
            doge = True
        if bonus == 1:
            gravity = "Inverse"
        if bonus == 2:
            lives += 1
        countdown = time

    # ship collisions
    group_collide(rock_group, my_ship)
    group_collide(bonus_group, my_ship)
    group_collide(quer_group, my_ship)
    group_collide(falling_group, my_ship)

    # missile collisions
    group_group_collide(missile_group, rock_group)
    group_group_collide(missile_group, quer_group)
    group_group_collide(missile_group, bonus_group)
    group_group_collide(missile_group, falling_group)

    # inter mob collisions
    group_collide(rock_group, a_quer)
    group_collide(rock_group, a_falling)

    # ground collisions
    ground_collide(falling_group)


# timer handler that spawns a rock
def rock_spawner():
    global rock_group, bonus, a_falling
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    d = dist(rock_pos, my_ship.get_pos())
    m = 0
    if mode == "Hardcore":
        m = 1
    if mode == "Allaz":
        m = 3

    # choose a random mob
    k = 0
    limage = [asteroid_image, minion_image]
    linfo = [asteroid_info, minion_info]
    if score > 15:
        k = 1
    r = random.randint(0, k)
    image = limage[r]
    info = linfo[r]

    if len(rock_group) < 13 and started and (d > (asteroid_info.get_radius() + my_ship.get_radius() + 10)):
        rock_vel = [random.random() * .6 - .3 + m, random.random() * .6 - .3 + m]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, image, info)
        rock_group.add(a_rock)

    if random.randint(0, 10) == 0 and len(bonus_group) < 1 and score > 1:
        bonus_pos = [0, random.randrange(5, HEIGHT - 5)]
        bonus = random.randint(0, 2)
        bonus_info = ImageInfo([85 + bonus * 170, 85], [170, 170], 60)
        d = dist(bonus_pos, my_ship.get_pos())

        if (d > (bonus_info.get_radius() + my_ship.get_radius() + 10)):
            bonus_vel = [random.random() * .3 - .3, random.random() * .3 - .3]
            bonus_avel = random.random() / 300
            a_bonus = Sprite(bonus_pos, bonus_vel, 0, bonus_avel, bonus_image, bonus_info)
            bonus_group.add(a_bonus)

    if random.randint(0, 6) == 0 and len(falling_group) < 1 and score > 1:
        falling_pos = [random.randrange(5, WIDTH - 5), 0]
        falling = random.randint(0, 3)
        falling_info = ImageInfo([45, 45 + falling * 90], [90, 90], 40)
        d = dist(falling_pos, my_ship.get_pos())

        if (d > (falling_info.get_radius() + my_ship.get_radius() + 10)):
            falling_vel = [random.random() * .3 - .3 + m, 1 + m]
            falling_avel = random.random() * .2 - .1
            a_falling = Sprite(falling_pos, falling_vel, 0, falling_avel, falling_image, falling_info, bounce=False)
            falling_group.add(a_falling)

        # group collissions


def ground_collide(group):
    remove = set([])
    l = (group)
    for i in l:
        pos = i.get_pos()
        r = i.get_radius()
        if pos[1] + r > HEIGHT:
            remove.add(i)
            group.difference_update(remove)
            ex_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
            explosion = Sprite(i.pos, i.vel, 0, 0, explosion_list[random.randint(0, 3)], ex_info, explosion_sound)
            explosion_group.add(explosion)
            return True
    return False


def group_collide(group, other_object):
    if other_object:
        remove = set([])
        l = (group)
        for i in l:
            if i.collide(other_object):
                remove.add(i)
                group.difference_update(remove)
                ex_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
                explosion = Sprite(i.pos, i.vel, 0, 0, explosion_list[random.randint(0, 3)], ex_info, explosion_sound)
                explosion_group.add(explosion)
                return True
    return False


def group_group_collide(group1, group2):
    global score
    remove = set([])
    for i in group1:
        if group_collide(group2, i):
            group_collide(group2, i)
            remove.add(i)
            score += 1
    group1.difference_update(remove)


def button_handler1():
    global mode
    mode = "Antoine"


def button_handler2():
    global mode
    mode = "Normal"


def button_handler3():
    global mode
    mode = "Hardcore"


def button_handler4():
    global mode
    mode = "Allaz"


# initialize stuff
frame = simplegui.create_frame("Kwikou", WIDTH, HEIGHT)
label = frame.add_label('Difficulty : 200')
label = frame.add_label(' ')
button1 = frame.add_button('Antoine', button_handler1)
label = frame.add_label(' ')
button2 = frame.add_button('Normal', button_handler2)
label = frame.add_label(' ')
button3 = frame.add_button('Hardcore', button_handler3)
label = frame.add_label(' ')
button4 = frame.add_button('Allaz', button_handler4)

# initialize ship and sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_quer = None
a_falling = None
gravity = False
rock_group = set([])
quer_group = set([])
falling_group = set([])
bonus_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
