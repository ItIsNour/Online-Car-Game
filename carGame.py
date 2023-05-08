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


road = scale_image(pygame.image.load("images/road.png"),1.005)

finishLine = scale_image(pygame.image.load("images/finishLine.png"),1.1)

startPage = pygame.image.load("images/startPage.png")

window = pygame.image.load("images/window.png")
width, height = window.get_width(), window.get_height()
win = pygame.display.set_mode((width, height))

# Window name
pygame.display.set_caption("Client")

# Variable that detects number of clients playing
clientNumber = 0




# The score to show finish line after
win_score = 50




class ObstaclesLeft():

    img1 = obsWhite
    img2 = obsGreen

    def __init__(self, x, y,speedy,finish):
        self.img = self.img1
        self.x = x
        self.y = y
        self.speedy = speedy
        self.score = 0
        self.obs = 0
        self.finish = finish



    def draw(self, win):
            win.blit(self.img, (self.x, self.y))

    def update(self):
        if self.score < 15:
            self.y = self.y +self.speedy
        else:
            self.y = self.y +self.speedy*2


        if self.y > height:
            self.y = 0-self.img.get_height()
            self.x = random.randrange(73,303)
            if self.finish:
                self.score = self.score
            else:
                self.score = self.score + 2
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
        if self.score < 15:
            self.y = self.y +self.speedy
        else:
            self.y = self.y +self.speedy*2


        if self.y > height:
            self.y = 0-self.img.get_height()
            self.x = random.randrange(330,620)
            if self.score >= win_score:
                self.score = self.score
            else:
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

class PlayerWon():
    img = finishLine
    img2 = road

    def __init__(self, x, y,speedy,finish):
        self.img = self.img
        self.x = x
        self.y = y
        self.speedy = speedy
        self.finish = finish

    def draw(self, win,show):
        if show:
            win.blit(self.img, (80, self.y))



    def update(self,show):
        # self.y = self.y+self.speedy*2
        if show:
            self.speedy = self.speedy + 0.3           # 0.3 is the acceleration
            self.y = self.y + min(self.speedy, 15)    # 15 is the max_vel

        # if self.y > height:
        #     self.y = 0-self.img.get_height()





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

def game_Info(score,startTime):
    font = pygame.font.Font(None,25)
    text = font.render("Score: "+str(score),True,'white')
    win.blit(text,(81, height-50))

    text = font.render("Time: " + str(round(time.time()-startTime)) + "s", True, 'white')
    win.blit(text, (81, height-20))


def gameOver(finish):
    if not finish:
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


def Winner(show,obstacleScore):
    if show:
        font = pygame.font.Font(None, 80)
        text = font.render("YOU WON!",True, 'white')
        text_width = text.get_width()
        text_height = text.get_height()
        x = int(width/2 - text_width/2)
        y = int(height/2 - text_height/2)
        win.blit(text, (260, y))
        pygame.display.update()
        time.sleep(10)
        main()
        # obstacleScore.finish = True





def redraw(win,images,car,roadx,roady, obstacle,obstacleR,won,show,finish,startTime):
    for img, pos in images:
        win.blit(img, pos)
    win.blit(borders, [44, -2])
    win.blit(road, [roadx, roady - height])  # minus window height
    win.blit(road, [roadx, roady])
    won.draw(win, show)
    obstacle.draw(win)
    obstacleR.draw(win)
    game_Info(obstacle.score,startTime)
    car.draw(win)
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
    car_vel = 15
    road_vel = 15
    max_vel = 50
    acceleration = 0.4

    # car_x = 345
    # car_y = 400

    car_x = 475
    car_y = 400


    obstacle_x = random.randrange(73,303)
    obstacle_x_R = random.randrange(330, 620)
    obstacle_y = -100

    started = False
    finish = False
    show = False
    finishY = -100

    startTime = time.time()


    car = Car(car_x,car_y,car_vel)
    obstacle = ObstaclesLeft(obstacle_x, obstacle_y, road_vel,finish)
    obstacleR = ObstaclesRight(obstacle_x_R,obstacle_y,road_vel)

    won = PlayerWon(0,finishY,road_vel,show)


    while run:
        clock.tick(60)

        while not started:
            font = pygame.font.Font(None, 50)
            text = font.render("Press any key to start! ", True, 'white')
            win.blit(startPage, (0, 0))
            win.blit(text, (185, (height/2)-200))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN:
                    started = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        car.move()
        obstacle.update()
        obstacleR.update()
        won.update(show)


        redraw(win,images, car,roadx,roady,obstacle,obstacleR,won,show,finish,startTime)

        keys = pygame.key.get_pressed()

        # if keys[pygame.K_UP]:
        #     road_vel = road_vel + acceleration
        # else:
        #     road_vel = road_vel - (acceleration*5)
        #     road_vel = max(road_vel/2,0)

        if obstacle.score < 15:
            # road_vel = road_vel + acceleration*0.5
            roady = roady + road_vel*2
            if (roady == height) or (roady > height):
                roady = 0
        else:
            # road_vel = road_vel + acceleration*2
            roady = roady + road_vel*3
            if (roady == height) or (roady > height):
                roady = 0

        if car.collide(borders_mask) != None:
            car.bounce()
        if car.collide(borderY_mask) != None:
            car.boundary()

        if ((obstacle.x-car.x)<55 and abs(car.y-obstacle.y) <= 124):
            if ((car.x-obstacle.x)<55 and abs(car.y-obstacle.y) <= 124):
                    gameOver(finish)
        if ((obstacleR.x-car.x)<55 and abs(car.y-obstacleR.y) <= 124):
            if ((car.x-obstacleR.x)<55 and abs(car.y-obstacleR.y) <= 124):
                    gameOver(finish)

        if obstacle.score >= win_score:
            show = True
            if abs(won.y - car.y) < won.img.get_height()/11:
                Winner(show,obstacle)
                print("finish")



main()


