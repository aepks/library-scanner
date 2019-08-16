This is a small script to grab details of books in the Skulls library.  Feed it a list of ISBNs, one number per line, and it'll spit out a CSV with details from the Google Books API.  You can include non-ISBN text (like a comment or shelf number) to be applied to the "Comment" field for the following ISBNs.

Grab an API key from [this page](https://developers.google.com/books/docs/v1/using#APIKey) and fill in `GOOGLE_API_KEY`.

Run `pip install -r requirements.txt` to set up.

Run `python make-csv.py --help` for usage instructions.


### Usage example:


input.txt:
```
shelf #1
9780495802778
9781938073373
shelf #2
9781604266139
9780791463888
```
command: `python make-csv input.txt output.csv`

output.csv:
```
Google Books ID,ISBN,Last Name,First Author,Title,Comment
TY-jMQEACAAJ,9780495802778,Reviews,Cram101 Textbook Reviews,"Studyguide for the Modern Presidency, 6th Edition by James P. Pfiffner, Isbn 9780495802778",shelf #1
7XO_NAEACAAJ,9781938073373,Petty,Audrey Petty,High Rise Stories: Voices from Chicago Public Housing,shelf #1
E9c8AQAAIAAJ,9781604266139,,,"Choice: Publication of the Association of College and Research Libraries, a Division of the American Library Association",shelf #2
j4c6zMDlQwMC,9780791463888,Paper,Jordan Paper,The Deities Are Many: A Polytheistic Theology,shelf #2
```
