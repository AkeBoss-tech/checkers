from Pieces import Board, screen, loadBoard, simulateGame, createNewSave, computer
import pygame, sys, math, random, pathlib, time
import pickle as p
from os import listdir
from os.path import isfile, join

path = pathlib.Path(__file__).parent.absolute()
print("System Start")

def drawRectangle(screen, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))

def drawHollowCircle(screen, color, radius, center_x, center_y):
    iterations = 100
    for i in range(iterations):
            ang = i * 3.14159 * 2 / iterations
            dx = int(math.cos(ang) * radius)
            dy = int(math.sin(ang) * radius)
            x = center_x + dx
            y = center_y + dy
            pygame.draw.circle(screen, color, (x, y), 5)

def drawCircle(screen, color, x, y, width, height):
    rect = [x, y, width, height]
    pygame.draw.ellipse(screen, color, rect, 0)

def writeText(text, screen, X, Y, color=(0, 0, 0), fontSize=64):
    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', fontSize)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render(text, True, color)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = (X, Y)
    screen.blit(text, textRect)

def drawGrid(screen, board, turn, highlightList=[], text=""):
    screen.fill((162, 163, 162))
    colorsGrid = [
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]
    ]
    white = (255, 255, 255)
    black = (3, 71, 1)
    pureBlack = (1, 4, 105)
    gray = (166, 166, 166)
    red = (207, 0, 0)
    blue = (7, 219, 131)
    green = (10, 186, 7)
    bufferX = 0
    bufferY = 0
    writeText("<-", screen, 50, 50)
    for a, r in enumerate(colorsGrid):
        for b, c in enumerate(r):
            if c == 0:
                drawRectangle(screen, black, bufferX + (b + 1) * 100, bufferY + (a + 1) * 100, 100, 100)
            elif c == 1:
                drawRectangle(screen, white, bufferX + (b + 1) * 100, bufferY + (a + 1) * 100, 100, 100)

            for i in range(len(highlightList)):
                if highlightList[i][0] == [int(a), int(b)]:
                    if highlightList[i][1] == "green":
                        drawHollowCircle(screen, green, 35, bufferX + (b + 1) * 100 + 50, bufferY + (a + 1) * 100 + 50)
                    elif highlightList[i][1] == "red":
                        drawHollowCircle(screen, red, 50, bufferX + (b + 1) * 100 + 50, bufferY + (a + 1) * 100 + 50)
                    elif highlightList[i][1] == "blue":
                        drawHollowCircle(screen, blue, 50, bufferX + (b + 1) * 100 + 50, bufferY + (a + 1) * 100 + 50)
                    if highlightList[i][1] == "circle":
                        drawHollowCircle(screen, gray, 35, bufferX + (b + 1) * 100 + 50, bufferY + (a + 1) * 100 + 50)

    for x, row in enumerate(board):
        for y, val in enumerate(row):
            if val != "--":
                pieceVal = val.type
                color = val.color

                if color == "red":
                    drawCircle(screen, red, bufferX + (y + 1) * 100 + 12, bufferY + (x + 1) * 100 + 12, 75, 75)
                elif color == "black":
                    drawCircle(screen, pureBlack, bufferX + (y + 1) * 100 + 12, bufferY + (x + 1) * 100 + 12, 75, 75)
                

                if pieceVal == "king": 
                    writeText("K", screen, bufferX + (y + 1) * 100 + 50,  bufferY + (x + 1) * 100 + 50, (255,255,255))

    s = 150
    for a in range(8):
        #writeText(str(a+1), screen, s + a * 100, 50)
        pass
    writeText(text, screen,  450, 50)
    if turn == "red":
        writeText("Red's Turn", screen,  450, 50)
        pass
    elif turn == "black":
        writeText("Black's Turn", screen,  450, 50)
        pass
    else:
        writeText(turn, screen,  450, 50)

    for b in range(8):
        #writeText(str(b+1), screen, 50, s + b * 100)
        pass

    pygame.display.update()

