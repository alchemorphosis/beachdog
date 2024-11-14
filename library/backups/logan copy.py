
# Import Libraries
import sys
import os
import ssl
import shutil
from os import system
from os.path import exists
from pathlib import Path
from tkinter import *
from tkinter import ttk 
# Fix ssl
context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context
# Import constants
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
            ]
SCRABBLE_VALUES = {'A':1, 'E':1, 'I':1, 'O':1, 'U':1, 'L':1, 'N':1,
                   'S':1, 'T':1, 'R':1, 'D':2, 'G':2, 'B':3, 'C':3,
                   'M':3, 'P':3, 'F':4, 'H':4, 'V':4, 'W':4,
                   'Y':4, 'K':5, 'J':8, 'X':8, 'Q':10, 'Z':10
                   }
# Set Default Directories
downloads = Path().home() / 'iCloudDrive' / 'Downloads'
desktop = Path().home() / 'iCloudDrive' / 'Desktop'
documents = Path().home() / 'iCloudDrive' / 'Documents'
pyLib = Path().cwd() / '.library'
listDir = documents / 'Work' / 'Crosswords' / 'Lists' / 'Masters'
# Set Default File Paths
masterFile = listDir / 'Logan_Gold_Master.txt'
xwiFile = listDir / 'XwiJeffChenList.txt'
clueFile = listDir / 'Clue Database.txt'
masterFile_backup = listDir / 'Logan_Gold_Master.bak'
# Define Classes
class l:
    """Defines a set of lines for drawing grids."""
    tlc = '\u250C' # ┌ 
    trc = '\u2510' # ┐
    blc = '\u2514' # └ 
    brc = '\u2518' # ┘
    ver = '\u2502' # │
    hor = '\u2500' # ─ 
    int = '\u253C' # ┼ 
    lst = '\u251C' # ├
    rst = '\u2524' # ┤
    tst = '\u252C' # ┬
    bst = '\u2534' # ┴
    # blk = '\u2591' # ░
class b:
    """Defines a set of blocks for drawing grids."""
    fb = '\u2588' # █ 
    uh = '\u2580' # ▀ 
    bh = '\u2584' # ▄
    rh = '\u2590' # ▐ 
    lh = '\u258C' # ▌
    ul = '\u2598' # ▘
    ur = '\u259D' # ▝
    bl = '\u2596' # ▖
    br = '\u2597' # ▗
    nbtl = '\u259F' # ▟
    nbtr = '\u2599' # ▙
    nbbl = '\u259C' # ▜
    nbbr = '\u259B' # ▜
class c:
    """Defines a set of color classes for printing."""
    d = '\033[90m'
    r = '\033[91m' # ightred
    y = '\033[93m' # lightyellow
    w = '\033[0m' # reset
    c = '\033[96m' # cyan
    g = '\033[92m' # lightgreen
    p = '\033[95m' # lightpurple
    b = '\033[1m' # bold

# Create lists and dictionaries

def myList(min_score:int=50, min_len:int=3, max_len:int=15) -> list[str]:
    """Input; my word list file: Output; list of scored words"""
    return fileToList(masterFile, min_score, min_len, max_len)

def xwiList(min_score:int=50, min_len:int=3, max_len:int=15) -> list[str]:
    """Imports Jeff's word list to a list of scored words"""
    return fileToList(xwiFile, min_score, min_len, max_len)

def goldList(min_score:int=50, min_len:int=3, max_len:int=15) -> list[str]:
    """Returns a gold list of scored words with my scores prevailing"""
    return dictToList(goldDict(min_score, min_len, max_len))

def myDict(min_score:int=50, min_len:int=3, max_len:int=15) -> dict[str,int]:
    """Imports my word list to a dictionary of scored words"""
    dictionary = {}
    for entry in myList(min_score, min_len, max_len):
        w, s = entry.split(';')
        dictionary.update({w: int(s)})
    return dictionary

def xwiDict(min_score:int=50, min_len:int=3, max_len:int=15) -> dict[str,int]:
    """Imports Jeff's file to dictionary of scored words"""
    dictionary = {}
    for entry in xwiList(min_score, min_len, max_len):
        w, s = entry.split(';')
        dictionary.update({w : int(s)})
    return dictionary

def goldDict(min_score:int=50, min_len:int=3, max_len:int=15) -> dict[str,int]:
    """Imports mine and Jeff's word lists to a combined dictionary of scored words"""
    dictionary = {}
    dictionary.update(xwiDict(min_score, min_len, max_len))
    dictionary.update(myDict(min_score, min_len, max_len))
    return dictionary

# Convert between lists and dictionaries

