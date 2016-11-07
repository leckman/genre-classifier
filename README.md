# genre-classifier
Determines the genre of books given keyword data.

##Usage

First, cd to genre-classifier directory.

###Option 1

```python classify.py --books="<bookfile.json>" --genres="<genrefile.csv>"```

###Option 2

Make classify.py an executable file:

Right click on ```classify.py``` and follow Properties > Permissions > Exectue

Then run ```./classify.py --books="<bookfile.json>" --genres="<genrefile.csv>"```

###Optional Arguments
-s     save classification output
-h     help: show usage information