def findWhichSquare(mouseX, mouseY, highlight, Board, x, turn, isComputer=False):
    arrayValue = ["-1", "-1"]
    for i in range(8):
        if ((i + 1) * 100) <= mouseX <= ((i + 1) * 100) + 100:
            arrayValue[1] = int(i)
            break

    for t in range(8):
        if ((t + 1) * 100) <= mouseY <= ((t + 1) * 100) + 100:
            arrayValue[0] = int(t)
            break
    
    if mouseX < 100 and mouseY < 100:
        if isComputer:
            if len(Board.previousMoves) == 0:
                turn = changeTurn(turn)
            elif len(Board.previousMoves) == 1:
                turn = changeTurn(turn)
                turn = Board.undo()
            else:
                Board.undoTillPlayerTurn("red")
                Board.undoTillPlayerTurn("black")
                turn = "red"

        else:
            if len(Board.previousMoves) != 0:
                turn = Board.undo()
            else:
                turn = changeTurn(turn)

    if "-1" in arrayValue:
        onBoard = False
    else:
        onBoard = True

    if highlight and onBoard:
        Board.changeHighlightedPieces(arrayValue, "green")

    isPiece = False
    if onBoard:
        o = x[arrayValue[0]][arrayValue[1]]
        if o != "--":
            isPiece = True
    return arrayValue, onBoard, isPiece, turn

def main():
    pygame.init()
    screenClass = screen()
    while True:
        mode = welcome(screenClass.screen)
        if mode == "human":
            board = Board()
            endBoard = runGame(board, screenClass)
            end(endBoard, screenClass.screen)
        
        elif mode == "computer":
            board = Board()
            mode = chooseComputer(screenClass.screen)
            if mode == "0":
                computerObj = computer("black", 0)
                endBoard = computerView(board, screenClass, computerObj)
                end(endBoard, screenClass.screen)
            elif mode == "1":
                computerObj = computer("black", 1)
                endBoard = computerView(board, screenClass, computerObj)
                end(endBoard, screenClass.screen)
            elif mode == "2":
                computerObj = computer("black", 2)
                endBoard = computerView(board, screenClass, computerObj)
                end(endBoard, screenClass.screen)
            elif mode == "3":
                continueFunc = confirm(screenClass.screen, "Hard mode is really slow", "Do you want to continue?")
                if continueFunc:
                    computerObj = computer("black", 3)
                    endBoard = computerView(board, screenClass, computerObj)
                    end(endBoard, screenClass.screen)
            

        elif mode == "view":
            watchGame(screenClass.screen)

        elif mode == "help":
            infoScreen(screenClass.screen, "Welcome to the Help Menu")
            infoScreen(screenClass.screen, "This Screen will ", "walk you through the game")
            playGrid(screenClass.screen, " This is the undo button")
            infoScreen(screenClass.screen, "At the start", "it lets the other player move")
            infoScreen(screenClass.screen, "You can select pieces", " by clicking them")
            infoScreen(screenClass.screen, "You can deselect by", "Clicking outside the board")
            infoScreen(screenClass.screen, "In view mode use", "arrow keys to move")
            infoScreen(screenClass.screen, "This means that", " the computer is thinking", True)
            infoScreen(screenClass.screen, "You are ready to play!")
            
def runGame(board, screen):
    run = True
    takingPiece = []
    turn = "red"
    mode = "ready"
    forceTake = False
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                mode, turn = board.findWinner(mode, turn)
                board.refreshGame()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                arrayValue, onBoard, isPiece, turn = findWhichSquare(x, y, False, board, board.returnBoard(), turn)
                
                if onBoard:
                    if mode == "take":
                        val, turn = board.valid_move_piece(takingPiece, arrayValue, turn)
                        mode = "reset"

                    if mode == "counting":
                        delete = False
                        for s in board.highlightedPieces:
                            if arrayValue in s:
                                board.highlightedPieces.remove(s)
                                drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                                delete = True

                        if delete is False:
                            if isPiece:
                                board.changeHighlightedPieces(arrayValue, "blue")
                            else:
                                board.changeHighlightedPieces(arrayValue, "green")
                        
                        if len(board.highlightedPieces) == 0:
                            mode = "reset"

                    if isPiece and mode == "ready" and board.board[arrayValue[0]][arrayValue[1]].color == turn:
                        takingPiece = arrayValue
                        board.changeHighlightedPieces(arrayValue, "red")
                        mode = "take"
                        x, forceTake = board.getAllMoves(turn)
                        t = board.board[takingPiece[0]][takingPiece[1]].checkAttackingPieces(board.board)
                        
                        for y in x:
                            for e in t:
                                if e == y:
                                    board.changeHighlightedPieces(y, "circle")
                    elif mode == "ready" or isPiece and board.board[arrayValue[0]][arrayValue[1]].color != turn:
                        if len(board.highlightedPieces) == 0:
                            if isPiece:
                                board.changeHighlightedPieces(arrayValue, "blue")
                            else:
                                board.changeHighlightedPieces(arrayValue, "green")
                        mode = "counting"
                    

                elif not onBoard:
                    mode = "reset"

                if mode == "reset":
                    takingPiece = []
                    board.clearHighlightedPieces()
                    mode = "ready"

                if mode == "DONE":
                    drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                    return board

                drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                mode, turn = board.findWinner(mode, turn)
                board.refreshGame()
                
