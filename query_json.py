# a method to find the most upvoted/downvoted users

import json
import os
import pickle
import argparse 
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import csv
import networkx as nx
path = "json/"
files = [f for f in os.listdir(path)]

    

def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--tag', type=str, help='tags to search stackexchange database for')
parser.add_argument('--newquery', type=boolean_string, default=False, help='set to true to run new query')
parser.add_argument('--load', type=boolean_string, default=False, help='load from save file')
parser.add_argument('--answer', type=boolean_string, default=True, help='choose True to get questions or False for actions')
parser.add_argument('--no_tag', type=boolean_string, default=False, help='choose True for entire dataset')


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


def queryReputation():
    
    f = open('json/Users.json') 
    # returns JSON object as a dictionary
    data = json.load(f)
    data_ = data['users'] # returns dict
    users_list = data_['row'] # returns list

    
    users_rep_dict = {}
    
    for user in users_list:
        if checkKey(d=user, key='@Id'):
            if user['@Id'] not in users_rep_dict and user['@Id'] != '-1':
                tmp = {user['@Id']:user['@Reputation']}
                users_rep_dict.update(tmp)
    f.close()
    return users_rep_dict


def voteAnalysis(tagged_votes=None, tagged_posts=None, users_rep_dict=None):
    postID_vote_dict = {}
    for post in tagged_posts:
        for vote in tagged_votes:
            # print("pp --> ", post['@Id'])
            # print("dd --> ", checkKey(d=users_rep_dict, key=post['@Id']))
            # assert False
            
            if vote['@Id'] == post['@Id'] and checkKey(d=users_rep_dict, key=post['@Id']):
                
                if post['@Id'] not in postID_vote_dict:
                    tmp = {post['@Id']:{"1":0, "2":0, "3":0, "12":0, "15":0, "count":0, "rep": 0}}
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
                        
                    postID_vote_dict[post['@Id']]["count"] += 1
                    postID_vote_dict[post['@Id']]["rep"] = users_rep_dict[post['@Id']]

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
    with open('data/' + args.tag[1:-1] + str(args.answer) +'.pickle', 'wb') as handle:
        pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('data/' + args.tag[1:-1] + str(args.answer) + '.pickle', 'rb') as handle:
        d_dict = pickle.load(handle)
        print(dict == d_dict)


def sum_userVotes(tag=args.tag):
    d_dict = None
    
    try:
        with open('data/' + tag[1:-1] + str(args.answer) + '.pickle', 'rb') as handle:
            d_dict = pickle.load(handle)
    except:
        with open('data/' + tag  + '.pickle', 'rb') as handle:
            d_dict = pickle.load(handle)
    
    
    sorted_keys = sorted(d_dict.keys())
    
    sorted_keys = [eval(i) for i in sorted_keys]
    sorted_keys.sort()
    
    accepted_vote_list = []
    spam_vote_list = []
    up_vote_list = []
    down_vote_list = []
    post_count_list = []
    reputation_list = []

    
    for idx, key in enumerate(sorted_keys):
        
        d = d_dict[str(key)]
        tmp = sorted(d_dict[str(key)].keys())

        up_votes = 0
        down_votes = 0
        accepted_votes = 0
        spam_votes = 0
        
        for key in tmp:
            for vote_types in  d[key].keys():
                if vote_types == '1':
                    accepted_votes += d[key]['1']
                    
                elif vote_types == '2':
                    up_votes += d[key]['2']

                elif vote_types == '3':
                    down_votes += d[key]['3']
                
                elif vote_types == '12':
                    spam_votes += d[key]['12']
                    
        reputation_list.append(d[key]['rep'])
        post_count_list.append(d[key]['count'])
        up_vote_list.append(up_votes)
        down_vote_list.append(down_votes)
        accepted_vote_list.append(accepted_votes)
        spam_vote_list.append(spam_votes)
      
    return [
        np.array(up_vote_list).astype(np.float32), 
        np.array(down_vote_list).astype(np.float32), 
        np.array(accepted_vote_list).astype(np.float32),
        np.array(spam_vote_list).astype(np.float32),
        np.array(post_count_list).astype(np.float32),
        np.array(reputation_list).astype(np.float32),
        ]
    
