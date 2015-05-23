import json
import os
import time



def getSettings(mainfile_dir):
    try:
        with open(mainfile_dir + '/settings.cbs','r') as f:
            return json.load(f)
    except FileNotFoundError:
        restoreDefaultSettings(mainfile_dir)
        with open(mainfile_dir + '/settings.cbs', 'r') as f:
            return json.load(f)
    except Exception as e:
        print("Error getting settings: " + str(e))


def getDefaultSettings():
    with open('./codebook_fileops/default_settings.cbs') as defaults:
        return json.load(defaults)


def save_settings(mainfile_dir, settingsDict):
    with open(mainfile_dir + '/settings.cbs','w') as settingsfile:
        settingsfile.write(json.dumps(settingsDict, indent="    "))


def restoreDefaultSettings(mainfile_dir):
    save_settings(mainfile_dir, getDefaultSettings())
    pass


def getDefaultCodebook(cb_name):
    # entries will be of style {'entry_dir':'tags', ... }
    codebook_name = cb_name
    codebook_entries = {}
    cb = {"codebook_name":codebook_name, "creation_date":time.strftime('%a %B %d, %Y')}
    return json.dumps(cb, indent = "    ")
