from __future__ import print_function
from TwitterFunctions import *
import os


# Output file details

filePath = './csv/'
fileName = 'friends_list.csv'

write = 'w'
append = 'a'


# Main program

print('Getting friends list and saving to file...')
friendsList = getFriendsList(myID,200)

if not (os.path.exists(filePath)):
    os.mkdir(filePath)

outputFilePath = filePath + fileName

with open(outputFilePath, write) as outputFile:
    outputFile.write('id_str,screen_name,name\n')

for eachItem in friendsList:
    with open(outputFilePath, append) as outputFile:
        outputFile.write(str(eachItem['id_str'] + ',' + eachItem['screen_name'] + ',"' + eachItem['name'] + '"\n'))
