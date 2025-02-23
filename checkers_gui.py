import tkinter as tk
from checker_games import CheckersGames

class CheckersGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Dame-Game with Expert System")
        
        self.start_screen()
    
    def start_screen(self):
        self.clear_screen()

        tk.Label(self.master, text="Choose Difficulty", font=("Arial", 16, "bold")).pack(pady=20)
        self.difficulty = tk.IntVar(value=2)
        tk.Radiobutton(self.master, text="Simple", variable=self.difficulty, value=2, font=("Arial", 12)).pack()
        tk.Radiobutton(self.master, text="Difficult", variable=self.difficulty, value=5, font=("Arial", 12)).pack()

        # select algorithmus
        tk.Label(self.master, text="Choose AI Algorithm", font=("Arial", 16, "bold")).pack(pady=20)
        self.ai_algorithm = tk.StringVar(value="minimax")
        tk.Radiobutton(self.master, text="Minimax", variable=self.ai_algorithm, value="minimax", font=("Arial", 12)).pack()
        tk.Radiobutton(self.master, text="Monte Carlo Tree Search", variable=self.ai_algorithm, value="mcts", font=("Arial", 12)).pack()

        tk.Button(self.master, text="Start Game", command=self.start_game, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white").pack(pady=20)

            
    def start_game(self):
        self.clear_screen()
        self.setup_game()
    
    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()
    
    def setup_game(self):
        self.cellSize = 80
        self.canvasSize = self.cellSize * 8
        self.canvas = tk.Canvas(self.master, width=self.canvasSize, height=self.canvasSize, bg="#D18B47")
        self.canvas.pack()
        
        self.game = CheckersGames()
        self.selectedPiece = None
        
        self.canvas.bind("<Button-1>", self.onCanvasClick)
        self.drawBoard()

    def drawBoard(self):
        self.canvas.delete("all")
        colors = {"light": "#F0D9B5", "dark": "#B58863"}
        # draw game board
        for row in range(8):
            for col in range(8):
                x1 = col * self.cellSize
                y1 = row * self.cellSize
                x2 = x1 + self.cellSize
                y2 = y1 + self.cellSize
                fill = colors["dark"] if (row + col) % 2 != 0 else colors["light"]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black", width=2)

        # shows selected cell
        if self.selectedPiece is not None:
            row, col = self.selectedPiece
            x1 = col * self.cellSize
            y1 = row * self.cellSize
            x2 = x1 + self.cellSize
            y2 = y1 + self.cellSize
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=4)

        # print stones
        for row in range(8):
            for col in range(8):
                piece = self.game.board[row][col]
                if piece is not None:
                    x = col * self.cellSize + self.cellSize / 2
                    y = row * self.cellSize + self.cellSize / 2
                    radius = self.cellSize * 0.4
                    color = "white" if piece.lower() == 'w' else "black"
                    outline_color = "gray" if color == "black" else "darkgray"

                    self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline=outline_color, width=3)
                        # mark dame with a "D"
                    if piece.isupper():
                        self.canvas.create_text(x, y, text="D", fill="red", font=("Arial", 20, "bold"))
        
    def onCanvasClick(self, event):
        # player move only, if it is white's turn
        if self.game.turn != 'w':
            return
        
        col = event.x // self.cellSize
        row = event.y // self.cellSize

        # select a stone (own turn)
        if self.selectedPiece is None:
            piece = self.game.board[row][col]
            if piece is not None and piece.lower() == 'w':
                self.selectedPiece = (row, col)
                self.drawBoard()
        else:
            start = self.selectedPiece
            end = (row, col)
            validMove = None
            moves = self.game.getAllMoves('w')
            for move in moves:
                if move[0] == start and move[1] == end:
                    validMove = move
                    break
            if validMove:
                self.game.makeMove(validMove)
                self.selectedPiece = None
                self.drawBoard()
                if not self.game.getAllMoves('b'):
                    self.showGameOver("Game over! No Stones more available for KI-Enemy")
                    return
                self.game.turn = 'b'
                self.master.after(500, self.aiMove)
            else:
                # disallowed selection - reset selection
                self.selectedPiece = None
                self.drawBoard()

    def aiMove(self):
        searchDepth = self.difficulty.get()

        if self.ai_algorithm.get() == "minimax":
            _, move = self.game.minimax(searchDepth, False, -float('inf'), float('inf'))
        else:
            move = self.game.monteCarloTreeSearch(20)  # 20 simulations

        if move is None:
            self.showGameOver("Game Over! No more stones available for KI!")
            return

        self.game.makeMove(move)
        self.drawBoard()
        self.game.turn = 'w'

    def showGameOver(self, message):
        self.canvas.create_text(self.canvasSize/2, self.canvasSize/2, text=message, fill="red", font=("Arial", 24, "bold"))
        self.canvas.unbind("<Button-1>")