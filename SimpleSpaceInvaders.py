import math as m
import pygame
import random
pygame.init()

win = pygame.display.set_mode((700,500))
pygame.display.set_caption("Space invaders")

#Klasser
class Space:
    def __init__(self,x,y,width,height,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=vel

    def draw(self,r,g,b):
        pygame.draw.rect(win, (r,g,b), (self.x, self.y, self.width, self.height))

class Romskip(Space):
    def __init__(self,x,y,width,height,vel):
        super().__init__(x,y,width,height,vel)

    def moveRight(self):
        if self.x<660:
            self.x+=self.vel

    def moveLeft(self):
        if self.x>0:
            self.x-=self.vel

class Invaders(Space):
    def __init__(self,x,y,width,height,vel):
        super().__init__(x,y,width,height,vel)

class Kulesprut():
    def __init__(self,x,y,radius,vel):
        self.radius=radius
        self.x=x
        self.y=y
        self.vel=vel

    def skyt(self):
        self.y=self.y-self.vel

    def draw2(self,r,g,b):
        pygame.draw.circle(win,(r,g,b), (self.x,self.y),self.radius)


#Objekter
r1=Romskip(350,450,40,20,3)
kuleList=[]    
invaderList=[]

posx=0
for i in range(20):
    posx=posx+25
    invaderList.append(Invaders(posx,10,20,10,1))
    invaderList.append(Invaders(posx,25,20,10,1))
    invaderList.append(Invaders(posx,40,20,10,1))
    invaderList.append(Invaders(posx,55,20,10,1))
    invaderList.append(Invaders(posx,70,20,10,1))


#Funksjoner
def more():
    kuleList.append(Kulesprut(r1.x,r1.y,3,3))

invader_vel = 1  

def move_invaders():
    global invader_vel
    shift_ned = False

    for invader in invaderList:
        if invader.x > 680 or invader.x < 0:
            invader_vel *= -1
            shift_ned = True
            break  


    for invader in invaderList:
        invader.x += invader_vel
        if shift_ned:
            invader.y += 10

#Stjerne funksjoner
stjerner = []
for _ in range(50):  
    stjerner.append([random.randint(0,700), random.randint(0,500), random.randint(1,3)]) 

def draw_stars():
    for stjerne in stjerner:
        pygame.draw.circle(win, (255,255,255), (stjerne[0], stjerne[1]), stjerne[2])
       
        stjerne[1] += 0.5
        if stjerne[1] > 500: 
            stjerne[1] = 0
            stjerne[0] = random.randint(0,700)

#Game over Funksjon
def check_game_over():
    for invader in invaderList:
        if invader.y + invader.height >= r1.y:
            return True
    return False

#Hovedloop
run = True
while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                more()

    keys = pygame.key.get_pressed()
        
    win.fill((0,0,0))

    draw_stars()  

    #romskip-bevegelse
    if keys[pygame.K_RIGHT]:
        r1.moveRight()
    if keys[pygame.K_LEFT]:
        r1.moveLeft()
    r1.draw(0,0,255)
    
    #kuler
    for kule in kuleList:
        kule.draw2(0,255,0)
        kule.skyt()
    
    #invaders
    move_invaders()
    for invader in invaderList:
        invader.draw(255,0,0)

    #sjekk kollisjon kuler og invaders
    destroyList=[]
    destroykuler=[]
    for i in range(len(invaderList)):
        for j in range(len(kuleList)):
            x1=kuleList[j].x
            y1=kuleList[j].y
            x2=invaderList[i].x
            y2=invaderList[i].y
            avstand=m.sqrt(((x2-x1)**2)+((y2-y1)**2))
            if avstand<13:
                destroyList.append(i)
                destroykuler.append(j)

    for k in range(len(destroyList)):
        invaderList.pop(destroyList[k]-k)

    for k in range(len(destroykuler)):
        kuleList.pop(destroykuler[k]-k)
    
    if len(invaderList)==0:
        run=False
        print("GODT JOBBET, DU VANT!")
    
    if check_game_over():
        run = False
        print("GAME OVER! Du tapte!")
        
    pygame.display.update() 
pygame.quit()
