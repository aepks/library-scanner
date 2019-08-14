This is a small script to grab details of books in the Skulls library.  Feed it a list of ISBNs, one number per line, and it'll spit out a CSV with details from the Google Books API.

Grab an API key from [this page](https://developers.google.com/books/docs/v1/using#APIKey) and fill in `GOOGLE_API_KEY`.

Run `pip install -r requirements.txt` to set up.

Run `python make-csv.py --help` for usage instructions.
