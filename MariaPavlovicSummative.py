import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20,20)

from random import *

from pygame import *

init()
SIZE = (1000, 700)
screen = display.set_mode(SIZE)	
myClock = time.Clock()

# COLOURS
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
lightRed = (135, 0, 0)
blue = (153, 186, 239)
grey = (198, 198, 198)

# FONTS
menuButtonsText = font.SysFont("Arial Black", 40)
font2 = font.SysFont("Arial Black", 20)
mainScreenFont = font.SysFont("Impact", 100)
# COLOUR VARIABLES FOR BUTTONS
menuButtonA, menuButtonB, menuButtonC, menuButtonD = grey, grey, grey, grey
backButton = black
dropDown = grey
dropButtonA, dropButtonB, dropButtonC = white, white, white
endGameButtonA, endGameButtonB, endGameButtonC = black, black, black
# SCREENS
running = True
startUpScreen = True
menuScreen = False
instructionScreen = False
leaderboardScreen = False
playScreen = False
dropDownScreen = False
endGameScreen = False
pause = False
viewScreen = False
# GAME VARIABLES
characterX = 470  # x pos of character
characterY = 600  # x pos of character
keyLeft, keyRight, keyUp, keyDown = False, False, False, False  # keyboard buttons pressed to move character
sideMoved = ''  # used to know which direction to face character when first running (havn't moved yet)
spaceBar = False  # initializing space bar variable (used later in game)
dropCounter = 0  # counter for the drop down menu on play screen, draws rectangle that gets longer
loadCounter = 0  # counter for the laptop's red bar that has to be stopped by player
characterPos = []  # keeps character's position, used to check if character is fully on top of laptops
randComp = randint(0, 19)  # randomly chooses a laptop to draw the red loading bar on
scoreCount = 0  # score keeper
level = 1  # initializing level
loadCounter2 = 0  # laptops red bar counter in level 3 (where multiple laptops are drawn)
randComp2 = randint(0, 19)  # randomly chooses laptop
loadCounter3 = -60
randComp3 = randint(0, 19)
endGamePos = []  # keep drawing player when player loses game
scoreList = []  # reads lines from file for the scores to decide top 3 later on
movingDown, movingUp = True, True  # values for the icons that bounce up/down on menu screen
highestScore = 0  # initialising high score value
shouldReadScoreFile = True  # so program doesn't read the scores file every time it loops
highScores = {}
icon1Y = 500  # start value of first pic on menu screen that bounces up/down
icon2Y = 270  # start value of other pic on menu screen that bounces up/down
name = ''  # user input for their name
textX = 480  # starting x value of letters when user types in their name (starts in middle, moves to left as user types)
coordinates = [[10,60], [10,200], [10,340], [10,480], [210,60],  # coordinates of each laptop, used to
               [210,200], [210,340], [210,480], [410,60], [410,200],  # find coordinates of laptop that was randomly
               [410,340], [410,480], [610,60], [610,200], [610,340],  # chosen by randComp variable
               [610,480], [810,60], [810,200], [810,340], [810,480]]

# IMAGES
laptop = image.load("laptop2.png")
dataPic = image.load("blackbg.jpg")
character2 = image.load("character2.png")
character3 = image.load("character3.png")
upDownKeys = image.load("updownkeys1.png")
metalplate = image.load("metalplate1.jpeg")
icon1 = image.load("netsecurity1.png")
icon2 = image.load("data-leak1.png")
instructPic = image.load("instructions.jpg")
instructPicBig = image.load("instructionsBig.jpg")
networkPic = image.load("network4.png")
startPic = image.load("startpic.png")
picCounter2 = 0  # counter for second gif to display as a gif
hackerGif = [image.load("21.gif"), image.load("22.gif"), image.load("23.gif"), image.load("24.gif"),
        image.load("25.gif"), image.load("26.gif"), image.load("27.gif"), image.load("28.gif"),
        image.load("29.gif"), image.load("30.gif"), image.load("31.gif")]


