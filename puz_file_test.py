import library.puz as puz
import library.beachdoglib as lib
import sys

def loadPuzFile(inputFile)
    puzzle = 
    solution = inputFile.solution

    puzzleGrid = [['' for i in range(inputFile.p.height)] for j in range(inputFile.p.width)]
    for i in range(p.height):
        for j in range(p.width):
            puzzleGrid[i] = solution[i * p.width:i * p.width + j + 1]
    return puzzleGrid


in_file = lib.userInputOpenFilePath()

grid = loadPuzFile(in_file)

print(grid)