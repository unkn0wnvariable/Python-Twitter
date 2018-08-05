# Import the modules we need
from __future__ import print_function
import os.path

# Import those of my functions which are being used here
from TwitterFunctions import myID,getFriendIDs,getFollowerIDs,getListingMeIDs,findListMatches,findFriendsNotFollowing,findFollowersNotFollowing,readBinaryFile,findListDifferences,getUserLists,findListID,getListMemberIDs,addListMembers,removeListMembers,writeBinaryFile

# Where should the script store data files?
dataFolder = './TwitterUpdateLists_Data/'

# What are the excluded ID files called?
deletedAccountIDsName = dataFolder + 'deleted_ids.txt'
protectedAccountIDsName = dataFolder + 'protected_ids.txt'

# What should the previous run data files be called?
friendIDsFileName = dataFolder + 'friend_ids.dat'
followerIDsFileName = dataFolder + 'follower_ids.dat'

# Set up the names, descriptions and modes for the lists to be created, if they don't already exist.
mutualListName = 'Mutual Following'
mutualListDescription = 'List of mutual followings.'
mutualListMode = 'private'

nmFollowersListName = 'Non-Mutual Followers'
nmFollowersListDescription = 'List of accounts that I\'m not following back.'
nmFollowersListMode = 'private'

nmFriendsListName = 'Non-Mutual Following'
nmFriendsListDescription = 'List of accounts that aren\'t following me back.'
nmFriendsListMode = 'private'

exclusionsListName = 'Exclusions'
exclusionsListDescription = 'List of accounts to be excluded from Non-Mutual Followers list.'
exclusionsListMode = 'private'

listingMeListName = 'Listing Me'
listingMeListDescription = 'List of accounts owning lists I have been added to.'
listingMeListMode = 'private'

newFriendsListName = 'New Following'
newFriendsListDescription = 'List of accounts that have I have recently started following.'
newFriendsListMode = 'private'

lostFriendsListName = 'Lost Following'
lostFriendsListDescription = 'List of accounts I have stopped following.'
lostFriendsListMode = 'private'

newFollowersListName = 'New Followers'
newFollowersListDescription = 'List of accounts that have recently started following me.'
newFollowersListMode = 'private'

lostFollowersListName = 'Lost Followers'
lostFollowersListDescription = 'List of accounts that have stopped following me.'
lostFollowersListMode = 'private'


# Read in accounts to be excluded from the exculsion files, if they exist.

if os.path.exists(deletedAccountIDsName):
	deletedAccountIDsFile = open(deletedAccountIDsName, 'r')
	deletedAccountIDs = deletedAccountIDsFile.readlines()
	deletedAccountIDsFile.close()
else:
	deletedAccountIDs = ''

if os.path.exists(protectedAccountIDsName):
	protectedAccountIDsFile = open(protectedAccountIDsName, 'r')
	protectedAccountIDs = protectedAccountIDsFile.readlines()
	deletedAccountIDsFile.close()
else:
	protectedAccountIDs = ''

excludedIDs = deletedAccountIDs + protectedAccountIDs


# Lets start doing some work

print('\nRetriving User IDs...\n')

rawFriendIDs = getFriendIDs(myID)
rawFollowerIDs = getFollowerIDs(myID)
rawListingMeIDs = getListingMeIDs(myID)

friendIDs = []
followerIDs = []
listingMeIDs = []

for eachID in rawFriendIDs:
	if eachID not in excludedIDs:
		friendIDs.append(eachID)

for eachID in rawFollowerIDs:
	if eachID not in excludedIDs:
		followerIDs.append(eachID)

for eachID in rawListingMeIDs:
	if eachID not in excludedIDs:
		listingMeIDs.append(eachID)

mutualIDs = findListMatches(friendIDs,followerIDs)
nmFriendsIDs = findFriendsNotFollowing(friendIDs,followerIDs)
nmFollowersIDs = findFollowersNotFollowing(friendIDs,followerIDs)

print('Followers:                 ' + str(len(followerIDs)))
print('Following:                 ' + str(len(friendIDs)))
print('Mutual:                    ' + str(len(mutualIDs)))
print('Non-mutual Followers:      ' + str(len(nmFollowersIDs)))
print('Non-mutual Following:      ' + str(len(nmFriendsIDs)))
print('Listing Me:                ' + str(len(listingMeIDs)))
print('Excluded IDs:              ' + str(len(excludedIDs)))

