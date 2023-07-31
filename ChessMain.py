from tabnanny import check
import pygame
from ChessEngine import *
import os
#Set Dimensions of GUI
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE= HEIGHT//DIMENSION
MAX_FPS = 15
#Init dictionay of images
IMAGES= {}
def load_images(g):
    pieces=[]
    for arr in g.board:
        for i in arr:
            if i != "--":
                pieces.append(i)
    for piece in pieces:
        base_path = os.path.dirname(__file__)
        IMAGES[piece.icon] = pygame.image.load(os.path.join(base_path,f"images/{piece.icon}.png"))
        
#create board image
def drawboard(screen,selectedsq,available,attack):
    colors={0:pygame.Color("white"),1:pygame.Color("gray")}
    for y in range(DIMENSION):
        for x in range(DIMENSION):
            color=colors[((y+x)%2)]
            pygame.draw.rect(screen,color,pygame.Rect(x*SQ_SIZE,y*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    if selectedsq != ():#if piece selected
        sy,sx = selectedsq
        pygame.draw.rect(screen,"green",pygame.Rect(sx*SQ_SIZE,sy*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        for pos in available:
            colour = "light green"
            py,px = pos
            if pos in attack:
                colour = "red"
            pygame.draw.rect(screen, colour ,pygame.Rect(px*SQ_SIZE,py*SQ_SIZE,SQ_SIZE,SQ_SIZE))

#put pieces on board
def drawpieces(screen,board):
    for y in range(DIMENSION):
        for x in range(DIMENSION):
            piece = board[y][x]
            if piece != "--":
                screen.blit(IMAGES[piece.icon],pygame.Rect(x*SQ_SIZE,y*SQ_SIZE,SQ_SIZE,SQ_SIZE))

#show current gamestate
def drawGameState(screen,g,selectedsq,available,attack):
    drawboard(screen,selectedsq,available,attack)
    #WIP: piece highlighting,move suggestions
    drawpieces(screen,g.board)

#Main code

g=Game()
reverse = {'w':'b','b':'w'}
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
load_images(g)
screen.fill(pygame.Color('white'))
running= True
selectedsq = ()
available = []
attack = []
bk_pos = (0,3)
wk_pos = (7,3)

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            cx,cy = pygame.mouse.get_pos()
            cy,cx = cy//SQ_SIZE,cx//SQ_SIZE
            currsq = cy,cx
            if selectedsq == ():#select new square
                if g.board[cy][cx] != "--":#checks if piece exists
                    if (g.board[cy][cx].side == g.whitetomove):#checks if its that sides turn
                        available,attack = g.board[cy][cx].get_available(g.board,currsq)
                        selectedsq = currsq
            elif currsq == selectedsq:#deselect,select twice
                selectedsq = ()
                available = []
                attack =[]
            else:#selected second new square
                sy,sx = selectedsq
                if (cy,cx) in available:
                    g.board[cy][cx],g.board[sy][sx]=g.board[sy][sx],"--"
                    x,check_attack = g.board[cy][cx].get_available(g.board,currsq)
                    g.display_debug()
                    g.movelog.append([(sy,sx),(cy,cx)])#prev to new position
                    print(cy,cx,g.board[cy][cx].icon)
                    if (g.board[cy][cx].icon == "wp" and cy == 0) or (g.board[cy][cx].icon == "bp" and cy == 7):#promote case
                        g.board[cy][cx] = Queen(g.board[cy][cx].side)
                    g.whitetomove = reverse[g.whitetomove]
                available = []
                attack =[]
                selectedsq = ()
    clock.tick(MAX_FPS)
    drawGameState(screen,g,selectedsq,available,attack)
    pygame.display.flip()
print(g.movelog)
pygame.quit()
