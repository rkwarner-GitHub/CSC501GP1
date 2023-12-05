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

    questions_list = []
    for post in post_list:
        if checkKey(d=post, key='@PostTypeId') and post['@PostTypeId'] == str(1):
            questions_list.append(post)
    
    print(len(questions_list))
                
    return questions_list

def getAnswers():
    # Opening JSON file
    f = open('json/Posts.json') 
 
    # returns JSON object as a dictionary
    data = json.load(f)
    data_ = data['posts'] # returns dict
    post_list = data_['row'] # returns list

    answers_list = []
    for post in post_list:
        if checkKey(d=post, key='@PostTypeId') and post['@PostTypeId'] == str(2):
            answers_list.append(post)
    
    print(len(answers_list))         
    return answers_list
    
def queryQuestions(questions_list=None, tag=None):
    # Opening JSON file
    f = open('json/Posts.json') 

    tagged_PostID_list = []
    for post in questions_list:
        if checkKey(d=post, key='@Tags') and checkKey(d=post, key='@OwnerUserId')  and checkKey(d=post, key='@Score') and checkKey(d=post, key='@ViewCount'):
            if post['@Tags'] == tag: 
                tagged_PostID_list.append({'@Id':post['@Id'], '@OwnerUserId':post['@OwnerUserId'], '@Score':post['@Score'], '@ViewCount':post['@ViewCount']})
                
    print("machine learning posts found --> ", len(tagged_PostID_list))
    f.close()
    return tagged_PostID_list

# posttype --> 1:question, 2:answers
# parentID (for answer) 
def queryAnswers(answers_list=None, tagged_PostList=None):
    f = open('json/Posts.json') 

    
    # Query PosttypeID --> 2 (answer), if posttypeID==2 get parentID 
    # to find the most downvoted:
    # 1) find posts w/ PostTypeID == 2 then take parentID and compare it to the list of postID dictionaries
    # 2)to find votes --> take the new postID list and find the VoteTypeID and count it
    # 3) then we need to the list postIDs according to score and or the amount of downvotes?
    
    tagged_answer_list = []
    for answer in answers_list:
        for post in tagged_PostList:
            if answer['@ParentId'] == post["@Id"]:
                tagged_answer_list.append(answer)
    

    return tagged_answer_list
    
    
def queryVotes(tagged_list=None):
    f = open('json/Votes.json') 
 
    # returns JSON object as a dictionary
    data = json.load(f)
    print(data.keys())
    data_ = data['votes'] # returns dict
    vote_list = data_['row'] # returns list
    
    print(len(vote_list))
    
    tagged_vote_list = []
    for vote in vote_list:
        # print(vote.keys())
        for post in tagged_list:
            if vote['@Id'] == post["@Id"]:
                tagged_vote_list.append(vote)
                # can we make a dictionary that quickly shows the votetype based postID
    
    print(len(tagged_vote_list))
    print(tagged_vote_list[0])
    assert False


questions = getQuestions()
answers = getAnswers()

tagged_Questions = queryQuestions(questions_list=questions, tag="<machine-learning>")
tagged_Answers = queryAnswers(answers_list=answers, tagged_PostList=tagged_Questions)

queryVotes(tagged_list=tagged_Answers)