print('\nChecking against last run...\n')

rawPreviousFriendIDs = readBinaryFile(friendIDsFileName)
rawPreviousFollowerIDs = readBinaryFile(followerIDsFileName)

previousFriendIDs = []
previousFollowerIDs = []

for eachID in rawPreviousFriendIDs:
	if eachID not in excludedIDs:
		previousFriendIDs.append(eachID)

for eachID in rawPreviousFollowerIDs:
	if eachID not in excludedIDs:
		previousFollowerIDs.append(eachID)

if len(previousFriendIDs) > 0:
    gainedFriendIDs = findListDifferences(friendIDs,previousFriendIDs)
    lostFriendIDs = findListDifferences(previousFriendIDs,friendIDs)
    print('Gained Following:          ' + str(len(gainedFriendIDs)))
    print('Lost Following:            ' + str(len(lostFriendIDs)))
else:
    gainedFriendIDs = []
    lostFriendIDs = []
    print('No previous following ID data.')

if len(previousFollowerIDs) > 0:
    gainedFollowerIDs = findListDifferences(followerIDs,previousFollowerIDs)
    lostFollowerIDs = findListDifferences(previousFollowerIDs,followerIDs)
    print('Gained Followers:          ' + str(len(gainedFollowerIDs)))
    print('Lost Followers:            ' + str(len(lostFollowerIDs)))
else:
    gainedFollowerIDs = []
    lostFollowerIDs = []
    print('No previous follower ID data')

print('\nRetriving list IDs...\n')

myLists = getUserLists(myID)

mutualListID = findListID(myID,myLists,mutualListName,mutualListDescription,mutualListMode)
nmFollowersListID = findListID(myID,myLists,nmFollowersListName,nmFollowersListDescription,nmFollowersListMode)
nmFriendsListID = findListID(myID,myLists,nmFriendsListName,nmFriendsListDescription,nmFriendsListMode)
exclusionsListID = findListID(myID,myLists,exclusionsListName,exclusionsListDescription,exclusionsListMode)
listingMeListID = findListID(myID,myLists,listingMeListName,listingMeListDescription,listingMeListMode)

newFriendsListID = findListID(myID,myLists,newFriendsListName,newFriendsListDescription,newFriendsListMode)
lostFriendsListID = findListID(myID,myLists,lostFriendsListName,lostFriendsListDescription,lostFriendsListMode)
newFollowersListID = findListID(myID,myLists,newFollowersListName,newFollowersListDescription,newFollowersListMode)
lostFollowersListID = findListID(myID,myLists,lostFollowersListName,lostFollowersListDescription,lostFollowersListMode)

print('List ID for ' + mutualListName + ' is ' + str(mutualListID))
print('List ID for ' + nmFollowersListName + ' is ' + str(nmFollowersListID))
print('List ID for ' + nmFriendsListName + ' is ' + str(nmFriendsListID))
print('List ID for ' + exclusionsListName + ' is ' + str(exclusionsListID))
print('List ID for ' + listingMeListName + ' is ' + str(listingMeListID))
print('List ID for ' + newFriendsListName + ' is ' + str(newFriendsListID))
print('List ID for ' + lostFriendsListName + ' is ' + str(lostFriendsListID))
print('List ID for ' + newFollowersListName + ' is ' + str(newFollowersListID))
print('List ID for ' + lostFollowersListName + ' is ' + str(lostFollowersListID))

print('\nRetriving List Members...\n')

mutualListMemberIDs = getListMemberIDs(mutualListID,myID)
nmFollowersListMemberIDs = getListMemberIDs(nmFollowersListID,myID)
nmFriendsListMemberIDs = getListMemberIDs(nmFriendsListID,myID)
exclusionsListMemberIDs = getListMemberIDs(exclusionsListID,myID)
listingMeListMemberIDs = getListMemberIDs(listingMeListID,myID)

print('Mutuals list:              ' + str(len(mutualListMemberIDs)))
print('Non-mutual Followers list: ' + str(len(nmFollowersListMemberIDs)))
print('Non-mutual Following list: ' + str(len(nmFriendsListMemberIDs)))
print('Exclusions list:           ' + str(len(exclusionsListMemberIDs)))
print('Listing Me list:           ' + str(len(listingMeListMemberIDs)))

print('\nCaculating list changes...\n')