def welcomeScreen(screen):
    white = (255, 255, 255)
    black = (38, 38, 38)
    pureBlack = (1, 4, 105)
    gray = (166, 166, 166)
    red = (207, 0, 0)
    blue = (7, 219, 131)
    green = (10, 186, 7)
    screen.fill(black)
    for i in range(15):
        drawCircle(screen, white, random.randint(0,950), random.randint(0,950), 5, 5)
        
    writeText("Checkers", screen, 450, 60, white)
    drawRectangle(screen, gray, 250, 350, 400, 150)
    drawRectangle(screen, gray, 250, 650, 400, 150)
    drawRectangle(screen, gray, 750, 0, 200, 100)
    
    writeText("View", screen, 455, 425, white)
    writeText("Play", screen, 455, 725, white)
    writeText("Help", screen, 850, 50, white)
    writeText("By: Akash Dubey", screen, 650, 900, white)
    

    pygame.display.update()
 
def welcome(screen):
    mode = ""
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                play = checkButtton(x, y, 250, 650, 400, 150)
                view = checkButtton(x, y, 250, 350, 400, 150)
                helper = checkButtton(x, y, 750, 0, 200, 100)
                if play:
                    mode = "play"
                    run = False
                elif view:
                    mode = "view"
                    run = False
                elif helper:
                    return "help"
            welcomeScreen(screen)
    
    while True:
        if mode == "play":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    human = checkButtton(x,y,250, 550, 400, 150)
                    computer = checkButtton(x,y, 250, 350, 400, 150)
                    back = checkButtton(x,y, 250, 750, 400, 100)
                    if human:
                        return "human"
                    elif computer:
                        return "computer"
                    elif back:
                        return False
                    
                playScreen(screen)
        if mode == "view":
            return "view"

def playScreen(screen):
    
    white = (255, 255, 255)
    black = (38, 38, 38)
    pureBlack = (1, 4, 105)
    gray = (166, 166, 166)
    red = (207, 0, 0)
    blue = (7, 219, 131)
    green = (10, 186, 7)
    screen.fill(black)
    for i in range(10):
        drawCircle(screen, white, random.randint(0,950), random.randint(0,950), 5, 5)
        
    writeText("Play", screen, 450, 60, white)
    drawRectangle(screen, gray, 250, 350, 400, 150)
    drawRectangle(screen, gray, 250, 750, 400, 100)
    drawRectangle(screen, gray, 250, 550, 400, 150)
    writeText("COMPUTER", screen, 455, 425, white)
    writeText("HUMAN", screen, 455, 625, white)
    writeText("BACK", screen, 455, 800, white)
    writeText("vs.", screen, 450, 200, white)

    pygame.display.update()

def viewScreen(screen, text, subText=""):
    white = (255, 255, 255)
    black = (38, 38, 38)
    pureBlack = (1, 4, 105)
    gray = (166, 166, 166)
    red = (207, 0, 0)
    blue = (7, 219, 131)
    green = (10, 186, 7)
    screen.fill(black)
    for i in range(10):
        drawCircle(screen, white, random.randint(0,950), random.randint(0,950), 5, 5)
    
    writeText(text, screen, 455, 260, white)
    writeText(subText, screen, 450, 425, white)
    writeText("Click to advance", screen, 455, 625, white)

    pygame.display.update()

def openFile():
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    possibleFiles = []
    for val in onlyfiles:
        if val[-3:] == "pkl":
            possibleFiles.append(val)

    if len(possibleFiles) != 0:
        fileName = getNumberInput(possibleFiles)
        return possibleFiles[fileName]
    else:
        print("Looks like you don't have any files to open")
        return False

def getNumberInput(choices):
        print("\n\n Choose the game you would like to view")
        print(" Saved Games are in D-M-Y_H-M format")
        print(" Type quit to end program")

        for x,i in enumerate(choices):
            print(f"""\t({x+1}) {i[:-4]}""")
                 
        y = True
        while y:
            b = input(">> ").strip()
            if b =="quit":
                sys.exit()

            try:
                a = int(b)
            except:
                print("Not a number please try again.")
                continue
                
            if a-1 >= 0 and a-1 <= len(choices):
                print("Your choice was accepted.")
                y = False
            else:
                print("Your number is not in the right range. Try again.")
        
        return a - 1

