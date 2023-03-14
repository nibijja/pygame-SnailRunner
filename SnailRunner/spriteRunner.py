from random import randint, choice
import pygame
from sys import exit


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.gravity = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.jumpSound = pygame.mixer.Sound('audio/jump.mp3')
        self.jumpSound.set_volume(0.04)

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jumpSound.play()

    def applyGravity(self):
        self.rect.y += self.gravity
        self.gravity += 1
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.animation()
        self.input()
        self.applyGravity()


class Obstacles(pygame.sprite.Sprite):

    def __init__(self, type):
        super().__init__()
        if type == "snail":
            snail_glide_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_glide_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.obstacle = [snail_glide_1, snail_glide_2]
            yPos = 300

        else:
            fly_flap_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_flap_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.obstacle = [fly_flap_1, fly_flap_2]
            yPos = 210

        self.animationIndex = 0
        self.image = self.obstacle[self.animationIndex]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), yPos))

    def animationState(self):
        self.animationIndex += 0.1
        if self.animationIndex >= len(self.obstacle):
            self.animationIndex = 0
        self.image = self.obstacle[int(self.animationIndex)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animationState()
        self.rect.x -= 5
        self.destroy()


def gameScore():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surface = textFont.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time


def collision():
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        return False
    else:
        return True


def introScreen():
    screen.fill((94, 129, 162))
    screen.blit(player_scale, player_scale_rectangle)
    screen.blit(intro_title, intro_rectangle)

    score_surface = textFont.render(f'Score: {score}', False, (111, 196, 169))
    score_rectangle = score_surface.get_rect(center=(400, 350))

    if score == 0:
        screen.blit(intro_message, intro_message_rectangle)
    else:
        screen.blit(score_surface, score_rectangle)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
textFont = pygame.font.Font("font/pixeltype.ttf", 50)
clock = pygame.time.Clock()
gameActive = False
score = 0

bgSound = pygame.mixer.Sound('audio/music.wav')
bgSound.play(loops=-1)
bgSound.set_volume(0.04)

sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# GAME INTRO SCREEN
# player logo
intro_title = textFont.render("Snail Runner", False, (111, 196, 169))
intro_rectangle = intro_title.get_rect(center=(400, 80))

# intro title text
player_stand = pygame.image.load("graphics/player/player_stand.png")
player_scale = pygame.transform.rotozoom(player_stand, 0, 2)
player_scale_rectangle = player_scale.get_rect(center=(400, 200))

# intro Message
intro_message = textFont.render("Press SPACE to start", False, (111, 196, 169))
intro_message_rectangle = intro_message.get_rect(center=(400, 350))

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()

obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if gameActive:
            if event.type == obstacleTimer:
                obstacles.add(Obstacles(choice(["fly", "snail", "snail", "snail"])))

        # STRAT THE GAME IF NOT ACTIVE
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameActive = True
                start_time = pygame.time.get_ticks()

    if gameActive:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        player.draw(screen)
        player.update()
        obstacles.draw(screen)
        obstacles.update()
        gameActive = collision()
        score = gameScore()

    else:
        introScreen()

    pygame.display.update()
    clock.tick(60)