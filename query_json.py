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
    
    tagged_vote_list = []
    for vote in vote_list:
        # print(vote.keys())
        for post in tagged_list:
            if vote['@PostId'] == post["@Id"]:
                tagged_vote_list.append({'@Id':vote['@PostId'], '@VoteTypeId': vote['@VoteTypeId']})
    
    return tagged_vote_list


def voteAnalysis(tagged_votes=None, tagged_posts=None):
    postID_vote_dict = {}
    for post in tagged_posts:
        for vote in tagged_votes:
            if vote['@Id'] == post['@Id']:
                # print(post['@Id'],vote['@Id'],vote['@VoteTypeId'])
                
                if post['@Id'] not in postID_vote_dict:
                    tmp = {post['@Id']:{"1":0, "2":0, "3":0, "12":0, "15":0}}
                    postID_vote_dict.update(tmp)
                    # vote ID 1, 2, 3, 12 and 15
                    # print(tmp)
                    # assert False
                else:
                    if vote['@VoteTypeId'] == str(1):
                        postID_vote_dict[post['@Id']]["1"] += 1
                    
                    elif vote['@VoteTypeId'] == str(2):
                        postID_vote_dict[post['@Id']]["2"] += 1
                    
                    elif vote['@VoteTypeId'] == str(3):
                        postID_vote_dict[post['@Id']]["3"] += 1
                    
                    elif vote['@VoteTypeId'] == str(12):
                        postID_vote_dict[post['@Id']]["12"] += 1
                        
                    elif vote['@VoteTypeId'] == str(15):
                        postID_vote_dict[post['@Id']]["15"] += 1

                    # postID_vote_dict[post['@Id']] += 1
    # print(postID_vote_dict['120324'])
    return postID_vote_dict   




questions = getQuestions()
answers = getAnswers()

tagged_Questions = queryQuestions(questions_list=questions, tag="<machine-learning>")
print("len(tagged questions: ) --> ", len(tagged_Questions))
tagged_Answers = queryAnswers(answers_list=answers, tagged_PostList=tagged_Questions)
print("len(tagged_Answers) --> ", len(tagged_Answers))

tagged_Votes = queryVotes(tagged_list=tagged_Answers)
vote_Counts = voteAnalysis(tagged_votes=tagged_Votes, tagged_posts=tagged_Answers)


# print("wtf: ", len(tagged_votes))
# print(tagged_votes[69])