def selectValue(x):  # selects value in a key-value pair (the tuple with the player's name as a key and their score as a value)
    return x[1]


def readHighScores():  # takes top 3 high scores
    global highScores, shouldReadScoreFile
    if not shouldReadScoreFile:  # only reads the file once, not through every loop of game
        return
    shouldReadScoreFile = False
    with open("scores.txt", "r") as scores:
        fileLines = scores.readlines()
    scoreList = [line.rstrip().split(':') for line in fileLines]  # reads the lines of the file and splits them on the ':' --> [ ['maria', '13'], ... ]
    scoreData = [[s[0], int(s[1])] for s in scoreList]  # takes scoreList and converts the score string into an integer --> [ ['maria', 13], ... ]
    hsDict = {} # create a dictionary
    for name, score in scoreData: # for each score, store the data in a dictionary
        if name in hsDict:  # checks if certain player already in dictionary
            hsDict[name] = max(score, hsDict[name])  # if yes, player's score is the highest score out of the old one and new one
        else:
            hsDict[name] = score  # if not a key in dict, add their name as a key with the score (value) received that game
    highScores = sorted(hsDict.items(), key=selectValue, reverse=True)[:3]  # comparing the values in dict to each other to find the top 3 high scores
    return


def writeHighScores(score):
    global name, shouldReadScoreFile
    shouldReadScoreFile = True  # every time a new score is added to file, allow file to be read
    scoreFile = open("scores.txt", "a")
    scoreFile.write(name[:-1] + ':' + str(score) + '\n')  # writes down 'name:score' in file
    scoreFile.close()


def drawHackerGif():  # draws a gif that was split into multiple pictures that display as game loops
    global hackerGif, picCounter2
    if picCounter2 <= 10:  # certain value of the counter draws a certain pic of the gif
        screen.blit(hackerGif[0], Rect(50, 60, 105, 78))
    if 10 < picCounter2 <= 20:
        screen.blit(hackerGif[1], Rect(50, 60, 105, 78))
    if 20 < picCounter2 <= 30:
        screen.blit(hackerGif[2], Rect(50, 60, 105, 78))
    if 30 < picCounter2 <= 40:
        screen.blit(hackerGif[3], Rect(50, 60, 105, 78))
    if 40 < picCounter2 <= 50:
        screen.blit(hackerGif[4], Rect(50, 60, 105, 78))
    if 50 < picCounter2 <= 60:
        screen.blit(hackerGif[5], Rect(50, 60, 105, 78))
    if 60 < picCounter2 <= 70:
        screen.blit(hackerGif[6], Rect(50, 60, 105, 78))
    if 70 < picCounter2 <= 80:
        screen.blit(hackerGif[7], Rect(50, 60, 105, 78))
    if 80 < picCounter2 <= 90:
        screen.blit(hackerGif[8], Rect(50, 60, 105, 78))
    if 90 < picCounter2 <= 100:
        screen.blit(hackerGif[9], Rect(50, 60, 105, 78))
    if 100 < picCounter2 <= 110:
        screen.blit(hackerGif[10], Rect(50, 60, 105, 78))
    if picCounter2 > 109:
        picCounter2 = 0
    picCounter2 += 1


def findCoords(computer):  # uses the randComp to see what computer its looking the coordinated for
    global coordinates # uses the predefined list
    return coordinates[computer]


def level1and2(speedOfComps): # level 1 and level 2 (same except for speed of computers loading)
    global loadCounter, randComp, characterPos, endGameScreen, playScreen, endGamePos, scoreCount
    global startUpScreen, endGameButtonA, endGameButtonB, endGameButtonC
    x, y = findCoords(randComp)  # sets x and y values of computer that will be "loaded" first
    draw.rect(screen, red, (x + 23, y + 7, loadCounter, 67))  # loading bar drawn in relation to x and y values of laptop chosen
    loadCounter += speedOfComps  # speed of the loading bar (defined when calling function)
    whackCoords = [x + 15, y, x + 15 + 130, y + 100]  # coordinates of the laptop that the player will need to be in to "disable" laptop
    playerCoords = characterPos  # player coordinates throughout game
    whacked = collision(playerCoords, whackCoords)  # returns True or False for if the player "disabled" laptop
    if whacked:  # if player disabled laptop
        loadCounter = 0  # reset loading bar
        randComp = randint(0, 19)  # reset laptop chosen to display loading bar
    elif loadCounter > 120:  # if loading bar reached the end of the screen
        endGamePos = [x, y]  # where to draw the "data leaked" on the computer
        writeHighScores(scoreCount)
        endGameScreen = True
        endGameButtonA = black
        endGameButtonB = black
        endGameButtonC = black
        playScreen = False


