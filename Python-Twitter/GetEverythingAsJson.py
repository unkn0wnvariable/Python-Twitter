from __future__ import print_function
from TwitterFunctions import *
import json
import os

filePath = './json/'
listsFilesPath = filePath + 'my_lists/'

read = 'r'
write = 'w'
append = 'a'

meOutputFile = filePath + 'verify_credentials.json'
followerIDsOutputFile = filePath + 'get_followers_ids.json'
friendIDsOutputFile = filePath + 'get_friends_ids.json'
followersLookupOutputFile = filePath + 'followers_lookup_user.json'
friendsLookupOutputFile = filePath + 'friends_lookup_user.json'
listMembershipsFileName = filePath + 'get_list_memberships.json'
friendsListFileName = filePath + 'get_friends_list.json'
followersListFileName = filePath + 'get_followers_list.json'

if not (os.path.exists(filePath)):
    os.mkdir(filePath)

if not (os.path.exists(listsFilesPath)):
    os.mkdir(listsFilesPath)

print('Getting my details and saving to file.')
with open(meOutputFile, write) as meFile:
    json.dump(me, meFile, indent=4)

print('Getting friend IDs and saving to file.')
friendIDs = getFriendIDs(myID)
with open(friendIDsOutputFile, write) as friendIDsFile:
    json.dump(friendIDs, friendIDsFile, indent=4)

print('Getting details for ' + str(len(friendIDs)) + ' friends and saving to file.')
friendDetails = userLookup(friendIDs,100)
with open(friendsLookupOutputFile, write) as friendsLookupFile:
    json.dump(friendDetails, friendsLookupFile, indent=4)

print('Getting follower IDs and saving to file.')
followerIDs = getFollowerIDs(myID)
with open(followerIDsOutputFile, write) as followerIDsFile:
    json.dump(followerIDs, followerIDsFile, indent=4)

print('Getting details for ' + str(len(followerIDs)) + ' followers and saving to file.')
followerDetails = userLookup(followerIDs,100)
with open(followersLookupOutputFile, write) as followersLookupFile:
    json.dump(followerDetails, followersLookupFile, indent=4)

print('Getting list memberships and saving to file.')
listMemberships = getListMemberships(myID)
with open(listMembershipsFileName, write) as listMembershipsFile:
    json.dump(listMemberships, listMembershipsFile, indent=4)

print('Getting followers list and saving to file.')
followersList = getFollowersList(myID,200)
with open(followersListFileName, write) as followersListFile:
    json.dump(followersList, followersListFile, indent=4)

print('Getting friends list and saving to file.')
friendsList = getFriendsList(myID,200)
with open(friendsListFileName, write) as friendsListFile:
    json.dump(friendsList, friendsListFile, indent=4)

print('Getting my lists and saving to files.')
pageCursor = -1
while(pageCursor):
    pageResults = twitter.show_owned_lists(user_id=myID,cursor=pageCursor)
    for eachList in pageResults['lists']:
        print('Getting list members for ' + eachList['name'] + '.')
        listMembersOutputFile = (listsFilesPath + eachList['name'].replace(' ','_').lower() + '_members.json')
        listMemberIDs = getListMemberIDs(eachList['id'],myID)
        listMemberDetails = userLookup(listMemberIDs,100)
        with open(listMembersOutputFile, write) as listMembersFile:
            json.dump(listMemberDetails, listMembersFile, indent=4)
    pageCursor = pageResults['next_cursor']
