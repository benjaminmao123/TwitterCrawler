import sys, lucene
from index import Index
from org.apache.lucene.analysis.standard import StandardAnalyzer

if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        print('To run index store directory is required as an argument. e.g.: python index.py \"/index\"')
        sys.exit()

    # required to run java functions for lucene
    lucene.initVM(classpath = lucene.CLASSPATH)

    analyzer = StandardAnalyzer()
    index = Index(sys.argv[1], analyzer)

    index.CreateIndex()