def listToDict(input_list:list[str]) -> dict[str,int]:
    """Converts a list of words to a dictionary of words"""
    dictionary = {}
    for entry in input_list:
        w, s = entry.split(';')
        dictionary.update({w : int(s)})
    return dictionary

def dictToList(in_dict:dict[str,int]) -> list[str]:
    """Converts a word dictionary to a list of words"""
    answer = []
    for entry in in_dict:
        string = entry + ';' + str(in_dict[entry])
        answer.append(string)
    return answer 

# File Operations

def fileToList(open_file:Path, min_score:int=0, min_len:int=3, max_len:int=15) -> list[str]:
    """Imports a word list file to list of scored words"""
    if open_file:
        f = open(open_file, 'r')
        wordList = [line.strip().upper() for line in f
                                if int(line.split(';')[1]) >= min_score
                                if len(line.split(';')[0]) >= min_len
                                if len(line.split(';')[0]) <= max_len
                                if line.strip()
                                ]
        f.close()
        return wordList
    
def fileToDict(open_file:Path, min_score:int=0, min_len:int=3, max_len:int=15) -> dict[str,int]:
    """Imports a word list file to dictionary of scored words"""
    return listToDict(fileToList(open_file, min_score, min_len, max_len))

def listToFile(input_list, save_file:Path) -> None:
    """Writes a word list to a file"""
    if save_file:
        with open(save_file, 'w') as f:
            for item in input_list:
                f.write('%s\n' % item)
        return
    else:
        opCancel()
    
def dictToFile(input_dict:dict[str,int], save_file:Path) -> None:
    """Writes a word dictionary to a file"""
    return(listToFile(dictToList(input_dict), save_file))

# User Input

def userInputLengthAndScore():
    """Gets user word length value input"""
    root = Tk()
    root.title('') 
    root.geometry('290x150+450+300')
    root.resizable(False, False)
    root.overrideredirect(True)

    def get_input():
        global y, z
        y = length.get()
        z = scr.get()
        root.destroy()

    # label text for title
    length_label = Label(root, text="   Select a Word Length:", font=('Fira Code', 10), justify='right')
    length_label.grid(row=0, column=0)

    # Length Combobox creation
    length = IntVar() 
    length_choosen = ttk.Combobox(root, width=4, textvariable=length, font=('Fira Code', 10), state="readonly") 
    length_choosen['values'] = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15) 
    length_choosen.grid(row=0, column=1, padx=10, pady=25)
    length_choosen.current(5) 

    # label text for title
    score_label = Label(root, text="   Select a word score:", font=('Fira Code', 10), justify='right')
    score_label.grid(row=1, column=0)

    # Combobox creation
    scr = IntVar() 
    score_choosen = ttk.Combobox(root, width=4, textvariable=scr, font=('Fira Code', 10), state="readonly") 
    score_choosen['values'] = (20, 30, 40, 50, 60, 70, 80) 
    score_choosen.grid(row=1, column=1, padx=10)
    score_choosen.current(3)

    # Save button creation
    save_button = Button(root, text='Submit', command=get_input, default='active')
    save_button.grid(row=2, column=0, columnspan=2, pady=25)

    root.mainloop()

    return y, z

def userInputLength():
    """Gets user word length value input"""
    root = Tk()
    root.title('') 
    root.geometry('350x100+250+300') 

    def get_input():
        global y
        y = length.get()
        root.destroy()

    # label text for title
    label = Label(root, text="   Select a Word Length:", font=('Fira Code', 10), justify='right')
    label.grid(row=0, column=0)

    # Combobox creation
    length = IntVar() 
    length_choosen = ttk.Combobox(root, width=3, textvariable=length, font=('Fira Code', 10), state="readonly") 
    length_choosen['values'] = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15) 
    length_choosen.grid(row=0, column=1, padx=10, pady=25)
    length_choosen.current(5) 

    # Save button creation
    save_button = Button(root, text='Submit', command=get_input, default='active')
    save_button.grid(row=0, column=2)

    root.mainloop()
    return y

def userInputScore():
    """Gets user word length value input"""
    root = Tk()
    root.title('') 
    root.geometry('350x100+250+300') 

    def get_input():
        global y
        y = scr.get()
        root.destroy()

    # label text for title
    score_label = Label(root, text="   Select a word score:", font=('Fira Code', 10), justify='right')
    score_label.grid(row=0, column=0)

    # Combobox creation
    scr = IntVar() 
    score_choosen = ttk.Combobox(root, width=3, textvariable=scr, font=('Fira Code', 10), state="readonly") 
    score_choosen['values'] = (20, 30, 40, 50, 60, 70, 80) 
    score_choosen.grid(row=0, column=1, padx=10, pady=25)
    score_choosen.current(3)

    # Save button creation
    save_button = Button(root, text='Submit', command=get_input, default='active')
    save_button.grid(row=0, column=2)

    root.mainloop()
    return y

