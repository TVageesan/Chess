#Backend code for calculations
##############################################################################
#TODOLOG:
#checking and pinning of king caclulations
##--->calculate from pieces or from king
##--->
#selection menu for promotion
#castling,en passant
#flip side
#score calculator
#put alphabetic and numeric labelling on the sides
##############################################################################

class Piece:

    def __init__(self,side):
        self.side = side
        self.icon = " "

    def validate_moveset(self,moveset,board):
        available = []
        attack = []
        for pos in moveset:
            y,x = pos
            if -1<x<8:
                if -1<y<8:
                    if board[y][x] == '--':
                        available.append(pos)
                    elif board[y][x].side != self.side:
                        available.append(pos)
                        attack.append(pos)
        return available,attack

    def iter_N_S(self,direction,pos,board):
        iy,ix = pos #iterative y,x
        mody = 1 if direction == "S" else -1
        while True:
            iy = iy + mody
            if -1<iy<8:
                if board[iy][ix] == '--':
                    self.available.append((iy,ix))
                elif board[iy][ix].side != self.side:
                    self.available.append((iy,ix))
                    self.attack.append((iy,ix))
                    break
                else:
                    break
            else:
                break


    def iter_W_E(self,direction,pos,board):
        iy,ix = pos
        modx = -1 if direction == "W" else 1 
        while True:
            ix = ix + modx
            if -1<ix<8:
                if board[iy][ix] == '--':
                    self.available.append((iy,ix))
                elif board[iy][ix].side != self.side:
                    self.available.append((iy,ix))
                    self.attack.append((iy,ix))
                    break
                else:
                    break
            else:
                break


    def iter_diagonals(self,direction,pos,board):
        diry,dirx = map(str,direction)
        iy,ix = pos
        mody = -1 if diry == "N" else 1
        modx = -1 if dirx == "W" else 1
        while True:
            iy = iy + mody
            ix = ix + modx
            if -1<iy<8:
                if -1<ix<8:
                    if board[iy][ix] == '--':
                        self.available.append((iy,ix))
                    elif board[iy][ix].side != self.side:
                        self.available.append((iy,ix))
                        self.attack.append((iy,ix))
                        break
                    else:
                        break
                else:
                    break
            else:
                break

class Pawn(Piece):
    def __init__(self,side):
        super().__init__(side)
        self.icon = self.side+"p"

    def get_available(self,board,curr):#para: 2 tuples(y,x)
        available = []
        attack = []
        cy,cx = curr
        mods = {"w":(-1,-2,6),"b":(1,2,1)}
        mod,mod2,row = mods[self.side]
        if cy>0:#movement
            if board[cy+mod][cx] == "--":#check 1 move forward
                available.append((cy+mod,cx))
                if cy == row and board[cy+mod2][cx] == "--":#check double move clause
                    available.append((cy+mod2,cx))
        if -1<cx<7:#side attack
            if  board[cy+mod][cx+1] != "--" and board[cy+mod][cx+1].side != self.side:
                available.append((cy+mod,cx+1))
                attack.append((cy+mod,cx+1))
        if 0<cx<8:#side attack
            if board[cy+mod][cx-1] != "--" and board[cy+mod][cx-1].side != self.side:
                available.append((cy+mod,cx-1))
                attack.append((cy+mod,cx-1)) 
        print(available)
        return available,attack

class Knight(Piece):
    def __init__(self,side):
        super().__init__(side)
        self.icon = self.side+"h"

    def get_available(self,board,curr):
        cy,cx = curr
        moveset = [(cy+1,cx+2),(cy-1,cx+2),(cy+1,cx-2),(cy-1,cx-2),(cy-2,cx-1),(cy+2,cx-1),(cy-2,cx+1),(cy+2,cx+1)]
        available,attack = self.validate_moveset(moveset,board)
        print(available)
        return available,attack

class King(Piece):
    def __init__(self,side):
        super().__init__(side)
        self.icon = self.side+"k"

    def get_available(self,board,curr):
        cy,cx = curr
        moveset = [(cy+1,cx-1),(cy+1,cx),(cy+1,cx+1),
                 (cy,cx-1),            (cy,cx+1),
                 (cy-1,cx-1),(cy-1,cx),(cy-1,cx+1)]
        available,attack = self.validate_moveset(moveset,board)
        print(available)
        return available,attack 
    def check_scan(self,board,curr):
        cy,cx = curr
        


class Rook(Piece):
    def __init__(self,side):
        super().__init__(side)
        self.icon = self.side+"r"

    def get_available(self,board,curr):
        self.available = []
        self.attack = []
        self.iter_N_S("N",curr,board)
        self.iter_N_S("S",curr,board)
        self.iter_W_E("W",curr,board)
        self.iter_W_E("E",curr,board)
        print(self.available)
        return self.available,self.attack

class Bishop(Piece):
    def __init__(self,side):
        super().__init__(side)
        self.icon = self.side+"b"

    def get_available(self,board,curr):
        self.available = []
        self.attack = []
        self.iter_diagonals("NW",curr,board)
        self.iter_diagonals("NE",curr,board)
        self.iter_diagonals("SW",curr,board)
        self.iter_diagonals("SE",curr,board)
        print(self.available)
        return self.available,self.attack

class Queen(Piece):
    def __init__(self,side):
        super().__init__(side)
        self.icon = self.side+"q"
        
    def get_available(self,board,curr):
        self.available = []
        self.attack = []
        self.iter_N_S("N",curr,board)
        self.iter_N_S("S",curr,board)
        self.iter_W_E("W",curr,board)
        self.iter_W_E("E",curr,board)
        self.iter_diagonals("NW",curr,board)
        self.iter_diagonals("NE",curr,board)
        self.iter_diagonals("SW",curr,board)
        self.iter_diagonals("SE",curr,board)
        print(self.available)
        return self.available,self.attack

#main() for gamestate
class Game:

    def __init__(self):
        self.board = [[Rook("b"),Knight("b"),Bishop("b"),King("b"),Queen("b"),Bishop("b"),Knight("b"),Rook("b")],
                    [Pawn("b") for i in range(8)],
                    ["--" for i in range(8)],
                    ["--" for i in range(8)],
                    ["--" for i in range(8)],
                    ["--" for i in range(8)],
                    [Pawn("w") for i in range(8)],
                    [Rook("w"),Knight("w"),Bishop("w"),King("w"),Queen("w"),Bishop("w"),Knight("w"),Rook("w")]]
        self.whitetomove = 'w'
        self.movelog = []

    def display_debug(self):
        for row in self.board:
            new = []
            for piece in row:
                if piece != "--":
                    new.append(piece.icon)
                else:
                    new.append("  ")
            print(" ".join(new))

    #this function was made redundant in ChessMain, kept for debugging
    def move(self,curr,target):
        cy,cx = curr
        ty,tx = target
        if self.board[cy][cx] != "--":
            available = self.board[cy][cx].get_available(self.board,curr)
            if target in available:
                self.board[ty][tx],self.board[cy][cx] = g.board[cy][cx],"--"
g = Game()
g.display_debug()

