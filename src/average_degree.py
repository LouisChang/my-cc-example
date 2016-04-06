import json
import os
import time
import scipy as sp
from decimal import Decimal

# remove older twittes in the graph
def remove_graph(graph, older_hashtag):
    connected_hashtags = graph[older_hashtag]
    for hashtag in connected_hashtags:
        graph[hashtag].remove(older_hashtag)
    del graph[older_hashtag]
    return graph

start_time = time.time()

input_dir = "tweet_input/tweets.txt"
output_dir = "tweet_output/output.txt"

graph = {}
hashtags_init = {}
output = []

with open(input_dir) as f:
    for ln in f: #read every tweet
        tweet = json.loads(ln)
        # Make the time easier to use, use seconds other than ms
        try:
            timestamp = int(tweet['timestamp_ms'])/1000
        except:
            continue

        try: 
            # hashtags data cleaning
            hashtags = sp.unique(['#'+hashtag['text'] for hashtag in tweet['entities']['hashtags']])
            hashtags = [hashtag.encode('ascii','ignore') for hashtag in hashtags]
            new_hashtags_init = dict([(hashtag,timestamp) for hashtag in hashtags])
        except:
            new_hashtags_init = {}
        # Figure out older_hashtags by finding their entering time
        older_hashtags = [hashtag * ((timestamp - hashtags_init.get(hashtag,timestamp)) > 60) for hashtag in hashtags_init.keys()]
        older_hashtags = filter(None, older_hashtags)

        for hashtag in older_hashtags:
            del hashtags_init[hashtag]
            graph = remove_graph(graph, hashtag)
        # Clean dumplicate 
        hashtags_init.update(new_hashtags_init)
        for hashtag in new_hashtags_init.keys():
            graph[hashtag] = list(sp.unique(graph.get(hashtag,[]) + new_hashtags_init.keys()))
            #graph(hashtag) = list(sp.unique(graph.get(hashtag,[])+ new_hashtags_init.keys()))
            graph[hashtag].remove(hashtag)

        # Calcute avg degree in the graph
        degrees = [len(graph[node]) for node in graph.keys()]

        # Import the decimal package to make every calculation to 0.00 format       
        try:
            avg_degree = str(Decimal(str(1.00*sum(degrees)/sp.count_nonzero(degrees))).quantize(Decimal('0.00')))
        except:
            avg_degree = str(Decimal('0.00').quantize(Decimal('0.00')))
        # Combine the data and ready to write file
        output.append(avg_degree)
# Write the file
with open(output_dir,'w') as out_f:
    out_f.write(os.linesep.join(output))




