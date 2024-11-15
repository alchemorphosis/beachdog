import sys
import os
import library.beachdoglib as library
import customtkinter as ctk
from pathlib import Path

# Define main() function
def main():
    def regexSubmitButtonClicked():
        # regexStr = regexString.get()
        if entryBox.get() and entryBox.get() != regexStr.get():
            regexStr.set(value=entryBox.get())
            # Display the submitted string and erase previous output
            submittedStringLabel.configure(text=regexStr)
            submittedStringLabel.grid()
            fileFrameMessageLabel.configure(text='')
            outputBox.grid_remove()
            fileSaveButton.grid_remove()
            filenameSavedToLabel.grid_remove()
            # Perform the search
            global results
            results = sorted(library.regx(regexStr), key=len)
            # Display the results, if any
            if len(results) == 10000:
                max = '(max) '
            else:
                max = ''
            outputFrameMessageLabel.configure(
                text=f'{len(results):,} {max}result{'' if len(results) == 1 else 's'} found for'
                )
            if results:
                resultsText = ''
                for entry in results:
                    resultsText += entry + '\n'
                outputBox.configure(state='normal')
                outputBox.delete(0.0, 'end')
                outputBox.insert('0.0', resultsText)
                outputBox.configure(state='disabled')
                outputBox.grid()
                # If results, display Save to File button
                if outputBox.winfo_exists():
                    fileSaveButton.grid()
                    fileSaveButtonFrame.grid()
                    fileSaveButton.configure(state='enabled')

    def regexResultListToFile():
        # Disable Save to File button
        fileSaveButton.configure(state='enabled')
        # Get save filename from user and write list to file
        outputFile = library.userInputSaveAsFile()
        regexApp.after(50, lambda: regexApp.attributes('-topmost', 1))
        regexApp.after(50, lambda: regexApp.attributes('-topmost', 0))
        # Write result to file
        if outputFile:
            fileSaveButton.grid_remove()
            library.listToFile(results, outputFile)
            # Inform results of file save
            fileFrameMessageLabel.configure(text=f'{len(results):,} results saved to')
            filenameSavedToLabel.configure(text=f'{Path(outputFile).name}')
            filenameSavedToLabel.grid()
        else:
            fileFrameMessageLabel.configure(text='Save to file cancelled')

        submitButton.configure(state='enabled')

    regexApp = ctk.CTkToplevel()
    regexApp.title(' Regex Search')
    regexApp.after(50, lambda: regexApp.attributes('-topmost', 1))
    regexApp.after(50, lambda: regexApp.attributes('-topmost', 0))
    # after(200, lambda: regexApp.iconbitmap('assets.bdogicon.ico'))
    regexApp.resizable(False, False)
    
    regexStr = ctk.StringVar
    regexStr.set(self=regexApp, value='')
    # Define fonts
    defaultFont = ctk.CTkFont(
    family='Helvetica Now Text',
    size=14,
    )
    monoFont = ctk.CTkFont(
        family='Monaco',
        size=14,
    )
    mainMenuButtonFg = '#3a7ebf'
    messageHighlightStyle = {
        'text_color': ['#8b6736', '#e8d9c4'],
        'corner_radius': 6,
        'font': monoFont,
        'padx': 0,
        'pady': 0,
    }
    # Create master frames
    masterFrame = ctk.CTkFrame(regexApp, fg_color='#dcdcdc')
    inputFrame = ctk.CTkFrame(masterFrame, fg_color='#dcdcdc')
    submitFrame = ctk.CTkFrame(masterFrame, fg_color='#dcdcdc')
    outputFrame = ctk.CTkFrame(masterFrame, fg_color='#dcdcdc')
    fileFrame = ctk.CTkFrame(masterFrame, fg_color='#dcdcdc')
    fileSaveButtonFrame = ctk.CTkFrame(masterFrame, fg_color='#dcdcdc')
    # Create widgets
    entryBox = ctk.CTkEntry(inputFrame,
        width=250,
        # placeholder_text='Enter a valid regex string',
        placeholder_text_color=['gray65', 'gray65'],
        font=monoFont,
        border_width=1,
        border_color=mainMenuButtonFg,
        corner_radius=6,
        )
    submitButton = ctk.CTkButton(submitFrame,
        text='Submit',
        command=regexSubmitButtonClicked,
        )
    outputFrameMessageLabel = ctk.CTkLabel(outputFrame,
        text='',
        width=250,
        # text=f'returned {len(results):,} results',
        font=defaultFont, 
        )
    fileFrameMessageLabel = ctk.CTkLabel(fileFrame,
        text='',
        width=250,
        font=defaultFont, 
        )
    submittedStringLabel = ctk.CTkLabel(outputFrame,
        text='',
        width=250,
        **messageHighlightStyle,
        )
    outputBox = ctk.CTkTextbox(outputFrame,
        width=250,
        font=monoFont,
        border_width=0,
        border_color=mainMenuButtonFg,
        state='disabled',
        )
    filenameSavedToLabel = ctk.CTkLabel(fileFrame,
        text=f'',
        width=250,
        **messageHighlightStyle,
        )
    fileSaveButton = ctk.CTkButton(fileSaveButtonFrame,
        text='Save to file',
        command=regexResultListToFile,
        font=defaultFont,
        state='normal',
        )
    # Place master frames
    masterFrame.grid(row=0, column=0)
    inputFrame.grid(row=0, column=0, padx=(12, 6), pady=(12, 6), sticky='ew')
    submitFrame.grid(row=0, column=1, padx=(6, 12), pady=(12, 6), sticky='ew')
    outputFrame.grid(row=1, column=0, rowspan=6, padx=(12, 6), pady=(6, 12), sticky='n')
    fileFrame.grid(row=1, column=1, rowspan=2, padx=(6, 12), pady=(6, 6), sticky='n')
    fileSaveButtonFrame.grid(row=3, column=1, padx=(6, 12), pady=(6, 12), sticky='new')
    # Place widgets
    entryBox.grid(row=0, column=0, padx=(12, 12), pady=(12, 12), sticky='ew')
    submitButton.grid(row=0, column=0, padx=(12, 12), pady=(12, 12), sticky='new')
    outputFrameMessageLabel.grid(row=0, column=0, padx=(12, 12), pady=(0, 0), sticky='new')
    submittedStringLabel.grid(row=1, column=0, padx=(12, 12), pady=(0, 12), sticky='new')
    outputBox.grid(row=2, column=0, padx=(12, 12), pady=(18, 12), sticky='new')
    fileFrameMessageLabel.grid(row=0, column=0, padx=(12, 12), pady=(0, 0), sticky='new')
    filenameSavedToLabel.grid(row=1, column=0, padx=(12, 12), pady=(0 ,0), sticky='new')
    fileSaveButton.grid(row=0, column=0, padx=(12, 12), pady=(0 ,12), sticky='nw')
    # Clear the grid of unwanted widgets
    submittedStringLabel.grid_remove()
    outputBox.grid_remove()
    filenameSavedToLabel.grid_remove()
    fileSaveButtonFrame.grid_remove()

    regexApp.mainloop()
# Entry point of the script
if __name__ == "__main__":
    main()
