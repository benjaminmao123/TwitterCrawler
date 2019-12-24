import sys, os, lucene, json
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, DirectoryReader, IndexOptions, IndexReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis import LowerCaseFilter, StopFilter
from org.apache.lucene.analysis.en import PorterStemFilter, EnglishAnalyzer
from org.apache.pylucene.analysis import PythonAnalyzer
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths
from index import Index

if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        print('To run index directory is required as an argument. e.g.: python index.py \"/index\"')
        sys.exit()

    # required to run java functions for lucene
    lucene.initVM(classpath = lucene.CLASSPATH)

    analyzer = StandardAnalyzer()
    index = Index(sys.argv[1], analyzer)

    store = SimpleFSDirectory(Paths.get(sys.argv[1]))
    searcher = IndexSearcher(DirectoryReader.open(store))
    # open file for searching
    index.SearchIndex(searcher, analyzer, 20)

    
