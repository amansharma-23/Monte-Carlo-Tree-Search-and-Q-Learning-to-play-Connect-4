import numpy
import copy
import random
import gzip
import json
import matplotlib.pyplot

from numpy.random.mtrand import RandomState

##############

#Your program can go here.

ROWS = 4
COLUMNS = 5
EPSILON = 0.15
LEARNING_RATE = 0.7
GAMMA = 0.75


class connect4board():

    def __init__(self):
        self.board = numpy.zeros((ROWS,COLUMNS))

    def available_row(self,column):
        for i in reversed(range(ROWS)):
            if(self.board[i][column]==0):
                return i
        return -1

    def getValidMoves(self):
        valid_moves = []
        for col in range(COLUMNS):
            if(self.available_row(col)!=-1):
                valid_moves.append(col)
        return valid_moves


    def move(self,column,playernumber):
        if(self.available_row(column)!=-1):
            self.board[self.available_row(column)][column]= playernumber
            # if(self.winning_condition(playernumber)):
            if(self.winning_condition_efficient(playernumber,column)):
                return 1
            else:
                return 0
        else:
            return -1

    def winning_condition_efficient(self,player,column):
        toprow = 0
        for i in range(ROWS):
            if(self.board[i][column]!=0):
                toprow=i
                break
        # print(type(COLUMNS), "COL")
        # print(type(column),"col")
        # if((column)<COLUMNS-3):
        #     if(toprow-3>=0):
        #         if(self.board[toprow][column]==player and self.board[toprow-1][column+1]==player and self.board[toprow-2][column+2]==player and self.board[toprow-3][column+3]==player):
        #             return True
        #     if(toprow+3<ROWS):
        #         if(self.board[toprow][column]==player and self.board[toprow+1][column+1]==player and self.board[toprow+2][column+2]==player and self.board[toprow+3][column+3]==player):
        #             return True
        #     if(self.board[toprow][column]==player and self.board[toprow][column+1]==player and self.board[toprow][column+2]==player and self.board[toprow][column+3]==player):
        #             return True
        # if(column-3>=0):
        #     if(toprow-3>=0):
        #         if(self.board[toprow][column]==player and self.board[toprow-1][column-1]==player and self.board[toprow-2][column-2]==player and self.board[toprow-3][column-3]==player):
        #             return True
        #     if(toprow+3<ROWS):
        #         if(self.board[toprow][column]==player and self.board[toprow+1][column-1]==player and self.board[toprow+2][column-2]==player and self.board[toprow+3][column-3]==player):
        #             return True
        #     if(self.board[toprow][column]==player and self.board[toprow][column-1]==player and self.board[toprow][column-2]==player and self.board[toprow][column-3]==player):
        #             return True
        # if(toprow+3<ROWS):
        #     if(self.board[toprow][column]==player and self.board[toprow+1][column]==player and self.board[toprow+2][column]==player and self.board[toprow+3][column]==player):
        #             return True
        # return False

        for i in range(ROWS):
            if(toprow!=i):
                continue
            for j in range(COLUMNS-3):
                if(column<j or column>j+3):
                    continue
                if(self.board[i][j]==player and self.board[i][j+1]==player and self.board[i][j+2]==player and self.board[i][j+3]==player):
                    return True
        
        for i in range(ROWS-3):
            if(toprow<i or toprow>i+3):
                continue
            for j in range(COLUMNS):
                if(column!=j):
                    continue
                if(self.board[i][j]==player and self.board[i+1][j]==player and self.board[i+2][j]==player and self.board[i+3][j]==player):
                    return True

        for i in range(ROWS-3):
            if(toprow<i or toprow>i+3):
                continue
            for j in range(COLUMNS-3):
                if(column<j or column>j+3):
                    continue
                if(self.board[i][j]==player and self.board[i+1][j+1]==player and self.board[i+2][j+2]==player and self.board[i+3][j+3]==player):
                    return True

        for i in range(ROWS-3):
            if(toprow<i or toprow>i+3):
                continue
            for j in range(3,COLUMNS):
                if(self.board[i][j]==player and self.board[i+1][j-1]==player and self.board[i+2][j-2]==player and self.board[i+3][j-3]==player):
                    return True

        return False
    
    def winning_condition(self,player):

        for i in range(ROWS):
            for j in range(COLUMNS-3):
                if(self.board[i][j]==player and self.board[i][j+1]==player and self.board[i][j+2]==player and self.board[i][j+3]==player):
                    return True
        
        for i in range(ROWS-3):
            for j in range(COLUMNS):
                if(self.board[i][j]==player and self.board[i+1][j]==player and self.board[i+2][j]==player and self.board[i+3][j]==player):
                    return True

        for i in range(ROWS-3):
            for j in range(COLUMNS-3):
                if(self.board[i][j]==player and self.board[i+1][j+1]==player and self.board[i+2][j+2]==player and self.board[i+3][j+3]==player):
                    return True

        for i in range(ROWS-3):
            for j in range(3,COLUMNS):
                if(self.board[i][j]==player and self.board[i+1][j-1]==player and self.board[i+2][j-2]==player and self.board[i+3][j-3]==player):
                    return True

        return False

    def full(self):
        f = True
        for i in range(COLUMNS):
            if self.board[0][i]==0:
                f = False
        return f

