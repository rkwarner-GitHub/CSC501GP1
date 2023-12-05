# a method to find the most upvoted/downvoted users

import json
import os
path = "json/"
files = [f for f in os.listdir(path)]
print("files \n",files)
 


def checkKey(d=None, key=None):
     
    if key in d:
       return True
    else:
        return False
    
def queryQuestions(tag=None):
    # Opening JSON file
    f = open('json/Posts.json') 
 
    # returns JSON object as a dictionary
    data = json.load(f)
    data_ = data['posts'] # returns dict
    post_list = data_['row'] # returns list
    # keys I want for Q: '@ParentId' , '@Id', '@Score', '@OwnerUserId', '@ViewCount'
    # keys I want for A: '@ParentId' , '@Id', '@Score', '@OwnerUserId''
    print(post_list[0].keys()) # dict_keys(['@Id', '@PostTypeId', '@CreationDate', '@Score', '@ViewCount', '@Body', '@OwnerUserId', '@LastActivityDate', '@Title', '@Tags', '@AnswerCount', '@CommentCount', '@ClosedDate', '@ContentLicense'])
    # assert False
    tagged_PostID_list = []
    for post in post_list:
        # print("type(@PostTypeId) --> ", type(post['@PostTypeId']))
        if checkKey(d=post, key=tag) and checkKey(d=post, key='@OwnerUserId')  and checkKey(d=post, key='@Score') and checkKey(d=post, key='@ViewCount'):
            if post['@Tags'] == "<machine-learning>": 
                tagged_PostID_list.append({'@Id':post['@Id'], '@OwnerUserId':post['@OwnerUserId'], '@Score':post['@Score'], '@ViewCount':post['@ViewCount']})
                
    print("machine learning posts found --> ", len(tagged_PostID_list))
    # print(tagged_PostID_list)
    # assert False

    # Closing file
    f.close()
    return tagged_PostID_list

# posttype --> 1:question, 2:answers
# parentID (for answer) 
def queryAnswers(postID=None):
    f = open('json/Comments.json') 
    
    
    # Query PosttypeID --> 2 (answer), if posttypeID==2 get parentID 
 
    # returns JSON object as a dictionary
    data = json.load(f)
    data_ = data['comments'] # returns dict
    comment_list = data_['row'] # returns list
    
    tagged_comment_list = []
    for comment in comment_list:
        print(comment.keys())
        assert False
        if checkKey(d=post, key=tag):
            if post['@Tags'] == "<machine-learning>": 
                tagged_comment_list.append(post['@Id'])
                
    print("machine learning posts found --> ", len(tagged_PostID_list))
    
    
def queryVotes():
    raise NotImplementedError



tagged_Posts = queryQuestions(tag='@Tags')
# queryComments()