import sys
import library.beachdoglib as library
import customtkinter as ctk
from pathlib import Path

def runAddXwiWords(self):

    addXwiWordsApp = ctk.CTkToplevel()
    def print_word(word):
        wo, so = word.split(';')
        print(f'          {wo} {so} ', end='', flush=True)


    def get_new_score():
        """Returns new word score as a two chararcter string."""
        prompt = '(Q, W, E, R, X, ENTER): '
        while True:
            try:
                ns = {'':'00', 'Q':'20', 'W':'35', 'E':'60',
                    'R':'70', 'X':'-99'} \
                [input(prompt).upper()]
                if ns == '35':
                    if int(len(wo)) <= 4:
                        ns = '40'
                    else:
                        ns = '30'
                return (ns)
            except KeyError:
                print(' '*25, end='')

    def submitButtonClicked():
        pass
    def undoButtonClicked():
        pass

    addedWords = 0
    a = []

    self.mDict = library.myDict()
    self.xDict = library.xwiDict()
    self.mFilename = Path(library.masterFile).stem
    self.xFilename = Path(library.xwiFile).stem
    # FInd all words on the xwi word list that aren't on my word list
    self.newWords = library.getNewWords(self.xDict, self.mDict)
    
    # Get user to imput the length to work on
    self.selectedLength = 10 # Placeholder until user input code developed
    
    # Find new words of selected length
    self.newLengthWords = [x for x in self.newWords.items() if x.value() == self.selectedLength]
    # Calculate word counts
    self.newLengthWordCount = len(self.newLengthWords)
    self.newWordCount = len(self.newWords)
    self.xwiWordCount = len(self.xDict)
    self.startWordcount = len(self.mDict)
    self.addedCount = 0
    self.newTotal = self.startWordCount + self.addedCount

    # Process words
    for w in self.newLengthWords:
        wo, so = w.split(';')
        self.newWordDisplayString = f'{wo}{' '*(16 - len(wo))}{so}'
        # update label and display word and score here
        ns = get_new_score()
        nw = wo + ';' + ns

        # update label and display word with new score here            
            
        open(library.masterFile,'a').write(nw + '\n')
        self.newLengthWordCount -= 1
        self.newWordCount -= 1
        self.addedWords += 1
        self.newTotal += 1
            


            # Create adn open the main popup window
    self.addXwiWordsApp = ctk.CTkToplevel()
    self.addXwiWordsApp.title(' Score and add new words to my list')
    self.after(50, lambda: self.addXwiWordsApp.attributes('-topmost', 1))
    self.after(50, lambda: self.addXwiWordsApp.attributes('-topmost', 0))
    # self.after(200, lambda: self.addXwiWordsApp.iconbitmap('assets.bdogicon.ico'))
    # self.addXwiWordsApp.resizable(False, False)
   
   
    # Create master frames
    self.masterFrame = ctk.CTkFrame(self.addXwiWordsApp, fg_color='#dcdcdc')
    self.filenamesFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
    self.infoFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
    self.workingFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
    self.submitButtonFrame = ctk.CTkFrame(self.workingFrame, fg_color='#dcdcdc')
    self.undoButtonFrame = ctk.CTkFrame(self.workingFrame, fg_color='#dcdcdc')
    # Create static labels (9)
    self.fromFilenameLabel = ctk.CTkLabel(
        self.filenameFrame,
        text='From',
        font=self.defaultFont, 
        )
    self.toFilenameLabel = ctk.CTkLabel(
        self.filenameFrame,
        text='To',
        font=self.defaultFont, 
        )
    self.arrowLabel = ctk.CTkLabel(
        self.filenameFrame,
        text='--->',
        font=self.defaultFont, 
        **self.messageHighlightStyle,
        )
    self.lengthNewTotalLabel = ctk.CTkLabel(
        self.infoFrame,
        text=f'{self.selectedLength} long new',
        font=self.defaultFont, 
        )
    self.xwiNewTotalLabel = ctk.CTkLabel(
        self.infoFrame,
        text='New words',
        font=self.defaultFont, 
        )
    self.xwiTotalLabel = ctk.CTkLabel(
        self.infoFrame,
        text='Total words',
        font=self.defaultFont, 
        )
    self.startTotalLabel = ctk.CTkLabel(
        self.infoFrame,
        text='Start',
        font=self.defaultFont, 
        )
    self.addedTotalLabel = ctk.CTkLabel(
        self.infoFrame,
        text=f'Added',
        font=self.defaultFont, 
        )
    self.currentTotalLabel = ctk.CTkLabel(
        self.infoFrame,
        text=f'New total',
        font=self.defaultFont, 
        )
    # Create dynamic labels (10)

    # Create entry box (1)
    self.entryBox = ctk.CTkEntry(
        self.workingFrame,
        width=10,
        font=self.monoFont,
        border_width=1,
        border_color=self.mainMenuButtonFg,
        corner_radius=6,
        )
    # Create buttons (2)
    self.submitButton = ctk.CTkButton(
        self.submitButtonFrame,
        text='Submit',
        command=submitButtonClicked,
        font=self.defaultFont,
        state='normal'
        )
    self.undoButton = ctk.CTkButton(
        self.undoButtonFrame,
        text='Undo',
        command=undoButtonClicked,
        font=self.defaultFont,
        state='normal',
        )
   
   
    # Place master frames
    self.masterFrame.grid(row=0, column=0)
    self.filenamesFrame.grid(row=0, column=0, padx=(12, 12), pady=(12, 12), sticky='ew')
    self.infoFrame.grid(row=1, column=0, padx=(12, 12), pady=(12, 12), sticky='ew')
    self.workingFrame.grid(row=2, column=0, padx=(12, 12), pady=(6, 12), sticky='ew')
    self.submitButtonFrame.grid(row=1, column=1, padx=(6, 12), pady=(6, 6))
    self.undoButtonFrame.grid(row=1, column=2, padx=(6, 12), pady=(6, 12))
    # Place static labels
    self.fromFilenameLabel.grid(row=0, column=0, padx=(12, 12), pady=(0, 0), sticky='new')
    self.toFilenameLabel.grid(row=0, column=2, padx=(12, 12), pady=(0, 12), sticky='new')
    self.arrowLabel.grid(row=1, column=1, padx=(12, 12), pady=(18, 12), sticky='new')
    self.lengthNewTotalLabel.grid(row=0, column=0, padx=(12, 12), pady=(0, 0), sticky='new')
    self.xwiNewTotalLabel.grid(row=1, column=0, padx=(12, 12), pady=(0 ,0), sticky='new')
    self.xwiTotalLabel.grid(row=2, column=0, padx=(12, 12), pady=(0 ,0), sticky='new')
    self.startTotalLabel.grid(row=0, column=2, padx=(12, 12), pady=(0 ,0), sticky='new')
    self.addedTotalLabel.grid(row=1, column=2, padx=(12, 12), pady=(0 ,0), sticky='new')
    self.currentTotalLabel.grid(row=2, column=2, padx=(12, 12), pady=(0 ,0), sticky='new')
    # Place dynamic labels

    # Place entry box
    self.entryBox.grid(row=0, column=1, padx=(12, 12), pady=(12, 12))
    # Place buttons
    self.submitButton.grid(row=0, column=0, padx=(12, 12), pady=(12, 12))
    self.undoButton.grid(row=0, column=0, padx=(12, 12), pady=(12 ,12))
