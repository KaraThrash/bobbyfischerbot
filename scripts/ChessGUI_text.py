#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessGUI_text.py
 Description:  Draws a text based chess board in the console window.
    Gets user input through text entry.

 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """

from ChessRules import ChessRules

class ChessGUI_text:
    def __init__(self):
        self.Rules = ChessRules()

    # def GetGameSetupParams(self):
    #MOVED FUNCTIONALITY TO CHESSGAMEPARAMS.PY
        # player1Name = raw_input("Player 1 name: ")
        # player1Color = 'red'
        # while not player1Color == 'black' and not player1Color == 'white':
            # player1Color = raw_input("  Player 1 color ('white' or 'black'): ")
        # if player1Color == 'white':
            # player2Color = 'black'
        # else:
            # player2Color = 'white'
        # player1Type = 'monkey'
        # while not player1Type == 'human' and not player1Type == 'AI':
            # player1Type = raw_input("  Is player 1 'human' or 'AI'? ")

        # player2Name = raw_input("Player 2 name: ");
        # player2Type = 'monkey'
        # while not player2Type == 'human' and not player2Type == 'AI':
            # player2Type = raw_input("  Is player 2 'human' or 'AI'? ")

        # print "Setting up game..."
        # print "Player 1:", player1Name, player1Color, player1Type
        # print "Player 2:", player2Name, player2Color, player2Type

        # return (player1Name,player1Color,player1Type,player2Name,player2Color,player2Type)


    def Draw(self,board):
        print "     0   1   2   3   4   5   6   7 "
        print "   ----------------------------------------"
        count = -1
        for r in ['a','b','c','d','e','f','g','h']:
            count = count + 1
            print "",r,"|",
            for c in range(8):
                if board[count][c] != 'e':
                    print  str(board[count][c]), "|",
                else:
                    print "   |",
                if c == 7:
                    print #to get a new line
            print "   ----------------------------------------"

    def EndGame(self,board):
        self.Draw(board)

    def GetPlayerInput(self,board,color):
        fromTuple = self.GetPlayerInput_SquareFrom(board,color)
        toTuple = self.GetPlayerInput_SquareTo(board,color,fromTuple)
        return (fromTuple,toTuple)


    def GetPlayerInput_SquareFrom(self,board,color):
        ch = "?"
        cmd_r = 0
        cmd_c = 0
        cmd_c = 0
        rowinput = 0
        colinput = 0
        while (ch not in board[rowinput][colinput] or self.Rules.GetListOfValidMoves(board,color,(rowinput,colinput))==[]):
            print "Player", color
            # cmd_r = int(raw_input("  From row: "))
            # cmd_c = int(raw_input("  From col: "))
            rawinput = raw_input("> Your Move:\n ")
            if len(rawinput) != 2:
                print("invalid move")
            else: #97 - 104 a-h 48-56 0-7
                inputstring = rawinput.lower()
                if ord(inputstring[0]) >= 97 and ord(inputstring[0]) <= 104 and ord(inputstring[1]) >= 48 and ord(inputstring[1]) <= 56:
                    # print("row and col valid")
                    rowinput = ord(inputstring[0]) - 97
                    colinput = ord(inputstring[1]) - 48
                    if color == "black":
                        ch = "b"
                    else:
                        ch = "w"
                    if (board[rowinput][colinput] == 'e'):
                        print "  Nothing there!"
                    elif (ch not in board[rowinput][colinput]):
                        print "  That's not your piece!"
                    elif self.Rules.GetListOfValidMoves(board,color,(rowinput,colinput)) == []:
                        print "  No valid moves for that piece!"
                else:
                    print " -               - "
                    print " - Invalid Input - "
                    print " -               - "
        # print (rowinput,colinput)
        return (rowinput,colinput)
        #     if color == "black":
        #         ch = "b"
        #     else:
        #         ch = "w"
        #     if (board[cmd_r][cmd_c] == 'e'):
        #         print "  Nothing there!"
        #     elif (ch not in board[cmd_r][cmd_c]):
        #         print "  That's not your piece!"
        #     elif self.Rules.GetListOfValidMoves(board,color,(cmd_r,cmd_c)) == []:
        #         print "  No valid moves for that piece!"
        #
        # return (cmd_r,cmd_c)


    def GetPlayerInput_SquareTo(self,board,color,fromTuple):
        toTuple = ('x','x')
        collist = ['0','1','2','3','4','5','6','7']
        rowlist = ['a','b','c','d','e','f','g','h']
        validMoveList = self.Rules.GetListOfValidMoves(board,color,fromTuple)
        realvalidMoveList = []
        for el in validMoveList:
            temp = str(rowlist[el[0]]).upper() + str(collist[el[1]])
            realvalidMoveList.append(temp)
        # print "List of valid moves for piece at",rowlist[fromTuple[0]]collist[fromTuple[1]],": ", validMoveList
        print "List of valid moves for piece at",str(rowlist[fromTuple[0]]).upper() + str(collist[fromTuple[1]]),": ", realvalidMoveList

        while (not toTuple in validMoveList):
            rawinput = raw_input("> Target Square:\n ")
            if len(rawinput) != 2:
                print("invalid move")
            else: #97 - 104 a-h 48-56 0-7
                inputstring = rawinput.lower()

                if ord(inputstring[0]) >= 97 and ord(inputstring[0]) <= 104 and ord(inputstring[1]) >= 48 and ord(inputstring[1]) <= 56:
                    # print("row and col valid")
                    rowinput = ord(inputstring[0]) - 97
                    colinput = ord(inputstring[1]) - 48
                    toTuple = (rowinput,colinput)
                    if not inputstring in validMoveList:
                        print "  Invalid move!"
                    elif not toTuple in validMoveList:
                        print "  Invalid move!"
                    elif self.Rules.GetListOfValidMoves(board,color,(rowinput,colinput)) == []:
                        print "  No valid moves for that piece!"
                else:
                    print " -               - "
                    print " - Invalid Input - "
                    print " -               - "



        return toTuple


    def PrintMessage(self,message):
        print message

if __name__ == "__main__":
    from ChessBoard import ChessBoard

    cb = ChessBoard(0)

    gui = ChessGUI_text()
    gui.Draw(cb.GetState())