def dataLeakedComp(x,y):  # draws laptop if loading bar reaches end (player fails)
    draw.rect(screen, black, (x + 21, y + 4, 122, 72))
    laptopText = font2.render("DATA", 1, white)
    screen.blit(laptopText, Rect(x + 52, y + 15, 400, 100))
    laptopText = font2.render("LEAKED", 1, white)
    screen.blit(laptopText, Rect(x + 38, y + 35, 400, 100))


def level3():
    global loadCounter2, loadCounter3, randComp2, randComp3, characterPos, endGameScreen, startUpScreen
    global playScreen, endGamePos, endGameButtonA, endGameButtonB, endGameButtonC
    x2, y2 = findCoords(randComp2)  # two different laptops will be drawn
    x3, y3 = findCoords(randComp3)
    draw.rect(screen, red, (x2 + 23, y2 + 7, loadCounter2, 67))
    if loadCounter3 >= 0:  # this is because I set this counter to be -10 (to have a bigger gap between drawing laptops)
        draw.rect(screen, red, (x3 + 23, y3 + 7, loadCounter3, 67))
    loadCounter2 += 0.5  # speed of loading bars
    loadCounter3 += 0.5
    whackCoords2 = [x2 + 15, y2, x2 + 15 + 130, y2 + 100]  # coordinates on laptop that the player has to be on
    whackCoords3 = [x3 + 15, y3, x3 + 15 + 130, y3 + 100]
    playerCoords = characterPos
    whacked2 = collision(playerCoords, whackCoords2)  # check if player disabled computer
    whacked3 = collision(playerCoords, whackCoords3)
    if whacked2:  # if player disables computer, reset loadCounter and random choice
        loadCounter2 = 0
        randComp2 = randint(0, 19)
    if whacked3:
        loadCounter3 = -10
        randComp3 = randint(0, 19)
    if loadCounter2 > 120:  # if loading bar reaches end (player fails)
        endGamePos = [x2, y2]
        writeHighScores(scoreCount)  # add score received to file once player fails game
        endGameScreen = True
        endGameButtonA = black  # resetting variables
        endGameButtonB = black
        endGameButtonC = black
        loadCounter2 = 0
        randComp2 = randint(0, 19)        
        playScreen = False
    if loadCounter3 > 120:
        endGamePos = [x3, y3]
        writeHighScores(scoreCount)
        endGameScreen = True
        endGameButtonA = black  # resetting variables
        endGameButtonB = black
        endGameButtonC = black
        playScreen = False
        loadCounter3 = -10
        randComp3 = randint(0, 19)        


def laptops():  # draws laptops and the loading bars
    global level
    y = 60
    for i in range(4):
        x = 10
        for j in range(5):
            screen.blit(laptop, Rect(x, y, 105, 78))  # draws laptops on its own
            x += 200  # in rows
        y += 140  # and in columns
    if level == 1:
        level1and2(0.3)  # calling on function + speed of loading bar in level 1
    elif level == 2:
        level1and2(0.6)  # speed of loading bar in level 2
    elif level == 3:
        level3()  # level 3 speed defined in function already