def make_upvote_vs_downvote_Histogram(vote_list=None):
    from matplotlib import colors
    from matplotlib.ticker import PercentFormatter
    
    
    
    
    N_points = len(vote_list[0])
    n_bins = len(vote_list[1])
    
    # Fixing random state for reproducibility
    up_votes =  np.array(vote_list[0]).astype(np.float32)
    down_votes = np.array(vote_list[1]).astype(np.float32)
    
    # fig, axs = plt.subplots(tight_layout=True)
    # hist = axs.hist2d(up_votes, down_votes)
    
    # print(axs)
    fig, axs = plt.subplots(3, 1, figsize=(5, 15), sharex=True, sharey=True,
                        tight_layout=True)
    
    ## We can increase the number of bins on each axis
    axs[0].hist2d(up_votes, down_votes, bins=40)

    # As well as define normalization of the colors
    axs[1].hist2d(up_votes, down_votes, bins=40, norm=colors.LogNorm())

    # We can also define custom numbers of bins for each axis
    axs[2].hist2d(up_votes, down_votes, bins=(80, 10), norm=colors.LogNorm())

    # plt.show()
    plt.savefig("data/imgs/" + args.tag[1:-1] + str(args.answer) + 'histogram.png') 
    
def hexagonalHistogram(vote_list=None):

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    x =  np.array(vote_list[0]).astype(np.float32)
    y = np.array(vote_list[1]).astype(np.float32)
    xlim = x.min(), x.max()
    ylim = y.min(), y.max()

    fig, (ax0, ax1) = plt.subplots(ncols=2, sharey=True, figsize=(9, 4))

    hb = ax0.hexbin(x, y, gridsize=50, cmap='inferno')
    ax0.set(xlim=xlim, ylim=ylim)
    ax0.set_title("Hexagon binning")
    cb = fig.colorbar(hb, ax=ax0, label='counts')

    hb = ax1.hexbin(x, y, gridsize=50, bins='log', cmap='inferno')
    ax1.set(xlim=xlim, ylim=ylim)
    ax1.set_title("With a log color scale")
    cb = fig.colorbar(hb, ax=ax1, label='log10(N)')

    # plt.show()
    plt.savefig("data/imgs/" + args.tag[1:-1] + str(args.answer) + 'hexagonalhistogram.png') 
    

def adjacent_values(vals, q1, q3):
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value


