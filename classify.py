#!/usr/bin/env python2

import getopt, sys
import json, csv
import numpy as np

def classify(books, genre_info):
    """TODO docstring"""
    books = getJSON(books)
    genres = getCSV(genre_info)
    output = []

    for book in books:
        title = book["title"]
        desc = book["description"]

        # find matches between genre keywords and book description
        matches = []
        for genre in genres:
            search = genre[1]

            num = getMatches(desc, search)
            if num > 0:
                # matches of form [genre, points, numOccurences]
                matches.append([genre[0], int(genre[2]), num])

        # group matches by genre
        grouped = {}
        for match in matches:
            groupGenres(match, grouped)

        # calculate a score for each genre
        scores = []
        for genre in grouped.keys():
            # score is average # points for each matched term * number of matches in that genre
            score = np.mean(grouped[genre]["points"]) * grouped[genre]["occurences"]
            scores.append((genre, score))

        # formatting final record for output
        final_classifications = {
            "title": title,
            "scores": {}
            }
        for genre, score in scores:
            final_classifications["scores"][genre] = score
        output.append(final_classifications)

    return json.dumps(output)

def getMatches(string, search_string):
    numMatches = 0
    i = 0

    while i < len(string):
        start = (string[i:]).find(search_string)
        if start > -1:
            i += start + len(search_string)
            numMatches += 1
        else:
            break

    return numMatches

def groupGenres(match, store):
    genre = match[0]
    if genre in store.keys():
        store[genre]["points"].append(match[1])
        store[genre]["occurences"] += match[2]
    else:
        store[match[0]] = {
            "points": [match[1]],  # list of matched point values
            "occurences": match[2]  # number of matches to this genre
        }        

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
        data = []
        for row in csv_data:
            data.append(row)
        return data
    except IOError as err:
        print err
        sys.exit(1)

if __name__ == '__main__':

    # defaults
    books = "sample_books.json"
    genres = "sample_genres.csv"
    save = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], ":s", ["books=", "genres="])
    except getopt.GetoptError as err:
        print err
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--books":
            books = arg
        if opt == "--genres":
            genres = arg
        if opt =="-s":
            save = True

    if (books == "sample_books.json" 
        and genres == "sample_genres.csv"):
        print "[INFO] Running under default parameters."

    print "[INFO] Classifying books from %s using %s." % (books, genres)
    classified = classify(books, genres)
    print classified

    if save: 
        name = raw_input("Save to: ")
        output = open(name, "w")
        output.write(classified)
        output.close()

