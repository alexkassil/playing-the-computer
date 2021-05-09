from itertools import chain
import random
class CheckerGame:
    """
    Represent checkerboard as two lists, black piece locations and white piece locations.
    White is at the bottom, and black is at the top. 
    The squares are ordered left to right and top to bottom

    White is 1, black is -1.
    """
    # numeric position from going left down, right down, left up, or right up from a square
    leftd = {**{i:i+4 for i in chain(range(1, 5), range(9, 13), range(17, 21), range(25,29))},
             **{i:i+3 for i in chain(range(6, 9), range(14,17), range(22, 25))}}
    rightd= {**{i:i+5 for i in chain(range(1, 4), range(9, 12), range(17, 20), range(25, 28))},
             **{i:i+4 for i in chain(range(5, 9), range(13,17), range(21, 25))}}
    leftu = {val:key for key, val in rightd.items()}
    rightu= {val:key for key, val in leftd.items()}


    def __init__(self, white=None, black=None, bkings=None, wkings=None, player=1):
        if white == None:
            white = list(range(21,33))
        if wkings == None:
            wkings = [0] * len(white)
        if black == None:
            black = list(range(1, 13))
        if bkings == None:
            bkings = [0] * len(black)
        self.white = white
        self.wkings = wkings
        self.black = black
        self.bkings = bkings
        self.player = player
        self.moves = []
        self.starting_position = [list(white), list(black)]

        
    def move(self, movement):
        """
        Movement is either 11-15 start end position or 15x22 a jump.

        Multiple jumps are 15x22x29.

        Regular checkers can only jump/move forward, king checkers can jump/move forward and backwards.

        If a regular checker reaches end of board, it becomes a king
        """
        pieces = self.white  if self.player == 1 else self.black
        other_pieces = self.white  if self.player == -1 else self.black
        kings  = self.wkings if self.player == 1 else self.bkings
        other_kings  = self.wkings if self.player == -1 else self.bkings
        if "x" in movement:
            moves = list(map(int, movement.split("x")))
            while len(moves) >= 2:
                start = moves.pop(0)
                end   = moves[0]
                assert start in pieces, str(start) + " not found in " + str(pieces) + " "
                assert end not in self.white and end not in self.black, "cannot jump to square " + str(end) + " since occupied by pieces already, white:" + str(self.white) + ", black: " + str(self.black)
                jumped_square = -1
                if kings[pieces.index(start)] == 1:
                    # Check all 4 directions
                    if self.leftu.get(self.leftu.get(start)) == end:
                        jumped_square = self.leftu.get(start)
                    elif self.rightu.get(self.rightu.get(start)) == end:
                        jumped_square = self.rightu.get(start)
                    elif self.leftd.get(self.leftd.get(start)) == end:
                        jumped_square = self.leftd.get(start)
                    elif self.rightd.get(self.rightd.get(start)) == end:
                        jumped_square = self.rightd.get(start)
                elif self.player == 1:
                    if self.leftu.get(self.leftu.get(start)) == end:
                        jumped_square = self.leftu.get(start)
                    elif self.rightu.get(self.rightu.get(start)) == end:
                        jumped_square = self.rightu.get(start)
                else:
                    if self.leftd.get(self.leftd.get(start)) == end:
                        jumped_square = self.leftd.get(start)
                    elif self.rightd.get(self.rightd.get(start)) == end:
                        jumped_square = self.rightd.get(start)
                assert jumped_square != -1, "invalid jump from " + str(start) + " to " + str(end)
                assert jumped_square in other_pieces, "jumped square " + str(jumped_square) + " not in " + str(other_pieces)
                other_kings.pop(other_pieces.index(jumped_square))
                other_pieces.pop(other_pieces.index(jumped_square))
                pieces[pieces.index(start)] = end
                if end in [1, 2, 3, 4, 29, 30, 31, 32]:
                    kings[pieces.index(end)] = 1
        else:
            start, end = map(int, movement.split("-"))
            assert start in pieces, str(start) + " not found in " + str(pieces) + " "
            assert end not in self.white and end not in self.black, "cannot jump to square " + str(end) + " since occupied by pieces already, white:" + str(self.white) + ", black: " + str(self.black)
            if kings[pieces.index(start)] == 1:
                assert self.leftu.get(start) == end or self.rightd.get(start) == end or self.rightu.get(start) == end or self.leftd.get(start) == end, "king " +str(start) + " cannot move to square " + str(end)
            elif self.player == 1:
                assert self.leftu.get(start) == end or self.rightu.get(start) == end, "white piece " +str(start) + " cannot move to square " + str(end)
            else:
                assert self.leftd.get(start) == end or self.rightd.get(start) == end, "black piece " +str(start) + " cannot move to square " + str(end)
            pieces[pieces.index(start)] = end
            if end in [1, 2, 3, 4, 29, 30, 31, 32]:
                kings[pieces.index(end)] = 1
            
        self.player = 1 if self.player == -1 else -1
        print(self)
    def make_move(self):
        pieces = self.white  if self.player == 1 else self.black
        other_pieces = self.white  if self.player == -1 else self.black
        kings  = self.wkings if self.player == 1 else self.bkings
        other_kings  = self.wkings if self.player == -1 else self.bkings
        # Easy Algorithm
        # Try's to jump, then makes random move
        moved = False
        for piece in random.sample(pieces, len(pieces)):
            try:
                self.move(str(piece)+"x"+str(self.leftu.get(self.leftu.get(piece))))
                moved = True
            except:
                pass
            if moved == True:
                return
            try:
                self.move(str(piece)+"x"+str(self.rightd.get(self.rightd.get(piece))))
                moved = True
            except:
                pass
            if moved == True:
                return
            try:
                self.move(str(piece)+"x"+str(self.rightu.get(self.rightu.get(piece))))
                moved = True
            except:
                pass
            if moved == True:
                return
            try:
                self.move(str(piece)+"x"+str(self.leftd.get(self.leftd.get(piece))))
                moved = True
            except:
                pass
            if moved == True:
                return
        for piece in random.sample(pieces, len(pieces)):
            try:
                self.move(str(piece)+"-"+str(self.leftu.get(piece)))
                moved = True
            except:
                pass
            if moved == True:
                return
            try:
                self.move(str(piece)+"-"+str(self.leftd.get(piece)))
                moved = True
            except:
                pass
            if moved == True:
                return
            try:
                self.move(str(piece)+"-"+str(self.rightd.get(piece)))
                moved = True
            except:
                pass
            if moved == True:
                return
            try:
                self.move(str(piece)+"-"+str(self.rightu.get(piece)))
                moved = True
            except:
                pass
            if moved == True:
                return
        
                    
        
    def __repr__(self):
        res = ""
        for j in range(1, 9):
            res += "|"
            for i in range(1, 9):
                cur = i + (j - 1) * 8 + ((j+1) % 2)
                if cur % 2 == 1:
                    res += "_"
                elif (cur // 2) in self.black:
                    res += "o"
                elif (cur // 2) in self.white:
                    res += "+"
                else:
                    res += "_"
                res += "|"
            res += "\n"
        return res

        
            
