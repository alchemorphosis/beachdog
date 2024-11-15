import customtkinter as ctk
import library.beachdoglib as lib
import modules.analyze as analyze
import modules.changes as changes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('dark-blue')

def main():
    class MainMenu(ctk.CTkFrame):
        def __init__(self, master, mainMenuItems):
            super().__init__(master)
            # Set app fonts
            self.defaultFont = ctk.CTkFont(
                family='Helvetica Now Text',
                size=14,
            )
            self.monoFont = ctk.CTkFont(
                family='Monaco',
                size=14,
            )
            self.monoFontAddWords = ctk.CTkFont(
                family='Fira Code',
                size=14,
            )
            self.gridAnalysisFont = ctk.CTkFont(
                family='Helvetica Now Text',
                size=14
            )
            # self.master = master
            self.selectedButton = None  # Track currently selected button
            # Button styles
            self.mainMenuButtonStyle = {
                'text_color_disabled': ['#ffffff', 'gray85'],
                'font': self.defaultFont,
                }
            self.mainMenuButtonDisabledStyle = {
                'fg_color': '#325882',
                'text_color': '#000000'
                }
            self.subMenuButtonStyle = {
                'width': 100,
                'border_spacing': 10,
                'font': self.defaultFont,
                }
            # Main menu buttons
            self.mainMenuFrame = ctk.CTkFrame(self)
            self.mainMenuFrame.grid(row=0, column=0, columnspan=len(mainMenuItems), padx=10, pady=10)
            self.mainMenuButtons = {}
            for i, item in enumerate(mainMenuItems):
                button = ctk.CTkButton(
                    self.mainMenuFrame,
                    text=item,
                    command=lambda item=item, btn=i: self.selectMainMenuButton(item, btn),
                    **self.mainMenuButtonStyle,
                    )
                button.grid(row=0, column=i, padx=10, pady=10)
                self.mainMenuButtons[i] = button
            # Save menu button default colors
            self.mainMenuButtonFg = button.cget('fg_color')
            self.mainMenuButtonHoverFg = button.cget('hover_color')
            self.mainMenuButtonTextColor = button.cget('text_color')
            # Style utility buttons
            self.exitButtonStyle = {
                'width': 60,
                'fg_color': 'transparent',
                'font': self.defaultFont,
                'text_color': '#ff0f0f',
                'hover_color': ['gray95', 'gray30'],
                'border_color': '#ff0f0f',
                'border_width': 1
                }
            self.regexButtonStyle = {
                'width': 60,
                'fg_color': 'transparent',
                'text_color': self.mainMenuButtonFg,
                'font': self.defaultFont,
                'hover_color': ['gray95', 'gray30'],
                'border_color': self.mainMenuButtonFg,
                'border_width': 1
                }
            self.messageHighlightStyle = {
                # 'fg_color': ['#ffffff', 'gray85'],
                'text_color': ['#8b6736', '#e8d9c4'],
                'corner_radius': 6,
                'font': self.monoFont,
                'padx': 0,
                'pady': 0,
                }
            # Utility frame
            self.utilityFrame = ctk.CTkFrame(
                self,
                )
            self.utilityFrame.grid(row=0, column=len(mainMenuItems)+1, padx=10, pady=10, sticky='w')
            # Regex button
            ctk.CTkButton(
                self.utilityFrame,
                text='REGEX',
                command=self.runRegexApplet,
                **self.regexButtonStyle,
                ).grid(row=0, column=0, padx=10, pady=10)
            # Exit button
            ctk.CTkButton(
                self.utilityFrame,
                text='EXIT',
                command=lambda: app.quit(),
                **self.exitButtonStyle
                ).grid(row=0, column=1, padx=10, pady=10)#, sticky='e')
            # Sub-menu frame (created once, reused)
            self.subMenuFrame = ctk.CTkFrame(
                self,
                )
            self.subMenuFrame.grid(row=1, column=0, columnspan=len(mainMenuItems)+2, padx=10, pady=10, sticky='ew')
            # Messge frame (created once, reused)
            self.messageFrame = ctk.CTkFrame(
                self,
                )
            self.messageFrame.grid(row=2, column=0, columnspan=len(mainMenuItems)+2, padx=10, pady=10, sticky='eswn')
            # Get message frame color
            self.messageFrameFgColor = self.messageFrame.cget('fg_color')

        def selectMainMenuButton(self, menuItem, button_index):
            # Reset the previously selected button, if any
            if self.selectedButton is not None:
                self.selectedButton.configure(state='normal', fg_color=self.mainMenuButtonFg)

            # Disable and change the color of the currently selected button
            selected_button = self.mainMenuButtons[button_index]
            selected_button.configure(state='disabled', fg_color=self.mainMenuButtonHoverFg)

            # Update selected button reference
            self.selectedButton = selected_button

            # Load the sub-menu for the selected main menu item
            self.loadSubMenu(self.master, menuItem)

        def loadSubMenu(self, master, subMenuName):
            # Clear and remove previous message frame
            if self.messageFrame != None and self.messageFrame.winfo_children() != None:
                for widget in self.messageFrame.winfo_children():
                    widget.destroy()
                # self.messageFrame.grid(row=2, column=0, columnspan=100, padx=10, pady=10)#, sticky='nesw')

            # Clear previous sub-menu buttons
            if self.subMenuFrame and self.subMenuFrame.winfo_children():
                for widget in self.subMenuFrame.winfo_children():
                    widget.destroy()

            # Filter relevant sub-menu items
            subMenuItems = [name for name, category in master.subMenuItems.items() if category == subMenuName]

            # Create sub-menu buttons
            for i, item in enumerate(subMenuItems):
                ctk.CTkButton(
                    self.subMenuFrame,
                    text=item,
                    command=lambda item=item: self.loadScript(item),
                    **self.subMenuButtonStyle,
                    ).grid(row=1, column=i, padx=10, pady=10, sticky='we')

            # Add the message frame
            # if self.messageFrame and self.messageFrame.winfo_children():
            #     for widget in self.messageFrame.winfo_children():
            #         widget.destroy()
            # self.messageFrame.grid(row=2, column=0, columnspan=len(master.mainMenuItems)+2, padx=10, pady=10, sticky='ew')

        def loadScript(self, scriptName):
            # self.messageFrame.grid(row=2, column=0, columnspan=len(master.mainMenuItems)+2, padx=10, pady=10, sticky='ew')
            ctk.CTkLabel(
                self.messageFrame,
                text=f'Executing script: {scriptName}',
                font=self.monoFont,
                ).grid(row=0, column=0, columnspan=100, padx=10, pady=10)#, sticky='news')
            
            if scriptName == 'changes':
                self.runChanges()
            elif scriptName == 'analyze':
                self.runAnalyzePuzzle()
            elif scriptName == 'fetch':
                self.runFetchClues()
            elif scriptName == 'add_xwi':
                self.runAddXwiWords()

        def runRegexApplet(self):

            def regexSubmitButtonClicked():
                if self.entryBox.get() and  self.entryBox.get()  != self.regexString:
                    self.regexString = self.entryBox.get()
                    # Display the submitted string and erase previous output
                    self.submittedStringLabel.configure(text=self.regexString)
                    self.submittedStringLabel.grid()
                    self.fileFrameMessageLabel.configure(text='')
                    self.outputBox.grid_remove()
                    self.fileSaveButton.grid_remove()
                    self.filenameSavedToLabel.grid_remove()
                    # Perform the search
                    self.regexResults = sorted(lib.regx(self.regexString), key=len)
                    # Display the results, if any
                    if len(self.regexResults) == 10000:
                        self.max = '(max) '
                    else:
                        self.max = ''
                    self.outputFrameMessageLabel.configure(
                        text=f'{len(self.regexResults):,} {self.max}result{'' if len(self.regexResults) == 1 else 's'} found for'
                        )
                    if self.regexResults:
                        self.regexResultsText = ''
                        for entry in self.regexResults:
                            self.regexResultsText += entry + '\n'
                        self.outputBox.configure(state='normal')
                        self.outputBox.delete(0.0, 'end')
                        self.outputBox.insert('0.0', self.regexResultsText)
                        self.outputBox.configure(state='disabled')
                        self.outputBox.grid()
                        # If results, display Save to File button
                        if self.outputBox.winfo_exists():
                            self.fileSaveButton.grid()
                            self.fileSaveButtonFrame.grid()
                            self.fileSaveButton.configure(state='enabled')

            def regexResultListToFile():
                # Disable Save to File button
                self.fileSaveButton.configure(state='enabled')
                # Get save filename from user and write list to file
                self.outputFile = lib.userInputSaveAsFile()
                self.after(50, lambda: self.regexApp.attributes('-topmost', 1))
                self.after(50, lambda: self.regexApp.attributes('-topmost', 0))
                # Write result to file
                if self.outputFile:
                    self.fileSaveButton.grid_remove()
                    lib.listToFile(self.regexResults, self.outputFile)
                    # Inform results of file save
                    self.fileFrameMessageLabel.configure(text=f'{len(self.regexResults):,} results saved to')
                    self.filenameSavedToLabel.configure(text=f'{Path(self.outputFile).name}')
                    self.filenameSavedToLabel.grid()
                else:
                    self.fileFrameMessageLabel.configure(text='Save to file cancelled')

                self.submitButton.configure(state='enabled')
            
            # Create adn open the main popup window
            self.regexApp = ctk.CTkToplevel()
            self.regexApp.title(' Regex Search')
            self.after(50, lambda: self.regexApp.attributes('-topmost', 1))
            self.after(50, lambda: self.regexApp.attributes('-topmost', 0))
            # self.after(200, lambda: self.regexApp.iconbitmap('assets.bdogicon.ico'))
            # self.regexApp.resizable(False, False)
            self.regexString = ''
            # Create master frames
            self.masterFrame = ctk.CTkFrame(self.regexApp, fg_color='#dcdcdc')
            self.inputFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
            self.submitFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
            self.outputFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
            self.fileFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
            self.fileSaveButtonFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
            # Create widgets
            self.entryBox = ctk.CTkEntry(self.inputFrame,
                width=250,
                # placeholder_text='Enter a valid regex string',
                placeholder_text_color=['gray65', 'gray65'],
                font=self.monoFont,
                border_width=1,
                border_color=self.mainMenuButtonFg,
                corner_radius=6,
                )
            self.submitButton = ctk.CTkButton(self.submitFrame,
                text='Submit',
                command=regexSubmitButtonClicked,
                )
            self.outputFrameMessageLabel = ctk.CTkLabel(self.outputFrame,
                text='',
                width=250,
                # text=f'returned {len(self.regexResults):,} results',
                font=self.defaultFont, 
                )
            self.fileFrameMessageLabel = ctk.CTkLabel(self.fileFrame,
                text='',
                width=250,
                font=self.defaultFont, 
                )
            self.submittedStringLabel = ctk.CTkLabel(self.outputFrame,
                text='',
                width=250,
                **self.messageHighlightStyle,
                )
            self.outputBox = ctk.CTkTextbox(self.outputFrame,
                width=250,
                font=self.monoFont,
                border_width=0,
                border_color=self.mainMenuButtonFg,
                state='disabled',
                )
            self.filenameSavedToLabel = ctk.CTkLabel(self.fileFrame,
                text=f'',
                width=250,
                **self.messageHighlightStyle,
                )
            self.fileSaveButton = ctk.CTkButton(self.fileSaveButtonFrame,
                text='Save to file',
                command=regexResultListToFile,
                font=self.defaultFont,
                state='normal',
                )
            # Place master frames
            self.masterFrame.grid(row=0, column=0)
            self.inputFrame.grid(row=0, column=0, padx=(12, 6), pady=(12, 6), sticky='ew')
            self.submitFrame.grid(row=0, column=1, padx=(6, 12), pady=(12, 6), sticky='ew')
            self.outputFrame.grid(row=1, column=0, rowspan=6, padx=(12, 6), pady=(6, 12), sticky='n')
            self.fileFrame.grid(row=1, column=1, rowspan=2, padx=(6, 12), pady=(6, 6), sticky='n')
            self.fileSaveButtonFrame.grid(row=3, column=1, padx=(6, 12), pady=(6, 12), sticky='new')
            # Place widgets
            self.entryBox.grid(row=0, column=0, padx=(12, 12), pady=(12, 12), sticky='ew')
            self.submitButton.grid(row=0, column=0, padx=(12, 12), pady=(12, 12), sticky='new')
            self.outputFrameMessageLabel.grid(row=0, column=0, padx=(12, 12), pady=(0, 0), sticky='new')
            self.submittedStringLabel.grid(row=1, column=0, padx=(12, 12), pady=(0, 12), sticky='new')
            self.outputBox.grid(row=2, column=0, padx=(12, 12), pady=(18, 12), sticky='new')
            self.fileFrameMessageLabel.grid(row=0, column=0, padx=(12, 12), pady=(0, 0), sticky='new')
            self.filenameSavedToLabel.grid(row=1, column=0, padx=(12, 12), pady=(0 ,0), sticky='new')
            self.fileSaveButton.grid(row=0, column=0, padx=(12, 12), pady=(0 ,12), sticky='nw')
            # Clear the grid of unwanted widgets
            self.submittedStringLabel.grid_remove()
            self.outputBox.grid_remove()
            self.filenameSavedToLabel.grid_remove()
            self.fileSaveButtonFrame.grid_remove()

        def runChanges(self):
            # Clear previous message frame
            for widget in self.messageFrame.winfo_children():
                widget.destroy()
            self.messageFrame.grid(row=2, column=0, columnspan=100, padx=10, pady=10)#, sticky='nesw')
            # Run the changes script and save the results
            #Display the results
            self.changesResultPopup = ctk.CTkToplevel()
            self.changesResultPopup.wm_attributes('-topmost', True)

            self.m = ctk.StringVar()
            self.m.set(changes.main())
            self.messageLabel = ctk.CTkTextbox(
                self.changesResultPopup,
                width=1000,
                height=250,
                bg_color='transparent',
                font=self.monoFont,
                )
            self.messageLabel.insert('0.0', self.m.get())
            self.messageLabel.grid(row=0, column=0, padx=10, pady=10, sticky='eswn')

        def runAnalyzePuzzle(self):

            def dataFrameReset():
                self.dataFrame1.grid()
                self.dataFrame2.grid()
                if self.graphFrame:
                    self.graphFrame.grid_remove()
                for widget in self.dataFrame1.winfo_children():
                    widget.grid_remove()
                for widget in self.dataFrame2.winfo_children():
                    widget.grid_remove()

            def saveFillImage():
                # Set canvas dimensions
                self.canvasWidth = self.blockSize * self.cols + self.lineWidth
                self.canvasHeight = self.blockSize * self.rows + self.lineWidth
                # PIL create an empty image and draw object to draw on
                # memory only, not visible
                image1 = Image.new("RGB", (self.canvasWidth, self.canvasHeight), 'white')
                draw = ImageDraw.Draw(image1)
                # Initialize block colors
                # block_colors = [['#ffffff' if cell != '.' else '#000000' for cell in row] for row in self.puzzleGrid]
                # Fill blocks with colors
                for i in range(self.rows):
                    for j in range(self.cols):
                        if self.puzzleGrid[i][j] == '.':
                            x1, y1 = j * self.blockSize + self.lineWidth, i * self.blockSize + self.lineWidth
                            x2, y2 = x1 + self.blockSize, y1 + self.blockSize
                            draw.rectangle(((x1, y1), (x2, y2)), fill='#000000', width=0)
                # Fill in the letters
                for i in range(self.rows):
                    for j in range(self.cols):
                        x = int(j * self.blockSize + (self.lineWidth) + self.blockSize / 2)
                        y = int(i * self.blockSize + (self.lineWidth + self.lineWidth) + self.blockSize / 2)
                        draw.text(
                            (x, y),
                            text=self.puzzleGrid[i][j],
                            fill='#000000',
                            anchor='mm',
                            font=ImageFont.truetype('assets\\Monaco.ttf', int(self.blockSize / 2 + 3))
                        )
                # Draw grid lines
                for i in range(self.rows + 1):
                    y = i * self.blockSize# + self.lineWidth
                    draw.line(((0, y), (self.canvasWidth - self.lineWidth, y)), fill='#000000', width=self.lineWidth)
                for j in range(self.cols + 1):
                    x = j * self.blockSize# + self.lineWidth
                    draw.line(((x, 0), (x, self.canvasWidth - self.lineWidth)), fill='#000000', width=self.lineWidth)
                # PIL image can be saved as .png .jpg .gif or .bmp file (among others)
                outputFile = lib.userInputSaveAsFile()
                if outputFile:
                    image1.save(outputFile)
                else:
                    return

            def viewPuzzle(master, puzzleGrid, fill=True, numbers=False):
                # Set canvas dimensions
                canvas_width = self.blockSize * self.cols
                canvas_height = self.blockSize * self.rows
                # Initialize canvas
                canvas = ctk.CTkCanvas(master.puzzleViewFrame, width=canvas_width, height=canvas_height)
                canvas.grid(row=0, column=0, columnspan=3, padx=(12, 12), pady=(12, 0))
                # Draw grid lines
                for i in range(self.rows + 1):
                    y = i * self.blockSize + self.lineWidth
                    canvas.create_line(self.lineWidth, y, canvas_width, y, width=self.lineWidth)
                for j in range(self.cols + 1):
                    x = j * self.blockSize + self.lineWidth
                    canvas.create_line(x, self.lineWidth, x, canvas_height, width=self.lineWidth)
                # Initialize block colors
                block_colors = [['#ffffff' if cell != '.' else '#000000' for cell in row] for row in puzzleGrid]
                # Set colors based on scores
                def updateColorsForScore(score):
                    for i in range(self.rows):
                        for j in range(self.cols):
                            if puzzleGrid[i][j] != '.':
                                # Across word color setting
                                if j == 0 or puzzleGrid[i][j - 1] == '.':
                                    across_word = analyze.fillWordAcross(puzzleGrid, i, j)
                                    if self.scores[across_word] == score:
                                        for k in range(len(across_word)):
                                            block_colors[i][j + k] = self.blockHighlightColor[score]
                                # Down word color setting
                                if i == 0 or puzzleGrid[i - 1][j] == '.':
                                    down_word = analyze.fillWordDown(puzzleGrid, i, j)
                                    if self.scores[down_word] == score:
                                        for k in range(len(down_word)):
                                            block_colors[i + k][j] = self.blockHighlightColor[score]
                # for score in [30, 40, 60, 70, 80]
                if self.displayScoreHighlights:
                    for score in self.blockHighlightColor.keys():
                        updateColorsForScore(score)
                # Fill blocks with colors
                for i in range(self.rows):
                    for j in range(self.cols):
                        x1, y1 = j * self.blockSize + self.lineWidth, i * self.blockSize + self.lineWidth
                        x2, y2 = x1 + self.blockSize, y1 + self.blockSize
                        canvas.create_rectangle(x1, y1, x2, y2, fill=block_colors[i][j], width=self.lineWidth)
                # Insert puzzle grid fill if enabled
                if fill:
                    for i in range(self.rows):
                        for j in range(self.cols):
                            x = j * self.blockSize + self.lineWidth + self.blockSize / 2
                            y = i * self.blockSize + self.lineWidth + self.blockSize / 2
                            canvas.create_text(x, y, text=puzzleGrid[i][j], font=('Monaco', 16))
                # Insert grid numbering if enabled
                if numbers:
                    for i in range(self.rows):
                        for j in range(self.cols):
                            x = j * self.blockSize + self.lineWidth + self.blockSize / 3.2
                            y = i * self.blockSize + self.lineWidth + self.blockSize / 3.2
                            canvas.create_text(
                                x, y,
                                text=f'{self.numbering[i][j] if self.numbering[i][j] != 0 else ''}',
                                font=('Monaco', 10),
                            )

            def displayGridStats():
                dataFrameReset()
                labelKwargs = {'font': self.gridAnalysisFont}
                valueKwargs = {'font': self.monoFont}
                # Loop through the data to create labels and values
                self.statsColorCodes = getStatsColors()
                # Statistics data
                averages = [
                    'Score Index',
                    'Scrabble',
                    'Overs Average'
                ]

                for i, (labelText, value) in enumerate(self.gridStatsData.items()):
                    # Create label and value widgets
                    label = ctk.CTkLabel(
                        self.dataFrame1, 
                        text=f'{labelText}:', 
                        **labelKwargs
                    )
                    # Adjust formatting for Average Length
                    valueFormat = f'{value:>6.2f}' if labelText == 'Average' else f'{value:>6d}'
                    valueLabel = ctk.CTkLabel(
                        self.dataFrame1, 
                        text=valueFormat,
                        text_color=self.statsColorCodes[labelText],
                        **valueKwargs
                    )
                    # Place labels and values in the grid
                    label.grid(row=i, column=0, padx=(12, 0), pady=(0, 0), sticky='nw')
                    valueLabel.grid(row=i, column=1, padx=(24, 12), pady=(0, 0), sticky='ne')
                # Loop through the data to create labels and values
                for i, (labelText, value) in enumerate(self.fillStatsData.items()):
                    # Create label and value widgets
                    label = ctk.CTkLabel(
                        self.dataFrame2, 
                        text=f'{labelText}:', 
                        **labelKwargs
                    )
                    # Adjust formatting for Average Length
                    valueFormat = f'{value:>4.2f}' if labelText in averages else f'{value}' if labelText == 'Missing' else f'{value:>4d}'
                    valueLabel = ctk.CTkLabel(
                        self.dataFrame2, 
                        text=valueFormat,
                        text_color=self.statsColorCodes[labelText],
                        **valueKwargs
                    )
                    # Place labels and values in the grid
                    label.grid(row=i, column=0, padx=(12, 0), pady=(0, 0), sticky='w')
                    valueLabel.grid(row=i, column=1, padx=(24, 12), pady=(0, 0), sticky='e')

                label = ctk.CTkLabel(
                    self.dataFrame2, 
                    text='Missing:', 
                    **labelKwargs
                )
                # Adjust formatting for Average Length
                valueLabel = ctk.CTkLabel(
                    self.dataFrame2, 
                    text=self.missingLetters,
                    text_color='#ffa500',
                    **valueKwargs
                )
                label.grid(row=(len(self.fillStatsData) + i), column=0, padx=(12, 0), pady=(0, 0), sticky='w')
                valueLabel.grid(row=(len(self.fillStatsData) + i), column=1, padx=(24, 12), pady=(0, 0), sticky='e')

            def displayLengthDistribution():
                self.dataFrame1.grid_remove()
                self.dataFrame2.grid_remove()
                self.graphFrame.grid(row=1, column=4, columnspan=3, padx=(12, 12), pady=(12, 12), sticky='new')
                for widget in self.graphFrame.winfo_children():
                    widget.grid_remove()

                lengthDist = analyze.fillCountLengths(self.words)
                x, y = [x for x in lengthDist.keys()], [y for y in lengthDist.values()]

                figure = Figure()
                a = figure.add_subplot(111)
                a.bar(x, y, width=0.6, color=self.mainMenuButtonFg[0])                
                canvas = FigureCanvasTkAgg(figure, self.graphFrame)
                # canvas.show()
                canvas.get_tk_widget().grid(row=0, column=0)

            def displayWordsByLength():
                dataFrameReset()
                self.dataFrame2.grid_remove()

                message = ""
                wordsByLength = [''] * 16
                for i in range(3, 16):
                    wordsByLength[i] = sorted([w for w in self.words if len(w) == i])
                for i in range(15, 2, -1):
                    if wordsByLength[i]:
                        message += '\u2502' + str(i) + '\u2502' + '\n\n'
                        for j in range(len(wordsByLength[i])):
                            message += wordsByLength[i][j] + '  '
                        message += '\n\n'

                self.dataTextbox.configure(font=self.monoFont)
                self.dataTextbox.configure(state='normal')
                self.dataTextbox.delete('0.0', 'end')
                self.dataTextbox.insert('0.0', text=message)
                self.dataTextbox.grid()
                self.dataTextbox.configure(state='disabled')

            def displayCrossers():
                dataFrameReset()
                self.dataFrame2.grid_remove()
                self.crossers = analyze.outputCrossers(self.numbering, self.across, self.down)
                self.dataTextbox.configure(font=self.monoFont)
                self.dataTextbox.configure(state='normal')
                self.dataTextbox.delete('0.0', 'end')
                self.dataTextbox.insert('0.0', text=self.crossers)
                self.dataTextbox.grid()
                self.dataTextbox.configure(state='disabled')

            def toggleHighlightsButton():
                if self.displayScoreHighlights:
                    self.displayScoreHighlights = False
                    self.toggleHighlightsButton.configure(text='Show Highlights')
                else:
                    self.displayScoreHighlights = True
                    self.toggleHighlightsButton.configure(text='Hide Highlights')
                viewPuzzle(self, self.puzzleGrid, fill=self.displayFill, numbers=self.displayNumbering)

            def toggleFill(value):
                if value == 'Grid':
                    self.displayFill = False
                    self.displayNumbering = False
                if value == 'Fill':
                    self.displayFill = True
                    self.displayNumbering = False
                if value == 'Numbering':
                    self.displayFill = False
                    self.displayNumbering = True
                viewPuzzle(self, self.puzzleGrid, fill=self.displayFill, numbers=self.displayNumbering)

            def segmentedButtonCallback(value):
                if value == 'Stats':
                    displayGridStats()
                if value == 'Lengths':
                    displayLengthDistribution()
                if value == 'Words':
                    displayWordsByLength()
                if value == 'Crossers':
                    displayCrossers()

            def getStatsColors():

                # Define the function that generates a color code for each stat
                def generate_color_code(stat_value, thresholds, colors):
                    for i, threshold in enumerate(thresholds):
                        if stat_value < threshold:
                            return colors[i]
                    return colors[-1]  # Default color if no thresholds matched
                
                # Define color selections
                cPurple ='#8760d7' 
                cGreen = '#00bb00'
                cBlue = '#48a2e5'
                cBlack = '#000000'
                cYellow = '#ffca00'
                cRed = '#ff0000'
                cGray = 'gray75'

                        
                # Define threshold and color mappings for each stat type
                self.thresholds_and_colors = {
                    'Words': ([63, 65, 67, 73, 79, 100], [cPurple, cGreen, cBlue, cBlack, cYellow, cRed]),
                    'Across': ([100], [cGray]),
                    'Down': ([100], [cGray]),
                    'Blocks': ([24, 29, 34, 39, 44, 100], [cPurple, cGreen, cBlue, cBlack, cYellow, cRed]),
                    'Longs': ([6, 8, 12, 14, 16, 100], [cRed, cYellow, cBlack, cBlue, cGreen, cPurple]),
                    '3s': ([5, 9, 13, 18, 22, 100], [cPurple, cGreen, cBlue, cBlack, cYellow, cRed]),
                    'Spans': ([1, 2, 3, 100], [cBlack, cBlue, cGreen, cPurple]),
                    'Opens': ([70, 80, 90, 100, 110, 200], [cRed, cYellow, cBlack, cBlue, cGreen, cPurple]),
                    'Average': ([5, 5.3, 5.5, 5.8, 6.1, 10.0], [cRed, cYellow, cBlack, cBlue, cGreen, cPurple]),
                    'Score Index': ([50, 52.5, 53.5, 54.5, 55.5, 100], [cRed, cYellow, cBlack, cBlue, cGreen, cPurple]),
                    'Overs Average': ([60, 62, 64, 66, 68, 100], [cRed, cYellow, cBlack, cBlue, cGreen, cPurple]),
                    'Scrabble': ([1.5, 1.54, 1.58, 1.6, 1.62, 10.0], [cRed, cYellow, cBlack, cBlue, cGreen, cPurple]),
                    'Unique': ([1, 2, 4, 100], [cBlack, cBlue, cGreen, cPurple]),
                    'Over/Under': ([0, 8, 11, 13, 100], [cRed, cYellow, cBlack, cBlue, cGreen, cPurple]),
                    '60s': ([1, 200], [cBlack, cBlue]),
                    '70s': ([1, 200], [cBlack, cGreen]),
                    '80s': ([1, 200], [cBlack, cPurple]),
                }
                # Combine the dictionaries
                self.allStatsData = {**self.gridStatsData, **self.fillStatsData}
                # Generate a color code dictionary with the final color for each labelValue
                self.statsColorCodes = {}
                for label, value in self.allStatsData.items():
                    self.thresholds, self.colors = self.thresholds_and_colors[label]
                    self.statsColorCodes[label] = generate_color_code(value, self.thresholds, self.colors)
                # Result: colorCodeData will contain {labelValue: final_color}
                return self.statsColorCodes

            # Assign colors to scores
            self.blockHighlightColor = {
                30: '#ffd8d8',
                40: '#ffffd8',
                60: '#d8d8ff',
                70: '#d8ffd8',
                80: '#ffceff'
            }
            self.displayFill = True
            self.displayNumbering = False
            self.displayScoreHighlights = False
            self.blockSize = 40
            self.lineWidth = 2
            self.analyzeTabButtonNames = ['Stats', 'Lengths', 'Words', 'Crossers']

            self.inputFile = lib.userInputOpenFilePath()
            self.puzzleGrid = analyze.loadAcrossLiteFile(self.inputFile)
            self.rows = len(self.puzzleGrid)
            self.cols = len(self.puzzleGrid[0])
            self.numbering, self.across, self.down = analyze.puzzleLayout(self.puzzleGrid)
            self.words = analyze.fillWordsList(self.across, self.down)
            self.scores = analyze.fillWordsScores(self.words)
            self.gridStatsData = {
                'Words': len(self.words),
                'Across': len(self.across),
                'Down': len(self.down),
                'Blocks': sum(r.count('.') for r in self.puzzleGrid),
                'Longs': analyze.gridCountLongs(self.words),
                '3s': analyze.gridCountThrees(self.words),
                'Spans': analyze.gridCountSpans(self.words),
                'Opens': analyze.gridCountOpens(self.puzzleGrid),
                'Average': analyze.gridAverageLength(self.words),
            }
            self.fillStatsData = {
                'Score Index': analyze.fillAverageScore(self.scores),
                'Overs Average': analyze.fillAverageOvers(self.scores),
                'Scrabble': analyze.fillAvergeScrabble(self.puzzleGrid),
                'Unique': analyze.fillCountUniques(self.scores),
                'Over/Under': analyze.fillCountOvers(self.scores),
                '60s': analyze.countHighScores(self.scores)[0],
                '70s': analyze.countHighScores(self.scores)[1],
                '80s': analyze.countHighScores(self.scores)[2],
            }
            # Determine missing letters
            self.missingLetters = analyze.missingLetters(self.puzzleGrid)
            # Set up main window
            self.puzzleAnalysis = ctk.CTkToplevel(fg_color='#ffffff')
            self.puzzleAnalysis.resizable(False,False)
            self.puzzleAnalysis.title(f' Puzzle Analysis - {Path(self.inputFile).stem}')
            self.after(200, lambda: self.puzzleAnalysis.attributes('-topmost', 1))
            self.after(200, lambda: self.puzzleAnalysis.attributes('-topmost', 0))
            # self.after(200, lambda: self.puzzleAnalysis.iconbitmap('assets.bdogicon.ico'))
            # Define frames
            self.masterFrame = ctk.CTkFrame(self.puzzleAnalysis, width=900, height=480, fg_color='#ffffff')
            self.puzzleViewFrame = ctk.CTkFrame(self.masterFrame, fg_color='#ffffff')
            self.tabFrame = ctk.CTkFrame(self.masterFrame, fg_color='#ffffff')
            self.dataFrame1 = ctk.CTkFrame(self.masterFrame, fg_color='#ffffff')
            self.dataFrame2 = ctk.CTkFrame(self.masterFrame, fg_color='#ffffff')
            self.graphFrame = ctk.CTkFrame(self.masterFrame, fg_color='#ffffff')
            # Define widgets
            self.tabs = ctk.CTkSegmentedButton(self.tabFrame, values=self.analyzeTabButtonNames, command=segmentedButtonCallback)
            self.centeringLabel1 = ctk.CTkLabel(self.tabFrame, text='', width=95)
            self.toggleFillButton = ctk.CTkSegmentedButton(self.puzzleViewFrame, values=['Fill', 'Grid', 'Numbering'], width=150, command=toggleFill)
            self.toggleHighlightsButton = ctk.CTkButton(self.puzzleViewFrame, text='Show Highlights', width=150, command=toggleHighlightsButton)
            self.saveFillToFileButton = ctk.CTkButton(self.puzzleViewFrame, text='Save', width=80, command=saveFillImage)
            self.dataTextbox = ctk.CTkTextbox(self.dataFrame1, width=400, height=350, wrap='word', font=self.monoFont)
            # Set up master frame layout
            self.masterFrame.grid(row=0, column=0, padx=(12, 12), pady=(12, 12), sticky='nsew')
            self.masterFrame.grid_propagate(False)
            self.puzzleViewFrame.grid(row=0, column=0, rowspan=2, columnspan=4, padx=(12, 12), pady=(12, 12), sticky='new')
            self.tabFrame.grid(row=0, column=4, columnspan=2, padx=(12, 12), pady=(9, 12), sticky='new')
            self.dataFrame1.grid(row=1, column=4, padx=(12, 12), pady=(12, 12), sticky='n')
            self.dataFrame2.grid(row=1, column=5, padx=(12, 12), pady=(12, 12), sticky='n')
            # Display buttons
            self.toggleHighlightsButton.grid(row=1, column=0, padx=(12, 6), pady=(12, 12), sticky='w')
            self.saveFillToFileButton.grid(row=1, column=1, padx=(6, 6), pady=(12, 12), sticky='w')
            self.toggleFillButton.grid(row=1, column=2, padx=(6, 12), pady=(12, 12), sticky='e')
            self.toggleFillButton.set('Fill')
            self.centeringLabel1.grid(row=0, column=0)
            self.tabs.grid(row=0, column=1, padx=(12, 12), pady=(12, 12))
            self.tabs.set('Stats')

            viewPuzzle(self, self.puzzleGrid, fill=self.displayFill, numbers=self.displayNumbering)
            displayGridStats()

        def runFetchClues(self):
            # Get the puzzle file from the user
            self.inputFile = lib.userInputOpenFilePath('Select puzzle to get clues for')
            # Extract the puzzle's words
            self.puzzleGrid = analyze.loadAcrossLiteFile(self.inputFile)
            self.numbering, self.across, self.down = analyze.puzzleLayout(self.puzzleGrid)
            self.words = analyze.fillWordsList(self.across, self.down)

            # Open the file containing the clues
            with open(lib.clueFile, 'r') as f:
                clueList = [line.strip() for line in f if line.strip()]
            
            # Find clues for words in the puzzle
            answer = {}
            for line in self.words:
                for entry in clueList:
                    if entry.startswith(f'{line};'):
                        key, clue = entry.split(';', 1)
                        answer[key] = clue.replace('"', '')

            # Create the string output
            message = ''
            for entry in answer.keys():
                message += f'{entry} : {answer[entry]}\n'

            # Open the pop up window for the results to be displayed            
            self.cluesFetchResultPopup = ctk.CTkToplevel()
            self.cluesFetchResultPopup.wm_attributes('-topmost', True)

            self.m = ctk.StringVar()
            self.m.set(message)
            self.messageTextBox = ctk.CTkTextbox(
                self.cluesFetchResultPopup,
                width=700,
                bg_color='transparent',
                wrap='word',
                font=self.monoFont,
                )
            self.messageTextBox.insert('0.0', self.m.get())
            self.messageTextBox.grid(row=0, column=0, padx=10, pady=10, sticky='eswn')
   
        def runAddXwiWords(self):

            def print_word(word):
                wo, so = word.split(';')
                print(f'          {wo} {so} ', end='', flush=True)


            # def get_new_score():
            #     """Returns new word score as a two chararcter string."""
            #     prompt = '(Q, W, E, R, X, ENTER): '
            #     while True:
            #         try:
            #             ns = {'':'00', 'Q':'20', 'W':'35', 'E':'60',
            #                 'R':'70', 'X':'-99'} \
            #             [input(prompt).upper()]
            #             if ns == '35':
            #                 if int(len(wo)) <= 4:
            #                     ns = '40'
            #                 else:
            #                     ns = '30'
            #             return (ns)
            #         except KeyError:
            #             print(' '*25, end='')

            def submitButtonClicked():
                pass
            def undoButtonClicked():
                pass

            # Set column width
            columnWidth = 160

            # Create adn open the main popup window
            self.addXwiWordsApp = ctk.CTkToplevel()
            self.addXwiWordsApp.title(' Score and add new words to my list')
            self.after(50, lambda: self.addXwiWordsApp.attributes('-topmost', 1))
            self.after(50, lambda: self.addXwiWordsApp.attributes('-topmost', 0))
            # self.after(200, lambda: self.addXwiWordsApp.iconbitmap('assets.bdogicon.ico'))
            # self.addXwiWordsApp.resizable(False, False)
            self.addedWords = 0
            self.mDict = lib.myDict(min_score=0)
            self.xDict = lib.xwiDict(min_score=0)
            # FInd all words on the xwi word list that aren't on my word list
            self.newWords = lib.getNewWords(self.xDict, self.mDict)
            # Get user to imput the length to work on
            
            self.selectedLength = 9





            # Find new words of selected length
            self.newLengthWords = [x for x in self.newWords.keys() if len(x) == self.selectedLength]

            # Get label values
            self.mFilename = Path(lib.masterFile).stem
            self.xFilename = Path(lib.xwiFile).stem

            self.newLengthWordCount = ctk.IntVar()
            self.newWordCount = ctk.IntVar()
            self.addedCount = ctk.IntVar()
            self.newTotal = ctk.IntVar()

            self.newLengthWordCount.set(value=len(self.newLengthWords))
            self.newWordCount.set(value=len(self.newWords))
            self.xwiWordCount = len(self.xDict)
            self.startWordCount = len(self.mDict)
            self.addedCount.set(value=0)
            self.newTotal.set(value=(self.startWordCount + self.addedCount.get()))

            # Process words
            # for w in self.newLengthWords:
            #     wo, so = w.split(';')
            #     self.newWordDisplayString = f'{wo}{' '*(16 - len(wo))}{so}'
            #     # update label and display word and score here
            #     ns = get_new_score()
            #     nw = wo + ';' + ns

            #     # update label and display word with new score here            
                    
            #     open(lib.masterFile,'a').write(nw + '\n')
            #     self.newLengthWordCount -= 1
            #     self.newWordCount -= 1
            #     self.addedWords += 1
            #     self.newTotal += 1
        
        
            # Create master frames
            self.masterFrame = ctk.CTkFrame(self.addXwiWordsApp, fg_color='#dcdcdc')
            self.headerFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
            self.infoFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
            self.workingFrame = ctk.CTkFrame(self.masterFrame, fg_color='#dcdcdc')
            self.submitButtonFrame = ctk.CTkFrame(self.workingFrame, fg_color='#dcdcdc')
            self.undoButtonFrame = ctk.CTkFrame(self.workingFrame, fg_color='#dcdcdc')
            # Create static labels (8)
            self.headerLabel = ctk.CTkLabel(
                self.headerFrame,
                # width=160,
                text=f'{self.xFilename} --> {self.mFilename}',
                anchor='n',
                **self.messageHighlightStyle,
            )
            self.spacerLabel = ctk.CTkLabel(
                self.infoFrame,
                width=50,
                text='',
                )
            self.lengthNewTotalLabel = ctk.CTkLabel(
                self.infoFrame,
                width=columnWidth * 0.75,
                text=f'{self.selectedLength} long new',
                font=self.defaultFont, 
                anchor='w',
                )
            self.xwiNewTotalLabel = ctk.CTkLabel(
                self.infoFrame,
                text='New words',
                font=self.defaultFont, 
                anchor='w',
                )
            self.xwiTotalLabel = ctk.CTkLabel(
                self.infoFrame,
                text='Total words',
                font=self.defaultFont, 
                anchor='w',
                )
            self.startTotalLabel = ctk.CTkLabel(
                self.infoFrame,
                width=columnWidth * 0.75,
                text='Start',
                font=self.defaultFont, 
                anchor='w',
                )
            self.addedTotalLabel = ctk.CTkLabel(
                self.infoFrame,
                text=f'Added',
                font=self.defaultFont, 
                anchor='w',
                )
            self.currentTotalLabel = ctk.CTkLabel(
                self.infoFrame,
                text=f'New total',
                font=self.defaultFont, 
                anchor='w',
                )
            # Create dynamic labels (10)
            # self.fromFilenameValue = ctk.CTkLabel(
            #     self.headerFrame,
            #     width=160,
            #     text=f'{self.xFilename}',
            #     **self.messageHighlightStyle,
            #     )
            self.lengthNewTotalValue = ctk.CTkLabel(
                self.infoFrame,
                text=f'{self.newLengthWordCount.get(): 8,}',
                font=self.defaultFont,
                justify='right',
            )
            self.xwiNewTotalValue = ctk.CTkLabel(
                self.infoFrame,
                width=columnWidth * 0.25,
                text=f'{self.newWordCount.get(): 8,}',
                font=self.defaultFont,
                justify='right',
                )
            self.xwiTotalValue = ctk.CTkLabel(
                self.infoFrame,
                text=f'{self.xwiWordCount: 8,}',
                font=self.defaultFont,
                justify='right',
                )
            self.startTotalValue = ctk.CTkLabel(
                self.infoFrame,
                width=columnWidth * 0.25,
                text=f'{self.startWordCount: 8,}',
                font=self.defaultFont,
                justify='right',
                )
            self.addedTotalValue = ctk.CTkLabel(
                self.infoFrame,
                text=f'{self.addedCount.get(): 8,}',
                font=self.defaultFont,
                justify='right',
                )
            self.currentTotalValue = ctk.CTkLabel(
                self.infoFrame,
                text=f'{self.newTotal.get(): 8,}',
                font=self.defaultFont,
                justify='right',
                )
            self.displayNewWordLabel = ctk.CTkLabel(
                self.workingFrame,
                width=columnWidth,
                bg_color='#ffffff',
                text=f'',
                font=self.defaultFont,
                justify='right',
                )
            self.displayAddedWordLabel = ctk.CTkLabel(
                self.workingFrame,
                width=columnWidth,
                bg_color='#ffffff',
                text=f'',
                font=self.defaultFont,
                justify='right',
                )

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
                width=60,
                text='Submit',
                command=submitButtonClicked,
                font=self.defaultFont,
                state='normal'
                )
            self.undoButton = ctk.CTkButton(
                self.undoButtonFrame,
                width=60,
                text='Undo',
                command=undoButtonClicked,
                font=self.defaultFont,
                state='normal',
                )
        
        
            # Place master frames
            self.masterFrame.grid(row=0, column=0)
            self.headerFrame.grid(row=0, column=0, padx=(12, 12), pady=(12, 12), sticky='ew')
            self.infoFrame.grid(row=1, column=0, padx=(12, 12), pady=(12, 12), sticky='ew')
            self.workingFrame.grid(row=2, column=0, padx=(12, 12), pady=(12, 12), sticky='ew')
            self.submitButtonFrame.grid(row=1, column=1, padx=(12, 12), pady=(12, 12))
            self.undoButtonFrame.grid(row=1, column=2, padx=(12, 12), pady=(12, 12))
            # Place static labels
            # self.arrowLabel.grid(row=0, column=1, padx=(0, 0), pady=(12, 6), sticky='new')
            self.spacerLabel.grid(row=0, column=2, padx=(0, 0), pady=(0, 0), sticky='new')
            self.lengthNewTotalLabel.grid(row=0, column=0, padx=(12, 12), pady=(0, 0), sticky='nw')
            self.xwiNewTotalLabel.grid(row=1, column=0, padx=(12, 12), pady=(0 ,0), sticky='nw')
            self.xwiTotalLabel.grid(row=2, column=0, padx=(12, 12), pady=(0 ,0), sticky='nw')
            self.startTotalLabel.grid(row=0, column=3, padx=(12, 12), pady=(0 ,0), sticky='nw')
            self.addedTotalLabel.grid(row=1, column=3, padx=(12, 12), pady=(0 ,0), sticky='nw')
            self.currentTotalLabel.grid(row=2, column=3, padx=(12, 12), pady=(0 ,0), sticky='nw')
            # Place dynamic labels
            # self.fromFilenameValue.grid(row=0, column=0, padx=(12, 0), pady=(12 ,6), sticky='new')
            self.headerLabel.pack()#grid(row=0, column=0, padx=(12, 12), pady=(12 ,6))
            self.lengthNewTotalValue.grid(row=0, column=1, padx=(12, 12), pady=(0 ,0), sticky='ne')
            self.xwiNewTotalValue.grid(row=1, column=1, padx=(12, 12), pady=(0 ,0), sticky='ne')
            self.xwiTotalValue.grid(row=2, column=1, padx=(12, 12), pady=(0 ,0), sticky='ne')
            self.startTotalValue.grid(row=0, column=4, padx=(12, 12), pady=(0 ,0), sticky='ne')
            self.addedTotalValue.grid(row=1, column=4, padx=(12, 12), pady=(0 ,0), sticky='ne')
            self.currentTotalValue.grid(row=2, column=4, padx=(12, 12), pady=(0 ,0), sticky='ne')
            self.displayNewWordLabel.grid(row=0, column=0, padx=(12, 0), pady=(12 ,12), sticky='ne')
            self.displayAddedWordLabel.grid(row=0, column=2, padx=(0, 12), pady=(12 ,12), sticky='ne')

            # Place entry box
            self.entryBox.grid(row=0, column=1, padx=(0, 0), pady=(12, 12))
            # Place buttons
            self.submitButton.grid(row=0, column=0, padx=(12, 12), pady=(12, 12))
            self.undoButton.grid(row=0, column=0, padx=(12, 12), pady=(12 ,12))



    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.iconbitmap('assets/bdogicon.ico')
            self.title(' Beach Dog Crosswords')
            self.resizable(False,False)
            # Set menu Items
            self.mainMenuItems = [
                'Puzzles',
                'Master',
                'Lists',
                'Words',
                'Clues'
            ]
            self.subMenuItems = {
                'analyze': 'Puzzles',
                'compare': 'Puzzles',
                'find_new_words': 'Lists',
                'remove_dupes': 'Lists',
                'clean': 'Lists',
                'length': 'Words',
                'changes': 'Words',
                'fetch': 'Clues',
                'add': 'Clues',
                'tables': 'Master',
                'add_xwi': 'Master',
                'new_on_xwi': 'Master', 
                'check_80': 'Master',
                'publish_gold': 'Master',
                'update_master' : 'Master'
            }
            # Initialize main menu
            MainMenu(self, self.mainMenuItems).grid(row=0, column=0, padx=10, pady=10, sticky='w')


    app = App()
    app.mainloop()
    
if __name__ == '__main__':
    main()
