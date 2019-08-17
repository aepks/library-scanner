This is a small script to grab details of books in the Skulls library.  Feed it a list of ISBNs, one number per line, and it'll spit out a CSV with details from the Google Books API.  You can include non-ISBN text (like a comment or shelf number) to be applied to the "Comment" field for the following ISBNs.

Grab an API key from [this page](https://developers.google.com/books/docs/v1/using#APIKey) and fill in `GOOGLE_API_KEY`.

Run `pip install -r requirements.txt` to set up.

Run `python make-csv.py --help` for usage instructions.


### Usage example:


input.txt:
```
Table 28 - Sherpa (6)
9781305271760
9781118976272
Table 29 - Sherpa (8)
9781119175483
9780895828798
9780077861971
```
command: `python make-csv input.txt output.csv`

output.csv:

|Google Books ID|ISBN|Last Name|First Author|Title|Comment|Error?|
|---|-----|---------|------------|-----|-------|------|
|WFICswEACAAJ|9781305271760|Stewart|James Stewart|Calculus|Table 28 - Sherpa (6)||
|NIWbCgAAQBAJ|9781118976272|Landy|Frank J. Landy|Work in the 21st Century, Binder Ready Version|Table 28 - Sherpa (6)||
|Oh-RCgAAQBAJ|9781119175483|Callister|William D. Callister|Fundamentals of Materials Science and Engineering, Binder Ready Version|Table 29 - Sherpa (8)|ISBN mismatch|
|iVwZywAACAAJ|9780895828798|Smith|David G. Smith|A Dissection Guide & Atlas to the Fetal Pig|Table 29 - Sherpa (8)||
|eC_9sgEACAAJ|9780077861971|Myers|David Myers|Social Psychology|Table 29 - Sherpa (8)||
