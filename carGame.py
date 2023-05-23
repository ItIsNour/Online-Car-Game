from network import Network
from additionalFunctions import scale_image
import random
import time
import pygame
import re


pygame.init()

# Cars
blueCar = pygame.image.load("images/blueCar.png")
greenCar = pygame.image.load("images/greenCar.png")
pinkCar = pygame.image.load("images/pinkCar.png")
redCar = pygame.image.load("images/redCar.png")

# Obstacles
obsBus = pygame.image.load("images/obsBus.png")
obsGreen = pygame.image.load("images/obsGreen.png")
obsWhite = pygame.image.load("images/obsWhite.png")
obsYellow = pygame.image.load("images/obsYellow.png")


borders = scale_image(pygame.image.load("images/borders.png"),1.001)
borders_mask = pygame.mask.from_surface(borders)

borderY = pygame.image.load("images/borderY.png")
borderY_mask = pygame.mask.from_surface(borderY)

startPage = scale_image(pygame.image.load("images/startPage.png"),1.005)
readyPage = scale_image(pygame.image.load("images/readyPage.png"), 1)
window = pygame.image.load("images/window.png")
road = scale_image(pygame.image.load("images/road.png"),1.005)

finishLine = scale_image(pygame.image.load("images/finishLine.png"),1.1)



width, height = window.get_width(), window.get_height()
win = pygame.display.set_mode((width, height))

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
    img0 = blueCar
    img1 = greenCar
    img2 = redCar
    img3 = pinkCar

    def __init__(self, playerId, imgID, x, y):
        self.imgID =imgID
        self.x = x
        self.y = y
        self.rect = (x,y,50,50)
        self.vel = 20
        self.playerId = playerId
        self.activePlayers = 0
        self.nickname = ''
        if imgID == 0:
            self.img = self.img0
        elif self.imgID == 1:
            self.img = self.img1
        elif imgID == 2:
            self.img = self.img2
        elif self.imgID == 3:
            self.img = self.img3
        # else random car

    def draw(self, win):
        # pygame.draw.rect(win, self.color, self.rect)
        win.blit(self.img,(self.x,self.y))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, 50, 50)
        self.imgID = self.imgID
        self.playerId = self.playerId

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



def game_Info(score,startTime,car):
    font = pygame.font.Font(None,25)
    text = font.render("Score: "+str(score),True,'white')
    win.blit(text,(81, height-50))

    text = font.render("Time: " + str(round(time.time()-startTime)) + "s", True, 'white')
    win.blit(text, (81, height-20))

    text = font.render("Active Players: " + str(car.activePlayers) , True, 'white')
    # print(car.playerId)
    win.blit(text, (900, 15))


def gameOver(finish,obstacles):
    if not finish:
        font = pygame.font.Font(None, 80)
        text = font.render("Game Over!",True, 'white')
        text_width = text.get_width()
        text_height = text.get_height()
        x = int(width/2 - text_width/2)
        y = int(height/2 - text_height)
        score = "score: "+str(obstacles.score)
        displayScore = font.render(score, True, 'white')
        # win.blit(startPage, (0, 0))
        win.blit(text, (260, y))
        win.blit(displayScore, (300, y+100))
        pygame.display.update()
        time.sleep(2)
        main(inputText)


def Winner(show,obstacleScore):
    if show:
        font = pygame.font.Font(None, 80)
        text = font.render("YOU WON!",True, 'white')
        text_width = text.get_width()
        text_height = text.get_height()
        x = int(width/2 - text_width/2)
        y = int(height/2 - text_height/2)
        win.blit(startPage, (0, 0))
        win.blit(text, (260, y))
        pygame.display.update()
        # time.sleep(10)
        main(inputText)
        # obstacleScore.finish = True





#  Returns initial position in a tuple form to the client
def read_initPos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3])

# Reads the list of all players info sent by server
def read_info(str):
    list=[]
    tup0 = ()
    tup1 = ()
    tup2 = ()
    tup3 = ()
    str = re.findall(r'\(.*?\)', str)
    for i in range(len(str)):
        el = str[i]
        el_len = len(el)
        f_b = el[0]
        fb_removed = el.replace(f_b, "", 1)
        l_b = fb_removed[len(fb_removed) - 1]
        b_removed = fb_removed.replace(l_b, "", 1)
        fin = b_removed.split(",")
        for x in range(len(fin)):
            if i == 0:
                tup0 = tup0 + (int(fin[x]),)
            if i == 1:
                tup1 = tup1 + (int(fin[x]),)
            if i == 2:
                tup2 = tup2 + (int(fin[x]),)
            if i == 3:
                tup3 = tup3 + (int(fin[x]),)

    list.append(tup0)
    list.append(tup1)
    list.append(tup2)
    list.append(tup3)
    return list