nmFollowersIDsFiltered = findListDifferences(nmFollowersIDs,exclusionsListMemberIDs)
nmFriendsIDsFiltered = findListDifferences(nmFriendsIDs,listingMeListMemberIDs)

mutualToAdd = findListDifferences(mutualIDs,mutualListMemberIDs)
nmFollowersToAdd = findListDifferences(nmFollowersIDsFiltered,nmFollowersListMemberIDs)
nmFriendsToAdd = findListDifferences(nmFriendsIDs,nmFriendsListMemberIDs)
listingMeToAdd = findListDifferences(listingMeIDs,listingMeListMemberIDs)

mutualToRemove = findListDifferences(mutualListMemberIDs,mutualIDs)
nmFollowersToRemove = findListDifferences(nmFollowersListMemberIDs,nmFollowersIDsFiltered)
nmFriendsToRemove = findListDifferences(nmFriendsListMemberIDs,nmFriendsIDs)
listingMeToRemove = findListDifferences(listingMeListMemberIDs,listingMeIDs)

changesExist = False

if len(mutualToAdd) > 0:
	print('User ID(s) ' + str(mutualToAdd) + ' will be added to Mutual list.')
	changesExist = True
if len(nmFollowersToAdd) > 0:
	print('User ID(s) ' + str(nmFollowersToAdd) + ' will be added to Non-Mutual Followers list.')
	changesExist = True
if len(nmFriendsToAdd) > 0:
	print('User ID(s) ' + str(nmFriendsToAdd) + ' will be added to Non-Mutual Following list.')
	changesExist = True
if len(listingMeToAdd) > 0:
	print('User ID(s) ' + str(listingMeToAdd) + ' will be added to Listing Me list.')
	changesExist = True

if len(mutualToRemove) > 0:
	print('User ID(s) ' + str(mutualToRemove) + ' will be removed from Mutual list.')
	changesExist = True
if len(nmFollowersToRemove) > 0:
	print('User ID(s) ' + str(nmFollowersToRemove) + ' will be removed from Non-Mutual Followers list.')
	changesExist = True
if len(nmFriendsToRemove) > 0:
	print('User ID(s) ' + str(nmFriendsToRemove) + ' will be removed from Non-Mutual Following list.')
	changesExist = True
if len(listingMeToRemove) > 0:
	print('User ID(s) ' + str(listingMeToRemove) + ' will be removed from Listing Me list.')
	changesExist = True

if len(gainedFriendIDs) > 0:
	print('User ID(s) ' + str(gainedFriendIDs) + ' will be added to New Following list.')
	changesExist = True
if len(lostFriendIDs) > 0:
	print('User ID(s) ' + str(lostFriendIDs) + ' will be added to Lost Following list.')
	changesExist = True
if len(gainedFollowerIDs) > 0:
	print('User ID(s) ' + str(gainedFollowerIDs) + ' will be added to New Followers list.')
	changesExist = True
if len(lostFollowerIDs) > 0:
	print('User ID(s) ' + str(lostFollowerIDs) + ' will be added to Lost Followers list.')
	changesExist = True

if changesExist:
	makeChanges = ''
	while not makeChanges == 'y' and not makeChanges == 'n':
		makeChanges = input('Do you want to make these changes? (y/n) ')
else:
	print('\nNo changes have been found.')
	makeChanges = 'n'

if makeChanges == 'y':
	print('\nMaking list changes...\n')
	addListMembers(mutualToAdd,mutualListID,myID,25)
	addListMembers(nmFollowersToAdd,nmFollowersListID,myID,25)
	addListMembers(nmFriendsToAdd,nmFriendsListID,myID,25)
	addListMembers(listingMeToAdd,listingMeListID,myID,25)
	removeListMembers(mutualToRemove,mutualListID,myID,25)
	removeListMembers(nmFollowersToRemove,nmFollowersListID,myID,25)
	removeListMembers(nmFriendsToRemove,nmFriendsListID,myID,25)
	removeListMembers(listingMeToRemove,listingMeListID,myID,25)
	addListMembers(gainedFriendIDs,newFriendsListID,myID,25)
	addListMembers(lostFriendIDs,lostFriendsListID,myID,25)
	addListMembers(gainedFollowerIDs,newFollowersListID,myID,25)
	addListMembers(lostFollowerIDs,lostFollowersListID,myID,25)
	writeBinaryFile(friendIDsFileName,friendIDs)
	writeBinaryFile(followerIDsFileName,followerIDs)
else:
	print('\nNo changes have been made.')
