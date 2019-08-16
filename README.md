This is a small script to grab details of books in the Skulls library.  Feed it a list of ISBNs, one number per line, and it'll spit out a CSV with details from the Google Books API.  You can include non-ISBN text (like a comment or shelf number) to be applied to the "Comment" field for the following ISBNs.

Grab an API key from [this page](https://developers.google.com/books/docs/v1/using#APIKey) and fill in `GOOGLE_API_KEY`.

Run `pip install -r requirements.txt` to set up.

Run `python make-csv.py --help` for usage instructions.
