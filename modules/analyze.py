import library.beachdoglib as library
from pathlib import Path

def puzzleLayout(grid:list[str]) -> tuple[list[list[int]], dict[int, str], dict[int, str]]:
    """Returns the numbering grid and across and down dictionaries."""
    across, down = {}, {}
    rows, cols = len(grid), len(grid[0])
    numbering = [[0 if grid[x][y] != '.' else -1 for y in range(cols)] for x in range(rows)]
    
    clueNumber = 1
    
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == '.':
                continue
            
            # Check if a clue number should be assigned
            isNewAcross = (y == 0 or grid[x][y - 1] == '.')
            isNewDown = (x == 0 or grid[x - 1][y] == '.')
            
            if isNewAcross or isNewDown:
                numbering[x][y] = clueNumber
                
                # Add across word if new across clue
                if isNewAcross:
                    across[clueNumber] = fillWordAcross(grid, x, y)
                
                # Add down word if new down clue
                if isNewDown:
                    down[clueNumber] = fillWordDown(grid, x, y)
                
                clueNumber += 1

    return numbering, across, down

def gridCountBlocks(grid:list[str]) -> int:
    """Returns the number of '.' characters (blocks) in the grid."""
    return sum(row.count('.') for row in grid)

def gridCountOpens(grid:list[str]) -> int:
    """Returns the open square count for the grid"""
    x = 0
    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if i == 0:
                if j == 0:
                    touching = {grid[i][j] == '.', grid[i][j+1] == '.',
                                grid[i+1][j] == '.', grid[i+1][j+1] == '.'
                                }
                elif j == cols - 1:
                    touching = {grid[i][j-1] == '.', grid[i][j] == '.',
                                grid[i+1][j-1] == '.', grid[i+1][j] == '.'
                                }
                elif j > 0 and j < cols - 1:
                    touching = {grid[i][j-1] == '.', grid[i][j] == '.', grid[i][j+1] == '.',
                                grid[i+1][j-1] == '.', grid[i+1][j] == '.', grid[i+1][j+1] == '.'
                                }
            elif i == rows - 1:
                if j == 0:
                    touching = {grid[i-1][j] == '.', grid[i-1][j+1] == '.',
                                grid[i][j] == '.', grid[i][j+1] == '.'
                                }
                elif j == cols - 1:
                    touching = {grid[i-1][j-1] == '.', grid[i-1][j] == '.',
                                grid[i][j-1] == '.', grid[i][j] == '.' 
                                }
                elif j > 0 and j < cols - 1:
                    touching = {grid[i-1][j-1] == '.', grid[i-1][j] == '.',grid[i-1][j+1] == '.',
                                grid[i][j-1] == '.', grid[i][j] == '.', grid[i][j+1] == '.'
                                }
            else:
                if j == 0:
                    touching = {grid[i-1][j] == '.', grid[i-1][j+1] == '.', grid[i][j] == '.',
                                grid[i][j+1] == '.', grid[i+1][j] == '.', grid[i+1][j+1] == '.'
                                }
                elif j == cols - 1:
                    touching = {grid[i-1][j-1] == '.', grid[i-1][j] == '.', grid[i][j-1] == '.',
                                grid[i][j] == '.', grid[i+1][j-1] == '.', grid[i+1][j] == '.'
                                }
                elif j > 0 and j < cols - 1:
                    touching = {grid[i-1][j-1] == '.', grid[i-1][j] == '.', grid[i-1][j+1] == '.',
                                grid[i][j-1] == '.', grid[i][j] == '.', grid[i][j+1] == '.',
                                grid[i+1][j-1] == '.', grid[i+1][j] == '.', grid[i+1][j+1] == '.'
                                }
            if not any(touching):
                x += 1
    return(x)

def gridCountSpans(words:list[str]) -> int:
    """Returns the numbe of spans in the grid"""
    return len([entry for entry in words if len(entry) == 15])

def gridCountLongs(words:list[str]) -> int:
    """Returns the number of words in the grid of 8 letters or longer"""
    return len([entry for entry in words if len(entry) >= 8])

def gridCountThrees(words:list[str]) -> int:
    """Returns the numbe of 15-letter spans in the grid"""
    return len([entry for entry in words if len(entry) == 3])

def gridAverageLength(words:list[str]) -> float:
    """Returns the average length of the words in the grid"""
    import numpy as np
    return np.average([len(word) for word in words])

def fillWordAcross(grid:list[str], x:int, y:int) -> str:
    """Returns the across word at position [x, y,] in the grid"""
    line = grid[x][y:]
    if '.' in line:
        word = line[:line.find('.')].upper()
    else:
        word = line.upper()
    return(word)

def fillWordDown(grid:list[str], x:int, y:int) -> str:
    """Returns the down word at position [x, y,] in the grid"""
    line = ''
    for row in range(x, len(grid)):
        line += grid[row][y]
    if '.' in line:
        word = line[:line.find('.')].upper()
    else:
        word = line.upper()
    return(word)

