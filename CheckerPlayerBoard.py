import numpy as np
import tkinter as tk

BOARD_SIZE = 8
board = np.full((BOARD_SIZE, BOARD_SIZE), None)
turn = 'w'  # white starts
selectedPiece = None
selectedPos = None
buttons = []

def initializeBoard():
    global board
    board.fill(None)
    for i in range(3):
        for j in range(BOARD_SIZE):
            if (i+j) % 2 == 1:
                board[i][j] = 'b' #black figure
    for i in range(5, BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (i + j) % 2 == 1:
                board[i][j] = 'w' #white figure
                
def createBoard(root):
    global buttons
    for r in range(BOARD_SIZE):
        rowButtons = []
        for c in range(BOARD_SIZE):
            color = 'lightgray' if (r + c) % 2 == 0 else 'darkgray'
            button = tk.Button(
                root,
                bg=color,
                width=4,
                height=2,
                command=lambda r=r, c=c:onClick(r, c)
            )
            button.grid(row=r, column=c)
            rowButtons.append(button)
        buttons.append(rowButtons)
    


def updateButtons():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece = board[r, c]
            button = buttons[r][c]
            if piece == 'w':
                button.config(text='W', fg='white')
            elif piece == 'b':
                button.config(text='B', fg='black')
            else:
                button.config(text='', bg='lightgray' if (r + c) % 2 == 0 else 'darkgray')


def onClick(r, c):
    global selectedPiece, selectedPos, turn

    if selectedPiece is None:
        piece = board[r][c]
        if piece == turn:
            selectedPiece = piece
            selectedPos = (r, c)
            highlightMoves(r, c)
        else:
            if isValidMove(selectedPos, (r, c)):
                makeMove(selectedPos, (r, c))
                turn = 'b' if turn == 'w' else 'w'
                clearHighlights()
            selectedPiece = None
            selectedPos = None


def highlightMoves(r, c):
    global buttons
    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]: # available moves
        newR, newC = r + dr, c + dc
        if isValidMove((r, c), (newR, newC)):
            buttons[newR][newC].config(bg='yellow')

def clearHighlights():
    updateButtons()

def isValidMove(start, end):
    startR, startC = start
    endR, endC = end

    if (endR < 0 or endR >= BOARD_SIZE or endC < 0 or endC >= BOARD_SIZE):
        return False
    if board[endR][endC] is not None:
        return False
    
    piece = board[startR][startC]
    if abs(startR - endR) == 1 and abs(startC - endC) == 1:
        return True
    elif (
        abs(startR - endR) == 2 and
        abs(startC - endC) == 2
    ):
        midR, midC = (startR + endR) // 2, (startC + endC) //2
        if board[midR][midC] is not None and board[midR][midC] != piece:
            return True
        return False
    
def makeMove(start, end):
    startR, startC = start
    endR, endC = end

    board[endR, endC] = board[startR, startC] # move the figure
    board[startR, startC] = None # empty field
    updateButtons(buttons)

root = tk.Tk()
root.title("Dame-Game")

initializeBoard()
createBoard(root)
updateButtons()
root.mainloop()