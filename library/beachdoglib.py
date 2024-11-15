# Import Libraries
import sys
import ssl
import os
from os.path import exists
from customtkinter import CTk
from pathlib import Path
from tkinter import *
from tkinter import ttk 

# downloads = Path().home() / 'iCloudDrive' / 'Downloads'
# desktop = Path().home() / 'iCloudDrive' / 'Desktop'
# documents = Path().home() / 'iCloudDrive' / 'Documents'
# pyLib = Path().cwd() / 'library'
listDir = Path().home() / 'iCloudDrive' / 'Documents' / 'Work' / 'Crosswords' / 'Lists' / 'Masters'
masterFile = listDir / 'Logan_Gold_Master.txt'
masterFileBackup = listDir / 'Logan_Gold_Master.bak'
xwiFile = listDir / 'XwiJeffChenList.txt'
clueFile = listDir / 'Clue Database.txt'

# Fix ssl
# context = ssl._create_unverified_context()
# ssl._create_default_https_context = ssl._create_unverified_context
# Import constants
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
            ]
SCRABBLE_VALUES = {'A':1, 'E':1, 'I':1, 'O':1, 'U':1, 'L':1, 'N':1,
                   'S':1, 'T':1, 'R':1, 'D':2, 'G':2, 'B':3, 'C':3,
                   'M':3, 'P':3, 'F':4, 'H':4, 'V':4, 'W':4,
                   'Y':4, 'K':5, 'J':8, 'X':8, 'Q':10, 'Z':10
                   }

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

def listToFile(input_list :list, save_file:Path) -> bool:
    """Writes a word list to a file"""
    with open(save_file, 'w') as f:
        for item in input_list:
            f.write('%s\n' % item)
    f.close()
    return

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

def dictToFile(input_dict:dict[str,int], save_file:Path) -> None:
    """Writes a word dictionary to a file"""
    return(listToFile(dictToList(input_dict), save_file))

def fileToDict(open_file:Path, min_score:int=0, min_len:int=3, max_len:int=15) -> dict[str,int]:
    """Imports a word list file to dictionary of scored words"""
    return listToDict(fileToList(open_file, min_score, min_len, max_len))

# User Input

def userInputOpenFilePath(prompt:str='Select a file to open') -> Path:
    """Returns the full path of a user-selected file to open"""
    from tkinter.filedialog import askopenfilename
    filename = askopenfilename(
        filetypes = [('Text Files', '*.txt'), ('All Files', '*.*')],
        title = prompt
        )
    return filename

def userInputSaveAsFile(title:str='Select a file to save'):
    """Returns the full path of a user-selected file to save"""
    from tkinter.filedialog import asksaveasfilename
    filename = asksaveasfilename(
        filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
        title=title
        )
    return filename

# General Functions

def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

def getNewWords(new_dict:dict[str,int], old_dict:dict[str,int]) -> dict[str,int]:
    """Returns a scored list of new words on a list"""
    outDict = {}
    for word, value in new_dict.items():
        if word not in old_dict.keys():
            outDict.update({word: value})
    return outDict

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

def regx(searchString:str, minScore:int=50) -> list[str]:
    """Returns an unscored list of words from the gold list that match the RegEx string"""
    # Import re
    import re
    # Import the dictionary file
    g = goldDict(min_score=minScore)
    # Perform the regex search on the imported dictionary file
    pattern = searchString.replace("$v", "[aeiou]").replace("$c", "[^aeiou]")
    searchResult = [word for word in g if re.compile(pattern, re.IGNORECASE).search(word)]
    # Return the results
    return sorted(searchResult[:10000], key=len)

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
    print(' '*15, 'operation canceled', '\n\n')
    sys.exit()

