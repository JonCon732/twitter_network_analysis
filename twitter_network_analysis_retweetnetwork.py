#Jonathan Conrow
#DSSA Major Project
#Stockton University
#April 23, 2018
#DESCRIPTION: the purpose of this code is to collect tweets with a specific hashtag and store in a local CSV file to do a network analysis on.


#This code was built using python 3.6.4
import tweepy #using tweepy 3.6.0
import csv
import pandas as pd #using version 0.22.0
import os



#Using Tweepy
#Tweepy is a very straight forward Twitter API, I am using their search cursor method, 
#in order to collect tweets associated with a specific hashtage, #. There is alot of tweepy 
#documentation available online. It also allows for a higher rate limit than something like 
#the twitterapx Api. http://docs.tweepy.org/en/v3.6.0/

#provide the Keys and tokens from twitter after you have created a new app.

consumer_key = "your_consumer_key_here"
consumer_secret = "your_consumer_secret_here"
access_token = "your_access_token_here"
access_token_secret = "your_access_token_secret_here"

#Ohandler methond for tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#Be sure to respect the rate limit for the api, if 420 error start arising, wait time starts increasing exponential
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Open/Create a file to append data
csvFile2 = open('girther2.csv', 'a')
#Use csv Writer
csvWriter2 = csv.writer(csvFile2)