def iconMoving(direction):
    global movingDown, movingUp, icon1Y, icon2Y
    if direction == 'down':
        if movingDown:  # checking and deciding movement of picture
            icon2Y += 2
            if icon2Y > 500:
                movingDown = False  # if y value reaches below 560, start moving up
        else:
            icon2Y -= 2
            if icon2Y < 270:  # if y value reaches above 0, start moving down
                movingDown = True
    else:
        if movingUp == True:  # checking and deciding movement of picture
            icon1Y -= 2
            if icon1Y < 270:
                movingUp = False
        else:
            icon1Y += 2
            if icon1Y > 500:
                movingUp = True


def drawMenu():
    global movingDown, icon2Y, icon1Y, movingUp
    draw.rect(screen, white, (0, 0, 1000, 700))
    screen.blit(dataPic, Rect(0, 0, 105, 78))
    screen.blit(metalplate, Rect(450, 20, 105, 78))
    mainScreenText = mainScreenFont.render("DATA", 1, white)  # title
    screen.blit(mainScreenText, Rect(500, 40, 400, 100))
    mainScreenText = mainScreenFont.render("DEFENDER", 1, white)  # title
    screen.blit(mainScreenText, Rect(500, 125, 400, 100))
    drawHackerGif()  # draws the gif
    draw.rect(screen, black, (315, 300, 370, 70))  # first button, play
    draw.rect(screen, menuButtonA, (315, 300, 370, 70), 4)
    mainScreenText = menuButtonsText.render("PLAY", 1, white)
    screen.blit(mainScreenText, Rect(440, 305, 400, 100))
    draw.rect(screen, black, (315, 400, 370, 70))  # second button, instructions
    draw.rect(screen, menuButtonB, (315, 400, 370, 70), 4)
    mainScreenText = menuButtonsText.render("INSTRUCTIONS", 1, white)
    screen.blit(mainScreenText, Rect(330, 405, 400, 100))
    draw.rect(screen, black, (315, 500, 370, 70))  # third button, leader board
    draw.rect(screen, menuButtonC, (315, 500, 370, 70), 4)
    mainScreenText = menuButtonsText.render("LEADERBOARD", 1, white)
    screen.blit(mainScreenText, Rect(335, 505, 350, 100))
    draw.rect(screen, black, (315, 600, 370, 70))  # last button, exit
    draw.rect(screen, menuButtonD, (315, 600, 370, 70), 4)
    mainScreenText = menuButtonsText.render("EXIT", 1, white)
    screen.blit(mainScreenText, Rect(440, 605, 350, 100))
    screen.blit(icon2, Rect(90, icon2Y, 105, 78))  # icons that bounce up/down
    iconMoving('down')
    screen.blit(icon1, Rect(720, icon1Y, 105, 78))
    iconMoving('up')


def movingRight(x, y):  # drawing the character when moving right
    global characterPos
    screen.blit(character2, Rect(x, y, 105, 78))
    characterPos = [x + 5, y + 3, x + 5 + 45, y + 3 + 62]  # reassigning values to characterPos
    return characterPos


def movingLeft(x, y):  # drawing the character when moving left
    global characterPos
    screen.blit(character3, Rect(x, y, 105, 78))
    characterPos = [x + 5, y + 3, x + 5 + 45, y + 3 + 62]  # reassigning values to characterPos
    return characterPos


def notMovingR(x, y):  # drawing the character when moving right
    global characterPos
    screen.blit(character2, Rect(x, y, 105, 78))
    characterPos = [x + 5, y + 3, x + 5 + 45, y + 3 + 62]  # reassigning values to characterPos
    return characterPos


def notMovingL(x, y):  # drawing the character when moving right
    global characterPos
    screen.blit(character3, Rect(x, y, 105, 78))
    characterPos = [x + 5, y + 3, x + 5 + 45, y + 3 + 62]  # reassigning values to characterPos
    return characterPos


