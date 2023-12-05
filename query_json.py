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
    
def getQuestions():
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
    questions_list = []
    for post in post_list:
        # print("type(@PostTypeId) --> ", type(post['@PostTypeId']))
        if checkKey(d=post, key='@PostTypeId') and post['@PostTypeId'] == str(1):
            questions_list_list.append(post)
    
    print(len(questions_list))
                
    return questions_list

def getAnswers():
    raise NotImplementedError
    
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
        if checkKey(d=post, key='@Tags') and checkKey(d=post, key='@OwnerUserId')  and checkKey(d=post, key='@Score') and checkKey(d=post, key='@ViewCount'):
            if post['@Tags'] == tag: 
                tagged_PostID_list.append({'@Id':post['@Id'], '@OwnerUserId':post['@OwnerUserId'], '@Score':post['@Score'], '@ViewCount':post['@ViewCount']})
                
    print("machine learning posts found --> ", len(tagged_PostID_list))
    f.close()
    return tagged_PostID_list

# posttype --> 1:question, 2:answers
# parentID (for answer) 
def queryAnswers(tagged_PostList=None):
    f = open('json/Posts.json') 
    #input1 list of tagged post dictionaries
    #input2 list of posts again
    
    # Query PosttypeID --> 2 (answer), if posttypeID==2 get parentID 
    # to find the most downvoted:
    # 1) find posts w/ PostTypeID == 2 then take parentID and compare it to the list of postID dictionaries
    # 2)to find votes --> take the new postID list and find the VoteTypeID and count it
    # 3) then we need to the list postIDs according to score and or the amount of downvotes?

 
    # returns JSON object as a dictionary
    data = json.load(f)
    data_ = data['posts'] # returns dict
    answer_list = data_['row'] # returns list
    
    print(len(answer_list))
    print(len(tagged_PostList))
    tagged_answer_list = []
    # assert False
    for answer in answer_list:
        if checkKey(d=answer, key='@PostTypeId') and answer['@PostTypeId'] == str(2):
            print("answers?")
    
    
def queryVotes():
    raise NotImplementedError



tagged_Posts = queryQuestions(tag="<machine-learning>")
queryAnswers(tagged_PostList=tagged_Posts)
