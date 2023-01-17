from keys_ig import *
from InstagramAPI import InstagramAPI
import sys
from datetime import datetime
import time




def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def getTotalFollowings(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def nonFollowers(followers, followings):
    nonFollowers = {}
    dictFollowers = {}
    for follower in followers:
        dictFollowers[follower['username']] = follower['pk']

    for followedUser in followings:
        if followedUser['username'] not in dictFollowers:
            nonFollowers[followedUser['username']] = followedUser['pk']

    newDict = dict()
    for key, value in nonFollowers.items():
        found=False
        whitelist=open("whitelist.txt","r")
        while True:
            white=whitelist.readline()
            if not white:
                break
            if white==key+"\n":
                found=True
        whitelist.close()
        if found==False:
            newDict[key]=value
    
    return newDict

def unFollow(number : int):
    api = InstagramAPI(USERNAME, PASS)
    api.login()
    user_id = api.username_id
    followers = getTotalFollowers(api, user_id)
    following = getTotalFollowings(api, user_id)
    nonFollow = nonFollowers(followers, following)
    totalNonFollowers = len(nonFollow)
    print('Number of followers:', len(followers))
    print('Number of followings:', len(following))
    print('Number of nonFollowers:', len(nonFollow))

    for i in range(number):
        if i >= totalNonFollowers:
            break
        user = list(nonFollow.keys())[len(nonFollow)-1]
        print('Number of nonFollowers:', len(nonFollow))
        print('Just unfollowed:', user)
        api.unfollow(nonFollow[user])
        nonFollow.pop(user)
        time.sleep(20)
        


f = open("test.out", 'a')
sys.stdout = f


if __name__ == "__main__":
    unFollow(20)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

f.close()
