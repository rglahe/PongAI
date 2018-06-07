from pygame.locals import *
import pygame 
import time
import numpy as np
import math
import random
import decimal

 
class Player: ####computer now
    x = 600
    y = 250
    speed = 50
    def moveUp(self):
        self.y = self.y - self.speed
        if(self.y <= 0):
            self.y = 0
    def moveDown(self):
        self.y = self.y + self.speed
        if(self.y >= 500):
            self.y = 500
    def moveSame(self):
        self.y = self.y
    def draw(self, surface, image):
        surface.blit(image,(self.x,self.y)) 

class Ball:
    x = 300
    y = 300
    x_velocity = 18
    y_velocity = 6
 
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def update(self):
        self.x = self.x + self.x_velocity
        self.y = self.y + self.y_velocity
        if(self.x <= 0):
            self.x = 0
            self.x_velocity = self.x_velocity * -1
            
        if(self.y <= 0):
            self.y = 0
            self.y_velocity = self.y_velocity * -1
        if(self.y >= 585):
            self.y = 585
            self.y_velocity = self.y_velocity * -1
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y))
    def gameOver(self):
        return
class Menu:
    x = 0
    y = 0
    
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y))
        
class App:
 
    windowWidth = 615
    windowHeight = 600
    player = 0
    ball = 0
    menu = 0
    QMatrix = None
    QMatrixBeen = None
    ratioMatrix = None
    plotMatrix = None
    
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.player = Player() 
        self.ball = Ball(300,300)
        self.menu = Menu()
        self.QMatrix = self.initMatrix()
        self.QMatrixBeen = self.initMatrix()
        self.ratioMatrix = self.initRatio()
        self.plotMatrix = self.initPlot()
    def initPlot(self):
        return np.zeros(100000)
    def initRatio(self):
        temp = np.zeros((600))
        ticker = 0
        value = 0
        for i in range(600):
            temp[i] = value
            ticker = ticker + 1
            if(ticker == 50):
                value += 1
                ticker = 0
        return temp
        
    def initMatrix(self):
        temp = np.zeros((13,13,2,3,12,3))
        return temp
                        
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Pong AI')
        self._running = True
        self._image_surf = pygame.image.load("whiteBar.png").convert()
        self._ball_surf = pygame.image.load("whiteBall.png").convert()
        self._menu_surf = pygame.image.load("menuText.png").convert()
        self._menu2_surf = pygame.image.load("menuTrainedText.png").convert()
        self._menu_training_surf = pygame.image.load("trainingplswait.png").convert()
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        if(self.ball.x >= 585 and self.ball.y >= self.player.y -15 and self.ball.y <= self.player.y + 115):###the extra 15 is to account for image size 
            #####:update velocities
            randX = random.randrange(-30, 30)
            randY = random.randrange(-9, 9)
            self.ball.x_velocity = (self.ball.x_velocity * -1) + randX ##ball reflected off pattle
            self.ball.y_velocity = (self.ball.y_velocity + randY)
            if(self.ball.x > 0 and self.ball.x < 30):
                self.ball.x = 30
            if(self.ball.x < 0 and self.ball.x > -30):
                self.ball.x = -30
        elif(self.ball.x >= 600):
            self.ball.x_velocity = 0 
            self.ball.y_velocity = 0
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.ball.draw(self._display_surf, self._ball_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
        
    def reinstance(self):
        self.ball = Ball(300,300)
        self.player = Player()
    def drawNewMenu(self):
        self._display_surf.fill((0,0,0))
    def on_menu(self):
        self._display_surf.fill((0,0,0))
        self.menu.draw(self._display_surf,self._menu_surf)
        pygame.display.flip()
        ticker = 0
        nothingHappend = True
        while(nothingHappend):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if(ticker == 1):
                self.menu.draw(self._display_surf,self._menu2_surf)
                pygame.display.flip()
                ticker = 0
            if(keys[K_p]):
                nothingHappend = False
            ###### add keys here to make 20k - 100k tests to train the cpu
            
            if(keys[K_x]):
                self.menu.draw(self._display_surf,self._menu_training_surf)
                pygame.display.flip()
                
                self.TDtraining(100000)   ###TD 100k tests
                print(self.QMatrix[6][6][0][2])
                print(self.QMatrix[7][6][0][0])
                np.savetxt("data.txt",self.plotMatrix)
                
                ticker = 1
            
            if(keys[K_e]):
                self.on_cleanup()
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        menuChecker = True
        
        while( self._running ):
            if(menuChecker):
                self.on_menu()
                self.reinstance()    
            menuChecker = False
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            Xsign = 0
            Ysign = 0
            if(self.ball.x_velocity < 0):
                Xsign = 1
            if(self.ball.y_velocity > 0):
                if(self.ball.y_velocity < 6):
                    Ysign = 2
                else:
                    Ysign = 1
            else:
                if(self.ball.y_velocity > -6):
                    Ysign = 2
                else:
                    Ysign = 0
            paddleP = int(round(12 * (self.player.y /500)))
            if(paddleP >= 12):
                paddleP = 11
            
            if(self.ball.x >= 600):
                self.ball.x = 585
            
            if(self.QMatrix[int(self.ratioMatrix[self.ball.x])][int(self.ratioMatrix[self.ball.y])][Xsign][Ysign][paddleP][0] > self.QMatrix[int(self.ratioMatrix[self.ball.x])][int(self.ratioMatrix[self.ball.y])][Xsign][Ysign][paddleP][1]):
                if(self.QMatrix[int(self.ratioMatrix[self.ball.x])][int(self.ratioMatrix[self.ball.y])][Xsign][Ysign][paddleP][0] > self.QMatrix[int(self.ratioMatrix[self.ball.x])][int(self.ratioMatrix[self.ball.y])][Xsign][Ysign][paddleP][2]):
                    self.player.moveUp()
                else:
                    self.player.moveSame()
            else:
                if(self.QMatrix[int(self.ratioMatrix[self.ball.x])][int(self.ratioMatrix[self.ball.y])][Xsign][Ysign][paddleP][1] > self.QMatrix[int(self.ratioMatrix[self.ball.x])][int(self.ratioMatrix[self.ball.y])][Xsign][Ysign][paddleP][2]):
                    self.player.moveDown()
                else:
                    self.player.moveSame()
                    
 
            if (keys[K_ESCAPE]):
                menuChecker = True
            
            self.ball.update()
            
            self.on_loop()
            self.on_render()
            time.sleep(50.0 / 1000.0)
        self.on_cleanup()

######################################################################################################################################################### TD learning algo
    def TDtraining(self,numTests):
        Pballx = .5
        Pbally = .5
        PballxVel = .03
        PballyVel = .01
        Ppaddle = .4
        PpaddleHeight = .2
        PpaddleChange = .04
        up = 0
        down = 1
        stay = 2
        specialState = False
        for i in range(numTests):
            #print(i)
            specialState = False
            currState = (Pballx,Pbally,PballxVel,PballyVel,Ppaddle)
            count = 0
            gameOn = True
            while(gameOn):
              
                reward = 0
                
############################################################################################################################################3                        
        ################## Now we have the game state. Update based on returns, is next state
    
    
                #####discretize the ball's x and y location
                discreteBallx = math.floor(12 * currState[0])
                discreteBally = math.floor(12 * currState[1])
                
               
                xvelSign = -1
                yvelSign = -1
                #####discretize the ball's x and y velocity
                if(currState[2] > 0):
                    xvelSign = 0
                else:
                    xvelSign = 1

                if(currState[3] > 0):
                    if(currState[3] < .015):
                        yvelSign = 2
                    else:
                        yvelSign = 0
                elif(currState[3] < 0):
                    if(currState[3] > -0.015):
                        yvelSign = 2
                    else:
                        yvelSign = 1
                else:
                    yvelSign = 2

                ##########discretize the player's position
                discretePaddlePosition = math.floor((12 * currState[4]) / (1 - PpaddleHeight))
                if(discretePaddlePosition >= 12):
                    discretePaddlePosition = 11
 
                
                upCount = self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][up]
                downCount = self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][down]
                stayCount = self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][stay]

                upUtility = self.QMatrix[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][up]
                downUtility = self.QMatrix[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][down]
                stayUtility = self.QMatrix[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][stay]

                decision = -1
                
                #########
                #####Make decision based on exploration first, then exploitation
                
                if(upCount < 15 and downCount < 15 and stayCount < 15):
                    if(upCount < downCount):# and upCount < stayCount):
                        if(upCount < stayCount): 
                            decision = up
                            self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][up] += 1
                        else:
                            decision = stay
                            self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][stay] += 1
                    else:
                        if(downCount < stayCount):
                            decision = down
                            self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][down] += 1
                        else:
                            decision = stay
                            self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][stay] += 1
                else:        
                    if(upUtility > downUtility):# and upUtility > stayUtility):
                        if(upUtility > stayUtility):
                            decision = up
                            self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][down] += 1
                        else:
                            decision = stay
                            self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][stay] += 1
                    else:
                        if(downUtility > stayUtility):# and downUtility > stayUtility):
                            decision = down
                            self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][down] += 1
                        else:
                            decision = stay   
                paddle_add = -124421
                if(decision == up):
                    paddle_add = -.04
                if(decision == down):
                    paddle_add = .04
                if(decision == stay):
                    paddle_add = 0
                ######find next state based on decision
                if(currState[4] + paddle_add > 1):
                    nextState = (currState[0] + currState[2], currState[1] + currState[3],currState[2],currState[3], currState[4])
                elif(currState[4] + paddle_add < 0):
                    nextState = (currState[0] + currState[2], currState[1] + currState[3],currState[2],currState[3], currState[4])
                else:
                    nextState = (currState[0] + currState[2], currState[1] + currState[3],currState[2],currState[3], currState[4] + paddle_add)
                
                ####we have next State, check for out of bounds
                if(nextState[0] < 0):
                    nextState = (nextState[0] * -1, nextState[1], nextState[2] * -1, nextState[3],nextState[4])
                if(nextState[1] < 0):
                    nextState = (nextState[0], nextState[1] * -1, nextState[2], nextState[3] * -1, nextState[4])
                if(nextState[1] > 1):
                    nextState = (nextState[0], 2 - nextState[1], nextState[2], nextState[3] * -1, nextState[4])
                if(nextState[0] > 1):#####ball is on paddle side
                    
                    if(nextState[1] >= nextState[4] and nextState[1] <= nextState[4] + PpaddleHeight):#######ball rebounded off paddle
                        #######update velocities
                        randX = decimal.Decimal(random.randrange(-3, 3))/100
                        randY = decimal.Decimal(random.randrange(-3, 3))/200
                        xToMax = (nextState[2] * -1) + float(randX)
                        if(xToMax > 0):
                            if(xToMax < .03):
                                xToMax = .03
                        else:
                            if(xToMax > -.03):
                                xToMax = -.03
                        nextState = (2 - nextState[0], nextState[1], xToMax, nextState[3] + float(randY), nextState[4])
                        reward = 1
                        count += 1
                        
                    else:
                        reward = -1
                        specialState = True
                
                nextDiscreteBallx = math.floor(12 * nextState[0])
                nextDiscreteBally = math.floor(12 * nextState[1])
                
                
                
                nextxvelSign = -1
                nextyvelSign = -1
                #####discretize the ball's x and y velocity
                if(nextState[2] > 0):
                    nextxvelSign = 0
                else:
                    nextxvelSign = 1

                if(nextState[3] > 0):
                    if(nextState[3] < .015):
                        nextyvelSign = 2
                    else:
                        nextyvelSign = 0
                elif(nextState[3] < 0):
                    if(nextState[3] > -0.015):
                        nextyvelSign = 2
                    else:
                        nextyvelSign = 1
                else:
                    nextyvelSign = 2
                ##########discretize the player's position
                nextDiscretePaddlePosition = math.floor((12 * nextState[4]) / (1 - PpaddleHeight))
                if(nextDiscretePaddlePosition >= 12):
                    nextDiscretePaddlePosition = 11
               
                learningRate = 10/(self.QMatrixBeen[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][decision] +10)
                discountFactor = nextDiscreteBallx / 12
            
                if(specialState):
                    self.QMatrix[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][decision] = self.QMatrix[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][decision] + learningRate * -1 ### (reward + discountFactor * self.QMatrix[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][decision])
                    gameOn = False
                
                else:
                    
                    nextUpUtility = self.QMatrix[nextDiscreteBallx][nextDiscreteBally][nextxvelSign][nextyvelSign][nextDiscretePaddlePosition][up]
                    nextDownUtility = self.QMatrix[nextDiscreteBallx][nextDiscreteBally][nextxvelSign][nextyvelSign][nextDiscretePaddlePosition][down]
                    nextStayUtility = self.QMatrix[nextDiscreteBallx][nextDiscreteBally][nextxvelSign][nextyvelSign][nextDiscretePaddlePosition][stay]
                    best = -1
                    if(nextUpUtility > nextDownUtility):
                        if(nextUpUtility > nextStayUtility):
                            best = up
                        else:
                            best = stay
                    elif(nextDownUtility > nextStayUtility):
                        best = down
                    else:
                        best = stay  

                    self.QMatrix[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][decision] = self.QMatrix[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][decision] + (learningRate * ((reward + discountFactor * (self.QMatrix[nextDiscreteBallx][nextDiscreteBally][nextxvelSign][nextyvelSign][nextDiscretePaddlePosition][best] - self.QMatrix[discreteBallx][discreteBally][xvelSign][yvelSign][discretePaddlePosition][decision]))))
            
                    currState = nextState
            
            
            
            self.plotMatrix[i] = count       
               
                
########################################################################################################################################################################################################
#######################################################################################################################################################################################################
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()                    