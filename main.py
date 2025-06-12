import pygame
import sys
import random
import math

# original grid
original_grid = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,0,1,1,0,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,0,0,1,0,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
pygame.init() #initializing pygame modules 

#colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (225, 225, 0)
WHITE=(255, 255, 255)
RED=(255, 0, 0)
PINK=(255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

#grid dimensions
GRID_WIDTH=15
GRID_HEIGHT=16

#screen dimensions
SCREEN_WIDTH = 600
CELL_SIZE = 40
SCREEN_HEIGHT = 650


#boolean value of game state
PLAYING = 0 #when the game is running
GAME_OVER = 1

#will store the current state of the game
game_state = PLAYING

# create the screen of the game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man") #will appear on top of the window

# Font for score 
font = pygame.font.Font(None,36)

#game grid
grid = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,0,1,1,0,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,0,0,1,0,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
#pacman
pacman = {
'x':1, 'y':1, 'direction' : 3, 'mouth_open': False
}

#ghosts

ghosts = [ {'x':1, 'y':13, 'color' : RED}
   , {'x':13, 'y':13, 'color' : PINK},
   {'x':13, 'y':13, 'color' : CYAN} ,
   {'x':11, 'y':13, 'color' : ORANGE}
]

#SCORE
score = 0

#Game loop
clock= pygame.time.Clock()
running = True


#Movement delays
pacman_move_delay = 150
ghost_move_delay = 300
mouth_anim_delay = 600

#timing variables
last_pacman_move_time = 0
last_ghost_move_time = 0
last_mouth_anim_time = 0

def move_pacman():
    global score
    dx,dy =[(1,0),(0,1),(-1,0),(0,-1)] [pacman['direction']]
    new_x,new_y = pacman ['x'] + dx, pacman['y'] + dy
    if grid [new_y][new_x] != 1: #if it equals to 1, it means there is a wall
        pacman['x'], pacman['y'] = new_x, new_y #updating position
        if grid[new_y][new_x]==0:
         grid[new_y][new_x]=2  # 2 means already visited, empty
         score+=10

def move_ghost(ghost):
    dx = pacman['x'] - ghost['x']
    dy = pacman['y'] - ghost['y']

    directions = []
    if abs(dx) > abs(dy):
        # prioritize horizontal movement
        if dx > 0:
            directions.append((1, 0))
        else:
            directions.append((-1, 0))
        if dy != 0:
            directions.append((0, 1 if dy > 0 else -1))
    else:
        # prioritize vertical movement
        if dy > 0:
            directions.append((0, 1))
        else:
            directions.append((0, -1))
        if dx != 0:
            directions.append((1 if dx > 0 else -1, 0))

    # random shuffle if stuck
    directions += [(1, 0), (-1, 0), (0, 1), (0, -1)]
    tried = set()

    for d in directions:
        if d in tried:
            continue
        new_x = ghost['x'] + d[0]
        new_y = ghost['y'] + d[1]
        tried.add(d)
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and grid[new_y][new_x] != 1:
            ghost['x'] = new_x
            ghost['y'] = new_y
            break


def draw_pacman():
    x = pacman['x'] * CELL_SIZE + CELL_SIZE // 2 #to be centered
    y = pacman['y'] * CELL_SIZE + CELL_SIZE // 2 + 50  # +50 for top margin (score area)

    #douth opening angle (0 = closed, 45 = open)
    mouth_opening = 45 if pacman['mouth_open'] else 0

    #pacman body
    pygame.draw.circle(screen, YELLOW, (x, y), CELL_SIZE // 2)

    #mouth angle depending on direction
    if pacman['direction'] == 0:      # Right
        start_angle = 360 - mouth_opening / 2
        end_angle = mouth_opening / 2
    elif pacman['direction'] == 3:    # Down 
        start_angle = 90 - mouth_opening / 2
        end_angle = 90 + mouth_opening / 2
    elif pacman['direction'] == 2:    # Left 
        start_angle = 180 - mouth_opening / 2
        end_angle = 180 + mouth_opening / 2
    else:                             # Up 
        start_angle = 270 - mouth_opening / 2
        end_angle = 270 + mouth_opening / 2

    #little arc cicle as his mouth
    pygame.draw.arc(
        screen, BLACK,
        (x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE),
        math.radians(start_angle), math.radians(end_angle),
        CELL_SIZE // 2
    )

    #draw lines from center to the mouth edges ("pizza slice")
    mouth_line_end_x = x + math.cos(math.radians(start_angle)) * CELL_SIZE // 2
    mouth_line_end_y = y - math.sin(math.radians(start_angle)) * CELL_SIZE // 2
    pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)

    mouth_line_end_x = x + math.cos(math.radians(end_angle)) * CELL_SIZE // 2
    mouth_line_end_y = y - math.sin(math.radians(end_angle)) * CELL_SIZE // 2
    pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)


