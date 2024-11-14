import os
from customtkinter import CTk
from pathlib import Path


downloads = Path().home() / 'iCloudDrive' / 'Downloads'
desktop = Path().home() / 'iCloudDrive' / 'Desktop'
documents = Path().home() / 'iCloudDrive' / 'Documents'
pyLib = Path().cwd() / 'library'
listDir = documents / 'Work' / 'Crosswords' / 'Lists' / 'Masters'
masterFile = listDir / 'Logan_Gold_Master.txt'
xwiFile = listDir / 'XwiJeffChenList.txt'
clueFile = listDir / 'Clue Database.txt'

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

def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

# File Operations


def listToFile(input_list :list, save_file:Path) -> bool:
    """Writes a word list to a file"""
    with open(save_file, 'w') as f:
        for item in input_list:
            f.write('%s\n' % item)
    f.close()
    return

def myList(min_score:int=0, min_len:int=3, max_len:int=21) -> list[str]:
    """Imports master file to list of scored words"""
    return fileToList(masterFile, min_score, min_len, max_len)

def xwiList(min_score:int=0, min_len:int=3, max_len:int=21) -> list[str]:
    """Imports Jeff's file to a list of scored words"""
    return fileToList(xwiFile, min_score, min_len, max_len)

def goldList(min_score:int=0, min_len:int=3, max_len:int=21) -> list[str]:
    """Imports master and Jeff's files to a combined list of scored words"""
    g_list = myList(min_score, min_len, max_len)
    x_list = xwiList(min_score, min_len, max_len)
    m_dict = myDict(min_score, min_len, max_len)
    
    for entry in x_list:
        if entry.split(';')[0] not in m_dict.keys():
            g_list.append(entry)
    return g_list

def myDict(min_score:int=0, min_len:int=3, max_len:int=21) -> dict[str,int]:
    """Imports master file to dictionary of scored words"""
    dictionary = {}
    list_in = myList(min_score, min_len, max_len)
    for entry in list_in:
        w, s = entry.split(';')
        dictionary.update({w : int(s)})
    return dictionary

def xwiDict(min_score:int=0, min_len:int=3, max_len:int=21) -> dict[str,int]:
    """Imports Jeff's file to dictionary of scored words"""
    dictionary = {}
    list_in = xwiList(min_score, min_len, max_len)
    for entry in list_in:
        w, s = entry.split(';')
        dictionary.update({w : int(s)})
    return dictionary

def goldDict(min_score:int=0, min_len:int=3, max_len:int=21) -> dict[str,int]:
    """Imports master and Jeff's files to a combined dictionary of scored words"""
    dictionary = {}
    dictionary.update(xwiDict(min_score, min_len, max_len))
    dictionary.update(myDict(min_score, min_len, max_len))
    return dictionary

def fileToList(open_file:Path, min_score:int=0, min_len:int=3, max_len:int=21) -> list[str]:
    """Imports a word list file to list of scored words"""
    if open_file:
        f = open(open_file, 'r')
        word_list = [line.strip().upper() for line in f
                                if int(line.split(';')[1]) >= min_score
                                if len(line.split(';')[0]) >= min_len
                                if len(line.split(';')[0]) <= max_len
                                if line.strip()
                                ]
        f.close()
        return word_list
    
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


