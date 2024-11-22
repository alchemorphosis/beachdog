import modules.puz as puz
import library.beachdoglib as lib
import sys


p = puz.read(lib.userInputOpenFilePath())

# numbering = p.clue_numbering()

solution = p.solution
# print(p.width)
# print(p.height)

grid = [['' for i in range(p.height)] for j in range(p.width)]

for i in range(p.height):
    for j in range(p.width):
        grid[i] = solution[i * p.width:i * p.width + j + 1]

rows = p.height
cols = p.width

print(rows, cols)

print(grid)



# print()
# print('Across')
# for clue in numbering.across:
#     answer = ''.join(
#         p.solution[clue['cell'] + i]
#         for i in range(clue['len']))
#     print(clue['num'], clue['clue'], '-', answer)
# print()
# print()

# print('Down')
# for clue in numbering.down:
#     answer = ''.join(
#         p.solution[clue['cell'] + i * numbering.width]
#         for i in range(clue['len']))
#     print(clue['num'], clue['clue'], '-', answer)

# print()
# print()

# # Print the grid::

# for row in range(p.height):
#     cell = row * p.width
#     # Substitute p.solution for p.fill to print the answers
#     print(' '.join(p.fill[cell:cell + p.width]))

# # Unlock a scrambled solution::

# #     p.unlock_solution(7844)
#     # p.solution is unscambled

# Save a puzzle with modifications::

#     p.fill = 'LAMB' + p.fill[4:]
#     p.save('mine.puz')