def set_axis_style(ax, labels):
    ax.set_xticks(np.arange(1, len(labels) + 1), labels=labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel('Sample name')


def violinPlot(vote_list=None):
    
    # ai_vote_list, ml_vote_list, python_vote_list, nlp_vote_list
    
    ai_upvote =  np.array(vote_list[0][0]).astype(np.float32)
    ai_downvote = np.array(vote_list[0][1]).astype(np.float32)
    ml_upvote =  np.array(vote_list[1][0]).astype(np.float32)
    ml_downvote = np.array(vote_list[1][1]).astype(np.float32)
    python_upvote = np.array(vote_list[2][0]).astype(np.float32)
    python_downvote = np.array(vote_list[2][1]).astype(np.float32)
    nlp_upvote = np.array(vote_list[3][0]).astype(np.float32)
    nlp_downvote = np.array(vote_list[3][1]).astype(np.float32)
    all_upvote = np.array(vote_list[4][0]).astype(np.float32)
    all_downvote = np.array(vote_list[4][1]).astype(np.float32)
    
    ai_y = ai_upvote - ai_downvote
    ml_y = ml_upvote - ml_downvote
    python_y = python_upvote - python_downvote
    nlp_y = nlp_upvote - nlp_downvote
    all_y = all_upvote - all_downvote
    
    ai_reputation =  np.array(vote_list[0][5]).astype(np.float32)
    ml_reputation =  np.array(vote_list[1][5]).astype(np.float32)
    python_reputation = np.array(vote_list[2][5]).astype(np.float32)
    nlp_reputation = np.array(vote_list[3][5]).astype(np.float32)
    all_reputation = np.array(vote_list[4][5]).astype(np.float32)

    
    ai_y_rep = ai_reputation
    ml_y_rep = ml_reputation
    python_y_rep = python_reputation
    nlp_y_rep = nlp_reputation
    all_y_rep = all_reputation
    print("max_rep --> ", np.max(python_y_rep))
    print("max_rep --> ", np.max(all_y_rep))
    
    print("#users: ", len(all_y))
    
    vote_list = [ai_y, ml_y, python_y,  nlp_y, all_y]
    rep_list = [ai_y_rep, ml_y_rep, python_y_rep, nlp_y_rep, all_y_rep]
    
    # # create test data
    # np.random.seed(19680801)
    # data = [sorted(np.random.normal(0, std, 100)) for std in range(1, 5)]

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4), sharey=True)
    # ax1.set_title('Default violin plot')
    # ax1.set_ylabel('UpVotes - DownVotes')
    # ax1.violinplot(vote_list)
    
    # ax2.set_title('UpVotes - DownVotes for  various StackExchange tags violin plot')
    # parts = ax2.violinplot(
    #         vote_list, showmeans=False, showmedians=False,
    #         showextrema=False)
    
    ax1.set_title('Violin plot')
    ax1.set_ylabel('UpVotes - DownVotes')
    ax1.violinplot(vote_list)

    # parts = ax2.violinplot(
    #         vote_list, showmeans=False, showmedians=False,
    #         showextrema=False)
    
    labels = ['ai', 'ml', 'python', 'nlp', 'all']
    for ax in [ax1, ax2]:
        set_axis_style(ax, labels)


    # plt.show()

    plt.savefig("data/imgs/" + args.tag[1:-1] + str(args.answer) + 'volinPlot.png')
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4), sharey=True)
    
    ax1.set_title('Violin plot')
    ax1.set_ylabel('Reputation')
    ax1.violinplot(rep_list)
    labels = ['ai', 'ml', 'python', 'nlp', 'all']
    for ax in [ax1, ax2]:
        set_axis_style(ax, labels)
    plt.savefig("data/imgs/" + args.tag[1:-1] + str(args.answer) + 'RepVolinPlot.png')
    

def makeScatterPlot(vote_list=None):

    # Fixing random state for reproducibility
    up_votes =  np.array(vote_list[0]).astype(np.float32)
    reputations = np.array(vote_list[5]).astype(np.float32)
    down_votes = np.array(vote_list[1]).astype(np.float32)
    
    accepted_votes = np.array(vote_list[2]).astype(np.float32)
    spam_votes =  np.array(vote_list[3]).astype(np.float32)
    
    x = up_votes - down_votes
    x_ = reputations
    y = accepted_votes - spam_votes
    # y = accepted_votes
    
    print(len(x))
    print(np.max(x))
    print(np.min(x))
    print(np.max(accepted_votes))
    print(np.min(spam_votes))
    print("max_rep --> ", np.max(reputations))
    
    
    N = len(x)
    colors = np.random.rand(N)
    area = ((30 * np.random.rand(N))**2).astype(np.float32)  # 0 to 15 point radii
    
    fig = plt.figure()
    ax = fig.add_subplot()
    
    ax.scatter(x, y, s=area, c=colors, alpha=0.5)
    ax.set_xlabel('UpVotes - DownVotes')
    ax.set_ylabel('AcceptedAnswer - Spam')
    ax.set_title('Scatter plot: ' + args.tag + "Answer: " + str(args.answer))
    
    plt.savefig("data/imgs/" + args.tag[1:-1] + str(args.answer) + '.png') 
    
    fig = plt.figure()
    ax = fig.add_subplot()
    
    ax.scatter(x_, y, s=area, c=colors, alpha=0.5)
    ax.set_xlabel('Reputations')
    ax.set_ylabel('AcceptedAnswer - Spam')
    ax.set_title('Scatter plot: ' + args.tag + "Answer: " + str(args.answer))

    # plt.show() 
    plt.savefig("data/imgs/" + args.tag[1:-1] + str(args.answer) + 'Reputation.png') 