def fillWordsList(across:dict[int,str], down:dict[int,str]) -> list[str]:
    """Returns an unscored list of all words in the puzzle"""
    return list(across.values()) + list(down.values())

def fillWordsScores(words:list[str]) -> dict[str,int]:
    """Returns dictionary of words in the fill with scores"""
    gDict = library.goldDict(min_score=0)
    scores = {word: gDict[word] for word in words}
    return scores

def fillCountLetters(grid:list[str]) -> dict[str,int]:
    """Returns the letter count of the fill {letters: count}"""
    # Join all rows into a single string and count letters from the ALPHABET
    ALPHABET = [
        'A', 'B', 'C', 'D', 'E', 'F',
        'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X',
        'Y', 'Z'
    ]
    joinedGrid = ''.join(grid)
    return {letter: joinedGrid.count(letter) for letter in ALPHABET}

def fillCountUniques(scores:list[str]) -> int:
    """Returns the number of unique words in the fill that are not in Jeff's list (xDict)."""
    xDict = library.xwiDict()
    return len([word for word in scores if word not in xDict])

def fillCountOvers(scores: dict[str,int]) -> int:
    """Returns the over/under count for the fill"""
    return len([x for x in scores if scores[x] > 50])

def fillAvergeScrabble(puzzleGrid:list[str]) -> float:
    """Returns the Scrabble average of the letters in the fill"""
    t = 0

    for i in range(len(puzzleGrid)):
        for j in range(len(puzzleGrid[0])):
            if puzzleGrid[i][j] != '.':
                t += library.SCRABBLE_VALUES[puzzleGrid[i][j]]
    
    a = t / (len(puzzleGrid) * len(puzzleGrid[0]) - gridCountBlocks(puzzleGrid))
    return a

def fillAverageScore(scores:dict[str,int]) -> float:
    """Returns the weighted average word score for the fill"""
    import numpy as np
    score = np.array(list(scores.values()))
    weight = np.array([len(word) for word in scores])
    weightedSum = np.dot(score, weight)
    totalWeight = np.sum(weight)

    return weightedSum / totalWeight if totalWeight != 0 else 0.0

def fillAverageOvers(score:dict[str,int]) -> float:
    """Returns the weighted average word score for the fill"""
    overScores = [score[word] for word in score if score[word] > 50]
    average = sum(overScores) / len(overScores)
    return average

def countHighScores(scores:dict[str,int]) -> list[int]:
    scoreCount = [0, 0, 0]
    for score in scores.values():
        if score == 60:
            scoreCount[0] += 1
        elif score == 70:
            scoreCount[1] += 1
        elif score == 80:
            scoreCount[2] += 1
    return scoreCount

def missingLetters(grid:list[list[str]]) -> str:
    missing = ''
    ALPHABET = [
        'A', 'B', 'C', 'D', 'E', 'F',
        'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X',
        'Y', 'Z'
    ]
    letterDist = fillCountLetters(grid)
    for letter in ALPHABET:
        if int(letterDist[letter]) == 0:
            missing += f' {letter}'
    if not missing:
        missing = 'PANGRAM'
    return missing
    
def outputCrossers(numbering:list[list[int]], across, down) -> None:
    """Prints the word crossings for the across words"""
    t = 1
    rows = len(numbering)
    cols = len(numbering[0])
    message = ''
    acr = [[0 for z in range(cols)] for y in range(rows)]
    dwn = [[0 for z in range(cols)] for y in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if numbering[i][j] == -1:
                acr[i][j] = 0
                continue
            if j == 0:
                acr[i][j] = numbering[i][j]
            elif numbering[i][j-1] == -1:
                acr[i][j] = numbering[i][j]
            else:
                acr[i][j] = acr[i][j-1]
                
    for i in range(rows):
        for j in range(cols):
            if numbering[i][j] == -1:
                dwn[i][j] = 0
                continue
            if i == 0:
                dwn[i][j] = numbering[i][j]
            elif numbering[i-1][j] == -1:
                dwn[i][j] = numbering[i][j]
            else:
                dwn[i][j] = dwn[i-1][j]
    
    for i in range(rows):
        for j in range(cols):
            if acr[i][j] != 0 and t == 1:
                message += f'{' '*(15 - len(across[acr[i][j]]))} {across[acr[i][j]]} {down[dwn[i][j]]}\n'
                t += 1
            elif acr[i][j] != 0:
                message += f'{' '*16} {down[dwn[i][j]]}\n'
                t += 1
            if j == cols-1:
                message += '\n'
                t = 1
            elif acr[i][j] != acr[i][j+1] and acr[i][j] != 0:
                message += '\n'
                t = 1
    return message

def fillCountLengths(words:list[str]) -> dict[str,int]:
    """Prints the bar chart of number of words by length"""
    from collections import Counter
    import numpy
    length = []

    for entry in words:
        length.append(len(entry))

    wordDist = dict(Counter(length))
    for i in range(3, 16):
        if i not in wordDist:
            wordDist[i] = 0
    return wordDist
