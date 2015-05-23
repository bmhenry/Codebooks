import os
import shutil
from codebook_ui.codebook_main_ui import *
from codebook_ui.adapted_qtclasses import *
from codebook_fileops.fileops import *
from codebook_fileops.settingsops import *

# idea: import code button for a new entry

class CodebooksMainWindow(CodebooksMainUi):

    def __init__(self, mainfile_dir):
        self.main_dir = mainfile_dir  # directory program is running from
        self.settings = getSettings(mainfile_dir)  # load settings from file
        self.lastSelectedEntry = self.settings['open_entry'] if 'open_entry' in self.settings.keys() else -1
        self.lastSelectedCodebook = self.settings['focused_codebook'] if 'focused_codebook' in self.settings.keys() else -1

        # setup class variables
        self.isNewEntry = False
        self.entrySaved = True
        self.entryRenamed = False
        self.entryRetagged = False
        self.currentEntry = None

        super().__init__()


    def startupCalled(self):
        """Triggered by __init__ of CodebooksMainUi"""

        # open the codebooks that were left open in previous session
        if 'open_codebooks' in self.settings.keys():
            for codebook in self.settings['open_codebooks'].copy():
                self.openCodebook(self.settings['codebooks'][codebook], startup = True)

        # focus the codebook that was selected in the last session
        if 'focused_codebook' in self.settings.keys():
            lsc = self.settings['focused_codebook']
            if lsc > -1:
                self.codebookTabs.setCurrentIndex(lsc)

        # focus the entry that was selected in the last session
        if 'open_entry' in self.settings.keys():
            lse = self.settings['open_entry']
            if lse > -1:
                codebookEntries = self.getCodebookEntries()  # get codebookEntries widget
                codebookEntries.setCurrentRow(lse)

        pass


    def alert(self, message, infotext = ''):
        """Boilerplate simple alert message popup"""

        # Create a message box
        alertbox = QtWidgets.QMessageBox()
        alertbox.setFixedSize(600,200)

        alertbox.setText(message)
        alertbox.setInformativeText(infotext)
        alertbox.exec_()
        pass


    def save_alert(self):
        """Alert to ask if user would like to save"""

        # Create a message box
        alertbox = QtWidgets.QMessageBox()
        alertbox.setText("Entry has been modified.")
        alertbox.setInformativeText("Save before closing?")
        alertbox.setStandardButtons(
            QtWidgets.QMessageBox.Save |
            QtWidgets.QMessageBox.Discard |
            QtWidgets.QMessageBox.Cancel)

        alertbox.setDefaultButton(QtWidgets.QMessageBox.Save)

        # show the box and wait for user answer
        answer = alertbox.exec_()

        if answer == QtWidgets.QMessageBox.Save:
            return 'Save'
        elif answer == QtWidgets.QMessageBox.Cancel:
            return 'Cancel'
        elif answer == QtWidgets.QMessageBox.Discard:
            return 'Discard'
        else:
            return False 


    def delete_alert(self, message = "Are you sure you want to delete this entry?"):
        """Asks the user if they're sure they want to delete entry"""

        # Create a message box
        alertbox = QtWidgets.QMessageBox()
        alertbox.setText(message)
        alertbox.setInformativeText("Deletion is permanent.")
        alertbox.setStandardButtons(
            QtWidgets.QMessageBox.Ok |
            QtWidgets.QMessageBox.Cancel)
        alertbox.setDefaultButton(QtWidgets.QMessageBox.Ok)

        # Show the box and wait for user input
        answer = alertbox.exec_()

        if answer == QtWidgets.QMessageBox.Ok:
            return True
        elif answer == QtWidgets.QMessageBox.Cancel:
            return False

    
    # SINGLE FILE FUNCTIONS ######################################################################

    def newFile(self):
        """Add a single new tab to the entry panel"""

        self.addFileTab("(new file)", "")
        pass


    def openFile(self):
        """Open an existing file"""

        response = file_open()
        if response is not None:
            filename = response[0]

            self.addFileTab(filename,filetext)
        pass


    def saveFile(self):
        """Save the currently selected file as a single file, independent of an entry"""

        currentTabIndex = self.entryTabs.currentIndex()

        # Check that a file is selected
        if currentTabIndex < 0:
            return

        # Get the filename and file text
        currentTab = self.entryTabs.widget(currentTabIndex)
        currentFileName = self.entryTabs.tabText(currentTabIndex)
        currentFileText = currentTab.findChild(QtWidgets.QPlainTextEdit,"fileEdit").toPlainText()

        if currentFileName == "(new file)":
            currentFileName = ''

        # Attempt to save the file
        result = file_save(currentFileName, currentFileText)
        if result != '':
            self.entryTabs.setTabText(currentTabIndex, result)

        pass


    def saveFileAs(self):
        """Save a file to a new place"""

        currentTabIndex = self.entryTabs.currentIndex()

        # Check that a file is selected
        if currentTabIndex < 0 :
            return 

        # Get the file text
        currentTab = self.entryTabs.widget(currentTabIndex)
        currentFileText = currentTab.findChild(QtWidgets.QPlainTextEdit,"fileEdit").toPlainText()

        # Attempt to save the file
        result = file_save_as(currentFileText)
        if result != '':
            self.entryTabs.setTabText(currentTabIndex, result)

        pass


    def closeFile(self):
        """Close the currently selected file"""

        currentTabIndex = self.entryTabs.currentIndex()
        self.entryTabs.removeTab(currentTabIndex)
        pass


    def deleteFile(self):
        """Deletes the currently selected file"""

        entry_name = self.entryName.text().strip()

        if entry_name is '':
            return

        # get file directory
        cb_dir = self.getCurrentCodebook()[1]
        entry_index = self.entryTabs.currentIndex()
        file_name = self.entryTabs.tabText(entry_index)
        file_dir = '/'.join([cb_dir, entry_name, file_name])

        # check to see if file is a description file
        if file_name == 'description.txt':
            message = 'If you delete the description file, this entry will no longer be loaded as part of your codebook. Continue?'
            answer = self.delete_alert(message)

            if not answer:
                return

        # remove the file tab
        
        self.entryTabs.removeTab(entry_index)

        # delete the file
        os.remove(file_dir)

        pass


    # ENTRY TAB FUNCTIONS ########################################################################

    def addFileTab(self, fileName = 'newfile.txt', fileText = '', autofocus = True, directory = None):
        """Adds a file to the entry tabs given optional inputs of the file's name and text"""

        # Add UI element:
        # create the container widget
        fileTab = CBfilewidget(directory = directory)

        # editor for main file text
        fileEdit = QtWidgets.QPlainTextEdit(fileTab)
        fileEdit.setGeometry(QtCore.QRect(0,30,737,507))
        fileEdit.setObjectName("fileEdit")
        fileEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)
        fileEdit.textChanged.connect(self.entryModified)

        fileEdit.setPlainText(fileText)

        # Filename label
        filenameLabel = QtWidgets.QLabel("Filename:", fileTab)
        filenameLabel.setGeometry(QtCore.QRect(15,10,70,15))

        # text box for filename
        filenameEditor = QtWidgets.QLineEdit(fileTab)
        filenameEditor.setGeometry(QtCore.QRect(70,5,590,20))
        filenameEditor.setObjectName("filenameEditor")
        filenameEditor.setPlaceholderText("no file selected")
        filenameEditor.setText(fileName.strip('\n'))
        filenameEditor.textEdited.connect(self.entryModified)


        # add the new tab
        tab_index = self.entryTabs.addTab(fileTab, fileName)

        if autofocus:
            self.entryTabs.setCurrentIndex(tab_index)

        pass


    def addDescriptionTab(self, fileName = 'description.txt', fileTags = '', fileText = ''):
        """Adds a desciption tab to the entry tabs, given optional inputs of the file name, tags, and text"""

        # note: since the description tab is always added first, an autofocus arg is not needed
        # Add UI element:
        # container widget
        fileTab = CBfilewidget()

        # editor for main file text
        fileEdit = QtWidgets.QPlainTextEdit(fileTab)
        fileEdit.setGeometry(QtCore.QRect(0,30,737,507))
        fileEdit.setObjectName("fileEdit")
        fileEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)
        fileEdit.textChanged.connect(self.entryModified)

        # fill the editor with filetext
        fileEdit.setPlainText(fileText)

        # "Tags:" label
        tagLabel = QtWidgets.QLabel("Tags:", fileTab)
        tagLabel.setGeometry(QtCore.QRect(15,10,40,15))

        # text box for tags
        tagEditor = QtWidgets.QLineEdit(fileTab)
        tagEditor.setGeometry(QtCore.QRect(60,5,600,20))
        tagEditor.setObjectName("tagEditor")
        tagEditor.setPlaceholderText("<separate tags with commas>")
        tagEditor.textEdited.connect(self.entryTagsChanged)

        # fill the tag editor with tags
        tagEditor.setText(fileTags.strip('\n'))

        # add the new tab
        tab_index = self.entryTabs.addTab(fileTab, fileName)

        pass


    # CODEBOOK FUNCTIONS #########################################################################

    def getCodebookEntries(self):
        """ Returns the codebookEntries widget"""
        try:
            return self.codebookTabs.widget(self.codebookTabs.currentIndex()).findChild(QtWidgets.QListWidget, 'codebookEntries')
        except Exception:
            return False


    def codebookTabChanged(self):
        """Called if the selected tab of codebookTabs is changed"""

        # Check if currently selected codebook has changed
        if self.codebookTabs.currentIndex() == self.lastSelectedCodebook or self.clearEntry():
            self.lastSelectedEntry = -1
            self.lastSelectedCodebook = self.codebookTabs.currentIndex()
            if self.codebookTabs.currentIndex() > -1:
                codebookEntries = self.getCodebookEntries()
                codebookEntries.setCurrentRow(-1)
        else:
            self.codebookTabs.setCurrentIndex(self.lastSelectedCodebook)
            codebookEntries = self.getCodebookEntries()
            codebookEntries.setCurrentRow(self.lastSelectedEntry)
        pass


    def getCurrentCodebook(self):
        """Returns a tuple containing the (name, directory) of the currently selected codebook"""

        currentCodebookIndex = self.codebookTabs.currentIndex()
        cb_name = self.codebookTabs.tabText(currentCodebookIndex)
        return (cb_name, self.settings['codebooks'][cb_name])


    def addCodebookTab(self, tabName = '', items = None, autofocus = True):
        """Adds a tab to the codebookTabs"""

        cbTab = QtWidgets.QWidget()

        # list for entries
        codebookEntries = QtWidgets.QListWidget(cbTab)
        codebookEntries.setGeometry(QtCore.QRect(-1,-1,187,561))
        codebookEntries.setObjectName("codebookEntries")
        codebookEntries.setFrameShadow(QtWidgets.QFrame.Plain)
        codebookEntries.itemSelectionChanged.connect(self.entryChanged)

        # add entries
        if items is not None:
            for item in items:
                container = QtWidgets.QListWidgetItem(parent = codebookEntries)
                entryItem = CBlistEntryItem(name = item[0], tagString = item[1])

                container.setSizeHint(entryItem.sizeHint())  # turns out this is necessary

                codebookEntries.addItem(container)  # add the list item into the list
                codebookEntries.setItemWidget(container, entryItem)  # put the entry widget into the list item widget

        # add the tab and get the index of the new tab back
        tab_index = self.codebookTabs.addTab(cbTab, tabName)

        if autofocus:
            self.codebookTabs.setCurrentIndex(tab_index)

        pass


    def newCodebook(self):
        """Creates a new codebook and .cdb file inside a selected directory"""

        defaultName = 'new_codebook'

        # open file dialog to create a new codebook
        new_directory = new_codebook()
        if new_directory is not None:
            cb_dir, cb_name = new_directory
        else:
            return

        # add codebook to codebookTabs
        allowfocus = self.entrySaved
        self.addCodebookTab(tabName = cb_name, autofocus = allowfocus)

        # if the currently selected entry is saved, go ahead and close it and focus new codebook
        #  otherwise, do nothing
        if allowfocus:
            self.clearEntry()
            self.entryName.setText('')
            self.lastSelectedCodebook = self.codebookTabs.currentIndex()


        # add the directory and codebook to the settings
        self.settings['codebooks'][cb_name] = cb_dir
        self.settings['open_codebooks'].append(cb_name)
        self.saveSettings()
        pass


    def openCodebook(self, directory = None, startup = False):
        """Opens a codebook from a folder"""

        # open file dialog to get an existing directory
        # TODO: check that the directory is actually a codebook (do this in the open_codebook function)
        existing_codebook = open_codebook(dirname = directory)
        if existing_codebook is not None:
            cb_dir, cb_name = existing_codebook
        else:
            return

        # check if the codebook is already open
        if not startup:
            if 'open_codebooks' in self.settings.keys():
                if cb_name in self.settings['open_codebooks']:
                    if cb_dir == self.settings['codebooks'][cb_name]:
                        self.alert("This codebook is already open!")
                        return
            else:
                self.settings['open_codebooks'] = []

        # get a list of file & folders in the codebook
        try:
            subfolders = os.listdir(cb_dir)
        except FileNotFoundError:
            if not startup:
                alert("The codebook you've selected doesn't seem to exist.")
            return

        # open each entry
        entrylist = []
        for entry in subfolders:
            description_dir = cb_dir + '/' + entry + '/description.txt'
            tags = parse_description(fileloc = description_dir, tagsOnly = True)
            if tags:
                entrylist.append((entry, tags))

        # add the codebook to codebookTabs
        self.addCodebookTab(tabName = cb_name, items = entrylist, autofocus = not startup)


        # add the codebook to 'open_codebooks' in settings
        if not startup:
            self.settings['open_codebooks'].append(cb_name)
            self.saveSettings()

        pass


    def closeCodebook(self):
        """Closes the currently selected codebook"""

        # TODO: check whether entry is saved before closing codebook


        # get currently selected codebook
        currentTabIndex = self.codebookTabs.currentIndex()

        # get name of current codebook
        currentTabName = self.codebookTabs.tabText(currentTabIndex)

        # close tab and remove it from the 'open_codebooks'
        self.codebookTabs.removeTab(currentTabIndex)
        self.settings['open_codebooks'].remove(currentTabName)
        self.saveSettings()
        pass


    def deleteCodebook(self):
        """Deletes a codebook and everything contained therein"""
        if not self.delete_alert(message = "This will delete the codebook as well as ALL ENTRIES contained within.\nAre you sure? I mean, realllly sure?"):
            return

        # get codebook directory
        cb_name, cb_dir = self.getCurrentCodebook()

        # remove the codebook from tabs
        self.entryTabs.clear()
        self.entryName.setText('')
        self.codebookTabs.removeTab(self.codebookTabs.currentIndex())

        # delete it
        shutil.rmtree(cb_dir)

        # remove the codebook from settings
        self.settings['open_codebooks'].remove(cb_name)
        self.settings['codebooks'].pop(cb_name)
        self.saveSettings()

        pass


    def countCodebookEntries(self):
        """Counts the total number of entries in the current codebook"""

        cb_dir = self.getCurrentCodebook()[1]

        possible_entries = os.listdir(cb_dir)

        total_entries = 0
        for path in possible_entries:
            if os.path.exists('/'.join([cb_dir, path, 'description.txt'])):
                total_entries += 1

        return total_entries


    def codebookInfo(self):
        """Displays some basic information about the current codebook."""

        cb_name, cb_dir = self.getCurrentCodebook()

        infotext =  "Directory: " + cb_dir + '\n'
        infotext += "Entries: " + str(self.countCodebookEntries()) + '\n'

        data_path = cb_dir + '/' + cb_name + '.cdb'

        cb_data = getCodebookData(data_path)
        if 'creation_date' in cb_data:
            infotext += "Creation Date:    " + cb_data['creation_date']

        self.alert(message = "Codebook '{}'".format(cb_name), infotext = infotext)

        pass



    # CODEBOOK ENTRY FUNCTIONS ###################################################################

    def entryModified(self):
        """Called if any entry text is modeified"""

        self.entrySaved = False
        self.savedStatus.setText('Entry not saved')
        pass


    def entryNameChanged(self):
        """Called if an entry's name is changed"""

        self.entrySaved = False
        self.entryRenamed = True
        self.savedStatus.setText('Entry not saved')
        pass


    def entryTagsChanged(self):
        """Called if an entry's tags are changed"""

        self.entrySaved = False
        self.entryRetagged = True
        self.savedStatus.setText('Entry not saved')
        pass
    

    def newEntry(self):
        """Clears the current entry from entryTabs and adds a new one"""

        if self.codebookTabs.currentIndex() < 0:
            self.alert("Please select a codebook to create the entry in.")
        # attempt to close the current entry, will return False if user chooses to cancel action
        if not self.clearEntry():
            return

        # get the currently selected codebook
        currentTabIndex = self.codebookTabs.currentIndex()
        codebookEntries = self.getCodebookEntries()

        codebookEntries.setCurrentRow(-1)

        currentTabName = self.entryTabs.tabText(currentTabIndex)

        # add description tab and a single new file
        self.addDescriptionTab('description.txt')
        self.addFileTab(autofocus = False)

        # set class variables
        self.isNewEntry = True
        self.entrySaved = True
        self.entryRenamed = False
        self.entryRetagged = False
        self.currentEntry = None

        self.entryName.setText('(new entry)')

        self.savedStatus.setText('New entry')
        pass


    def entryChanged(self):
        """Opens the entry that has been selected in the list widget within the current tab of codebookTabs"""

        # get the listwidget containing entries
        codebookEntries = self.getCodebookEntries()

        # ignore if no real change was made
        #  (for example, allows this to be ignored if a new entry is added since lastSelectedEntry is set before
        #    changing the row)
        if self.lastSelectedEntry == codebookEntries.currentRow():
            return

        # test if the entry can be closed
        if not self.clearEntry():
            codebookEntries.setCurrentRow(self.lastSelectedEntry)
            return

        # if all goes well:
        self.lastSelectedEntry = codebookEntries.currentRow()

        # check if the current row is -1 (no entry selected) and if so don't try to open it
        if codebookEntries.currentRow() > -1:
            # get the newly selected entry
            selectedEntry = codebookEntries.itemWidget(codebookEntries.currentItem())
            # open the entry
            self.openEntry(entryName = selectedEntry.findChild(QtWidgets.QLabel, "entryName").text())

        self.savedStatus.setText(' ')
        pass


    def openEntry(self, entryName):
        """Opens an entry given the entry's name"""

        # test if an entry is already open
        entryNum = self.entryTabs.currentIndex()
        codebookEntries = self.getCodebookEntries()

        # set entry name
        self.entryName.setText(entryName)

        # set the entry directory
        entrydir = self.getCurrentCodebook()[1] + '/' + entryName
        self.currentEntry = entrydir

        # get the files within the entry
        files = os.listdir(entrydir)

        # get info from the entry description.txt file, then add the description to entryTabs
        tags, description = parse_description(entrydir + '/description.txt')
        self.addDescriptionTab(fileTags = tags, fileText = description)

        # set the class variable containing entry index
        self.lastSelectedEntry = codebookEntries.currentRow()

        # make sure we don't load the description twice
        if 'description.txt' in files:
            files.remove('description.txt')

        # add each file to entryTabs
        for f in files:
            try:
                with open(entrydir + '/' + f, 'r') as ft:
                    text = ft.read()
                    self.addFileTab(fileName = f, fileText = text, autofocus = False, directory = entrydir + '/' + f)
            except Exception as e:
                print('Error opening entry (openEntry): ', e)

        # set saved status
        self.isNewEntry = False
        self.entrySaved = True
        self.entryRenamed = False
        self.entryRetagged = False

        self.savedStatus.setText('Entry saved')

        pass


    def saveEntry(self):
        """Saves the currently selected entry"""

        if self.currentEntry is None:
            # get the codebook directory to save the entry in
            currentCodebookTab = self.codebookTabs.currentIndex()
            if currentCodebookTab < 0:
                self.alert("Please select a codebook to save the entry in.")
                return

            cb_dir = self.getCurrentCodebook()[1]

            # check that the codebook exists
            if cb_dir is None:
                alert("This codebook doesn't exist.")
                return

            entry_name = self.entryName.text()
            if entry_name == '(new entry)':
                self.alert("You're using the default entry name!")
                return

            if os.path.exists(cb_dir + '/' + entry_name):
                self.alert("This code entry already exists.")
                return

            entry_dir = cb_dir + '/' + entry_name
            os.mkdir(entry_dir)
            self.currentEntry = entry_dir

            # add entry to codebook list
            codebookEntries = self.getCodebookEntries()

            # container item to add to list
            element = QtWidgets.QListWidgetItem(parent = codebookEntries)
            # widget containing entry info
            entryItem = CBlistEntryItem(name = entry_name, 
                        tagString = self.entryTabs.widget(0).findChild(QtWidgets.QLineEdit, "tagEditor").text())

            element.setSizeHint(entryItem.sizeHint())  # required

            codebookEntries.addItem(element)
            codebookEntries.setItemWidget(element, entryItem)
            element_index = codebookEntries.row(element)

            # set the selected row to the new entry
            self.lastSelectedEntry = element_index
            codebookEntries.setCurrentRow(element_index)


        # Call save on each file in directory self.currentEntry
        for tab_index in range(self.entryTabs.count()):
            tab = self.entryTabs.widget(tab_index)
            if tab_index == 0:
                # change name of entry if it was modified
                if self.entryRenamed and not self.isNewEntry:
                    new_entry_dir = self.getCurrentCodebook()[1] + '/' + self.entryName.text()
                    os.rename(self.currentEntry, new_entry_dir)
                    self.currentEntry = new_entry_dir
                    codebookEntries = self.getCodebookEntries()
                    selectedEntry = codebookEntries.itemWidget(codebookEntries.item(self.lastSelectedEntry))
                    selectedEntry.findChild(QtWidgets.QLabel, 'entryName').setText(self.entryName.text())

                new_tags = tab.findChild(QtWidgets.QLineEdit, "tagEditor").text()

                # change tags of entry in codebookEntries if tags changed
                if self.entryRetagged and not self.isNewEntry:
                    codebookEntries = self.getCodebookEntries()
                    selectedEntry = codebookEntries.itemWidget(codebookEntries.item(self.lastSelectedEntry))
                    selectedEntry.findChild(QtWidgets.QLabel, 'entryTags').setText(new_tags)
                
                description_save(filename = self.currentEntry + '/description.txt',
                    tagString = new_tags,
                    fileText = tab.findChild(QtWidgets.QPlainTextEdit, "fileEdit").toPlainText())
                
            else:
                new_name = tab.findChild(QtWidgets.QLineEdit, "filenameEditor").text()
                new_dir = self.currentEntry + '/' + new_name

                # rename the file if it was changed
                if tab.directory is not None:
                    # if entry renamed, fix tab.directory
                    if self.entryRenamed:
                        tab.directory = self.currentEntry + '/' + tab.directory.split('/')[-1]

                    # rename the file
                    if tab.directory != new_dir:
                        try:
                            os.rename(tab.directory, new_dir)
                            tab.directory = new_dir
                        except Exception as e:
                            print('Error saving entry (saveEntry): ',e)
                            self.alert("Couldn't save file. Is it opened in another editor?")
                            return
                    codebookEntries = self.getCodebookEntries()
                if tab.directory is None:
                    tab.directory = new_dir

                file_save(new_dir, tab.findChild(QtWidgets.QPlainTextEdit, "fileEdit").toPlainText())
                self.entryTabs.setTabText(tab_index, new_dir.split('/')[-1])
                self.savedStatus.setText('Entry saved')
            pass

        # reset variables
        self.entryRenamed = False
        self.entryRetagged = False
        self.isNewEntry = False

        # set saved status
        self.entrySaved = True

        pass


    def closeEntry(self):
        """Attempts to close the current entry completely"""

        # clear the entry from entryTabs
        self.clearEntry()

        # reset codebookEntries
        codebookEntries = self.getCodebookEntries()
        codebookEntries.setCurrentRow(-1)
        self.lastSelectedEntry = -1


    def clearEntry(self):
        """Attempts to close an open entry."""

        # Check that an entry is open
        if self.entryTabs.count() > 0:
            # If the entry isn't saved, alert the user to save it, discard changes, or cancel action
            if not self.entrySaved:
                answer = self.save_alert()
                if answer == 'Save':
                    self.saveEntry()
                elif answer == 'Cancel':
                    return False
                else:
                    pass

            self.entryTabs.clear()
            self.entryName.setText('')

            self.isNewEntry = False
            self.entrySaved = True
            self.entryRenamed = False
            self.entryRetagged = False
            self.currentEntry = None

            self.savedStatus.setText(' ')

        return True


    def deleteEntry(self):
        """Removes an entry from a codebook"""
        # "Are you sure" check
        answer = self.delete_alert()
        if not answer:
            return

        # get entry information
        cb_dir = self.getCurrentCodebook()[1]
        codebookEntries = self.getCodebookEntries()
        cur_entry = codebookEntries.itemWidget(codebookEntries.currentItem())
        entry_name = cur_entry.findChild(QtWidgets.QLabel, "entryName").text()

        # delete entry from list
        old_entry = codebookEntries.takeItem(codebookEntries.currentRow())

        # delete the entry and directory
        entry_dir = cb_dir + '/' + entry_name
        shutil.rmtree(entry_dir)

        # fix variables
        self.lastSelectedEntry = -1
        self.isNewEntry = False
        self.entrySaved = True
        self.entryRenamed = False
        self.entryRetagged = False
        self.currentEntry = None
        pass

    # SETTINGS FUNCTIONS #########################################################################
    
    def openSettings(self):
        if not self.settingsWindow:
            self.settingsWindow = SettingsWindow()

        pass


    def saveSettings(self):
        save_settings(self.main_dir, self.settings)
        pass


    # HELP WINDOW FUNCTIONS ######################################################################

    def openHelp(self):

        pass


    # CODE BUTTON FUNCTIONS ######################################################################

    def getCode(self):
        """Called on user clicking 'Get Code'; downloads code to a new location"""

        codebookEntries = self.getCodebookEntries()

        if codebookEntries.currentRow() < 0:
            self.alert("You need to select an entry before you can download it.")
            return

        cur_entry = codebookEntries.itemWidget(codebookEntries.currentItem())
        entry_name = cur_entry.findChild(QtWidgets.QLabel, "entryName").text()

        entry_dir = self.getCurrentCodebook()[1] + '/' + entry_name

        copy_entry(entry_dir = entry_dir)

        pass
    

    # TAG SEARCH #################################################################################

    def searchbarChanged(self):
        """Captures textEdited event from the tag searchbox"""
        tagString = self.searchBox.text().strip('\n\t ')

        self.searchTags(tagString)

        pass


    def searchTags(self, tagString = ''):
        """Searches for entries in current codebook that contain the tags in the tagString"""

        codebookEntries = self.getCodebookEntries()

        # clear current entries
        codebookEntries.clear()

        # iterate through the entries in the directory and find those with tags that match
        cb_dir = self.getCurrentCodebook()[1]
        try:
            subfolders = os.listdir(cb_dir)
        except FileNotFoundError:
            if not startup:
                alert("The codebook you've selected doesn't seem to exist.")
            return

        # open each entry and put it in the codebookEntries list
        for entry_name in subfolders:
            description_dir = cb_dir + '/' + entry_name + '/description.txt'
            entry_tags = parse_description(fileloc = description_dir, tagsOnly = True)

            if entry_tags is not None:
                search_tags = [tag.strip() for tag in tagString.split(',')]

                tags_found = True

                if tagString.strip() is not '':  # skip the comparing if the tagString is empty
                    for tag in search_tags:
                        if tag in entry_tags:
                            pass
                        else:
                            tags_found = False
                            break

                    if entry_name in search_tags:
                        tags_found = True

                if tags_found:
                    container = QtWidgets.QListWidgetItem(parent = codebookEntries)
                    entryItem = CBlistEntryItem(name = entry, tagString = entry_tags)

                    container.setSizeHint(entryItem.sizeHint())  # turns out this is necessary

                    codebookEntries.addItem(container)  # add the list item into the list
                    codebookEntries.setItemWidget(container, entryItem)  # put the entry widget into the list item widget

        pass


    # WINDOW CLOSE ###############################################################################

    def closeEvent(self, event):
        # check that entry is saved
        def close():
            print("Closing...\n")
            self.settings['focused_codebook'] = self.lastSelectedCodebook
            self.settings['open_entry'] = self.lastSelectedEntry
            self.saveSettings()


        if not self.entrySaved:
            answer = self.save_alert()
            if answer == 'Save':
                self.saveEntry()
                close()
            elif answer == 'Discard':
                close()
            else:
                event.ignore()
        else:
            close()
        pass