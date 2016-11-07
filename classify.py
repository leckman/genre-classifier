#!/usr/bin/env python2

import getopt, sys
import json, csv

def classify(books, genre_info):
    """TODO docstring"""
    getJSON(books)
    getCSV(genre_info)
    return True

def getJSON(file_name):
    try:
        json_data = json.load(open(file_name));
        return json_data
    except IOError as err:
        print err
        sys.exit(1)


def getCSV(file_name):
    try:
        csv_data = csv.reader(open(file_name))
        return csv_data
    except IOError as err:
        print err
        sys.exit(1)

if __name__ == '__main__':

    # defaults
    books = "sample_books.json"
    genres = "sample_genres.csv"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["books=", "genres="])
    except getopt.GetoptError as err:
        print err
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--books":
            books = arg
        if opt == "--genres":
            genres = arg

    if (books == "sample_books.json" 
        and genres == "sample_genres.csv"):

        print "[INFO] Running under default parameters."

    print "[INFO] Classifying books from %s using %s." % (books, genres)
    classified = classify(books, genres)
