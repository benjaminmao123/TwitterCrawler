# CS172 Final Project

## Team Info
Group: **Lolipop**

Member and Work Division: 
- Alexander Wilkins (Part 1)
- Benjamin Mao(Part 2)
- Qicheng Hu (Part 3)  

## How to Run


### Part 1: Tweet Streaming
Dependencies: tweepy

Related code: [tweetstreams.py](tweetstreams.py)

Run in command line:
> python tweetstreams.py

This piece of code gets tweet streams using tweepy, and stores extended tweet json objects in file (Default= twitterDoc.txt)




### Part 2: Indexing and Searching
Dependencies: pylucene, json

Related code: [generateIndex.py](generateIndex.py), [searchIndex.py](searchIndex.py), [index.py](index.py)

Run in command line:

> python generateIndex.py index_folder

This python script generate index using Lucene and save indexed files to index_folder. (Default input=twitterDoc.txt)

> python searchIndex.py index_folder

This piece of code search and return result of query using indexed files in index_folder.



### Part 3: Popularity Measurement using Mapreduce
Dependencies: hadoop, json

Hadoop version: 2.7.7 (hadoop-streaming-2.7.7.jar)

Related code: [map.py](map.py), [reduce.py](reduce.py), [ave.py](ave.py) 

Run in command line:
> hadoop jar /usr/local/src/hadoop-2.7.7/share/hadoop/tools/lib/hadoop-streaming-2.7.7.jar \
-file 'map.py' -file  'reduce.py' \
-mapper "python map.py" -reducer "python reduce.py" \
-input 'input.txt' -output 'result' 

This mapreduce job counts the total number of retweet, quote, reply and favorite of each hashtag. However, the data should also be normalized by the size of file.
Normalizing:
>python ave.py

In output file (default=ave.txt) is the normalized popularity of topics(sorted from high to low).  


## Saved Files
Folder [index/](index/) contains the indexing results.

In folder [mapReduceResults](mapReduceResults/), there are 4 raw results of mapreduce (Named as result_Dec*) and 1 normalized result [Normalized Popularity](mapReduceResults/NormalizedPopularity.txt)