def userInputBool(prompt:str='(Y/N)') -> bool:
    """Returns user boolean input"""
    while True:
        try:
            return {'y':True,'n':False,}[input(prompt).lower().strip()]
        except KeyError:
            print()
            print(c.r+'Please enter Y or N'+c.w)
            print()

def userInputOpenFilePath(initial_path:Path=downloads, prompt:str='Select a file to open') -> Path:
    """Returns the full path of a user-selected file to open"""
    from tkinter.filedialog import askopenfilename
    filename = askopenfilename(initialdir = initial_path.stem,
                               filetypes = [('Text Files', '*.txt'), ('All Files', '*.*')],
                               title = prompt
                               )
    if Path(filename).is_file():
        return filename
    else:
        opCancel('NoOpenFileSelected')

def userInputSaveAsFile(initial_path:Path=desktop, title:str='Select a file to save') -> Path:
    """Returns the full path of a user-selected file to save"""
    from tkinter.filedialog import asksaveasfilename
    filename = asksaveasfilename(initialdir = initial_path.stem,
                                 filetypes = [('Text Files', '*.txt'), ('All Files', '*.*')],
                                 title = title
                                 )
    if filename:
        return filename
    else:
        opCancel('NoSaveFileSelected')
    
# General Functions

# def fmt(num:float, length:int=8, decimal:int=0, align:str='>') -> str:
#     """Returns formatted number as string object of length [length]"""
#     string = '{:' + align + str(length) + ',.' + str(decimal) + 'f}'
#     return str(string.format(num))

def getNewWords(new_dict:dict[str,int], old_dict:dict[str,int]) -> list[str]:
    """Returns a scored list of new words on a list"""
    out_list = []
    for word in new_dict:
        if word not in old_dict:
            s = word + ';' + str(new_dict[word])
            out_list.append(s)
    return sorted(list(set(out_list)))

def print2d(input_list:list, title:str='') -> None:
    """Prints a list in two dimensions"""
    import numpy as np
    np.set_printoptions(threshold=40, linewidth=80, edgeitems=5)

    if title:
        print('List name:', title, '\n')
    print(np.array(list(input_list)), '\n')
    print('Size:', np.shape(list(input_list)))
    return

def progress(now:int, total:int, width=50) -> None:
    """Displays a progress bar"""
    j = int(now / total * width)
    pct = int(now / total * 100)
    if 10 <= pct < 92:
        print(f'[{'█'*j}{pct: 3}%{' '*(width - j - 4)}]  {now:4>,}/{total:,}', end='\r')
    else:
        print(f'[{'█'*j}{' '*(width - j)}]  {now:4>,}/{total:,}', end='\r')

    return

def regx(search_string:str=None, min_score:int=0) -> list[str]:
    """Returns a list of words from the gold list that match the RegEx string"""
    import re
    i = 0
    result = []
    g = goldDict(min_score)
    pattern = search_string if search_string else input("Enter a valid RegEx string: ")
    if len(pattern) == 0:
        print(c.r+'no RegEx string entered' + '\n\n')
        sys.exit()
    prog = re.compile(pattern.replace("$v", "[aeiou]").replace("$c", "[^aeiou]"),
           re.IGNORECASE)
    for word in g.keys():
        if prog.search(word):
            result.append(word + ';' + str(g[word]))
            if i > 20000:
                break
            i += 1
    result = sorted(list(set(result)))
    return result

def score(word:str, score_dict:dict[str,int]) -> int:
    """Looks up a word's score on the gold list (score = 99 if word not found)"""
    if not word:
        return 99
    if word in score_dict.keys():
        return int(score_dict[word])
    return 99

def zzz(sleep_time:float=10) -> None:
    """Sleeps a number of seconds"""
    import time
    print()
    for i in range(int(sleep_time)):
        if i != sleep_time - 1:
            print('Sleeping for', sleep_time - i, 'seconds    ', end='\r')
        else:
            print('Sleeping for', sleep_time - i, 'second ', end='\r')
        time.sleep(1)
    print(' '*80, '\n')
    return

def opCancel(exception_string:str=None) -> None:
    error:dict[str,str] = {'NoOpenFileSelected' : 'no file selected to open',
                           'NoSaveFileSelected' : 'no file selected to save to',
                           'NotAcrossLiteFile' : 'not a valid across lite file'
                           }
    
    if exception_string:
        message:str = error[exception_string]
    else:
        message = 'unspecified error'

    print(' '*15, message)
    print(' '*15, c.r+'operation canceled'+c.w, '\n\n')
    sys.exit()

