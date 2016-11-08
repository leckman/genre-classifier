genre-classifier
Determines the genre of books given keyword data.

Usage

	First, cd to genre-classifier directory.

	Option 1

		python classify.py --books="<bookfile.json>" --genres="<genrefile.csv>"

	Option 2

		Make classify.py an executable file:

		Right click on classify.py and follow Properties > Permissions > Exectue

		Then run:
		./classify.py --books="<bookfile.json>" --genres="<genrefile.csv>"

	Optional Arguments
	-s		save classification output

	-h 		help, show usage information


Trade-Offs & Edge Cases

	Keyword matching edge cases: "racecaracecar" should not match "racecar" twice - used the native regexp findall function to prevent overlapping matches	

	I elected to use a few different loops to get from the regexp matches to the final scores - this uses more memory but makes the logic much more readable


I spent about 2.5 hours on this code.
