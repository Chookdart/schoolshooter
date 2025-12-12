import sys
import pygame
from random import randint


# Initialize pygame
pygame.init()

shoot_sound = pygame.mixer.Sound("shoot sound.wav")
hurt1 = pygame.mixer.Sound("aray ko.wav")
hurt2 = pygame.mixer.Sound("ha.wav")
life = pygame.mixer.Sound("power up.wav")
wowie = pygame.mixer.Sound("wowie.wav")

lives = 3
font = pygame.font.SysFont(None, 30)

pixel_font = pygame.font.Font("PressStart2P-Regular.ttf", 40)
button_font = pygame.font.Font("PressStart2P-Regular.ttf", 25)



# Window
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python ni Wally")

player_img = pygame.image.load("assets/Player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (40, 40)) 

# Player
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 80, 40, 40)


# Lists
bullets = []
enemies = []
enemies2 = []
life_items = []

enemy_img = pygame.image.load("assets/Bully.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

enemy2_img = pygame.image.load("assets/Bully2.png").convert_alpha()
enemy2_img = pygame.transform.scale(enemy2_img, (40, 40))

life_img = pygame.image.load("assets/C2.png").convert_alpha()
life_img = pygame.transform.scale(life_img, (40, 40))

# Enemy spawn timer
enemy_timer = 0
enemy2_timer = 0
life_timer = 0


def game_over_screen():
    while True:
        screen.fill((10, 10, 20))

        # GAME OVER text
        over_text = pixel_font.render("GAME OVER", True, (255, 0, 0))
        over_rect = over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(over_text, over_rect)

        # Restart button
        restart_text = button_font.render("RESTART", True, (255, 255, 255))
        restart_rect = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 20, 160, 50)
        pygame.draw.rect(screen, (50, 50, 50), restart_rect, border_radius=8)
        screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return  # return to main loop

        pygame.display.update()

pygame.mixer.music.load("bd ni wally instrumental.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Main loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and player.left > 0:
        player.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.move_ip(5, 0)
    if keys[pygame.K_SPACE]:
        # Shoot bullet
        bullets.append(pygame.Rect(player.centerx - 2, player.top, 4, 10))

    # Move bullets
    for b in bullets[:]:
        b.move_ip(0, -8)
        
        if b.bottom < 0:
            bullets.remove(b)
            shoot_sound.play()
            shoot_sound.set_volume(0.1)

    # Spawn enemies
    enemy_timer += 1
    if enemy_timer % 150 == 0:
        enemies.append(pygame.Rect(randint(0, WIDTH - 30), 0, 30, 30))
        
    enemy2_timer += 1
    if enemy_timer % 200 == 0:
        enemies2.append(pygame.Rect(randint(0, WIDTH - 30), 0, 30, 30))
        
    life_timer += 1
    if life_timer % 300 == 0:
        life_items.append(pygame.Rect(randint(0, WIDTH - 25), 0, 25, 25))

    # Move enemies
    for e in enemies[:]:
        e.move_ip(0, 1)
        if e.top > HEIGHT:
            enemies.remove(e)
            
    for f in enemies2[:]:
        f.move_ip(0, 1)
        if f.top > HEIGHT:
            enemies2.remove(f)
            
    for a in life_items[:]:
        a.move_ip(0, 2)
        if a.top > HEIGHT:
            life_items.remove(a)

    # Bullet–enemy collision
    for b in bullets[:]:
        for e in enemies[:]:
            if b.colliderect(e):
                bullets.remove(b)
                enemies.remove(e)
                hurt1.play()
                hurt1.set_volume(0.3)
                break
        for f in enemies2[:]:
            if b.colliderect(f):
         #       bullets.remove(b)
                enemies2.remove(f)
                hurt2.play()
                hurt2.set_volume(1)
                break
            
    for e in enemies[:]:
        if e.colliderect(player):
            enemies.remove(e)
            lives -= 1
            wowie.play()
            hurt1.set_volume(0.3)
            
            if lives <= 0:
                hurt1.play()
                hurt1.set_volume(4)
                game_over_screen()
                # RESET game after clicking restart
                lives = 3
                bullets.clear()
                enemies.clear()
                life_items.clear()
                player.topleft = (WIDTH // 2 - 15, HEIGHT - 80)
                
    for f in enemies2[:]:
        if f.colliderect(player):
            enemies2.remove(f)
            lives -= 1
            wowie.play()
            
            if lives <= 0:
                hurt1.play()
                hurt1.set_volume(4)
                game_over_screen()
                

                # RESET game after clicking restart
                lives = 3
                bullets.clear()
                enemies2.clear()
                life_items.clear()
                player.topleft = (WIDTH // 2 - 15, HEIGHT - 80)


    for a in life_items[:]:
        if a.colliderect(player): 
            life_items.remove(a)
            lives += 1
            life.play()
            life.set_volume(3)
            break
                

                
        

    # Drawing
    screen.fill((10, 10, 20))
    
    text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
 
    screen.blit(player_img, player)    # player 

    for b in bullets:
        pygame.draw.rect(screen, (255, 255, 0), b)    # bullets (yellow)

    for e in enemies:                                  # this is enemy
        screen.blit(enemy_img, e)
        
    for f in enemies2:                                  # this is enemy
        screen.blit(enemy2_img, f)
        
    for a in life_items:
        screen.blit(life_img, a)   # enemies (red)
        




    pygame.display.flip()
    pygame.time.delay(10)