#Tell the api what to search for and append the csv file that was given to a variable above
#Girther hashtag
for tweet in tweepy.Cursor(api.search,q="#girther",count=100,
                           lang="en",
                           since="2018-03-01").items():
    #print (tweet.created_at, tweet.text, tweet.user.screen_name)
    
    csvWriter2.writerow([tweet.created_at, tweet.user.screen_name, tweet.text.encode('utf-8')


#Check to see how many queres I can make
api.rate_limit_status()['resources']['search']


#Exploration of the data
#Since I know I want to extract the retweets using the specified hashtag I can clean up the data with the following snippet
df_g=pd.read_csv('girther.csv', header=None, names=["date_created", "source",'tweet'])
df_g=df_g.drop_duplicates()

#to clean the data up a little bit I remobed the "b" character that represented the "@" symbol when utf-8 encoding took place
df_g['source'] = df_g['source'].map(lambda x: x.lstrip('b').rstrip('aAbBcC'))
df_g['source'] = df_g['source'].str.replace("'", '')
df_g['tweet'] = df_g['tweet'].map(lambda x: x.lstrip('b').rstrip('aAbBcC'))
df_g['source'] = df_g['source'].map(lambda x: x.lstrip("'").rstrip('aAbBcC'))
df_g1= df_g[df_g['tweet'].str.contains("RT @")]

#extract the retweeted user names from the tweet column and put them in a seperate column
df_g1['target']=df_g1['tweet'].str.split('@') .str[1]
df_g1['target']=df_g1['target'].str.split(':') .str[0]

#reorder the columns so it is easier for me to see the data i am interested in
girther_meme_network_df = df_g1[['source','target','date_created','tweet']]
print(girther_meme_network_df.head())

#Get a summary of the tweet dataframe
print(girther_meme_network_df.describe())



#Network analysis of the dataset using networkx
# makes node and edge lists
source_g= girther_meme_network_df['source']
user_g= pd.DataFrame(girther_meme_network_df['source'])
retweeted_user_g= pd.DataFrame(girther_meme_network_df['target'])

source_list_g = girther_meme_network_df['source'].tolist()
edge_df1_g = user.join(retweeted_user_g)
el_g=[]
for row in edge_df1_g.itertuples(index=False, name=None):
    el_g.append(row)

#print(el_g)
#print(source_list)


#Make a network Graph 
girth=nx.Graph()
girth.add_nodes_from(source_list_g)
girth.add_edges_from(el_g)
GG= nx.draw(girth, node_size=5,with_label=True, node_color='green')
plt.show

#create a function that will sort the dictionary output of our centralities to easily find 
#the ouput centrality measures
import operator

def centrality_sort(centrality_dict):
    return sorted(centrality_dict.items(), key=operator.itemgetter(1))

#Print the degree of centrality of the non-normalized network
print("Degree Centrality")
degree_cen_g = nx.degree_centrality(girth)
print(degree_cen_g)

#Print betweeness centrality
print("Betweenness Centrality")
betwee_cen_g = nx.betweenness_centrality(girth, normalized=False)
print(betwee_cen_g)

#Closeness Centrality
print("Closeness Centrality")
close_cen_g = nx.closeness_centrality(girth)
print(close_cen_g)
#Z= nx.G.edges(data=True)

#Use the sorting function created in the cell above to find which nodes are the mose important in this network
degree_sorted_g = centrality_sort(degree_cen_g)
#To see the top ten users with the highest degree of centrality, we have to view the last 10 items in our dictionary
degree_sorted_g[-10:]

#Use the sorting function created in the cell above to find which nodes are the mose important in this network
between_sorted_g = centrality_sort(betwee_cen_g)
#To see the top ten users with the highest betweeness of centrality, we have to view the last 10 items in our dictionary
between_sorted_g[-10:]

#Use the sorting function created in the cell above to find which nodes are the mose important in this network
close_sorted_g = centrality_sort(close_cen_g)
#To see the top ten users with the highest closeness of centrality, we have to view the last 10 items in our dictionary
close_sorted_g[-10:]


#Networkx Page Rank algorithm
#Page ranking the individuals in the network
pr_g = nx.pagerank(girth, alpha = 0.9)
#Use the sorting function created in the cell above to find which nodes are the mose important in this network
pr_sorted_g = centrality_sort(close_cen_g)
#To see the top ten users with the highest closeness of centrality, we have to view the last 10 items in our dictionary
pr_sorted_g[-10:]



#Using Plotly to create a interactive visualization of the girther retweet network
#Import plotly and use it offline
#from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot, plot
#init_notebook_mode(connected=True)
#Initally plotly will ask you to input your api credentials 

import plotly.plotly as py
from plotly.graph_objs import *

#Obtain the positional data with networkx useing the "layout" method
#Obtain the positional data with networkx useing the "layout" method
pos_g=nx.kamada_kawai_layout(girth)

dmin=1
ncenter=0
for n in pos_g:
    x,y=pos_g[n]
    d=(x-0.5)**2+(y-0.5)**2
    if d<dmin:
        ncenter=n
        dmin=d

p_g=nx.single_source_shortest_path_length(girth,ncenter)

#Girther dataframe creation and manipulation of positions
pos_df_g= pd.DataFrame.from_dict(pos_g, orient='index')
pos_df_g.columns = ['x','y']

#now that I can FINALLY define a list of the X and Y coordinates
#Blank List for X coordinates
Xn_g=[]
#empty list for y coordinates
Yn_g=[]
#use the df index as a list of the labels
lab_g=pos_df_g.index.tolist()
#for loop to append the empty lists
for n in pos_df_g.x:
    Xn_g.append(n)
for i in pos_df_g.y:
    Yn_g.append(i)


#Defining the trace for nodes 
node_trace=dict(type='scatter',
                 x=Xn_g, 
                 y=Yn_g,
                 mode='markers',
                 marker=dict(
                     showscale=True,
                     colorscale='YIGnBu',
                     reversescale=True,
                     opacity = 0.75,
                     color=[],
                     symbol='dot', 
                     size=13, 
                     colorbar=dict(
                         thickness=15,
                         title='Page Rank',
                         xanchor='left',
                         titleside='right'),
                     ),
                 text=lab,
                 hoverinfo='text')

#Color The Node Points in respect to the page ranking value associated with each node
pagerank_df_g= pd.DataFrame(pr_sorted_g)
pagerank_df_g.columns = ['screen_name','PR']

#change the The Node size in respect to the degree centrality value associated with each node
degree_df_g = pd.DataFrame(degree_sorted_g)
degree_df_g.columns = ['screen_name','DC']


for i in pagerank_df_g.PR:
    node_trace['marker']['color'].append(i)

#I would like the Node sizes to be represented by the closeness centrality measure
"""
for i in degree_df_g.DC:
    node_trace['marker']['size'].append(i*100)
"""

#creat lists that record the edge end coordinates
Xe_g=[]
Ye_g=[]
for e in girth.edges():
    Xe_g.extend([pos_g[e[0]][0], pos_g[e[1]][0], None])
    Ye_g.extend([pos_g[e[0]][1], pos_g[e[1]][1], None])

 #Create the Edges
edge_trace=dict(type='scatter',
                 mode='lines',
                 x=Xe_g,
                 y=Ye_g,
                 line=dict(width=1, color='#888'),
                 hoverinfo='none'
                )



axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title='' 
          )
layout_g=dict(title= '#Girther Meme',  
            font= dict(family='Europa',
                       size=20
                      ),
            width=800,
            height=800,
            autosize=False,
            showlegend=False,
            xaxis=axis,
            yaxis=axis,
            margin=dict(
                l=5,
                r=5,
                b=20,
                t=40,
                pad=0,
            ),

    hovermode='closest',
    plot_bgcolor='#efecea', #set background color            
    )


girth_fig = dict(data=[edge_trace, node_trace], layout=layout_g)


#plot withplotly to direct to the web hosting page
py.plot(girth_fig)