def make3DScatterPlot(vote_list=None):

    up_votes =  np.array(vote_list[0]).astype(np.float32)
    down_votes = np.array(vote_list[1]).astype(np.float32)
    
    accepted_votes = np.array(vote_list[2]).astype(np.float32)
    spam_votes =  np.array(vote_list[3]).astype(np.float32)
    author_counts = np.array(vote_list[4]).astype(np.float32)
    reputations = np.array(vote_list[5]).astype(np.float32)
    
    x = up_votes - down_votes
    y = accepted_votes - spam_votes
    z = author_counts
    u = reputations
    
    print("max --> ", np.max(z))
    print("max y --> ", np.max(y))
    print('max rep --> ', np.max(u))
    


    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(x, y, z)

    ax.set_xlabel('UpVotes - DownVotes')
    ax.set_ylabel('AcceptedAnswer - Spam')
    ax.set_zlabel('# of posts')
    ax.set_title('3DScatter plot: ' + args.tag + "Answer: " + str(args.answer))
    plt.savefig("data/imgs/" + args.tag[1:-1] + str(args.answer) + '3Dscatter.png') 
    
    
    
    ax.scatter(x, y, u)
    ax.set_xlabel('UpVotes - DownVotes')
    ax.set_ylabel('AcceptedAnswer - Spam')
    ax.set_zlabel('Reputation')
    ax.set_title('3DReputationScatter plot: ' + args.tag + "Answer: " + str(args.answer))
    plt.savefig("data/imgs/" + args.tag[1:-1] + str(args.answer) + '3Dreputationscatter.png')
    
    ax.scatter(u, y, z)
    ax.set_xlabel('Reputation')
    ax.set_ylabel('AcceptedAnswer - Spam')
    ax.set_zlabel('# of posts')
    ax.set_title('3DReputationScatter plot: ' + args.tag + "Answer: " + str(args.answer))
    plt.savefig("data/imgs/" + args.tag[1:-1] + str(args.answer) + '3DXreputationscatter.png')

    # plt.show()  
    # assert False
    

def makeNodes():
    path = "json/"
    files = [f for f in os.listdir(path)]
    
    G = nx.DiGraph()
    
    for filename in files:
        # print(filename)

        f = open(path + filename) 

        data = json.load(f)
        filename = filename.split('.')
        node_name =  filename[0].lower()
        data_ = data[node_name] # returns dict
        post_list = data_['row'] # returns list

        post_dict = {}
        for post in post_list:
            # if post['@Id'] not in post_dict:
                # print(post)
            if node_name == 'users':
                if post['@Id'] not in post_dict:
                    tmp = {post['@Id']: post}
                
            elif node_name == 'posts':
                if checkKey(d=post, key='@OwnerUserId'):
                    if post['@OwnerUserId'] not in post_dict:
                        tmp = {post['@OwnerUserId']: post}
                
            elif node_name == 'votes':
                if checkKey(d=post, key='@PostId'):
                    if post['@PostId'] not in post_dict:
                        tmp = {post['@PostId']: post}
            
            else:
                tmp = {post['@Id']: post}
            # tmp = {post}
            
            post_dict.update(tmp)
            # if post['@Id'] not in post_dict:
            #     # print(post)
            #     if node_name == 'users':
            #         tmp = {post['@Id']: post}
                    
            #     elif node_name == 'posts':
            #         [print([post])]
            #         tmp = {post['OwnerUserId']: post}
                    
            #     elif node_name == 'votes':
            #         tmp = {post['PostId']: post}
                
            #     else:
            #         tmp = {post['@Id']: post}
            #     # tmp = {post}
                
            #     post_dict.update(tmp)
                
        G.add_nodes_from([(node_name, post_dict)])
        
        nx.draw(G, with_labels=True) 
        plt.savefig("data/imgs/GraphEdges.png", format="PNG") 
    
    # print("UMMM --> ", G.nodes['users']['29478'])
    # assert False
    return G