class MCTS_Node():
    def __init__(self, board, parent, player,move):
        self.board=board
        self.parent=parent
        self.children=[]
        self.wins = 0
        self.loses = 0
        self.move = move
        self.count = 0
        self.player = player

def ucb_score(node,parentnode):
    exploration = 100000000000000
    if(node.count>0):
        exploration = 2*numpy.sqrt(numpy.log(parentnode.count)/node.count)
    exploitation = 0
    if(node.count>0):
        exploitation = node.wins/node.count
        # exploitation = (node.wins-(node.loses*5))/node.count
    # print(exploration," ",node.count," ",parentnode.count)
    # print(exploitation," ",node.wins," ",node.count," ",node.loses)
    return exploitation+exploration

def play_game_mcts(myboard):
    turn = 1
    while(True):
        if(turn%2==1):
            # inp = int(input("player 1 : "))
            print("Player 1 (MCTS200)")
            inp = MCTS(copy.deepcopy(myboard),1,200)
            print("Action selected: ", inp)
            # inp = random_player(myboard)
            attempt = myboard.move(inp,1)
            print(myboard.board)
            if(attempt==1):
                print()
                print()
                print("Total Moves: ",turn)
                return 1
            elif(attempt==-1):
                continue
        else:
            # print(MCTS(copy.deepcopy(board),2,2))
            print("Player 2 (MCTS40)")
            inp = MCTS(copy.deepcopy(myboard),2,40)
            print("Action selected: ", inp)
            # inp = random_player(myboard)
            # inp = Q_learning(myboard,2)
            # inp = int(input("player 2 : "))
            attempt = myboard.move(inp,2)
            print(myboard.board)
            if(attempt==1):
                print()
                print()
                print("Total Moves: ",turn)
                return 2
            elif(attempt==-1):
                continue
            # # attempt = board.move(inp,2)
            # # attempt = 
            # if(myboard.winning_condition(2)):
            #     return 2
            # # elif(board.winning_condition(2)==-1):
            # #     continue
        turn = (turn+1)
        if(myboard.full()):
            return 0
        print()
        print()

def getWinningMoves(board,player):
    winning_moves = []
    valid_moves = board.getValidMoves()
    # print(valid_moves)
    # print("player: ",player)
    for move in valid_moves:
        temp = copy.deepcopy(board)
        result = temp.move(move,player)
        # if(temp.winning_condition_efficient(player,move)):
        if(result==1):
            winning_moves.append(move)
    # print(winning_moves)
    return winning_moves



