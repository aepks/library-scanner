import argparse
import requests
import csv
import json
import logging

GOOGLE_API_KEY = ''

def dump_response(r):
	return logging.debug(json.dumps(r.json(), indent=2, sort_keys=True))

def matches_isbn(isbn, volumeInfo):
	if 'industryIdentifiers' not in volumeInfo:
		logging.debug("no identifiers for {}".format(isbn))
		return False
	for identifier in volumeInfo['industryIdentifiers']:
		try:
			if int(identifier['identifier']) == isbn:
				return True
			# logging.debug("id {} != isbn {}".format(identifier['identifier'], isbn))
		except ValueError as e:
			pass # ignore non-numeric ISBNs, since our scanner doesn't generate them anyway
			# logging.debug("Found a non-numeric identifier: {}".format(identifier['identifier']))
	return False



parser = argparse.ArgumentParser(description="Turn a list of ISBNs into a CSV")
parser.add_argument("isbns", help="A file with an ISBN on each line", type=argparse.FileType('r'))
parser.add_argument("output", help="A CSV file with the book details", type=argparse.FileType('w'), default='-')
parser.add_argument('-v', '--verbose', action='count', default=0)
args = parser.parse_args()

logging.basicConfig(level={
	0: logging.WARNING,
	1: logging.INFO,
	2: logging.DEBUG}.get(args.verbose, 2))

writer = csv.DictWriter(args.output,
	fieldnames=['Google Books ID', 'ISBN', 'Last Name', 'First Author', 'Title', 'Comment', 'Error?'],
	restval="")
writer.writeheader()

comment = ""

for isbn in args.isbns:
	isbn = isbn.strip("\n")
	try:
		isbn = int(isbn)
	except ValueError:
		logging.debug("Found comment: {}".format(isbn))
		comment = isbn
		continue

	logging.info("Searching for {}".format(isbn))
	r = requests.get(
		'https://www.googleapis.com/books/v1/volumes', params={
			'q': 'isbn:{}'.format(isbn),
			'fields': 'items/volumeInfo/authors,items/volumeInfo/title,items/volumeInfo/industryIdentifiers,items/id',
			'maxResults': 1,
			'key': GOOGLE_API_KEY
			})
	if r.status_code == 403:
		logging.critical("Oop, we might be rate-limited. Stopping.")
		dump_response(r)
		exit()
	if r.status_code != 200:
		logging.warning("Uh-oh, got a non-200 return. Continuing to the next one. Response:")
		dump_response(r)
		continue

	csv_row = {
		'ISBN': isbn,
		'Comment': comment,
	}

	try:
		book = r.json()['items'][0]
	except KeyError as e:
		logging.warning("No results for {}!".format(isbn))
		dump_response(r)
		csv_row['Error?'] = "No results found"
		writer.writerow(csv_row)
		continue

	try:
		if not matches_isbn(isbn, book['volumeInfo']):
			logging.warning("Matching ISBN not found for {}!".format(isbn))
			csv_row['Error?'] = "ISBN mismatch"
			dump_response(r)
		
		if 'subtitle' in book['volumeInfo']:
			csv_row['Title'] = "{title}: {subtitle}".format(**book['volumeInfo'])
		else:
			csv_row['Title'] = book['volumeInfo']['title']
		csv_row['First Author'] = book['volumeInfo'].get('authors', [""])[0], # some books don't have authors listed :(
		csv_row['Last Name'] = book['volumeInfo'].get('authors', [""])[0].split(" ")[-1], # doesn't take into account multi-word last names
		csv_row['Google Books ID'] = book['id'],
		writer.writerow(csv_row)
	except KeyError as e:
		logging.error("Couldn't find field {} in results for {}!".format(e, isbn))
		logging.debug(json.dumps(book, indent=4, sort_keys=True))
