#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, sys, datetime, time, random, zlib

from jlav import loadAndValidateJSONfile

from time import localtime, strftime

appName = "Gistconfs"
instanceHash = zlib.crc32(bytes(random.randint(1000000,999999999)))

def readFile(filename: str) -> str:
    try:
        with open(filename, 'r') as f:
            return f.read()
    except:
        printlog(appName, instanceHash, "There was error while reading ({}) file.".format(filename))
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
        printlog(appName, instanceHash, "There was error while reading the file.")
        return 0

def getRawURL(inputObject: dict, fileName: str, gistID: str) -> str:
    for i in inputObject:
      if i['id'] == gistID:
        return i['files'][fileName]['raw_url']
    return printlog(appName, instanceHash, "There was some error while getting URL, possible issue with API.")


"""
This function serves for formalized logging
"""
def printlog(appName: str, instanceHash: str,  logText: str, dateTimeFormat = "%d-%m-%Y %H:%M:%S %Z %z") -> str:
    dateTime = strftime(dateTimeFormat, localtime())
    epochTime = time.time()
    return print("[{} {}]; [{}]; ({}); {}".format(dateTime, epochTime, instanceHash, appName, logText ))

def main():
    try:
        cred = loadAndValidateJSONfile("automated_configs_credentials.json", "automated_configs_credentials.schema")
        r = requests.get("https://api.github.com/users/LordShedy/gists", auth=(cred['username'],cred['token'])).json()
    except:
        printlog(appName, instanceHash, "There was some error while getting URL, network might be down or there might be some issues with the GitHub Gist API.")
        quit()
    else:
        fv = 0
        for i in cred['files']:
            fv = 1
            gistID = cred['files'][i]['id']
            raw_url = getRawURL(r, i, gistID)
            origin = requests.get(raw_url).text
            path = cred['files'][i]['localPath']
            local = readFile(path)
            if origin != local:
                writeIntoFile(path, origin)
                printlog(appName, instanceHash, "There has been a newer version of ({}) config, the file has been updated.".format(path))
            else:
                printlog(appName, instanceHash, "File ({}) is the same as at the origin, nothing has been changed.".format(path))
        if fv == 0:
            return printlog(appName, instanceHash, "No configs were newly synchronized, nothing else to do.")
        return printlog(appName, instanceHash, "All newer configs were synchronized, nothing else to do.")

if __name__ == "__main__":
    main()
