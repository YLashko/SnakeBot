import pygame #hotkeys:p - toggle pause
import random

screensize = (800, 800)
scale = 10
canvas_size = (int(screensize[0] / scale),int(screensize[1] / scale))
sc = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()
straight_mov = True
vision = 7
down = [0,1]
up = [0,-1]
left = [-1,0]
right = [1,0]
black = (0,0,0)
green = (0,255,0)
blue = (0,0,255)
red = (255,0,0)
yellow = (255,255,0)
white = (255,255,255)
colors = [black, white, green, red]
map_ = []

for i in range(canvas_size[0]):
    map_.append([])
    for o in range(canvas_size[1]):
        if i == 0 or o == 0 or i == canvas_size[0] - 1 or o == canvas_size[1] - 1:
            map_[i].append(1)
        else:
            map_[i].append(0)


class Snake:
    def __init__(self,coords,color):
        self.coordinates = coords
        self.dir = down
        self.color = color
        
    
    def move(self):
        self.coordinates.append([self.coordinates[len(self.coordinates) - 1][0] + self.dir[0], self.coordinates[len(self.coordinates) - 1][1] + self.dir[1]])
        self.coordinates.pop(0)
        if map_[self.coordinates[len(self.coordinates) - 1][0]][self.coordinates[len(self.coordinates) - 1][1]] == 3:
            self.grow()
        if map_[self.coordinates[len(self.coordinates) - 1][0]][self.coordinates[len(self.coordinates) - 1][1]] == 1:
            return False
        self.map_change()
        return True
        
    def turn(self,dire):
        self.dir = dire
        
    def grow(self):
        self.coordinates.append([])
        for i in range(len(self.coordinates) - 1, 0, -1):
            self.coordinates[i] = self.coordinates[i-1]
        self.place_apple()
        self.map_change()
        
    def map_change(self):
        for i in range(len(self.coordinates)):
            if i == len(self.coordinates) - 1:
                map_[self.coordinates[i][0]][self.coordinates[i][1]] = 2
            else:
                map_[self.coordinates[i][0]][self.coordinates[i][1]] = 1
        
    def generate_apple(self):
        coords = [random.randint(1, canvas_size[0] - 1),random.randint(1, canvas_size[1] - 1)]
        if map_[coords[0]][coords[1]] != 0:
            return self.generate_apple()
        return coords
    
    def place_apple(self):
        coords = self.generate_apple()
        map_[coords[0]][coords[1]] = 3
    
    def frame_fill(self, pixels):
        for i in range(len(pixels)):
            for o in range(len(pixels[0])):
                if pixels[i][o] != 0:
                    if pixels[i][o] == 2:
                        if self.coordinates[len(self.coordinates) - 1] == [i, o]:
                            pygame.draw.rect(sc, self.color, (i * scale, o * scale, scale, scale))
                    else:
                        if self.coordinates == snake[len(snake) - 1].coordinates:
                            pygame.draw.rect(sc, colors[pixels[i][o]], (i * scale, o * scale, scale, scale))
                    
        map_[self.coordinates[0][0]][self.coordinates[0][1]] = 0
        pygame.draw.rect(sc, (0, 0, 0), (self.coordinates[0][0] * scale, self.coordinates[0][1] * scale, scale, scale))
    
    def ai_make_turn(self):
        directional_weights = [0, 0, 0, 0]
        directions = [right, up, left, down]
        for i in range(-vision, vision + 1):
            for o in range(-vision, vision + 1):
                if self.coordinates[len(self.coordinates) - 1][0] + i >= 0 and self.coordinates[len(self.coordinates) - 1][0] + i <= canvas_size[0] - 1 and self.coordinates[len(self.coordinates) - 1][1] + o >= 0 and self.coordinates[len(self.coordinates) - 1][1] + o <= canvas_size[1] - 1:
                    if i > 0 and (o != 0 or i != 0):
                        if map_[self.coordinates[len(self.coordinates)-1][0] + i][self.coordinates[len(self.coordinates) - 1][1] + o] == 1:
                            directional_weights[0] += (23 / (abs(i) + abs(o))**(1.4))
                            if random.randint(0, 11) < 10 and straight_mov:
                                directional_weights[2] -= 0.01
                        elif map_[self.coordinates[len(self.coordinates)-1][0] + i][self.coordinates[len(self.coordinates) - 1][1] + o] == 3:
                            directional_weights[0] -= (100 / (abs(i) + abs(o))**(1.3))
                    if i < 0 and (o != 0 or i != 0):
                        if map_[self.coordinates[len(self.coordinates)-1][0] + i][self.coordinates[len(self.coordinates) - 1][1] + o] == 1:
                            directional_weights[2] += (23 / (abs(i) + abs(o))**(1.4))
                            if random.randint(0, 11) < 10 and straight_mov:
                                directional_weights[0] -= 0.01
                        elif map_[self.coordinates[len(self.coordinates)-1][0] + i][self.coordinates[len(self.coordinates) - 1][1] + o] == 3:
                            directional_weights[2] -= (100 / (abs(i) + abs(o))**(1.3))
                    if o > 0 and (o != 0 or i != 0):
                        if map_[self.coordinates[len(self.coordinates)-1][0] + i][self.coordinates[len(self.coordinates) - 1][1] + o] == 1:
                            directional_weights[3] += (23 / (abs(i) + abs(o))**(1.4))
                            if random.randint(0, 11) < 10 and straight_mov:
                                directional_weights[1] -= 0.01
                        elif map_[self.coordinates[len(self.coordinates)-1][0] + i][self.coordinates[len(self.coordinates) - 1][1] + o] == 3:
                            directional_weights[3] -= (100 / (abs(i) + abs(o))**(1.3))
                    if o < 0 and (o != 0 or i != 0):
                        if map_[self.coordinates[len(self.coordinates)-1][0] + i][self.coordinates[len(self.coordinates) - 1][1] + o] == 1:
                            directional_weights[1] += (23 / (abs(i) + abs(o))**(1.4))
                            if random.randint(0, 11) < 10 and straight_mov:
                                directional_weights[3] -= 0.01
                        elif map_[self.coordinates[len(self.coordinates)-1][0] + i][self.coordinates[len(self.coordinates) - 1][1] + o] == 3:
                            directional_weights[1] -= (100 / (abs(i) + abs(o))**(1.3))
            
        minimal = 10000
        chosen = []
        for i in range(len(directional_weights)):
            if directional_weights[i] <= minimal and directions[i] != [self.dir[0] * (-1), self.dir[1] * (-1)]:
                minimal = directional_weights[i]
        for i in range(len(directional_weights)):
            if directional_weights[i] == minimal and directions[i] != [self.dir[0] * (-1), self.dir[1] * (-1)]:
                chosen.append(directions[i])
        if len(chosen) > 1:
            return chosen[random.randint(0,len(chosen) - 1)]
        else:
            return chosen[0]

