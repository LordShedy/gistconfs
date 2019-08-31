#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, sys, datetime

from jlav import loadAndValidateJSONfile

from time import gmtime, strftime

from var_dump import var_dump
"""
add some option to have monokai color scheme as well
https://raw.githubusercontent.com/sickill/vim-monokai/master/colors/monokai.vim
there needs to be ~/.vim/colors/<thecolor>.vim
"""

def readFile(filename: str) -> str:
    try:
        with open(filename, 'r') as f:
            return f.read()
    except:
        printlog("There was error while reading the file.")
        quit()

def writeIntoFile(filename: str, content: str) -> str:
    try:
        with open(filename, 'r+') as f:
            data = f.read()
            f.seek(0)
            f.write(content)
            f.truncate()
            return 1
    except:
        printlog("There was error while reading the file.")
        return 0

def getRawURL(inputObject: dict, fileName: str, gistID: str) -> str:
    for i in inputObject:
      if i['id'] == gistID:
        return i['files'][fileName]['raw_url']
    return printlog("There was some error while getting URL, possible issue with API.")


"""
This function serves for formalized logging
"""
def printlog(logText: str, dateTimeFormat = "%d-%m-%Y %H:%M:%S") -> str:
    return print("Automated Configs [" + strftime(dateTimeFormat, gmtime()) + "] " + logText)

def main():
    try:
        cred = loadAndValidateJSONfile("automated_configs_credentials.json", "automated_configs_credentials.schema")
        r = requests.get("https://api.github.com/users/LordShedy/gists", auth=(cred['username'],cred['token'])).json()
    except:
        printlog("There was some error while getting URL, network might be down or there might be some issues with the GitHub Gist API.")
        quit()
    else:
        for i in cred['files']:
            gistID = cred['files'][i]['id']
            raw_url = getRawURL(r, i, gistID)
            origin = requests.get(raw_url).text
            path = cred['files'][i]['localPath']
            local = readFile(path)
            if origin != local:
                var_dump(writeIntoFile(path, origin))
                return printlog("There has been a newer version of this config, the file has been updated.")
            else:
                return printlog("This config file is the same as at the origin, nothing has been changed.")
        return printlog("There are no configs to be synchronized, nothing to do.")

if __name__ == "__main__":
    main()