def draw_ghost(ghost):
    # grid position to pixel position
    x = ghost['x'] * CELL_SIZE + CELL_SIZE // 2
    y = ghost['y'] * CELL_SIZE + CELL_SIZE // 2 + 50

    # body
    body_rect = pygame.Rect(x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE)
    pygame.draw.circle(screen, ghost['color'], (x, y - CELL_SIZE // 4), CELL_SIZE // 2)
    pygame.draw.rect(screen, ghost['color'], (x - CELL_SIZE // 2, y - CELL_SIZE // 4, CELL_SIZE, CELL_SIZE // 2))

    #eyes
    eye_radius = CELL_SIZE // 6
    pupil_radius = CELL_SIZE // 10
    eye_offset_x = CELL_SIZE // 5
    eye_offset_y = CELL_SIZE // 5

    for offset in [-eye_offset_x, eye_offset_x]:
        eye_x = x + offset
        eye_y = y - CELL_SIZE // 4
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), eye_radius)
        pygame.draw.circle(screen, BLUE, (eye_x, eye_y), pupil_radius)

def reset_game():
    global pacman, ghosts, score, grid, game_state
    global last_pacman_move_time, last_ghost_move_time, last_mouth_anim_time

    pacman = {'x': 1, 'y': 1, 'direction': 3, 'mouth_open': False}
    score = 0
    ghosts[:] = [
        {'x': 1, 'y': 13, 'color': RED},
        {'x': 13, 'y': 13, 'color': PINK},
        {'x': 13, 'y': 13, 'color': CYAN},
        {'x': 11, 'y': 13, 'color': ORANGE},
    ]
    grid[:] = [row[:] for row in original_grid]

    game_state = PLAYING
    current_time = pygame.time.get_ticks()
    last_pacman_move_time = current_time
    last_ghost_move_time = current_time
    last_mouth_anim_time = current_time

#game over
def draw_game_over():
   screen.fill(BLACK)
   game_over_font = pygame.font.Font(None,64)
   score_font = pygame.font.Font(None, 48)
   restart_font = pygame.font.Font(None,64)

   game_over_text = game_over_font.render("GAME OVER!", True, RED)
   score_text = score_font.render(f"Final score: {score}", True , WHITE)
   restart_text = restart_font.render( "Press space to restart", True, YELLOW)

   screen.blit(game_over_text,(SCREEN_WIDTH // 2- game_over_text.get_width()//2 , SCREEN_HEIGHT //3 ))
   screen.blit(score_text,(SCREEN_WIDTH // 2- score_text.get_width()//2 , SCREEN_HEIGHT //2 ))
   screen.blit(restart_text,(SCREEN_WIDTH // 2- restart_text.get_width()//2 ,2* SCREEN_HEIGHT //3 ))



#main game loop
running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        elif event.type == pygame.KEYDOWN:
            if game_state == PLAYING:
                if event.key == pygame.K_UP:
                    pacman['direction'] = 3
                elif event.key == pygame.K_DOWN:
                    pacman['direction'] = 1
                elif event.key == pygame.K_LEFT:
                    pacman['direction'] = 2
                elif event.key == pygame.K_RIGHT:
                    pacman['direction'] = 0
            elif game_state == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    reset_game()

    if game_state == PLAYING:
        if current_time - last_pacman_move_time > pacman_move_delay:
            move_pacman()
            last_pacman_move_time = current_time

        if current_time - last_ghost_move_time > ghost_move_delay:
            for ghost in ghosts:
                move_ghost(ghost)
            last_ghost_move_time = current_time

        if current_time - last_mouth_anim_time > mouth_anim_delay:
            pacman['mouth_open'] = not pacman['mouth_open']
            last_mouth_anim_time = current_time

    screen.fill(BLACK)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, 50 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif grid[y][x] == 0:
                pygame.draw.circle(screen, YELLOW, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2 + 50), 3)

    draw_pacman()

    for ghost in ghosts:
        draw_ghost(ghost)

    score_text = font.render(f"score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    for ghost in ghosts:
        if pacman['x'] == ghost['x'] and pacman['y'] == ghost['y']:
            game_state = GAME_OVER

    if game_state == GAME_OVER:
        draw_game_over()      

    pygame.display.flip()
    clock.tick(60)
pygame.quit()

sys.exit()
              

              
