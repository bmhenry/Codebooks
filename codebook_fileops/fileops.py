from PyQt5 import QtWidgets
from codebook_fileops.settingsops import *
import os
import shutil

# single file operations
def file_open():
    # get filename and show only .pdt files
    filename = QtWidgets.QFileDialog.getOpenFileName(None, "Open File")[0]
    if filename != '':
        with open(filename,"r") as file:
            return (filename, file.read())
    pass 


def file_save(filename, fileText):
        if filename is '':
            filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', '', '*.*')[0]

        if filename != '':
            with open(filename,'w') as file:
                file.write(fileText)

        return filename


def file_save_as(fileText):
        filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File As...', '', '*.*')[0]

        if filename != '':
            with open(filename,'w') as file:
                file.write(fileText)

        return filename

# codebook operations
def new_codebook():
    # get directory location to store codebook
    # TODO: check if the folder is already a codebook
    dirname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Create or Select Codebook Folder', 
                'NewCodebook', options = QtWidgets.QFileDialog.ShowDirsOnly)
    if dirname != '':
        cb_name = dirname.split('/')[-1]
        with open(dirname + "/" + cb_name + ".cdb", 'w') as cb_file:
            cb_file.write(getDefaultCodebook(cb_name))
        return (dirname, cb_name)
    else:
        return None


def open_codebook(dirname = None):
    # get directory location to open an existing codebook\
    if dirname == False or dirname == None:
        dirname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Create or Select Codebook Folder', 
                    'NewCodebook', options = QtWidgets.QFileDialog.ShowDirsOnly)

    if dirname != '':
        #TODO: check that there's a valid .cdb file to indicate that the folder is actually a codebook
        cb_name = dirname.split('/')[-1]
        return (dirname, cb_name)
    else:
        return None


def getCodebookData(cb_dir):
    """Gets information from the .cdb file of the codebook given the .cdb file location"""

    if os.path.exists(cb_dir):
        with open(cb_dir, 'r') as cdb:
            return json.loads(cdb.read())
    else:
        return False


# entry operations
def save_new_entry():
    # create a new codebook entry (hypothetically inside a codebook)
    dirname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Codebook Folder', 
                options = QtWidgets.QFileDialog.ShowDirsOnly)
    # TODO: check that it's a codebook
    if dirname != '':
        return dirname
    else:
        return None


def new_description(dirname):
    with open(dirname + '/description.txt', 'w') as descrip:
        descrip.write("%s:\nA new codebook entry" % filename)
    pass


def save_entry(dirname):
    
    pass


def save_entry_as():

    pass


def copy_entry(entry_dir):
    """Downloads the entry at from_dir to a new user-selected location"""

    to_dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Entry Save Location',
                options = QtWidgets.QFileDialog.ShowDirsOnly)

    entry_name = os.path.split(entry_dir)[1]
    shutil.copytree(entry_dir, to_dir + '/' + entry_name)
    pass


# fileops with tags
# def file_open():
#     # get filename and show only .pdt files
#     filename = QtWidgets.QFileDialog.getOpenFileName(None, "Open File")[0]
#     if filename != '':
#         with open(filename,"r") as file:
#             return (filename, file.readline(), file.read())
#     pass 

def parse_description(fileloc, tagsOnly = False):
    try:
        with open(fileloc, 'r') as f:
            tagline = f.readline().strip('\n')
            text = f.read()

            if tagline[0:6] == '<tags>' and tagline[-7:] == '</tags>':
                tags = tagline[6:-7]

            if tagsOnly:
                return tags
            else:
                return (tags, text)
    except Exception:
        return None
        pass

def description_save(filename, tagString, fileText):
    if filename is '':
        filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', '','','*.*')[0]

    if tagString != '':
        tagString = "<tags>" + tagString + "</tags>"

    if filename != '':
        with open(filename,'w') as file:
            file.write(tagString +'\n' + fileText)

    return filename


# def file_save_as(tagString, fileText):
#         filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File As...', '', '*.*')[0]

#         if tagString != '':
#             tagString = "<tags>" + tagString + "</tags>"

#         if filename != '':
#             with open(filename,'w') as file:
#                 file.write(tagString + fileText)

#         return filename