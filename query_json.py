# a method to find the most upvoted/downvoted users

import json
import os
import pickle
import argparse 
path = "json/"
files = [f for f in os.listdir(path)]

def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--tag', type=str, help='tags to search for')
parser.add_argument('--newquery', type=boolean_string, default=False, help='run new query')
parser.add_argument('--load', type=boolean_string, default=False, help='load from save file')
args = parser.parse_args()
print(args)
args.tag = "<" + args.tag + ">"

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

def check_tags(tags=None, queries=None):
    
    tags = tags.replace(">","")
    tags = tags.split('<')
    tags = tags[1:len(tags)]
    
    queries = queries.replace(">","")
    queries = queries.split('<')
    queries = queries[1:len(queries)]
    
    # print(queries)
    
    checker = False
    for tag in tags:
        for query in queries:
            if tag == query:
                checker = True
                
    return checker
    
def queryQuestions(questions_list=None, tag=None):
    # Opening JSON file
    f = open('json/Posts.json') 
    
    
    tagged_PostID_list = []
    for post in questions_list:
        # print(check_tags(tags=post["@Tags"], queries=tag))
            
            
        if checkKey(d=post, key='@Tags') and checkKey(d=post, key='@OwnerUserId')  and checkKey(d=post, key='@Score') and checkKey(d=post, key='@ViewCount'):
            # if post['@Tags'] == tag: 
            if check_tags(tags=post["@Tags"], queries=tag):
                tagged_PostID_list.append({'@Id':post['@Id'], '@OwnerUserId':post['@OwnerUserId'], '@Score':post['@Score'], '@ViewCount':post['@ViewCount']})
                
    # print(str(tag) + " posts found --> ", len(tagged_PostID_list))
    f.close()
    return tagged_PostID_list



def queryAnswers(answers_list=None, tagged_PostList=None):
    f = open('json/Posts.json') 
    
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
        for post in tagged_list:
            if vote['@PostId'] == post["@Id"]:
                tagged_vote_list.append({'@Id':vote['@PostId'], '@VoteTypeId': vote['@VoteTypeId']})
    
    return tagged_vote_list


def voteAnalysis(tagged_votes=None, tagged_posts=None):
    postID_vote_dict = {}
    for post in tagged_posts:
        for vote in tagged_votes:
            if vote['@Id'] == post['@Id']:
                
                if post['@Id'] not in postID_vote_dict:
                    tmp = {post['@Id']:{"1":0, "2":0, "3":0, "12":0, "15":0}}
                    postID_vote_dict.update(tmp)

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

    return postID_vote_dict   

def queryOwners(tagged_posts=None, vote_counts=None):

    owner_post_vote_counts_dicts = {}
    for post in tagged_posts:

        if checkKey(d=vote_counts, key=post['@Id']) and checkKey(d=post, key='@OwnerUserId'):
            if post['@OwnerUserId'] not in owner_post_vote_counts_dicts:
                tmp = {post['@OwnerUserId']: {post['@Id']:vote_counts[post['@Id']]}}
                owner_post_vote_counts_dicts.update(tmp)
                
            else:
                tmp = {post['@Id']:vote_counts[post['@Id']]}
                owner_post_vote_counts_dicts[post['@OwnerUserId']].update(tmp)

    return owner_post_vote_counts_dicts


def saveDict(dict):
    with open('data/' + args.tag + '.pickle', 'wb') as handle:
        pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('data/' + args.tag + '.pickle', 'rb') as handle:
        d_dict = pickle.load(handle)
        print(dict == d_dict)


def sum_userVotes():
    d_dict = None
    with open('data/' + args.tag + '.pickle', 'rb') as handle:
        d_dict = pickle.load(handle)
        
    
    
    sorted_keys = sorted(d_dict.keys())
    
    sorted_keys = [eval(i) for i in sorted_keys]
    sorted_keys.sort()
    
    accepted_vote_list = []
    spam_vote_list = []
    up_vote_list = []
    down_vote_list = []

    
    for idx, key in enumerate(sorted_keys):
        
        d = d_dict[str(key)]
        tmp = sorted(d_dict[str(key)].keys())
        d = d[tmp[0]]

        up_votes = 0
        down_votes = 0
        accepted_votes = 0
        spam_votes = 0
        
        for vote_types in d.keys():

            if vote_types == '1':
                accepted_votes += d['1']
                
            elif vote_types == '2':
                up_votes += d['2']

            elif vote_types == '3':
                down_votes += d['3']
            
            elif vote_types == '12':
                spam_votes += d['12']

                
        up_vote_list.append(up_votes)
        down_vote_list.append(down_votes)
        accepted_vote_list.append(accepted_votes)
        spam_vote_list.append(spam_votes)
            
    return [up_vote_list, down_vote_list, accepted_vote_list, spam_vote_list]
    
def makeHistogram(vote_list=None):
    raise NotImplementedError



def makeScatterPlot(vote_list=None):
    import matplotlib.pyplot as plt
    import numpy as np

    # Fixing random state for reproducibility
    up_votes =  np.array(vote_list[0]).astype(np.float32)
    down_votes = np.array(vote_list[1]).astype(np.float32)
    
    accepted_votes = np.array(vote_list[2]).astype(np.float32)
    spam_votes =  np.array(vote_list[3]).astype(np.float32)
    
    x = up_votes - down_votes
    y = accepted_votes - spam_votes
    y = accepted_votes
    
    # print(accepted_votes[0:100])
    # print(spam_votes[0:100])
    
    # print(np.max(accepted_votes))
    # print(np.min(down_votes))
    
    print(np.max(x))
    print(np.min(x))
    
    
    N = len(x)
    colors = np.random.rand(N)
    area = ((30 * np.random.rand(N))**2).astype(np.float32)  # 0 to 15 point radii

    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    # plt.scatter(x, y, c=colors, alpha=0.5)
    plt.scatter(x, y)
    plt.show() 
    plt.savefig("data/imgs/" + args.tag + '.png')   

def main():
    # print("Hello World!")

    if args.newquery and not args.load:
        questions = getQuestions()
        answers = getAnswers()
        tagged_Questions = queryQuestions(questions_list=questions, tag=args.tag)

        print("len(tagged questions: ) --> ", len(tagged_Questions))
        tagged_Answers = queryAnswers(answers_list=answers, tagged_PostList=tagged_Questions)
        print("len(tagged_Answers) --> ", len(tagged_Answers))

        tagged_Votes = queryVotes(tagged_list=tagged_Answers)
        vote_Counts = voteAnalysis(tagged_votes=tagged_Votes, tagged_posts=tagged_Answers)

        owner_post_VoteCounts = queryOwners(tagged_posts=tagged_Answers, vote_counts=vote_Counts)
        saveDict(owner_post_VoteCounts)
        vote_list = sum_userVotes()
        makeScatterPlot(vote_list=vote_list)
        
    elif args.load:
        vote_list = sum_userVotes()
        makeScatterPlot(vote_list=vote_list)
    
if __name__ == "__main__":
    main()