def checkButtton(MOUSE_X, MOUSE_Y, RECT_X, RECT_Y, WIDTH, HEIGHT):
    if RECT_X < MOUSE_X < RECT_X + WIDTH:
        if RECT_Y < MOUSE_Y < RECT_Y + HEIGHT:
            return True
    
    return False
    
def declareWinner(board, screen):
    winner = changeTurn(board.loser)
    if winner == "red":
        winner = "Red Wins!"
    elif winner == "black":
        winner = "Blue Wins!"

    infoScreen(screen, winner)

def end(board, screen):
    declareWinner(board, screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                save = checkButtton(x, y, 250, 650, 400, 150)
                skip = checkButtton(x, y, 250, 350, 400, 150)
                if skip:
                    createNewSave(board.previousMoves)
                    return
                elif save:
                    return
            endScreen(screen)
    
def endScreen(screen):
    white = (255, 255, 255)
    black = (38, 38, 38)
    pureBlack = (1, 4, 105)
    gray = (166, 166, 166)
    red = (207, 0, 0)
    blue = (7, 219, 131)
    green = (10, 186, 7)
    screen.fill(black)
    for i in range(15):
        drawCircle(screen, white, random.randint(0,950), random.randint(0,950), 5, 5)
        
    writeText("Save the game?", screen, 450, 160, white)
    drawRectangle(screen, gray, 250, 350, 400, 150)
    drawRectangle(screen, gray, 250, 650, 400, 150)
    writeText("Yes", screen, 455, 425, white)
    writeText("No", screen, 455, 725, white)
    

    pygame.display.update()

def watchGame(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    viewScreen(screen, "Read instructions on console")

    fileName = openFile()
    start = True
    if fileName != False:
        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    viewScreen(screen, "CLICK TO START")

                    start = False
        
        spectateGame(screen, fileName)
        infoScreen(screen, "GAME OVER")
        return

    else:
        while True:
            viewScreen(screen, "NO GAMES SAVED")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    viewScreen(screen, "NO GAMES SAVED")
                    return

def spectateGame(screen, fileName):
    moves = loadBoard(fileName)
    movesLeft = len(moves)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if movesLeft > 1:
                    currentMoves = moves[:-1*movesLeft]
                    movesLeft -= 1
                    board = simulateGame(currentMoves)
                    drawGrid(screen, board, "")
                else:
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                    if movesLeft < len(moves):
                        currentMoves = moves[:-1*movesLeft]
                        movesLeft += 1
                        board = simulateGame(currentMoves)
                        drawGrid(screen, board, "")
                
                if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                    if movesLeft > 1:
                        currentMoves = moves[:-1*movesLeft]
                        movesLeft -= 1
                        board = simulateGame(currentMoves)
                        drawGrid(screen, board, "")
                    else:
                        return
                    
            currentMoves = moves[:-1*movesLeft]
            board = simulateGame(currentMoves)
            drawGrid(screen, board, "")

def changeTurn(turn):
    if turn == "red":
        turn = "black"
    elif turn == "black":
        turn = "red"

    return turn

def computerView(board, screen, computer):
    run = True
    takingPiece = []
    turn = "red"
    mode = "ready"
    forceTake = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                mode, turn = board.findWinner(mode, turn)
                board.refreshGame()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                arrayValue, onBoard, isPiece, turn = findWhichSquare(x, y, False, board, board.returnBoard(), turn, isComputer=True)
                
                drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                mode, turn = board.findWinner(mode, turn)
                board.refreshGame()
                
                while True:
                    if turn == computer.color and board.loser == "":
                        move = computer.returnMove(board)
                        val, turn = board.valid_move_piece(move[0], move[1], turn)
                    else:
                        break

                drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                mode, turn = board.findWinner(mode, turn)
                board.refreshGame()

                if onBoard:
                    if mode == "take":
                        val, turn = board.valid_move_piece(takingPiece, arrayValue, turn)
                        if val:
                            takingPiece = []
                            board.clearHighlightedPieces()
                            drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                            mode, turn = board.findWinner(mode, turn)
                            board.refreshGame()
                        
                        while True:
                            if turn == computer.color and board.loser == "":
                                move = computer.returnMove(board)
                                val, turn = board.valid_move_piece(move[0], move[1], turn)
                            else:
                                break
                        mode = "reset"

                    if mode == "counting":
                        delete = False
                        for s in board.highlightedPieces:
                            if arrayValue in s:
                                board.highlightedPieces.remove(s)
                                drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                                delete = True

                        if delete is False:
                            if isPiece:
                                board.changeHighlightedPieces(arrayValue, "blue")
                            else:
                                board.changeHighlightedPieces(arrayValue, "green")
                        
                        if len(board.highlightedPieces) == 0:
                            mode = "reset"

                    if isPiece and mode == "ready" and board.board[arrayValue[0]][arrayValue[1]].color == turn:
                        takingPiece = arrayValue
                        board.changeHighlightedPieces(arrayValue, "red")
                        mode = "take"
                        x, forceTake = board.getAllMoves(turn)
                        t = board.board[takingPiece[0]][takingPiece[1]].checkAttackingPieces(board.board)
                        
                        for y in x:
                            for e in t:
                                if e == y:
                                    board.changeHighlightedPieces(y, "circle")
                    elif mode == "ready" or isPiece and board.board[arrayValue[0]][arrayValue[1]].color != turn:
                        if len(board.highlightedPieces) == 0:
                            if isPiece:
                                board.changeHighlightedPieces(arrayValue, "blue")
                            else:
                                board.changeHighlightedPieces(arrayValue, "green")
                        mode = "counting"
                    

                elif not onBoard:
                    mode = "reset"

                if mode == "reset":
                    takingPiece = []
                    board.clearHighlightedPieces()
                    mode = "ready"

                if mode == "DONE":
                    return board

                drawGrid(screen.screen, board.board, turn, board.highlightedPieces)
                mode, turn = board.findWinner(mode, turn)
                board.refreshGame()

def chooseComputer(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                random = checkButtton(x,y, 50, 250, 400, 250)
                easy = checkButtton(x,y, 500, 250, 400, 250)
                medium = checkButtton(x,y, 50, 550, 400, 250)
                hard = checkButtton(x,y, 500, 550, 400, 250)
                back = checkButtton(x,y, 50, 825, 850, 100)
                if random:
                    return "0"

                elif easy:
                    return "1"
                    
                elif medium:
                    return "2"
                    
                elif hard:
                    return "3"
                    
                elif back:
                    return
                    
            chooseComputerScreen(screen)

def chooseComputerScreen(screen):
    white = (255, 255, 255)
    black = (38, 38, 38)
    pureBlack = (1, 4, 105)
    gray = (166, 166, 166)
    red = (207, 0, 0)
    blue = (7, 219, 131)
    green = (10, 186, 7)
    screen.fill(black)
    for i in range(15):
        drawCircle(screen, white, random.randint(0,950), random.randint(0,950), 5, 5)
        
    writeText("Computer Menu", screen, 450, 60, white)
    drawRectangle(screen, gray, 50, 250, 400, 250) # Random
    drawRectangle(screen, gray, 500, 250, 400, 250) # Easy
    drawRectangle(screen, gray, 50, 550, 400, 250) # Medium
    drawRectangle(screen, gray, 500, 550, 400, 250) # Hard
    drawRectangle(screen, gray, 50, 825, 850, 100) # UNDO
    writeText("RANDOM", screen, 50+180, 250+130, white)
    writeText("EASY", screen, 500+185, 250+130, white)
    writeText("MEDIUM", screen, 250, 675, white)
    writeText("HARD", screen, 690, 675, white)
    writeText("BACK", screen, 455, 885, white)
    

    pygame.display.update()

def confirm(screen, text, subText=""):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                no = checkButtton(x,y,250, 650, 400, 150)
                yes = checkButtton(x,y,250, 350, 400, 150)
                if yes:
                    return True
                    
                elif no:
                    return False

            confirmScreen(screen, text, subText=subText)

def confirmScreen(screen, text, subText=""):
    white = (255, 255, 255)
    black = (38, 38, 38)
    pureBlack = (1, 4, 105)
    gray = (166, 166, 166)
    red = (207, 0, 0)
    blue = (7, 219, 131)
    green = (10, 186, 7)
    screen.fill(black)
    for i in range(15):
        drawCircle(screen, white, random.randint(0,950), random.randint(0,950), 5, 5)
        
    writeText(text, screen, 450, 160, white)
    writeText(subText, screen, 450, 260, white)
    drawRectangle(screen, gray, 250, 350, 400, 150)
    drawRectangle(screen, gray, 250, 650, 400, 150)
    writeText("Yes", screen, 455, 425, white)
    writeText("No", screen, 455, 725, white)
    

    pygame.display.update()

def infoScreen(screen, text, subText="", delay=False):
    viewScreen(screen, text, subText=subText)
    if delay:
        time.sleep(7)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                return

            viewScreen(screen, text, subText=subText)

def playGrid(screen, text):
    board = Board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                return

            drawGrid(screen, board.board, "", text=text)

main()