import pygame
import sys
import random
from time import sleep


# 게임화면 크기
padWidth = 480
padHeight = 640

# 운석
rockimage = ['rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
             'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', \
             'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
             'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png', \
             'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
             'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png']

# 게임의 객체 이미지 넣기
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

# 게임에 들어갈 것
def initGame():
    global gamePad, clock, background, flight, missile, explosion
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))

    # 게임 이름
    pygame.display.set_caption('준서의 shooting game')
    # 배경 이미지 가져오기
    background = pygame.image.load('background.png')
    # 전투기 이미지 불러오기
    flight = pygame.image.load('fighter.png')
    # 미사일 이미지 불러오기
    missile = pygame.image.load('missile.png')
    #폭발 이미지
    explosion = pygame.image.load('explosion.png')

    clock = pygame.time.Clock()

def runGame():
    global gapdPad, clock, background, flight, explosion

    # 전투기 크기
    flightSize = flight.get_rect().size
    flightWidth = flightSize[0]
    flightHeight = flightSize[1]

    # 전투기 초기 위치
    x = padWidth * 0.45
    y = padHeight * 0.9
    flightX = 0

    # 미사일 좌표
    missileXY = []

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockimage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY=0
    rockSpeed = 5

    isShot = False
    shotcount = 0
    rockpassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            # 게임종료
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            # 전투기 움직이기
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    flightX -= 5
                elif event.key == pygame.K_RIGHT:
                    flightX += 5
            # 미사일 쏘기
                elif event.key == pygame.K_SPACE:
                    missileX = x + flightWidth/2
                    missileY = y - flightHeight
                    missileXY.append([missileX, missileY])
                print(event.key)
            # 전투기 멈추기(키를 안누를때)
            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    flightX = 0

        # 배경넣기
        drawObject(background, 0, 0)

        # 전투기 바뀐 위치로 전투기 좌표 바꾸기
        x += flightX
        # 전투기는 화면 밖으로 나갈 수 없다
        if x < 0:
            x = 0
        elif x > padWidth - flightWidth:
            x = padWidth - flightWidth

        # 전투기 이미지 넣기
        drawObject(flight, x, y)

        # 미사일이 위로 쏴짐
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]
        # 미사일이 운석에 맞았을때
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotcount += 1


                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
        # 미사일 이미지 넣기
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)
        # 운석이 떨어짐
        rockY += rockSpeed
        # 떨어지면 새로
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockimage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0

        # 운석이 미사일에 맞아서 터짐
        if isShot:
            drawObject(explosion, rockX, rockY)
            rock = pygame.image.load(random.choice(rockimage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            isShot = False

        # 운석 그리기
        drawObject(rock, rockX, rockY)


        pygame.display.update()

        clock.tick(60)
    pygame.quit()

initGame()
runGame()

