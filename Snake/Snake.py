import random
import pygame

#color settings
SNAKE = (41,186,62)
BACKGROUND = (224,225,246)
TARGET = (117,190,49)
DARK_GROUND = (124,115,46)

#pygame init
b_number = 50
b_size = 10
w_size = b_size*b_number
size = (w_size,w_size)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Psycho Snake")
pygame.init()

#font init
arial18 = pygame.font.SysFont('arial',18, False, False)
arial30 = pygame.font.SysFont('arial',30, False, False)

clock = pygame.time.Clock()

#snake
class Snake():
    x = []
    y = []
    direction = 0
    step = 1
    status = 1
    def __init__(self):
        self.x.append(b_number/2)
        self.y.append(b_number/2)
        for i in range(5):
            self.__grow()
        self.length = len(self.x)
        self.status = 1
    def reset(self):
        self.x = []
        self.y = []
        self.x.append(b_number/2)
        self.y.append(b_number/2)
        for i in range(5):
            self.__grow()
        self.length = len(self.x)
        self.direction = 0
        self.status = 1

    def __if_collision(self):
        for block in range(1,self.length):
            if(self.x[0] == self.x[block] and self.y[0] == self.y[block]):
                return True
        return False

    def __grow(self):
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])
        self.length = len(self.x)

    def update(self):
        for block in range(self.length-1,0,-1):
            self.x[block] = self.x[block-1]
            self.y[block] = self.y[block-1]
        if(self.direction == 0):
            self.y[0] -= 1
        elif(self.direction == 1):
            self.y[0] += 1
        elif(self.direction == 2):
            self.x[0] -= 1
        elif(self.direction == 3):
            self.x[0] += 1
        if(self.x[0] < 0 or self.x[0] > b_number or self.y[0] < 0 or self.y[0] > b_number or self.__if_collision()):
            self.status = 0

    def move_up(self):
        if self.y[0] != self.y[1]+1:
            self.direction = 0
    def move_down(self):
        if self.y[0] != self.y[1]-1:
            self.direction = 1
    def move_left(self):
        if self.x[0] != self.x[1]+1:
            self.direction = 2
    def move_right(self):
        if self.x[0] != self.x[1]-1:
            self.direction = 3
    def draw(self):
        for block in range(0,self.length):
            pygame.draw.rect(screen,SNAKE,(self.x[block]*b_size,self.y[block]*b_size,b_size,b_size))
    def is_overlapped(self, x, y):
        for block in range(self.length):
            if(x == self.x[block] and y == self.y[block]):
                return True
        return False
    def try_eat(self, target):
        if(self.x[0] == target.x and self.y[0] == target.y):
            self.__grow()
            return True
        return False

snake = Snake()

#target
class Target():
    x = None
    y = None
    def __init__(self):
        pass
    def reset(self):
        global snake
        self.x = random.randint(0,b_number-1)
        self.y = random.randint(0,b_number-1)
        while snake.is_overlapped(self.x, self.y):
            self.x = random.randint(0,b_number-1)
            self.y = random.randint(0,b_number-1)
    def draw(self):
        pygame.draw.rect(screen,TARGET,(self.x*b_size,self.y*b_size,b_size,b_size))

target = Target()

done = False
start = False
score = 0
max_score = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if start == False:
                start = True
                score = 0
                snake.reset()
                target.reset()
            if event.key == pygame.K_UP:
                snake.move_up()
            elif event.key == pygame.K_DOWN:
                snake.move_down()
            elif event.key == pygame.K_LEFT:
                snake.move_left()
            elif event.key == pygame.K_RIGHT:
                snake.move_right()

    screen.fill(BACKGROUND)
    if start == True:
        snake.update()
        if snake.status == 0:
            text = arial18.render("Press any key to play",True,DARK_GROUND)
            textX = text.get_rect().width
            textY = text.get_rect().height
            screen.blit(text,((w_size/2 - (textX / 2)),(w_size/4*3 - (textY / 2))))
            start = False
        else:
            if snake.try_eat(target):
                target.reset()
                score += 1
        target.draw()
        text = arial18.render("Score : " + str(score),True,DARK_GROUND)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((w_size*0.8 - (textX / 2)),(w_size*0.8 - (textY / 2))))

    else:
        text = arial30.render("Score : " + str(score),True,DARK_GROUND)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((w_size*0.5 - (textX / 2)),(w_size*0.4 - (textY / 2))))

        text = arial18.render("Max Score : " + str(max_score),True,DARK_GROUND)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((w_size*0.5 - (textX / 2)),(w_size*0.4 + 3* (textY / 2))))

        text = arial18.render("Press any key to play",True,DARK_GROUND)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((w_size/2 - (textX / 2)),(w_size/4*3 - (textY / 2))))
    
        if score >= max_score and score != 0:
            max_score = score
            text = arial30.render("New record!",True,DARK_GROUND)
            textX = text.get_rect().width
            textY = text.get_rect().height
            screen.blit(text,((w_size*0.5 - (textX / 2)),(w_size*0.4 - 3 * (textY / 2))))
    snake.draw()
   
    pygame.display.flip()        
    clock.tick(10)
pygame.quit()