def drawDropDown():
    global dropCounter, pause, playScreen, dropDown, dropButtonA, dropButtonB, dropButtonC, running, menuScreen
    global instructionScreen, sideMoved, characterX, characterY
    pause = True
    while pause:
        for evnt in event.get():
            if evnt.type == QUIT:
                unpause()
                running = False
            if evnt.type == MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                if 10 < mx < 50 and 10 < my < 50:
                    unpause()  # if pressed again, un pause game
                elif 25 < mx < 145 and 65 < my < 105:
                    unpause()  # clicked menu button
                    playScreen = False
                    menuScreen = True
                    resetMenuColours()
                elif 25 < mx < 145 and 120 < my < 160:
                    unpause()  # clicked help button
                    playScreen = False
                    backButton = black
                    instructionScreen = True
                elif 25 < mx < 145 and 175 < my < 215:
                    unpause()  # clicked quit button
                    running = False
            if evnt.type == MOUSEMOTION:
                mx, my = evnt.pos
                if 10 < mx < 50 and 10 < my < 50:
                    dropDown = black
                elif 25 < mx < 145 and 65 < my < 105:
                    dropButtonA = red
                elif 25 < mx < 145 and 120 < my < 160:
                    dropButtonB = red
                elif 25 < mx < 145 and 175 < my < 215:
                    dropButtonC = red
                else:
                    dropDown = grey
                    dropButtonA = white
                    dropButtonB = white
                    dropButtonC = white
        if sideMoved == 'left' or sideMoved == '':  # redraw character during pause
            movingLeft(characterX, characterY)
        else:
            movingRight(characterX, characterY)
        draw.rect(screen, black,(10, 50, 150, 50 + dropCounter))
        if dropCounter <= 120:  # draw rectangle increasing
            dropCounter += 20
        else:  # once rectangle background fully drawn, draw buttons that go on top
            draw.rect(screen, dropButtonA, (25, 65, 120, 40))
            dropText = font2.render("MENU", 1, black)
            screen.blit(dropText, Rect(50, 70, 350, 100))
            draw.rect(screen, dropButtonB, (25, 120, 120, 40))
            dropText = font2.render("HELP", 1, black)
            screen.blit(dropText, Rect(54, 125, 350, 100))
            draw.rect(screen, dropButtonC, (25, 175, 120, 40))
            dropText = font2.render("QUIT", 1, black)
            screen.blit(dropText, Rect(53, 180, 350, 100))
        display.flip()


def unpause():
    global pause
    pause = False  # un pause, back to game


def collision(player, laptops):
    global spaceBar, endGameScreen, playScreen, loadCounter, scoreCount, level
    whack = False  # initializing value if player disabled the laptop
    if loadCounter <= 120: # only while load counter hasn't fully loaded
        if spaceBar:  # pressed space
            if laptops[0] < player[0] < laptops[2] and laptops[0] < player[2] < laptops[2] and laptops[1] < player[1] < laptops[3] and laptops[1] < player[3] < laptops[3]:  # if player is fully within coordinates of laptop
                whack = True  # player successfully disabled the laptop
                scoreCount += 1  # increase the score
                if 5 < scoreCount < 10:  # automatically moves up level once player reaches certain score
                    level = 2
                elif scoreCount >= 10:  # automatically moves up level once player reaches certain score
                    level = 3
    return whack


def drawStartUp(string):  # first screen shown when running game
    global textX
    screen.blit(startPic, Rect(0, 0, 105, 78))  # background
    text = menuButtonsText.render(string, 1, black)  # name
    screen.blit(text, Rect(textX, 320, 400, 100))  # displays letter that are being typed on screen


def resetMenuColours():  # stops buttons from keeping hover colour when going back to that screen
    global menuButtonA, menuButtonB, menuButtonC, menuButtonD
    menuButtonA = grey
    menuButtonB = grey
    menuButtonC = grey
    menuButtonD = grey

def resetPlayScreen():  # every time playscreen = True, resets the game
    global level, characterX, characterY, keyRight, keyLeft, keyUp, keyDown, randComp, scoreCount, loadCounter
    level = 1
    characterX = 470
    characterY = 600
    keyRight = False
    keyLeft = False
    keyUp = False
    keyDown = False
    randComp = randint(0, 19)
    scoreCount = 0
    loadCounter = 0