def MCTS(board,player,iterations):
   
    winning_moves = getWinningMoves(board,player)
    if (len(winning_moves)>0):
        print("Value of next state according to MCTS",iterations,": ", "infinite (winning move found)")
        # print("winning move returned")
        return winning_moves[0]
    root = MCTS_Node(copy.deepcopy(board),None,player,None)
    # print(root)
    for i in range(iterations):
        # print(i)
        current_node = root
        # print(len(current_node.children))
        # print(root.board.board)
        # print(current_node.board.board)
        # print(current_node)
        # selection
        while(len(current_node.children)!=0):
                current_node = select(current_node)
        # print(i,board)
        # exploration
        result = 0
        # if(current_node.board.winning_condition(1) or current_node.board.winning_condition(2) or current_node.board.full()):
        #     pass
        newnode=current_node
        for p in range(1):
            if(current_node.count==0):
                result = rollout(copy.deepcopy(current_node.board),current_node.player)
            else:
                newnode = expand(current_node)
                result = rollout(copy.deepcopy(newnode.board),newnode.player)
            if(result==player):
                result = 1
            elif(result==((player+1)%2)):
                result = -1
            backpropagate(newnode,result)
    count = 0
    ans = None
    for child in root.children:
        if(child.count>count):
            count=child.count
            ans=child
    print("Value of next state according to MCTS",iterations,": ", ucb_score(ans,root))
    return ans.move
        
        
def rollout(board,player):
    valid_moves  = board.getValidMoves()
    # print(valid_moves)
    # print("valid moves -",valid_moves)
    # print(board.board)
    childplayer = 1
    if(player==1):
        childplayer = 2
    if(len(valid_moves)==0):
        if(board.winning_condition(childplayer)):
            return childplayer
        elif(board.winning_condition(player)):
            return player
        else:
            return 0

    m = random.choice(valid_moves)
    # print(m)
    if(board.move(m,player)==1):
        return player
    elif(board.full()):
        return 0
    # print(board.board)
    return rollout(board,childplayer)

def backpropagate(node,result):
    node.count= node.count+1
    if(result==1):
        node.wins = node.wins+1
    elif(result==-1):
        node.loses = node.loses+1
    # print(node.wins," ",node.count)
    if(node.parent!=None):
        backpropagate(node.parent,result)

def select(node):
    highestUCB = -10000
    childWithHighestUcb = None
    for i in node.children:
        if(ucb_score(i,node)>highestUCB):
            highestUCB=ucb_score(i,node)
            childWithHighestUcb=i
    return childWithHighestUcb

def expand(parent_node):
    valid_moves = parent_node.board.getValidMoves()
    childplayer = 1
    if(len(valid_moves)==0):
        return parent_node
    for move in valid_moves:
        childplayer = 1
        if(parent_node.player==1):
            childplayer = 2
        newnode = MCTS_Node(copy.deepcopy(parent_node.board),parent_node,childplayer,move)
        # print(newnode.player," ",childplayer)
        newnode.board.move(move,parent_node.player)
        parent_node.children.append(newnode)
    return parent_node.children[0]


map = {}

def Q_learning_train(board):
    turn = 0
    reward=0
    while(True):
        if(turn==1):
            laststate = numpy.array2string(board.board)
            if(laststate not in map.keys()):
                map[laststate]=0
            inp = Q_learning_move(board,2)
            n = random.randint(0,100)
            if(n<100*EPSILON):
                nextmove = random.choices(board.getValidMoves())
                inp = nextmove[0]
            result = board.move(inp,2)
            if(result==1):
                reward=1
            else:
                reward=0
            newstate = numpy.array2string(board.board)
            if(newstate not in map.keys()):
                map[newstate]=0
            map[laststate] = map[laststate] + LEARNING_RATE * (reward + GAMMA * (map[newstate] - map[laststate]) )
            if(result==1):
                return 2
        else:
            laststate = numpy.array2string(board.board)
            if(laststate not in map.keys()):
                map[laststate]=0
            n = random.randint(2,25)
            inp = MCTS(copy.deepcopy(board),1,n)
            # inp = random_player(board)
            result = board.move(inp,1)
            if(result==1):
                reward=-1
            else:
                reward=0
            newstate = numpy.array2string(board.board)
            if(newstate not in map.keys()):
                map[newstate]=0
            map[laststate] = map[laststate] + LEARNING_RATE * (reward + GAMMA * (map[newstate] - map[laststate]) )
            if(result==1):
                return 1
        if(board.full()):
            return 0
        turn = (turn+1)%2
            


        


