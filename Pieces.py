import sys, pygame
import pickle as p
from datetime import datetime
from copy import deepcopy
from random import randint

def checkIfInBoard(row, col):
    onBoard = False
    if 0 <= row < 8 and 0 <= col < 8:
        onBoard = True

    return onBoard

class Piece():
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.type = "normal"
        self.startingPos = (row, col)
        self.firstMove = True
        self.canTake = False

    def changePos(self, newPos):
        self.row = newPos[0]
        self.col = newPos[1]

class normalPiece(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def checkAttackingPieces(self, board):
        direction = 1
        if self.color == "red":
            direction *= -1

        locations = []
        canTake = []
        possibleMoveLocations = [
            [self.row + direction, self.col - 1],
            [self.row + direction, self.col + 1],
        ]

        possibleTakeLocations = [
            [self.row + direction*2, self.col - 2],
            [self.row + direction*2, self.col + 2],
        ]

        for x, i in enumerate(possibleMoveLocations):
            t = checkIfInBoard(i[0], i[1])
            s = checkIfInBoard(possibleTakeLocations[x][0], possibleTakeLocations[x][1])

            if t and s and board[i[0]][i[1]] != "--" and board[i[0]][i[1]].color != self.color:
                lastSquare = board[possibleTakeLocations[x][0]][possibleTakeLocations[x][1]]
                if s and lastSquare == "--":
                    locations.append(possibleTakeLocations[x])
                    canTake.append(True)


            elif t and board[i[0]][i[1]] == "--":
                locations.append(i)
                canTake.append(False)

            

        while True:
            if True in canTake:
                if False in canTake:
                    indexPos = canTake.index(False)
                    locations.pop(indexPos)
                    canTake.pop(indexPos)
                else:
                    self.canTake = True
                    break
            else:
                self.canTake = False
                break


        return locations

    def findWhichToTake(self, board, newPos):
        direction = 1
        if self.color == "red":
            direction *= -1


        possibleMoveLocations = [
            [self.row + direction, self.col - 1],
            [self.row + direction, self.col + 1],
        ]

        possibleTakeLocations = [
            [self.row + direction*2, self.col - 2],
            [self.row + direction*2, self.col + 2],
        ]

        if newPos in possibleTakeLocations:
            return possibleMoveLocations[possibleTakeLocations.index(newPos)]
            
        else:
            return False

def convertPieceToKing(pieceObject):
    kingPiece = King(pieceObject.row, pieceObject.col, pieceObject.color)
    
    kingPiece.type = "king"
    kingPiece.startingPos = pieceObject.startingPos
    kingPiece.firstMove = False
    return kingPiece

class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def checkAttackingPieces(self, board):
        locations = []
        canTake = []

        possibleMoveLocations = [
            [self.row + 1, self.col - 1],
            [self.row + 1, self.col + 1],
            [self.row - 1, self.col - 1],
            [self.row - 1, self.col + 1],
        ]

        possibleTakeLocations = [
            [self.row + 2, self.col - 2],
            [self.row + 2, self.col + 2],
            [self.row - 2, self.col - 2],
            [self.row - 2, self.col + 2],
        ]

        for x, i in enumerate(possibleMoveLocations):
            t = checkIfInBoard(i[0], i[1])
            s = checkIfInBoard(possibleTakeLocations[x][0], possibleTakeLocations[x][1])

            if t and s and board[i[0]][i[1]] != "--" and board[i[0]][i[1]].color != self.color:
                lastSquare = board[possibleTakeLocations[x][0]][possibleTakeLocations[x][1]]
                if s and lastSquare == "--":
                    locations.append(possibleTakeLocations[x])
                    canTake.append(True)


            elif t and board[i[0]][i[1]] == "--":
                locations.append(i)
                canTake.append(False)

            

        while True:
            if True in canTake:
                if False in canTake:
                    indexPos = canTake.index(False)
                    locations.pop(indexPos)
                    canTake.pop(indexPos)
                else:
                    self.canTake = True
                    break
            else:
                self.canTake = False
                break


        return locations

    def findWhichToTake(self, board, newPos):
        direction = 1
        if self.color == "red":
            direction *= -1

        possibleMoveLocations = [
            [self.row + 1, self.col - 1],
            [self.row + 1, self.col + 1],
            [self.row - 1, self.col - 1],
            [self.row - 1, self.col + 1],
        ]

        possibleTakeLocations = [
            [self.row + 2, self.col - 2],
            [self.row + 2, self.col + 2],
            [self.row - 2, self.col - 2],
            [self.row - 2, self.col + 2],
        ]

        if newPos in possibleTakeLocations:
            return possibleMoveLocations[possibleTakeLocations.index(newPos)]
            
        else:
            return False



class Board():
    def __init__(self):
        
        self.board              = [
            ["--", normalPiece(0, 1, "black"), "--", normalPiece(0, 3, "black"),
             "--", normalPiece(0, 5, "black"), "--", normalPiece(0, 7, "black")],
            [normalPiece(1, 0, "black"), "--", normalPiece(1, 2, "black"), "--",
             normalPiece(1, 4, "black"), "--", normalPiece(1, 6, "black"), "--"],
           ["--", normalPiece(2, 1, "black"), "--", normalPiece(2, 3, "black"),
             "--", normalPiece(2, 5, "black"), "--", normalPiece(2, 7, "black")],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            [normalPiece(5, 0, "red"), "--", normalPiece(5, 2, "red"), "--",
             normalPiece(5, 4, "red"), "--", normalPiece(5, 6, "red"), "--"],
            ["--", normalPiece(6, 1, "red"), "--", normalPiece(6, 3, "red"),
             "--", normalPiece(6, 5, "red"), "--", normalPiece(6, 7, "red")],
            [normalPiece(7, 0, "red"), "--", normalPiece(7, 2, "red"), "--",
             normalPiece(7, 4, "red"), "--", normalPiece(7, 6, "red"), "--"],
        ]
        
        self.highlightedPieces  = []
        self.previousMoves      = []
        self.previousMoveType   = ["", []]
        self.previousTurn = []
        self.loser              = ""
        listStuff               = []
        for i in self.board:
            listStuff.append(i)
        self.canMoveRed         = True
        self.canMoveBlack       = True
        
        self.redPiecesLeft      = self.blackPiecesLeft = 12
        self.redKings           = self.blackKings = 0
        
    def changeHighlightedPieces(self, pos, color):
        self.highlightedPieces.append([list(pos), color])

    def clearHighlightedPieces(self):
        self.highlightedPieces = []

    def movePiece(self, row, col, newRow, newCol):
        x = self.board[row][col]
        y = self.board[newRow][newCol]
        self.previousMoves.append([[row, col], [newRow, newCol]])
        self.previousTurn.append(x.color)
        if y != "--":
            if x.color is not y.color:
                self.board[newRow][newCol] = x
                self.board[row][col] = "--"
                self.board[newRow][newCol].row = newRow
                self.board[newRow][newCol].col = newCol
                self.board[newRow][newCol].firstMove = False
        else:
            self.board[newRow][newCol] = x
            self.board[row][col] = "--"
            self.board[newRow][newCol].row = newRow
            self.board[newRow][newCol].col = newCol
        
    def returnBoard(self):
        return self.board

    def refreshGame(self):
        for x, t in enumerate(self.board):
            for y, i in enumerate(t):
                if i != "--":
                    if i.color == "black" and x == 7:
                        self.board[x][y] = convertPieceToKing(self.board[x][y])
                    elif i.color == "red" and x == 0:
                        self.board[x][y] = convertPieceToKing(self.board[x][y])

        self.findNumberPieces()

    def findWinner(self, mode, turn):
        # Find if anyone has won
        self.findNumberPieces()
        if self.redPiecesLeft == 0:
            self.loser = "red"
            return "DONE", "Blue Won"

        if self.blackPiecesLeft == 0:
            self.loser = "black"
            return "DONE", "Red Won"
        
        if self.canMoveBlack == False:
            self.loser = "black"
            return "DONE", "Red Won"
        
        if self.canMoveRed == False:
            self.loser = "red"
            return "DONE", "Blue Won"

        movesLeft = self.getAllMoves(turn)
        if len(movesLeft) == 0:
            self.loser = turn
            return "DONE", "Ran out of moves"


        return mode, turn

    def valid_move_piece(self, takingPiece, arrayValue, turn):
        attackedPieces, forceTake = self.getAllMoves(turn)
        t = self.board[takingPiece[0]][takingPiece[1]].checkAttackingPieces(self.board)
        for piecePosition in attackedPieces:
            for possiblePiecePos in t:
                if list(piecePosition) == arrayValue == possiblePiecePos:
                    if forceTake:
                        if self.board[takingPiece[0]][takingPiece[1]].canTake and self.previousMoveType[0] == "take" and self.previousMoveType[1] == takingPiece:
                            ifPieceToTake = self.board[takingPiece[0]][takingPiece[1]].findWhichToTake(self.board, arrayValue)
                            if ifPieceToTake != False:
                                self.board[ifPieceToTake[0]][ifPieceToTake[1]] = "--"
                                self.previousMoveType = ["take", arrayValue]
                            else:
                                self.previousMoveType = ["", []]
                            self.movePiece(takingPiece[0], takingPiece[1], arrayValue[0], arrayValue[1])
                        elif self.board[takingPiece[0]][takingPiece[1]].canTake and self.previousMoveType[0] == "":
                            ifPieceToTake = self.board[takingPiece[0]][takingPiece[1]].findWhichToTake(self.board, arrayValue)
                            if ifPieceToTake != False:
                                self.board[ifPieceToTake[0]][ifPieceToTake[1]] = "--"
                                self.previousMoveType = ["take", arrayValue]
                            else:
                                self.previousMoveType = ["", []]
                            self.movePiece(takingPiece[0], takingPiece[1], arrayValue[0], arrayValue[1])
                        
                        self.findWinner("", turn)
                        self.refreshGame()
                        x, forceTake = self.getAllMoves(turn)
                        if forceTake == False:
                            self.previousMoveType = ["", []]
                            turn = changeTurn(turn)
                        return True, turn
                    else:
                        ifPieceToTake = self.board[takingPiece[0]][takingPiece[1]].findWhichToTake(self.board, arrayValue)
                        if ifPieceToTake != False:
                            self.board[ifPieceToTake[0]][ifPieceToTake[1]] = "--"
                            self.previousMoveType = ["take", arrayValue]
                        else:
                            self.previousMoveType = ["", []]
                        self.movePiece(takingPiece[0], takingPiece[1], arrayValue[0], arrayValue[1])
                        turn = changeTurn(turn)
                        return True, turn
        return False, turn

    def findNumberPieces(self):
        self.redPiecesLeft = self.blackPiecesLeft = 0
        self.redKings = self.blackKings = 0

        for i in self.board:
            for t in i:
                if t != "--":
                    if t.color == "red":
                        self.redPiecesLeft += 1
                        if t.type == "king":
                            self.redKings += 1

                    if t.color == "black":
                        self.blackPiecesLeft += 1
                        if t.type == "king":
                            self.blackKings += 1

    def undo(self):
        if len(self.previousMoves) != 0:
            newMoves    = self.previousMoves[:-1]
            turn        = self.previousTurn[len(self.previousTurn) - 1]
            self.previousMoves.pop()
            self.previousTurn.pop()
            self.board = simulateGame(newMoves)
            if len(self.previousTurn) == 0:
                return "red"
            
            return turn
        
    def getAllMoves(self, color, returnOGPos=False):
        possiblePos = []
        canTake = []
        OGPos = []
        for i in self.board:
            for t in i:
                if t != "--" and t.color == color:
                    attackingPiece = t.checkAttackingPieces(self.board)
                    if len(attackingPiece) != 0:
                        OGPos.append(t)
                        for val in attackingPiece:
                            possiblePos.append(val)
                            canTake.append(t.canTake)
        forceTake = False
        while True:
            if True in canTake:
                if False in canTake:
                    indexPos = canTake.index(False)
                    possiblePos.pop(indexPos)
                    canTake.pop(indexPos)
                    
                else:
                    break
                for r in OGPos:
                    if not r.canTake:
                        OGPos.pop(OGPos.index(r))

                forceTake = True
            else:
                break
        
        for takingPiece in OGPos:
            if takingPiece.canTake and self.previousMoveType[0] == "":
                pass
            if takingPiece.canTake and self.previousMoveType[0] == "take" and self.previousMoveType[1] == takingPiece:
                pass
            elif takingPiece.canTake and self.previousMoveType[0] == "take" and self.previousMoveType[1] in takingPiece.checkAttackingPieces(self.board):
                indexPos = OGPos.index(takingPiece)
                possiblePos.pop(indexPos)
                canTake.pop(indexPos)
            
            
       

        if len(possiblePos) == 0:
            if color == "red":
                self.canMoveRed = False
            elif color == "black":
                self.canMoveBlack = False
        else:
            self.canMoveRed = True
            self.canMoveBlack = True

        if returnOGPos:
            return possiblePos, OGPos, forceTake

        return possiblePos, forceTake

    def getAllMovesForComputer(self, color, board, returnOGPos=False):
        possiblePos = []
        canTake = []
        OGPos = []
        for x, i in enumerate(board.board):
            for y, t in enumerate(i):
                if t != "--" and t.color == color:
                    attackingPiece = t.checkAttackingPieces(board.board)
                    if len(attackingPiece) != 0:
                        for val in attackingPiece:
                            possiblePos.append([[x,y], val])
                            canTake.append(t.canTake)

        forceTake = False
        while True:
            if True in canTake:
                if False in canTake:
                    indexPos = canTake.index(False)
                    possiblePos.pop(indexPos)
                    canTake.pop(indexPos)
                    
                else:
                    break
                for r in OGPos:
                    if not r.canTake:
                        OGPos.pop(OGPos.index(r))

                forceTake = True
            else:
                break
        
        if len(possiblePos) == 0:
            if color == "red":
                self.canMoveRed = False
            elif color == "black":
                self.canMoveBlack = False

        for x, p in enumerate(possiblePos):
            playBoard = deepcopy(board)
            legal = checkIfLegal(playBoard, p[0], p[1], color)
            if not legal:
                possiblePos.pop(x)

        return possiblePos, forceTake

    def evaluate(self, color):
        self.findWinner("", color)
        if self.redPiecesLeft == 0: 
            return 100
        if self.blackPiecesLeft == 0:
            return -100
        
        if self.canMoveBlack == False: 
            return -100
        if self.canMoveRed == False:
            return 100

        redCantTake     = 0
        blackCantTake   = 0

        for i in self.board:
            for t in i:
                if t != "--":
                    if t.col == 0 or t.col == 7:
                        if t.color == "red":
                            redCantTake += 1
                        elif t.color == "black":
                            blackCantTake += 1
        
        possibleBlackPos = self.getAllMoves("black")
        possibleRedPos   = self.getAllMoves("red")

        return (self.blackPiecesLeft - self.redPiecesLeft + self.blackKings * 1.5 - self.redKings * 1.5 + blackCantTake/2 - redCantTake/2) 

    def undoTillPlayerTurn(self, color):
        while True:
            if len(self.previousTurn) != 0:
                if self.previousTurn[len(self.previousTurn) - 1] != color:
                    self.undo()
                else:
                    return
            else:
                return

class screen():
    def __init__(self):
        self.screenHeight = 950
        self.screenWidth = 950
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('Checkers')

def saveBoard(moves, name):
    open(name, 'xb')
    with open(name, 'wb') as f:
        p.dump(moves, f)
    
    f.close()

def createNewSave(moves):
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y_%H-%M")
    dt_string += ".pkl"
    saveBoard(moves, dt_string)

def loadBoard(name):
    with open(name, 'rb') as f:
        moves = p.load(f)
    return moves

def simulateGame(moves, returnBoard=False):
    board = Board()
    turn = "red"
    for move in moves:
        takingPiece = move[0]
        arrayValue = move[1]
        if board.board[takingPiece[0]][takingPiece[1]] != "--":
            attackedPieces = board.board[takingPiece[0]][takingPiece[1]].checkAttackingPieces(board.board)
            for piecePosition in attackedPieces:
                if list(piecePosition) == arrayValue:
                    ifPieceToTake = board.board[takingPiece[0]][takingPiece[1]].findWhichToTake(board.board, arrayValue)
                    if ifPieceToTake != False:
                        board.board[ifPieceToTake[0]][ifPieceToTake[1]] = "--"
                    board.movePiece(takingPiece[0], takingPiece[1], arrayValue[0], arrayValue[1])
                    break
                    
        board.refreshGame()
    
    if returnBoard:
        return board
    
    return board.board

def getTextInput(self):
        print("\n\n Now you have to make a choice. Enter your choice.")
            
        y = True
        while y:
            a = input(">> ").strip()
            if a.lower() == "exit":
                sys.exit()
            

            if a:
                print("Your choice was accepted.")
                y = False
            else:
                print("Not in the list. Try Again.")
                continue
        
        return a


class computer():
    def __init__(self, color, difficulty):
        self.color = color
        if color == "red":
            self.opponent = "black"
        elif color == "black":
            self.opponent = "red"
        self.difficulty = difficulty

    def returnMove(self, board):
        playBoard = deepcopy(board)
        if self.difficulty == 0:
            possiblePos = playBoard.getAllMovesForComputer(self.color, board)
            return possiblePos[0][randint(0, len(possiblePos[0]) - 1)]
        elif self.difficulty == 1:
            evaluation, move = self.miniMax(playBoard, 2, self.color, "", maxS=True)
            return move
        elif self.difficulty == 2:
            evaluation, move = self.miniMax(playBoard, 4, self.color, "", maxS=True)
            return move
        elif self.difficulty == 3:
            evaluation, move = self.miniMax(playBoard, 6, self.color, "", maxS=True)
            return move

    def miniMax(self, board, depth, color, movePos, maxS=False, minS=False):
        if depth == 0 or board.evaluate(self.color) == 100 or board.evaluate(color) == -100:
            return board.evaluate(self.color), movePos

        if maxS:
            maxEval = float('-inf')
            best_move = None
            possiblePos, forceTake = board.getAllMovesForComputer(color, board)
            for move in possiblePos:
                board.previousMoves.append(move)
                newMoves = board.previousMoves
                newBoard = simulateGame(newMoves, True)
                evaluation = self.miniMax(newBoard, depth-1, self.color, move, minS=True)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    best_move = move
            
            return maxEval, best_move

        if minS:
            minEval = float('inf')
            best_move = None
            possiblePos, forceTake = board.getAllMovesForComputer(color, board)
            for move in possiblePos:
                board.previousMoves.append(move)
                newMoves = board.previousMoves
                newBoard = simulateGame(newMoves, True)
                evaluation = self.miniMax(board, depth-1, self.opponent, move, maxS=True)[0]
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    best_move = move
            
            return minEval, best_move

def changeTurn(turn):
    if turn == "red":
        turn = "black"
    elif turn == "black":
        turn = "red"

    return turn

def checkIfLegal(board, takingPiece, arrayValue, turn):
    attackedPieces, forceTake = board.getAllMoves(turn)
    mode = ""
    t = board.board[takingPiece[0]][takingPiece[1]].checkAttackingPieces(board.board)
    for piecePosition in attackedPieces:
        for possiblePiecePos in t:
            if list(piecePosition) == arrayValue == possiblePiecePos:
                if forceTake:
                    if board.board[takingPiece[0]][takingPiece[1]].canTake:
                        ifPieceToTake = board.board[takingPiece[0]][takingPiece[1]].findWhichToTake(board.board, arrayValue)
                        if ifPieceToTake != False:
                            board.board[ifPieceToTake[0]][ifPieceToTake[1]] = "--"
                        board.movePiece(takingPiece[0], takingPiece[1], arrayValue[0], arrayValue[1])
                    mode = board.findWinner(mode, turn)
                    board.refreshGame()
                    return True
                    
                else:
                    ifPieceToTake = board.board[takingPiece[0]][takingPiece[1]].findWhichToTake(board.board, arrayValue)
                    if ifPieceToTake != False:
                        board.board[ifPieceToTake[0]][ifPieceToTake[1]] = "--"
                    board.movePiece(takingPiece[0], takingPiece[1], arrayValue[0], arrayValue[1])
                    return True
    
    return False

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

# Thanks for reading the code
# A game by Akash Dubey