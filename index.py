import sys, os, lucene, json
from tweet import Tweet
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, DirectoryReader, IndexOptions, Term
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis import LowerCaseFilter, StopFilter
from org.apache.lucene.analysis.en import PorterStemFilter, EnglishAnalyzer
from org.apache.pylucene.analysis import PythonAnalyzer
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths
from org.apache.lucene.search import Query

class Index:
    def __init__(this, storeDir, analyzer):
        store = SimpleFSDirectory(Paths.get(storeDir))
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        this.writer = IndexWriter(store, config)

    def CreateIndex(this):
        for i in range(8):
            with open('tweets/Dec11.txt.1' + str(i)) as file:
                tweets = []

                for line in file:
                    # check if line is empty, if so it is the end of a tweet 
                    # so we continue until we reach another starting '{'
                    if line.strip() == '':    
                        continue    
                    else:
                        try:
                        # convert line in dictionary
                            data = json.loads(line)
                        except:
                            continue
                        # create Tweet object and initialize dictionary
                        tweet = Tweet(data)
                        tweets.append(tweet)
                        print(len(tweets))
                
                file.close()
            cnt = 0
            for tweet in tweets:
                doc = Document()
                # create a field type
                t1 = FieldType()
                t1.setStored(True)
                t1.setTokenized(False)
                t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

                t2 = FieldType()
                t2.setStored(True)
                t2.setTokenized(True)
                t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

                # add fields to document
                if tweet.data.get('created_at') != None:
                    doc.add(Field('created_at', tweet.data.get('created_at'), t1))
                
                if tweet.data.get('id') != None:
                    doc.add(Field('id', tweet.data.get('id'), t1))
                
                if tweet.data.get('user') != None:
                    if tweet.data.get('user').get('screen_name') != None:
                            doc.add(Field('user', tweet.data.get('user').get('screen_name'), t1))
                
                if tweet.data.get('extended_tweet') != None:
                    if tweet.data.get('extended_tweet').get('full_text') != None:
                        doc.add(Field('text', tweet.data.get('extended_tweet').get('full_text'), t2))
                        print(tweet.data.get('extended_tweet').get('full_text'))
                
                    if tweet.data.get('extended_tweet').get('hashtags') != None:
                        for hashtag in tweet.data.get('extended_tweet').get('hashtags'):
                            doc.add(Field('hashtags', hashtag, t2))
                else:
                    if tweet.data.get('text') != None:
                        doc.add(Field('text', tweet.data.get('text'), t2))
                        print(tweet.data.get('text'))

                    if tweet.data.get('hashtags') != None:
                        for hashtag in tweet.data.get('hashtags'):
                            doc.add(Field('hashtags', hashtag, t2))

                this.writer.addDocument(doc)
                cnt+=1
                print(cnt)

        this.writer.close()

    def SearchIndex(this, searcher, analyzer, numTopHits):
        while True:
            command = raw_input('Enter a query: ')
            term = Term('text', command)
            query = TermQuery(term)
            # print(query.toString())
            topDocs = searcher.search(query, 10)

            num_results = len(topDocs.scoreDocs)

            for i in range(num_results):
                doc = searcher.doc(topDocs.scoreDocs[i].doc)
                print('Tweet ID: ' + doc.get('id').encode('utf-8'))
                print('User: ' + doc.getField('user').stringValue())
                print('Text: ' + doc.getField('text').stringValue())
                print('Date: ' + doc.getField('created_at').stringValue())
                print('Score: ' + str(topDocs.scoreDocs[i].score) + '\n')