while running:
    print(highestScore)
    if startUpScreen:  # user inputs name screen
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == KEYDOWN:  # if keyboard letter pressed
                if evnt.key == K_BACKSPACE:  # deleting letters
                    name = name[:-1]
                    textX += 10  # setting position of letters
                else:
                    name += evnt.unicode  # adding letters to name variable
                    if textX > 260:  # if x position of letters reaches 260
                        textX -= 10  # stop moving the letters to the left
                if evnt.key == K_RETURN:  # pressed enter
                    menuScreen = True  # move on to next screen (menu)
                    startUpScreen = False
        drawStartUp(name)  # drawing screen

    if menuScreen:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == MOUSEMOTION:  # changing button colours when mouse hovers over them
                mx, my = evnt.pos
                if 315 < mx < 685 and 300 < my < 370:
                    menuButtonA = red  # play button
                elif 315 < mx < 685 and 400 < my < 470:
                    menuButtonB = red  # instructions button
                elif 315 < mx < 685 and 500 < my < 570:
                    menuButtonC = red  # leader board button
                elif 315 < mx < 685 and 600 < my < 670:
                    menuButtonD = red  # exit button
                else:
                    resetMenuColours()
            if evnt.type == MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                if 315 < mx < 685 and 300 < my < 370:  # play button
                    playScreen = True
                    resetPlayScreen()
                    menuScreen = False
                elif 315 < mx < 685 and 400 < my < 470:  # instructions button
                    instructionScreen = True
                    backButton = black
                    menuScreen = False
                elif 315 < mx < 685 and 500 < my < 570:  # leader board button
                    menuScreen = False
                    backButton = black
                    leaderboardScreen = True
                elif 315 < mx < 685 and 600 < my < 670:  # quit button
                    running = False
        drawMenu()

    if leaderboardScreen:
        readHighScores() # takes three best players
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == MOUSEMOTION:
                mx, my = evnt.pos
                if 30 < mx < 95 and 36 < my < 53:
                    backButton = red
                else:
                    backButton = black
            if evnt.type == MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                if 30 < mx < 95 and 36 < my < 53:
                    leaderboardScreen = False # back to menu
                    menuScreen = True
                    resetMenuColours()
        draw.rect(screen, white, (0, 0, 1000, 700))
        text = mainScreenFont.render("LEADERBOARD", 1, black)
        screen.blit(text, Rect(230, 10, 400, 100))
        leaderBack = font2.render("BACK", 1, backButton)
        screen.blit(leaderBack, Rect(30, 30, 400, 100))
        draw.rect(screen, black, (100, 200, 800, 100), 4)
        draw.rect(screen, black, (100, 350, 800, 100), 4)
        draw.rect(screen, black, (100, 500, 800, 100), 4)
        rankingText = menuButtonsText.render(highScores[0][0], 1, black)  # name of player
        screen.blit(rankingText, Rect(150, 220, 400, 100))
        rankingText = menuButtonsText.render(str(highScores[0][1]), 1, black)  # score of player
        screen.blit(rankingText, Rect(780, 220, 400, 100))
        rankingText = menuButtonsText.render(highScores[1][0], 1, black)
        screen.blit(rankingText, Rect(150, 370, 400, 100))
        rankingText = menuButtonsText.render(str(highScores[1][1]), 1, black)
        screen.blit(rankingText, Rect(780, 370, 400, 100))
        rankingText = menuButtonsText.render(highScores[2][0], 1, black)
        screen.blit(rankingText, Rect(150, 520, 400, 100))
        rankingText = menuButtonsText.render(str(highScores[2][1]), 1, black)
        screen.blit(rankingText, Rect(780, 520, 400, 100))

    if instructionScreen:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == MOUSEMOTION:
                mx, my = evnt.pos
                if 30 < mx < 95 and 36 < my < 53:
                    backButton = red
                else:
                    backButton = black
            if evnt.type == MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                if 30 < mx < 95 and 36 < my < 53:  # back to menu
                    instructionScreen = False
                    menuScreen = True
                    resetMenuColours()
                if 150 < mx < 550 and 400 < my < 667:  # enlarging picture collage of instructions
                    instructionScreen = False
                    viewScreen = True
        draw.rect(screen, white,(0, 0, 1000, 700))
        instructText = menuButtonsText.render("INSTRUCTIONS" , 1, black)
        screen.blit(instructText, Rect(330, 50,400,100))
        instructText = font2.render("BACK", 1, backButton)
        screen.blit(instructText, Rect(30, 30, 400, 100))
        instructText = font2.render("Use the up/down/side keys to move your character.", 1, black)
        screen.blit(instructText, Rect(30, 170, 400, 130))
        screen.blit(upDownKeys, Rect(700, 90, 105, 78))
        instructText = font2.render("When a laptop has a red loading bar pop up, move your player in front of it before", 1, black)
        screen.blit(instructText, Rect(30, 230, 400, 130))
        instructText = font2.render("the screen before turns completely red, and press space. This will stop the screen", 1, black)
        screen.blit(instructText, Rect(30, 270, 400, 130))
        instructText = font2.render("from becoming red, and save the data from being leaked. If you don't get there in", 1, black)
        screen.blit(instructText, Rect(30, 310, 400, 130))
        instructText = font2.render("time, the data leaks, and you lose the game", 1, black)
        screen.blit(instructText, Rect(30, 350, 400, 130))
        screen.blit(instructPic, Rect(150, 400, 105, 78))
        draw.rect(screen, red, (150, 400, 400, 267),5)
        instructText = font2.render("<-- Click image to view in full screen.", 1, black)
        screen.blit(instructText, Rect(560, 500, 400, 130))
        instructText = font2.render("Click anywhere on the screen", 1, black)
        screen.blit(instructText, Rect(620, 540, 400, 130))
        instructText = font2.render("to leave full screen.", 1, black)
        screen.blit(instructText, Rect(620, 570, 400, 130))

    if viewScreen:  # enlarged instruction picture
        screen.blit(instructPicBig, Rect(0, 0, 105, 78))
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                if 0 < mx < 1000 and 0 < my < 700:  # click anywhere on screen to go back to instruction screen
                    instructionScreen = True
                    viewScreen = False

    if playScreen:  # game play
        screen.blit(networkPic, Rect(0, 0, 105, 78))
        laptops()  # draws laptops and loading bars based on level (level called in function laptops())
        draw.rect(screen, dropDown, (10, 10, 40, 40))  # draw drop down menu button
        draw.rect(screen, white, (18, 18, 24, 6))
        draw.rect(screen, white, (18, 27, 24, 6))
        draw.rect(screen, white, (18, 36, 24, 6))
        scoreText = font2.render("SCORE: " + str(scoreCount), 1, white)  # score counter
        screen.blit(scoreText, Rect(840, 15, 400, 100))
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == MOUSEMOTION:
                mx, my = evnt.pos
                if 10 < mx < 50 and 10 < my < 50:
                    dropDown = black
                elif 25 < mx < 145 and 65 < my < 105:
                    dropButtonA = red
                elif 25 < mx < 145 and 120 < my < 160:
                    dropButtonB = red
                elif 25 < mx < 145 and 175 < my < 215:
                    dropButtonC = red
                else:
                    dropDown = grey
                    dropButtonA = white
                    dropButtonB = white
                    dropButtonC = white
            if evnt.type == MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                if 10 < mx < 50 and 10 < my < 50:
                    pause = True  # pause game if drop down menu clicked
                    drawDropDown()
                    dropButtonA = white
                    dropButtonB = white
                    dropButtonC = white
            if evnt.type == KEYDOWN:  # moving player with keys
                if evnt.key == K_LEFT:
                    keyLeft = True
                if evnt.key == K_RIGHT:
                    keyRight = True
                if evnt.key == K_UP:
                    keyUp = True
                if evnt.key == K_DOWN:
                    keyDown = True
                if evnt.key == K_SPACE:
                    spaceBar = True
            if evnt.type == KEYUP:
                if evnt.key == K_LEFT:
                    keyLeft = False
                if evnt.key == K_RIGHT:
                    keyRight = False
                if evnt.key == K_UP:
                    keyUp = False
                if evnt.key == K_DOWN:
                    keyDown = False
                if evnt.key == K_SPACE:
                    spaceBar = False

        if keyUp == False and keyDown == False and keyRight == False and keyLeft == False:
            if sideMoved == '':  # if player is loaded for first time (hasn't moved yet)
                notMovingL(characterX, characterY)  # draw it facing left
            if sideMoved == 'left':
                notMovingL(characterX, characterY)
            if sideMoved == 'right':  # if previously moved to the right then stopped
                notMovingR(characterX, characterY)  # draw it facing right
        if keyLeft:  # directions and orientation of player moving
            sideMoved = 'left'
            characterX = characterX - 4
            movingLeft(characterX, characterY)
        if keyRight:
            sideMoved = 'right'
            characterX = characterX + 4
            movingRight(characterX, characterY)
        if keyDown:
            characterY = characterY + 4
            if sideMoved == 'left':
                movingLeft(characterX, characterY)
            elif sideMoved == 'right':
                movingRight(characterX, characterY)
            else:
                movingLeft(characterX, characterY)
        if keyUp:
            characterY = characterY - 4
            if sideMoved == 'left':
                movingLeft(characterX, characterY)
            elif sideMoved == 'right':
                movingRight(characterX, characterY)
            else:
                movingLeft(characterX, characterY)
        if characterX < 0:  # restrictions on player (can't go off screen)
            keyLeft = False
        if characterX > 945:
            keyRight = False
        if characterY < 7:
            keyUp = False
        if characterY > 630:
            keyDown = False

    if endGameScreen:
        highestScore = max(scoreCount, highestScore)  # set high score to be the higher one between the last time and current games' score
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == MOUSEMOTION:
                mx, my = evnt.pos
                if 100 < mx < 300 and 610 < my < 660:
                    endGameButtonA = red
                elif 400 < mx < 600 and 610 < my < 660:
                    endGameButtonB = red
                elif 700 < mx < 900 and 610 < my < 660:
                    endGameButtonC = red
                else:
                    endGameButtonA = black
                    endGameButtonB = black
                    endGameButtonC = black
            if evnt.type == MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                if 100 < mx < 300 and 610 < my < 660:
                    menuScreen = True  # back to menu after game fail
                    resetMenuColours()
                    endGameScreen = False
                elif 400 < mx < 600 and 610 < my < 660:
                    endGameScreen = False  # try again
                    playScreen = True
                    resetPlayScreen()
                elif 700 < mx < 900 and 610 < my < 660:
                    running = False  # quit game

        endX = int(endGamePos[0])  # draw final "data leaked" on end laptop that loaded fully
        endY = int(endGamePos[1])
        dataLeakedComp(endX, endY)
        if sideMoved == 'left':  # drawing the character again (so he doesn't disappear)
            movingLeft(characterX, characterY)  
        if sideMoved == 'right':
            movingRight(characterX, characterY)           
        else:
            movingLeft(characterX, characterY)
        draw.rect(screen, endGameButtonA, (100, 610, 200, 50))  # drawing buttons at bottom of screen when player loses
        draw.rect(screen, grey, (100, 610, 200, 50), 4)
        text = font2.render("MENU", 1, white)
        screen.blit(text, Rect(170, 620, 400, 100))
        draw.rect(screen, endGameButtonB, (400, 610, 200, 50))
        draw.rect(screen, grey, (400, 610, 200, 50), 4)
        text = font2.render("TRY AGAIN", 1, white)
        screen.blit(text, Rect(435, 620, 400, 100))
        draw.rect(screen, endGameButtonC, (700, 610, 200, 50))
        draw.rect(screen, grey, (700, 610, 200, 50), 4)
        text = font2.render("QUIT", 1, white)
        screen.blit(text, Rect(770, 620, 400, 100))

    display.flip()
    myClock.tick(60)

quit()