snake = [Snake([[10, 1],[10, 2],[10, 3]], blue), Snake([[15, 1],[15, 2],[15, 3]], red), Snake([[20, 1],[20, 2],[20, 3]], green), Snake([[25, 1],[25, 2],[25, 3]], yellow)]
#snake = [Snake([[10, 1], [10, 2], [10, 3]], blue)]
snake[0].frame_fill(map_)
running = True
changed = False
for i in range(3):
    snake[0].place_apple()
paused = False

for i in range(canvas_size[0]):
    for o in range(canvas_size[1]):
        if i == 0 or o == 0 or i == canvas_size[0]-1 or o == canvas_size[1]-1:
            map_[i][o] = 1
mousedown = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if paused:
                    paused = False
                else:
                    paused = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mousedown = False
        if event.type == pygame.MOUSEMOTION:
            mousepos = event.pos
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break
    if mousedown:
        map_[int(mousepos[0] / scale)][int(mousepos[1] / scale)] = 1
        pygame.draw.rect(sc, white, (int(mousepos[0] / scale) * scale, int(mousepos[1] / scale) * scale, scale, scale))
        pygame.display.update()
    if not paused and running:
        x = 0
        for snak in snake:
            if running:
                running = snak.move()
                if len(snake) > 1 and running == False:
                    snake.pop(x)
                    running = True
            snak.frame_fill(map_)
            snak.turn(snak.ai_make_turn())
            x += 1
        pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'Snake {str(clock.get_fps())}FPS Paused:{paused}')
    changed = False