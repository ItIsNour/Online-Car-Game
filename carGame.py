import random
import time
import pygame
from additionalFunctions import scale_image

pygame.init()

# Cars
blueCar = pygame.image.load("images/blueCar.png")
greenCar = pygame.image.load("images/greenCar.png")
pinkCar = pygame.image.load("images/pinkCar.png")


# Obstacles
obsBus = pygame.image.load("images/obsBus.png")
obsGreen = pygame.image.load("images/obsGreen.png")
obsWhite = pygame.image.load("images/obsWhite.png")
obsYellow = pygame.image.load("images/obsYellow.png")


borders = scale_image(pygame.image.load("images/borders.png"),1.001)
borders_mask = pygame.mask.from_surface(borders)

borderY = pygame.image.load("images/borderY.png")
borderY_mask = pygame.mask.from_surface(borderY)


road = scale_image(pygame.image.load("images/road.png"),0.977)

window = pygame.image.load("images/window.png")
width, height = window.get_width(), window.get_height()
win = pygame.display.set_mode((width, height))

# Window name
pygame.display.set_caption("Client")

# Variable that detects number of clients playing
clientNumber = 0


class ObstaclesLeft():

    img1 = obsWhite
    img2 = obsGreen

    def __init__(self, x, y,speedy):
        self.img = self.img1
        self.x = x
        self.y = y
        self.speedy = speedy
        self.score = 0
        self.obs = 0


    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def update(self):
        self.y = self.y+self.speedy*2


        if self.y > height:
            self.y = 0-self.img.get_height()
            self.x = random.randrange(73,303)
            self.score = self.score+2
            self.obs = random.randrange(0, 3)
            if self.obs == 0:
                self.img = self.img1
            elif self.obs == 1:
                self.img = self.img2
            elif self.obs == 2:
                self.img = self.img1
            elif self.obs == 3:
                self.img = self.img2




class ObstaclesRight():

    img1 = obsBus
    img2 = obsYellow

    def __init__(self, x, y,speedy):
        self.img = self.img1
        self.x = x
        self.y = y
        self.speedy = speedy
        self.score = 0
        self.obs = 0


    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def update(self):
        self.y = self.y+self.speedy*2


        if self.y > height:
            self.y = 0-self.img.get_height()
            self.x = random.randrange(330,620)
            self.score = self.score+2
            self.obs = random.randrange(0, 3)
            if self.obs == 0:
                self.img = self.img1
            elif self.obs == 1:
                self.img = self.img2
            elif self.obs == 2:
                self.img = self.img1
            elif self.obs == 3:
                self.img = self.img2

class Car():
    img = blueCar
    # startPosition = (313, 350)
    def __init__(self,x,y,car_vel):
        self.img = self.img
        self.x = x
        self.y = y
        self.car_vel = car_vel
        self.acceleration = 0.3


    def draw(self, win):
        win.blit(self.img,(self.x,self.y))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.car_vel

        if keys[pygame.K_RIGHT]:
            self.x += self.car_vel

        if keys[pygame.K_UP]:
            self.y -= self.car_vel

        if keys[pygame.K_DOWN]:
            self.y += self.car_vel


    def collide(self, mask, x=44, y=-2):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x -x), int(self.y - y))
        intersection_point = mask.overlap(car_mask, offset)
        return intersection_point

    def bounce(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x, self.y = (73,self.y)

        if keys[pygame.K_RIGHT]:
            self.x, self.y = (620,self.y)

    def boundary(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y<210:
            self.y = 75
        if keys[pygame.K_DOWN] and self.y > 210:
            self.y = 400

def score(score):
    font = pygame.font.Font(None,25)
    text = font.render("Score: "+str(score),True,'white')
    win.blit(text,(0, 0))


def gameOver():
    font = pygame.font.Font(None, 80)
    text = font.render("Game Over!",True, 'white')
    text_width = text.get_width()
    text_height = text.get_height()
    x = int(width/2 - text_width/2)
    y = int(height/2 - text_height/2)
    win.blit(text, (260, y))
    pygame.display.update()
    time.sleep(2)
    main()





def redraw(win,images,car,roadx,roady, obstacle,obstacleR):
    for img, pos in images:
        win.blit(img, pos)
    win.blit(borders, [44, -2])
    win.blit(road, [roadx, roady - height])  # minus window height
    win.blit(road, [roadx, roady])
    car.draw(win)
    obstacle.draw(win)
    obstacleR.draw(win)
    score(obstacle.score)
    pygame.display.update()


# In python 0,0 is top left
images = [(borderY,(0,0)),(window,(0,0)),(road,(0,0))]


def read_pos(str):
    str = str.split(", ")
    return  int(str[0]), int(str[1])

def  make_pos(tup):
    return str(tup[0] + "," + str(tup[1]))






def main():
    run = True
    clock = pygame.time.Clock()
    roadx = 0
    roady = 0
    car_vel = 10
    road_vel = 5
    max_vel = 15
    acceleration = 0.3

    car_x = 313
    car_y = 350

    obstacle_x = random.randrange(73,303)
    obstacle_x_R = random.randrange(330, 620)
    obstacle_y = -100




    car = Car(car_x,car_y,car_vel)
    obstacle = ObstaclesLeft(obstacle_x, obstacle_y, road_vel)
    obstacleR = ObstaclesRight(obstacle_x_R,obstacle_y,road_vel)


    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        car.move()
        obstacle.update()
        obstacleR.update()


        redraw(win,images, car,roadx,roady,obstacle,obstacleR)

        keys = pygame.key.get_pressed()

        # if keys[pygame.K_UP]:
        #     road_vel = road_vel + acceleration
        # else:
        #     road_vel = road_vel - (acceleration*5)
        #     road_vel = max(road_vel/2,0)
        road_vel = road_vel + acceleration
        roady = roady + min(road_vel, max_vel )
        if (roady == height) or (roady > height):
            roady = 0

        if car.collide(borders_mask) != None:
            car.bounce()
        if car.collide(borderY_mask) != None:
            car.boundary()

        if ((obstacle.x-car.x)<55 and abs(car.y-obstacle.y) <= 124):
            if ((car.x-obstacle.x)<55 and abs(car.y-obstacle.y) <= 124):
                    gameOver()
        if ((obstacleR.x-car.x)<55 and abs(car.y-obstacleR.y) <= 124):
            if ((car.x-obstacleR.x)<55 and abs(car.y-obstacleR.y) <= 124):
                    gameOver()



main()


