#serial port communication library
import serial
import time

#helps us break the board's ascii output into a 2d array for gui and IO utilization
def formatASCII(ASCIIBoard):
    #initialize an empty char array to represent the ascii board
    boardArray = [
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','','']
    ]
    
    #take the board object and make it a string
    #reformat it to be only piece and space characters
    #make a list with each element being an array from the board object string
    reformattedASCII = str(ASCIIBoard)
    reformattedASCII = reformattedASCII.replace(' ', '')
    reformattedASCII = reformattedASCII.replace('\n', '')
    charList = [char for char in reformattedASCII]

    #iterate through the boardArray and assign each element it's corresponding charList Element
    charListIndex = 0
    for i in range(0,8):
        for j in range(0,8):
            boardArray[i][j] = charList[charListIndex]
            charListIndex = charListIndex + 1

    #return an I/O compatible boardArray
    return boardArray