def makeEdges(G=None):

    
        
        # data_to_csv= open(path + filename + '.csv','w')
        
        # list_head=[]

        # Csv_writer=csv.writer(data_to_csv)
    
    # print("tree: \n ", tree)
    # print("root: \n ", root)
    
    # for item in root.iter("row"):
    #     # print("ehut --> ", item)
    #     print(item.attrib["Id"])
        
    # assert False
    
    #  G1 = nx.DiGraph()
    
    csv_path = "csv/"
    files = [f for f in os.listdir(csv_path)]
    
    print(files)
    
    df_users = None
    df_posts = None
    df_Tags = None
    df_votes = None
    
    users_head = []
    posts_head = []
    tags_head = []
    votes_head = []
    
    for file in files:
        file = file.split('.')
        
        df = None
        print("file[0] --> ", file[0])
        
        if file[0] == 'Users':
            head = users_head
            df_users = pd.read_csv(csv_path + file[0] + '.csv')
            df = df_users
            for col in df.columns:
                head.append(col)
            
        elif file[0] == 'Posts':
            head = posts_head
            df_posts = pd.read_csv(csv_path + file[0] + '.csv')
            df = df_posts
            for col in df.columns:
                head.append(col)
        
        elif file[0] == 'Tags':
            head = tags_head
            df_tags = pd.read_csv(csv_path + file[0] + '.csv')
            df = df_tags
            for col in df.columns:
                head.append(col)
        
        elif file[0] == 'Votes':
            head = votes_head
            df_votes = pd.read_csv(csv_path + file[0] + '.csv')
            df = df_votes
            for col in df.columns:
                head.append(col)
        else:
            next
        
        
        
            
        # df1 = df[head]
        
    # print("head --> ", head)
    print("users_head --> ", users_head)
    print("posts_head --> ", posts_head)
    print("tags_head --> ", tags_head)
    print("votes_head --> ", votes_head)
    
    # print(G.nodes['posts'])
    # assert False
    
    for user_node in G.nodes['users']:
        if user_node in G.nodes['posts']:
            
            if checkKey(d=G.nodes['posts'][user_node], key='@Tags'):
                G.add_edge(user_node, user_node, posttypeid=G.nodes['posts'][user_node]['@PostTypeId'], tags=G.nodes['posts'][user_node]['@Tags'])
                
    for post_node in G.nodes['posts']:
        if checkKey(d=G.nodes['votes'], key=G.nodes['posts'][post_node]['@Id']):
            if checkKey(d=G.nodes['votes'][G.nodes['posts'][post_node]['@Id']], key='@VoteTypeId'):
                if G.nodes['posts'][post_node]['@Id'] in G.nodes['votes']:
                    G.add_edge(
                        G.nodes['posts'][post_node]['@Id'],
                        G.nodes['posts'][post_node]['@Id'],
                        votetypeid=G.nodes['votes'][G.nodes['posts'][post_node]['@Id']]['@VoteTypeId']
                    )
    
    
    
    # nx.draw(G, with_labels=True) 
    # plt.savefig("data/imgs/EdgesGraph.png", format="PNG")
              

def saveCSV(filename=None, HEADERS=None, rows=None):
    
    json_path = "json/"
    files = [f for f in os.listdir(json_path)]
    
    for filename in files:

        f = open(path + filename) 

        data = json.load(f)
        filename_ = filename.split('.')
        data_ = data[filename_[0].lower()] # returns dict
        list = data_['row'] # returns list
        
        rows = []
        HEADERS = sorted(list[0].keys())
        # print("filename --> ", filename_[0])
        # if filename_[0] == "Posts":
        #     # print("old",len(HEADERS))
        #     HEADERS.remove('@Body')
        #     HEADERS.remove('@Title')
        #     HEADERS.remove('@ClosedDate')
        #     HEADERS.remove('@CommentCount')
        #     HEADERS.remove('@ContentLicense')
        #     HEADERS.remove('@CreationDate')
        #     HEADERS.remove('@LastActivityDate')
            
            # @ClosedDate,@CommentCount,@ContentLicense,@CreationDate,@LastActivityDate
            # print("new", len(HEADERS))
        
            # assert False
        for row in list:
            tmp = []
            for key in sorted(row.keys()):
                # @ClosedDate,@CommentCount,@ContentLicense,@CreationDate,@LastActivityDate
                # if key == '@Body' or key == '@Title' or key == '@ClosedDate' or key == '@CommentCount' or key == '@ContentLicense' or key == '@CreationDate' or key=='@LastActivityDate':
                #     del row[key]
                # else:
                #     tmp.append(row[key].split(','))
                tmp.append(row[key].split(','))
            rows.append(tmp)
        
            
        with open('csv/' + filename_[0] + '.csv', 'w', newline="") as f:
            write = csv.writer(f)
            write.writerow(HEADERS)
            write.writerows(rows)
            
    
    

