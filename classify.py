#!/usr/bin/env python2

import getopt, sys
import json, csv
import numpy as np
import re

def classify(books, genre_info):
    """Return matching genres for book descriptions with associated scores.

    Keyword arguments:
    books -- json file path with {title: BOOK_TITLE, description: BOOK_DESCRIPTION} entries
    genre_info -- csv file path with [genre_name, keyword, keyword_score] rows
    """
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
                # matches of form (genre, points, numOccurences)
                matches.append((genre[0], int(genre[2]), num))

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

    return output

def getMatches(string, search_string):
    """ Return number of nonoverlapping occurences of search_string in string """
    pattern = re.compile('(%s)' % search_string)
    matches = re.findall(pattern, string)
    return len(matches)

def groupGenres(match, store):
    """ Add a given genre match to the dictionary of genre matches

    Keywork arguments:
    match -- (genre_name, points_for_match, num_matches) 
              tuple for a given keyword match
    store -- dictionary with genre_name keys

    Modifies the input store
    """
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
    """ Load json from file """
    try:
        json_data = json.load(open(file_name));
        return json_data
    except IOError as err:
        print err
        sys.exit(1)


def getCSV(file_name):
    """ Load csv data from file as a 2D array """ 
    try:
        csv_data = csv.reader(open(file_name))
        data = []
        for row in csv_data:
            data.append(row)
        return data
    except IOError as err:
        print err
        sys.exit(1)

def prettyPrint(classification_data):
    """ Print human-readable classification data string """
    output = ""
    for book in classification_data:
        output += book["title"] + "\n"
        for genre in book["scores"].keys():
            output += "%s, %d\n" % (genre, book["scores"][genre])
        output += "\n"  # extra line break between books
    output = output[:-2] # remove last two newlines
    print output

if __name__ == '__main__':

    # defaults
    books = "sample_books.json"
    genres = "sample_genres.csv"
    save = False

    help_message = "Usage: ./classify.py --books=<bookFileName.json> --genres=<genreFileName.csv>\n" \
        "Optional flags:\n" \
        "-s\tsave output\n" \
        "-h\thelp"

    try:
        opts, args = getopt.getopt(sys.argv[1:], ":sh", ["books=", "genres="])
    except getopt.GetoptError as err:
        print help_message
        sys.exit(2) # argument error

    for opt, arg in opts:
        if opt == "-h":
            print help_message
            sys.exit(0)
        if opt == "--books":
            books = arg
        if opt == "--genres":
            genres = arg
        if opt == "-s":
            save = True

    if (books == "sample_books.json" 
        and genres == "sample_genres.csv"):
        print "[INFO] Running under default parameters."

    print "[INFO] Classifying books from %s using %s." % (books, genres)
    classified = classify(books, genres)
    prettyPrint(classified)

    if save: 
        name = raw_input("\nSave to: ")
        if name.find(".") == -1:
            # no file extension specified
            name += ".json"
        output = open(name, "w")
        json.dump(classified, output)
        output.close()
        print "[INFO] Saved classification data to", name

