import pygame
import random



class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, color, text, text_color, text_size, shift_x, shift_y, center=False):
        super().__init__()


        font = pygame.font.SysFont("Arial", text_size)
        self.rendered_text = font.render(text, 1, text_color)

        self.image = pygame.Surface((self.rendered_text.get_width()+shift_x*2, self.rendered_text.get_height()+shift_y*2))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        if center:
            self.rect.x = x - self.rendered_text.get_width() // 2 - shift_x
            self.rect.y = y - self.rendered_text.get_height() // 2 - shift_y
        else:
            self.rect.x = x
            self.rect.y = y

        self.shift_x = shift_x
        self.shift_y = shift_y

    def check_collide(self, x, y):
        return self.rect.collidepoint(x, y)

       

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.rendered_text, (self.rect.x + self.shift_x, self.rect.y + self.shift_y))

class ButtonIcon(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, center=False):
        super().__init__()



        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def check_collide(self, x, y):
        return self.rect.collidepoint(x, y)

       

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, width, height, player_image=None, bg_color="green"):
        super().__init__()


        if player_image:
            self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(bg_color)


        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
       
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed=0):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

       
    def blit(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player_Control(Player):
    # def __init__(self, player_image, x, y, width, height, speed):
    #     super().__init__(player_image, x, y, width, height, speed)


    def move(self):
        keys_pressed = pygame.key.get_pressed()


        if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_TAB] or keys_pressed[pygame.K_SPACE]:
            self.fire()


    def fire(self):
        bullet = Bullet("images/bullet.png", self.rect.centerx - 15 / 2, self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(Player):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > HEIGHT:
            self.spawn()
            lost += 1

    def spawn(self):
        self.rect.x = random.randint(80, WIDTH - 80)
        self.rect.y = -self.image.get_height() + random.randint(-20, -10)


    def set_start(self):
        self.rect.y = -self.rect.width + random.randint(-20, -10)


class Bullet(Player):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def set_start(self):
        self.rect.y = -self.rect.width + random.randint(-20, -10)


      


pygame.mixer.init()
#  фонова музика
pygame.mixer.music.load('music/space.ogg')
pygame.mixer.music.play()

# звуки
fire = pygame.mixer.Sound("music/fire.ogg")


# start position
RES = WIDTH, HEIGHT = 700, 500
window = pygame.display.set_mode(RES)
pygame.display.set_caption("Шутер")
background = pygame.transform.scale(pygame.image.load("images/galaxy.jpg"), RES)


# написи виграшу і програшу
pygame.font.init()
custom_font = pygame.font.SysFont("Arial", 70)
font2 = pygame.font.SysFont("Arial", 30)
win = custom_font.render("YOU WIN!", True, (255, 215, 0))
lose = custom_font.render("YOU LOSE!", True, (180, 0, 0))


btn_restart = Button(WIDTH//2, HEIGHT//2, (255, 255, 0), "Грати", (100, 100, 255), 70, 10, 5, True)
btn_restart.image.set_alpha(200)

# btn_test = Button(WIDTH//2, HEIGHT//1.3, (100, 255, 100), "Пауза", (50, 50, 255), 90, 30, 10, True)
# btn_test.image.set_alpha(100)

btn_pause = ButtonIcon(700-60, 10, 50, 50, "images/pause-my.png")



# Спрайти
# ufo = Player("images/ufo.png", 100, 100, 90, 60)
rocket = Player_Control("images/rocket.png", WIDTH // 2, HEIGHT-120, 80, 120, 10)


bullets = pygame.sprite.Group()
ufos = pygame.sprite.Group()
for i in range(6):
    ufos.add(Enemy("images/ufo.png", random.randint(80, WIDTH-80), -60, 80, 50, random.randint(1, 5)))


# ігровий цикл
run = True
finish = False
game_over = False
is_win = False
clock = pygame.time.Clock()
FPS = 60
lost = 0
score = 0
pause = False



while run:

    window.blit(background, (0, 0))
    rocket.blit()
    ufos.draw(window)
    bullets.draw(window)


    text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
    window.blit(text, (5, 10))

    text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
    window.blit(text_lose, (5, 40))

    btn_pause.draw()




    
    if not finish:
        if not pause:
            collides = pygame.sprite.groupcollide(ufos, bullets, False, True)
            for enemy in collides:
                # цей цикл повториться стільки разів, скільки монстрів збито
                enemy.spawn()
                score = score + 1
                # ufo = Enemy('images/ufo.png', random.randint(80, WIDTH - 80), -40, 80, 50, random.randint(1, 5))
                # ufos.add(ufo)

            collides = pygame.sprite.spritecollide(rocket, ufos, False)
            if collides or lost >= 5:
                finish = True
                is_win = False
                for enemy in collides:
                    enemy.spawn()

            if score >= 15:
                finish = True

            rocket.move()
            ufos.update()
            bullets.update()
    else:
        if score >= 15:
            window.blit(win, (WIDTH // 2 - win.get_width() // 2, HEIGHT // 2 - win.get_height() - 100))
        else:
            window.blit(lose, (WIDTH // 2 - lose.get_width() // 2, HEIGHT // 2 - lose.get_height() - 100))
        btn_restart.draw()
        # btn_test.draw()
        


    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if finish and btn_restart.check_collide(*e.pos):
                finish = False
                is_win = False
                lost = 0
                score = 0
                bullets.empty()
                for ufo in ufos:
                    ufo.spawn()
            elif btn_pause.check_collide(*e.pos):
                if pause == False:
                    pause = True 
                else:
                    pause = False

            # elif btn_test.check_collide(*e.pos):
            #     print("\033[95m" + "Test button!")
            #     print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')


    pygame.display.update()
    # clock.tick(FPS)
    pygame.time.delay(50)