def make_info(tup):
    return str(tup[0]) + "," + str(tup[1])+ "," + str(tup[2])+ "," + str(tup[3])+ "," + str(tup[4])


def redrawWindow(win,images,car, car1,roadx,roady, obstacle,obstacleR,won,show,startTime):
    for img, pos in images:
        win.blit(img, pos)
    win.blit(borders, [44, -2])
    win.blit(road, [roadx, roady - height])  # minus window height
    win.blit(road, [roadx, roady])
    won.draw(win, show)
    obstacle.draw(win)
    obstacleR.draw(win)
    game_Info(obstacle.score, startTime,car)
    car.draw(win)
    # car1.draw(win)
    pygame.display.update()


# In python 0,0 is top left
images = [(borderY,(0,0)),(window,(0,0)),(road,(0,0))]


n = Network()






def main(inputText):
    run = True

    roadx = 0
    roady = 0
    car_vel = 15
    road_vel = 15

    obstacle_x = random.randrange(73, 303)
    obstacle_x_R = random.randrange(330, 620)
    obstacle_y = -100

    started = False
    finish = False
    show = False
    finishY = -100

    startTime = time.time()



    startInfo = read_initPos(n.getInfo())
    print(startInfo, "init pos from server")
    car = Car(startInfo[0], startInfo[1], startInfo[2], startInfo[3])
    car1 = Car(0, 0, 0, 0)
    car2 = Car(0, 0, 0, 0)
    car3 = Car(0, 0, 0, 0)



    obstacle = ObstaclesLeft(obstacle_x, obstacle_y, road_vel,finish)
    obstacleR = ObstaclesRight(obstacle_x_R,obstacle_y,road_vel)

    won = PlayerWon(0,finishY,road_vel,show)


    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        # Send the current player class information in a tuple and receives all players info in a list and store it to
        info = read_info(n.send(make_info((car.playerId,car.imgID,car.x, car.y,car.activePlayers))))


        car.update()
        car1.update()
        car2.update()
        car3.update()

        print(" To server:" ,car.playerId,car.imgID,car.x, car.y,car.activePlayers)
        print("From server",info)
        car.activePlayers = info[0][4]
        car.nickname = inputText

        while not started:
            font = pygame.font.Font(None, 50)
            text = font.render("Press any key to start the game! ", True, 'white')
            win.blit(window,(0,0))
            win.blit(readyPage, (0, 0))
            win.blit(text, (165, (height / 2) - 200))
            text = pygame.font.Font(None, 25).render("Active Players: " + str(car.activePlayers), True, 'white')
            # print(car.playerId)
            win.blit(text, (900, 15))
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
                pygame.quit()
                break
        car.move()
        obstacle.update()
        obstacleR.update()
        won.update(show)
        redrawWindow(win,images, car, car1,roadx,roady,obstacle,obstacleR,won,show,startTime)


        if obstacle.score < 15:
            # road_vel = road_vel + acceleration*0.5
            roady = roady + road_vel*2.5
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
                    gameOver(finish,obstacle)
        if ((obstacleR.x-car.x)<55 and abs(car.y-obstacleR.y) <= 124):
            if ((car.x-obstacleR.x)<55 and abs(car.y-obstacleR.y) <= 124):
                    gameOver(finish,obstacle)

        if obstacle.score >= win_score:
            show = True
            if abs(won.y - car.y) < won.img.get_height()/11:
                Winner(show,obstacle)
                print("finish")

        print(inputText)






def startPageWindow():
    # Text box for the player to enter their nickname
    textBox = pygame.Rect(355, 260, 300, 50)
    selectBox = 0
    global inputText
    inputText = ''
    started = False
    font = pygame.font.Font(None, 50)

    while not started:
        text = font.render("Please enter your nickname :) ", True, 'white')
        win.blit(startPage, (0, 0))
        win.blit(text, (200, 200))
        textSurf = pygame.font.Font(None,35).render(inputText, True, 'white')
        win.blit(textSurf, (365,275))
        pygame.draw.rect(win, 'white', textBox, 2)
        pygame.display.flip()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if textBox.collidepoint(x, y):
                    selectBox = 1

            if event.type == pygame.KEYDOWN:
                if selectBox == 1:
                    if event.key == pygame.K_BACKSPACE:
                        inputText = inputText[:-1]
                    else:
                        inputText += event.unicode


            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                print(inputText)
                started = True
                main(inputText)






startPageWindow()


