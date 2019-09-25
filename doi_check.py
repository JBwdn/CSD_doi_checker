#!/usr/bin/env python
'''
Check whether DOIs have any structures associated with them.
Takes a DOI or .txt list of DOIs as input argument
TODO: Python 2/3 compatible
'''
import os
import argparse

# CSD API dependency:
from ccdc.search import TextNumericSearch


class checkDoi:
    def __init__(self):
        self.doiHits = []
        self.nDoiStructures = []
        self.doiList = []
        print 'Working in: ' + os.getcwd()

    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'filename', help='Paper DOI or path to .txt list of DOIs')
        args = parser.parse_args()
        self.inFile = args.filename

    def loadDois(self):
        try:
            self.doiList = [line.strip('\n') for line in open(self.inFile)]
            print 'Checking for structures associated with DOIs in: ' + self.inFile
        except IOError:
            self.doiList.append(self.inFile)
            print 'Checking for structures associated with DOI: ' + self.inFile

    def searchCSD(self):
        query = TextNumericSearch()
        for doi in self.doiList:
            # Return any dois which have any structures associated with them:
            refCodes = []
            query.add_doi(doi, mode='anywhere',
                          ignore_non_alpha_num=False)
            searchResults = query.search()
            n = int(len(searchResults))
            for i in searchResults:
                refCodes.append(i.identifier)
            query.clear()
            if n != 0:
                print 'Hit: ' + str(n) + ' in ' + str(doi)
                for i in refCodes:
                    print str(i)
                self.doiHits.append(doi)
                self.nDoiStructures.append(n)
        print str(len(self.doiHits)) + ' Hits found.'

    def main(self):
        self.parseArgs()
        self.loadDois()
        self.searchCSD()


if __name__ == '__main__':
    searcher = checkDoi()
    searcher.main()