def main():
    # saveCSV()
    G = makeNodes()
    print("WHAT THE FICL \n", G.nodes())
    G = makeEdges(G=G)
    assert False
    if args.no_tag and args.tag == "<all>" and not args.load:
        if not args.answer:
            questions = getQuestions()
            Votes = queryVotes(tagged_list=questions)
            users_Reputation = queryReputation()
            vote_Counts = voteAnalysis(tagged_votes=Votes, tagged_posts=questions, users_rep_dict=users_Reputation)
            owner_post_VoteCounts = queryOwners(tagged_posts=questions, vote_counts=vote_Counts)
            saveDict(owner_post_VoteCounts)
            vote_list = sum_userVotes()
            
            
        else:
            print("analyzin answers")
            answers = getAnswers()
            Votes = queryVotes(tagged_list=answers)
            users_Reputation = queryReputation()
            vote_Counts = voteAnalysis(tagged_votes=Votes, tagged_posts=answers, users_rep_dict=users_Reputation)
            owner_post_VoteCounts = queryOwners(tagged_posts=answers, vote_counts=vote_Counts)
            saveDict(owner_post_VoteCounts)
            vote_list = sum_userVotes()
            

    elif args.newquery and args.answer and not args.load:
        questions = getQuestions()
        answers = getAnswers()
        tagged_Questions = queryQuestions(questions_list=questions, tag=args.tag)

        print("len(tagged questions: ) --> ", len(tagged_Questions))
        tagged_Answers = queryAnswers(answers_list=answers, tagged_PostList=tagged_Questions)
        print("len(tagged_Answers) --> ", len(tagged_Answers))

        tagged_Votes = queryVotes(tagged_list=tagged_Answers)
        
        users_Reputation = queryReputation()
        
        vote_Counts = voteAnalysis(tagged_votes=tagged_Votes, tagged_posts=tagged_Answers, users_rep_dict=users_Reputation)
        owner_post_VoteCounts = queryOwners(tagged_posts=tagged_Answers, vote_counts=vote_Counts)
        saveDict(owner_post_VoteCounts)
        vote_list = sum_userVotes()
        makeScatterPlot(vote_list=vote_list)
    
    elif args.newquery and not args.answer and not args.load:
        print("looking for question")
        questions = getQuestions()
        answers = getAnswers()
        tagged_Questions = queryQuestions(questions_list=questions, tag=args.tag)


        tagged_Votes = queryVotes(tagged_list=tagged_Questions)
        users_Reputation = queryReputation()
        vote_Counts = voteAnalysis(tagged_votes=tagged_Votes, tagged_posts=tagged_Questions, users_rep_dict=users_Reputation)

        owner_post_VoteCounts = queryOwners(tagged_posts=tagged_Questions, vote_counts=vote_Counts)
        saveDict(owner_post_VoteCounts)
        vote_list = sum_userVotes()
        makeScatterPlot(vote_list=vote_list)
        
    elif args.load:
        vote_list = sum_userVotes()
        makeScatterPlot(vote_list=vote_list)
        make_upvote_vs_downvote_Histogram(vote_list=vote_list)
        hexagonalHistogram(vote_list=vote_list)
        make3DScatterPlot(vote_list=vote_list)
        
        
        ai_vote_list = sum_userVotes(tag="<ai>")
        ml_vote_list = sum_userVotes("<machine-learning>")
        python_vote_list = sum_userVotes("<python>")
        nlp_vote_list = sum_userVotes("<nlp>")
        all_vote_list = sum_userVotes("<all>")
        violin_list = [ai_vote_list, ml_vote_list, python_vote_list, nlp_vote_list, all_vote_list]
        violinPlot(vote_list=violin_list)
    
if __name__ == "__main__":
    main()