def Q_learning_move(board,player):
    valid_moves = board.getValidMoves()
    boardstring = numpy.array2string(board.board)
    if boardstring not in map.keys():
        map[boardstring]=0
    nextmove = None
    # reward = 0
    beststatevalue=-1000000000
    for i in valid_moves:
        newboard = copy.deepcopy(board)
        newboard.move(i,player)
        newboardstring = numpy.array2string(newboard.board)
        if(newboardstring not in map.keys()):
            map[newboardstring]=0
        if(map[newboardstring]>beststatevalue):
            beststatevalue=map[newboardstring]
            nextmove=i
    # n = random.randint(0,100)
    # if(n<100*EPSILON):
    #     nextmove = random.choices(valid_moves)
    #     nextmove = nextmove[0]
    print("value of next state according to Q-learning: ",beststatevalue)
    return nextmove
            

def random_player(board):
    valid_moves = board.getValidMoves()
    move = random.choices(valid_moves)
    # print(type(move))
    return move[0]


def play_game_qlearning(board):
    turn = 1
    while(True):
        if(turn%2==1):
            print("Player 1: MCn")
            inp = MCTS(copy.deepcopy(board),1,9)
            print("Action selected: ", inp)
            result = board.move(inp,1)
            if(result==1):
                print(board.board)
                print()
                print()
                print("total turns: ",turn)
                return 1
        else:
            print("Player 2: Q-Learning")
            inp = Q_learning_move(board,2)
            print("Action selected: ", inp)
            result = board.move(inp,2)
            if(result==1):
                print(board.board)
                print()
                print()
                print("total turns: ",turn)
                return 2
        print(board.board)
        print()
        print()
        turn = (turn+1)
        if(board.full()):
            return 0



###############


def PrintGrid(positions):
    print('\n'.join(' '.join(str(x) for x in row) for row in positions))
    print()

