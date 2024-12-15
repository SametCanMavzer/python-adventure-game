import pgzrun
from game_objects import Player, Enemy
from game_settings import *

# Oyun nesneleri
player = Player()
enemies = [Enemy(300, HEIGHT - 100), Enemy(500, HEIGHT - 100)]
platforms = [Rect(0, HEIGHT - 50, WIDTH, 50)]

# Oyun durumu değişkenleri
game_state = "menu"
music_on = True
score = 0
high_score = 0


def draw():
    screen.clear()
    screen.fill((135, 206, 235))

    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()
        draw_hud()
    elif game_state == "game_over":
        draw_game_over()


def draw_menu():
    screen.draw.filled_rect(Rect(300, 200, 200, 50), (0, 255, 0))
    screen.draw.filled_rect(Rect(300, 300, 200, 50), (0, 200, 200))
    screen.draw.filled_rect(Rect(300, 400, 200, 50), (255, 0, 0))

    screen.draw.text("OYUNA BAŞLA", center=(400, 225), fontsize=30)
    screen.draw.text(f"MÜZİK: {'AÇIK' if music_on else 'KAPALI'}", center=(400, 325), fontsize=30)
    screen.draw.text("ÇIKIŞ", center=(400, 425), fontsize=30)
    screen.draw.text(f"YÜKSEK SKOR: {high_score}", center=(400, 500), fontsize=30)


def draw_game():
    for platform in platforms:
        screen.draw.filled_rect(platform, (0, 150, 0))

    if player.facing == "right":
        screen.blit(player.frames_right[player.frame], player.rect)
    else:
        screen.blit(player.frames_left[player.frame], player.rect)

    for enemy in enemies:
        screen.draw.filled_rect(enemy.rect, (255, 0, 0))


def draw_hud():
    screen.draw.text(f"SKOR: {int(score)}", topleft=(10, 10), fontsize=30, color="white")
    screen.draw.text(f"CAN: {player.health}", topleft=(10, 40), fontsize=30, color="white")
    screen.draw.filled_rect(Rect(WIDTH - 60, 10, 50, 30), (255, 0, 0))
    screen.draw.text("EXIT", center=(WIDTH - 35, 25), fontsize=20)


def draw_game_over():
    screen.fill((0, 0, 0))
    screen.draw.text("OYUN BİTTİ!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=60, color="white")
    screen.draw.text(f"SKOR: {int(score)}", center=(WIDTH // 2, HEIGHT // 2 + 10), fontsize=40, color="white")
    screen.draw.text(f"YÜKSEK SKOR: {int(high_score)}", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40,
                     color="white")
    screen.draw.filled_rect(Rect(300, 400, 200, 50), (0, 255, 0))
    screen.draw.text("YENİDEN BAŞLAT", center=(400, 425), fontsize=30)


def update():
    global score, high_score, game_state

    if game_state == "game":
        if music_on and not music.is_playing('background_music'):
            music.play('background_music')
        elif not music_on:
            music.stop()

        if keyboard.left:
            player.vx = -PLAYER_SPEED
            player.facing = "left"
        elif keyboard.right:
            player.vx = PLAYER_SPEED
            player.facing = "right"
        else:
            player.vx = 0

        if keyboard.space and not player.jumping:
            player.vy = JUMP_SPEED
            player.jumping = True
            sounds.jump.play()

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                sounds.collision.play()
                player.health -= 1
                player.rect.x = 50

                if player.health <= 0:
                    if score > high_score:
                        high_score = score
                    game_state = "game_over"

        score += 1 / 60
        player.update()
        for enemy in enemies:
            enemy.update()


def on_mouse_down(pos):
    global game_state, music_on, score, player

    if game_state == "menu":
        if Rect(300, 200, 200, 50).collidepoint(pos):
            game_state = "game"
            score = 0
            player = Player()
            if music_on:
                music.play('background_music')
        elif Rect(300, 300, 200, 50).collidepoint(pos):
            music_on = not music_on
            if not music_on:
                music.stop()
        elif Rect(300, 400, 200, 50).collidepoint(pos):
            quit()

    elif game_state == "game":
        if Rect(WIDTH - 60, 10, 50, 30).collidepoint(pos):
            game_state = "menu"
            music.stop()

    elif game_state == "game_over":
        if Rect(300, 400, 200, 50).collidepoint(pos):
            game_state = "menu"
            score = 0
            player = Player()


pgzrun.go()