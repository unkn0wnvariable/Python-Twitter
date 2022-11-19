from __future__ import print_function
from twython import Twython
import pickle
import time

from TwitterAPIDetails import apiKey,apiSecret,accessToken,accessTokenSecret

# Connect to Twitter via Twython library
twitter = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

# Get my details and extract screen_name and id
me = twitter.verify_credentials(include_entities=False,skip_status=True)
myScreenName = me['screen_name']
myID = me['id']


# Functions to retrive data from Twitter

def getUsername(userID):
    userDetails = twitter.show_user(user_id=userID)
    return userDetails['screen_name']

def getFollowerIDs(userID):
    allResults = []
    pageCursor = -1
    while(pageCursor):
        pageResults = twitter.get_followers_ids(user_id=userID,cursor=pageCursor)
        for eachItem in pageResults['ids']:
            allResults.append(eachItem)
        pageCursor = pageResults['next_cursor']
    return allResults

def getFriendIDs(userID):
    allResults = []
    pageCursor = -1
    while(pageCursor):
        pageResults = twitter.get_friends_ids(user_id=userID,cursor=pageCursor)
        for eachItem in pageResults['ids']:
            allResults.append(eachItem)
        pageCursor = pageResults['next_cursor']
    return allResults

def getFollowersList(userID,pageCount):
    allResults = []
    pageCursor = -1
    while(pageCursor):
        pageResults = twitter.get_followers_list(user_id=userID,cursor=pageCursor,count=pageCount)
        for eachItem in pageResults['users']:
            allResults.append(eachItem)
        pageCursor = pageResults['next_cursor']
    return allResults

def getFriendsList(userID,pageCount):
    allResults = []
    pageCursor = -1
    while(pageCursor):
        pageResults = twitter.get_friends_list(user_id=userID,cursor=pageCursor,count=pageCount)
        for eachItem in pageResults['users']:
            allResults.append(eachItem)
        pageCursor = pageResults['next_cursor']
    return allResults

def getUserLists(userID):
    allResults = {}
    pageCursor = -1
    while(pageCursor):
        pageResults = twitter.show_owned_lists(user_id=userID,cursor=pageCursor)
        for eachItem in pageResults['lists']:
            allResults[eachItem['name']] = eachItem['id']
        pageCursor = pageResults['next_cursor']
    return allResults

def getListMemberIDs(listID,userID):
    allResults = []
    pageCursor = -1
    while(pageCursor):
        pageResults = twitter.get_list_members(list_id=listID,owner_id=userID,cursor=pageCursor)
        for eachItem in pageResults['users']:
            allResults.append(eachItem['id'])
        pageCursor = pageResults['next_cursor']
    return allResults

def getListMemberships(userID):
    allResults = []
    pageCursor = -1
    while(pageCursor):
        pageResults = twitter.get_list_memberships(user_id=myID,cursor=pageCursor)
        for eachItem in pageResults['lists']:
            allResults.append(eachItem)
        pageCursor = pageResults['next_cursor']
    return allResults

def getListingMeIDs(userID):
    allResults = []
    listMemberships = getListMemberships(userID)
    for twitterList in listMemberships:
        userID = twitterList['user']['id']
        if not userID in allResults:
            allResults.append(userID)
    return allResults

def userLookup(userIDs,count):
    userDetails = []
    for y in range(0, len(userIDs), count):
        batchUserIDs = userIDs[y:y+count]
        userDetails.append(twitter.lookup_user(user_id=batchUserIDs))
    return userDetails

def getBlockedIDs():
    allResults = []
    pageCursor = -1
    while(pageCursor):
        pageResults = twitter.list_block_ids()
        for eachItem in pageResults['ids']:
            allResults.append(eachItem)
        pageCursor = pageResults['next_cursor']
    return allResults


# functions to find things within retrived data

def findFriendsNotFollowing(friends,followers):
    userIDs = []
    for friendID in friends:
        if not friendID in followers:
            userIDs.append(friendID)
    return userIDs

def findFollowersNotFollowing(friends,followers):
    userIDs = []
    for followerID in followers:
        if not followerID in friends:
            userIDs.append(followerID)
    return userIDs   

def findListID(userID,userLists,listName,listDescription,listMode):
    if listName in userLists.keys():
        listID = userLists[listName]
    else:
        listID = createList(listName,listDescription,listMode)['id']
    return listID

def findListMatches(listA,listB):
    # Creates a list of items in listA which are also in listB
    listMatches = []
    for listItem in listA:
        if listItem in listB:
            listMatches.append(listItem)
    return listMatches

def findListDifferences(listA,listB):
    # Creates a list of items in listA which aren't in listB
    listDifferences = []
    for listItem in listA:
        if not listItem in listB:
            listDifferences.append(listItem)
    return listDifferences

def combineLists(listA,listB):
    # Combines two lists into one without any duplicates
    combinedList = []
    for listItem in findListDifferences(listA,combinedList):
        combinedList.append(listItem)
    for listItem in findListDifferences(listB,combinedList):
        combinedList.append(listItem)
    return combinedList


# Functions to write data back to Twitter

def createList(listName,listDescription,listMode):
    print('Creating list ' + listName + ' with mode ' + listMode + ' and description ' + listDescription)
    newList = twitter.create_list(name=listName,mode=listMode,description=listDescription)
    return newList

def addListMembers(allMemberIDs,listID,userID,count):
    for each in range(0, len(allMemberIDs), count):
        batchMemberIDs = allMemberIDs[each:each+count]
        print('Adding ID(s) ' + str(batchMemberIDs) + ' to list with ID ' + str(listID))
        twitter.create_list_members(list_id=listID,user_id=batchMemberIDs,owner_id=userID)

def removeListMembers(allMemberIDs,listID,userID,count):
    for each in range(0, len(allMemberIDs), count):
        batchMemberIDs = allMemberIDs[each:each+count]
        print('Removing ID(s) ' + str(batchMemberIDs) + ' from list with ID ' + str(listID))
        twitter.delete_list_members(list_id=listID,user_id=batchMemberIDs,owner_id=userID)

def removeBlock(userID):
	twitter.destroy_block(user_id=userID)


# Functions to read and write files

def readFile(fileName):
    try:
        with open(fileName, 'r') as file:
            fileData = file.read().splitlines()
    except:
        fileData = []
    return fileData

def writeFile(fileName,fileData):
    with open(fileName, 'w') as file:
        for eachLine in file:
            file.write(eachLine)

def readBinaryFile(fileName):
    try:
        with open(fileName, 'rb') as file:
            fileData = pickle.load(file)
    except:
        fileData = []
    return fileData


def writeBinaryFile(fileName,fileData):
    with open(fileName, 'wb') as file:
        pickle.dump(fileData, file)