def main():
    
    print("Welcome!")
    inp = (input("For part (a) enter a, for part (c) enter c: "))
    if(inp == 'a' or inp=='A'):
        global ROWS
        ROWS = 6
        board=connect4board()
        result = play_game_mcts(board)
        if(result==1):
            print("Player 1 (MCTS200) has won.")
        elif(result==2):
            print("player 2 (MCTS40) has won.")
        else:
            print("game drawn")
    elif(inp=='c' or inp=='C'):
        load = gzip.open('2019A7PS0053G_AMAN.dat.gz','rb').read()
        # print(json.loads(load))
        global map
        map = json.loads(load)
        print("The q-learning algorithm can win consistently against MC9 with r=4. The win percentage is a little lower against higher values of n")

        # print(map)
        # inp = int(input("Enter n: "))
        board = connect4board()
        result = play_game_qlearning(board)
        if(result==1):
            print("Player 1 (MCn) has won.")
        elif(result==2):
            print("player 2 (Qlearning) has won.")
        else:
            print("game drawn")


        # map["abcd"]="efgh"
        # map["ijkl"]="mnop"
        # tobesaved = json.dumps(map)
        # tobesaved = tobesaved.encode()
        # gzip.open('2019A7PS0053G_AMAN.dat.gz','wb').write(tobesaved)

    # num = []
    # den = []

    # print("main")
    # wins = 0
    # lose = 0
    # draw = 0
    # for i in range(20000):
    #     board=connect4board()
    #     result = Q_learning_train(board)
    #     if(result==2):
    #         # print("win")
    #         wins = wins+1
    #     elif(result==1):
    #         # print("lose")
    #         lose = lose+1
    #     else:
    #         # print("draw")
    #         draw=draw+1
    #     num.append(100*wins/(i+1))
    #     den.append(i+1)
    #     if(i%100==0):
    #         print(wins,"/",draw,"/",lose)

    # matplotlib.pyplot.plot(den,num)
    # matplotlib.pyplot.xlabel("Number of iterations")
    # matplotlib.pyplot.ylabel("Accuracy")
    # matplotlib.pyplot.show()
    # tobesaved = json.dumps(map)
    # tobesaved = tobesaved.encode()
    # gzip.open('2019A7PS0053G_AMAN.dat.gz','wb').write(tobesaved)

    # tobesaved = json.dumps(map)
    # tobesaved = tobesaved.encode()
    # gzip.open('2019A7PS0053G_AMAN.dat.gz','wb').write(tobesaved)


    # for i in range(1000):
    #     board = connect4board()
    #     result = play_game(board,1,2)

    # dict = {}
    # dict["a"]="b"
    # dict["c"]="d"
    # print(dict)
    # print(str(dict))
    # s = json.dumps(dict)
    # s = s.encode()
    # print(s)
    # print(json.loads(s))




    

    


    # ones=0
    # twos=0
    # draws=0
    # for i in range(50):
    #     board = connect4board()
    #     result = play_game_mcts(board)
    #     if(result==1):
    #         ones = ones+1
    #     elif(result==2):
    #         twos = twos+1
    #     else:
    #         draws=draws+1
    # print(ones," ",draws," ",twos)


    # print(type(numpy.array2string(board.board)))
    # s = numpy.array2string(board.board)
    # p = numpy.array2string(board.board)
    # dict = {}
    # dict[s] = True
    # dict[p] = False
    # print(dict[s])
    # result = play_game(board,1,2)
    # board.move(0,1)
    # board.move(0,1)
    # board.move(0,1)
    # board.move(0,1)
    # board.move(0,1)
    # board.move(1,1)
    # board.move(1,1)
    # board.move(1,1)
    # board.move(1,1)
    # board.move(1,1)
    # board.move(2,1)
    # board.move(2,1)
    # board.move(2,1)
    # board.move(2,1)
    # board.move(2,1)
    # board.move(3,1)
    # board.move(3,1)
    # board.move(3,1)
    # board.move(3,1)
    # board.move(3,1)
    # board.move(4,1)
    # board.move(4,1)
    # board.move(4,1)
    # board.move(4,1)
    # board.move(4,1)
    # print(board.getValidMoves())
    # board = connect4board()
    # # Q_learning(board)
    # result = play_game(board,1,2)
    # print(board.board)
    # # for i in reversed(range(ROWS)):
    # #     print(i)
    # print("player " , result , "wins")

    # PrintGrid(board.board)
    # print("************ Sample output of your program *******")

    # game1 = [[0,0,0,0,0],
    #       [0,0,0,0,0],
    #       [0,0,1,0,0],
    #       [0,2,2,0,0],
    #       [1,1,2,2,0],
    #       [2,1,1,1,2],
    #     ]


    # game2 = [[0,0,0,0,0],
    #       [0,0,0,0,0],
    #       [0,0,1,0,0],
    #       [1,2,2,0,0],
    #       [1,1,2,2,0],
    #       [2,1,1,1,2],
    #     ]

    
    # game3 = [ [0,0,0,0,0],
    #           [0,0,0,0,0],
    #           [0,2,1,0,0],
    #           [1,2,2,0,0],
    #           [1,1,2,2,0],
    #           [2,1,1,1,2],
    #         ]

    # print('Player 2 (Q-learning)')
    # print('Action selected : 2')
    # print('Value of next state according to Q-learning : .7312')
    # PrintGrid(game1)


    # print('Player 1 (MCTS with 25 playouts')
    # print('Action selected : 1')
    # print('Total playouts for next state: 5')
    # print('Value of next state according to MCTS : .1231')
    # PrintGrid(game2)

    # print('Player 2 (Q-learning)')
    # print('Action selected : 2')
    # print('Value of next state : 1')
    # PrintGrid(game3)
    
    # print('Player 2 has WON. Total moves = 14.')
    
if __name__=='__main__':
    main()